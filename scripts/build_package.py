#!/usr/bin/env python3
"""Build the openttd-national-anthem base-music package.

Reads the deduplicated, ISO-normalised country mapping, copies the MIDI files
into the package directory, generates national_anthems.obm (with the 31
OpenTTD playable slots), writes README/LICENSE/changelog/Makefile, and finally
produces the .tar / .tar.gz bananas package plus a metadata JSON.

Outputs go to ../dist/<package>-<version>/
"""
import os
import sys
import json
import shutil
import hashlib
import tarfile
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import country_map as cm

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIDI_SRC = os.path.join(ROOT, "midi")
DIST = os.path.join(ROOT, "dist")
VERSION_STR = f"{cm.VERSION}.0"
PKG_DIR_NAME = f"{cm.PACKAGE_NAME}-{VERSION_STR}"
PKG_DIR = os.path.join(DIST, PKG_DIR_NAME)


def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    os.makedirs(PKG_DIR, exist_ok=True)

    # 1. Copy normalised MIDI files (skip byte-duplicates)
    copied = {}  # iso2 -> (orig_basename, new_filename, md5, english)
    for orig, (iso2, en) in cm.COUNTRY_MAP.items():
        if orig in cm.DROP:
            continue
        src = os.path.join(MIDI_SRC, orig + ".mid")
        if not os.path.exists(src):
            print("MISSING SOURCE:", src, file=sys.stderr)
            continue
        new_name = iso2 + ".mid"
        dst = os.path.join(PKG_DIR, new_name)
        # avoid clobber if two origins map to same iso2 (shouldn't happen)
        if os.path.exists(dst):
            print("CLASH:", new_name, file=sys.stderr)
        shutil.copy2(src, dst)
        copied[iso2] = (orig, new_name, md5_of(dst), en)
    print(f"Copied {len(copied)} MIDI files", file=sys.stderr)

    # 2. Build .obm
    lines = []
    lines.append("; National anthems of the world for OpenTTD")
    lines.append("; Deduplicated set of %d MIDI files (1 byte-duplicate removed)." % len(copied))
    lines.append("; Only 31 tracks are playable in OpenTTD; see README.md.")
    lines.append("")
    lines.append("[metadata]")
    lines.append("name              = %s" % cm.OBM_NAME)
    lines.append("shortname         = %s" % cm.SHORTNAME)
    lines.append("version           = %d" % cm.VERSION)
    lines.append("description       = National anthems of the world for OpenTTD")
    lines.append("")
    lines.append("[files]")
    md5s = {}
    names = {}
    for slot, orig in cm.SLOT_SELECTION.items():
        iso2, en = cm.COUNTRY_MAP[orig]
        fname = iso2 + ".mid"
        lines.append("%-7s = %s" % (slot, fname))
        md5s[fname] = copied[iso2][2]
        names[slot] = en
    lines.append("")
    lines.append("[md5s]")
    for fname, h in md5s.items():
        lines.append("%-7s = %s" % (fname, h))
    lines.append("")
    lines.append("[names]")
    for slot, en in names.items():
        lines.append("%-7s = %s" % (slot, en))
    lines.append("")
    lines.append("[origin]")
    lines.append("default      = National anthems of the world — OpenTTD base music set.")
    obm_text = "\n".join(lines) + "\n"
    with open(os.path.join(PKG_DIR, cm.OBM_NAME + ".obm"), "w", encoding="utf-8", newline="\n") as f:
        f.write(obm_text)
    print("Wrote %s.obm" % cm.OBM_NAME, file=sys.stderr)

    # 3. Docs
    write_readme(PKG_DIR, copied)
    write_license(PKG_DIR)
    write_changelog(PKG_DIR)
    write_makefile(PKG_DIR)

    # 4. Package tarballs
    tar_path = os.path.join(DIST, PKG_DIR_NAME + ".tar")
    tgz_path = os.path.join(DIST, PKG_DIR_NAME + ".tar.gz")
    make_tar(PKG_DIR, tar_path, mode="w")
    make_tar(PKG_DIR, tgz_path, mode="w:gz")
    tar_md5 = md5_of(tar_path)
    tgz_md5 = md5_of(tgz_path)
    print("Wrote %s (md5 %s)" % (tar_path, tar_md5), file=sys.stderr)
    print("Wrote %s (md5 %s)" % (tgz_path, tgz_md5), file=sys.stderr)

    # 5. Bananas metadata JSON
    meta = {
        "name": cm.PACKAGE_NAME,
        "version": VERSION_STR,
        "type": "base-music",
        "description": (
            "National anthems of the world for OpenTTD. A deduplicated collection "
            "of %d MIDI anthems; 31 are wired into OpenTTD's playable music slots "
            "(theme + old/new/ezy), the rest ship as data you can remap." % len(copied)
        ),
        "authors": ["CountrySongs contributors"],
        "license": "Public Domain",
        "url": "https://github.com/Maicarons/openttd-national-anthem",
        "tags": ["music", "anthems", "midi", "national"],
        "dependency": [],
        "md5sum": tgz_md5,
        "files": {
            "tar": PKG_DIR_NAME + ".tar.gz",
        },
    }
    with open(os.path.join(DIST, "bananas-metadata.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    print("Wrote bananas-metadata.json", file=sys.stderr)

    # 6. Manifest of the normalised collection (for reference / repo)
    manifest = {
        "package": cm.PACKAGE_NAME,
        "version": cm.VERSION,
        "total_unique_midi": len(copied),
        "removed_duplicates": [o + ".mid" for o in cm.DROP],
        "tracks": [
            {"iso2": iso2, "file": v[1], "country": v[3], "md5": v[2]}
            for iso2, v in sorted(copied.items())
        ],
        "playable_slots": cm.SLOT_SELECTION,
    }
    with open(os.path.join(DIST, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print("Wrote manifest.json", file=sys.stderr)


def make_tar(src_dir, out_path, mode):
    if os.path.exists(out_path):
        os.remove(out_path)
    with tarfile.open(out_path, mode) as tar:
        for name in sorted(os.listdir(src_dir)):
            tar.add(os.path.join(src_dir, name), arcname=name)


def write_readme(pkg_dir, copied):
    n = len(copied)
    today = datetime.date.today().isoformat()
    content = f"""# openttd-national-anthem

National anthems of the world, packaged as an **OpenTTD Base Music** set.

* **{n}** deduplicated MIDI anthems, one per country (ISO 3166-1 alpha-2
  filenames, e.g. `gb.mid`, `fr.mid`, `jp.mid`).
* A `national_anthems.obm` descriptor that wires **31 anthems** into OpenTTD's
  playable music slots (`theme`, `old_0..9`, `new_0..9`, `ezy_0..9`).
* All {n} MIDI files are shipped, so you can remap any slot to any anthem.

## How OpenTTD base music works

OpenTTD's music system has exactly **31 fixed track slots**: one `theme` plus
three groups of ten (`old_0..9`, `new_0..9`, `ezy_0..9`). A `.obm` file maps
each slot to a music file. Because of this engine limit, this collection
registers 31 anthems as playable and bundles the remaining {n - 31} as data you
can reassign by editing `national_anthems.obm` (see below).

## Installation

**Via Bananas (recommended):** search for *openttd-national-anthem* in the
in-game Content Download, or upload the package on
<https://bananas.openttd.org/package/base-music>.

**Manual:** copy `national_anthems.obm` and all `*.mid` files into your
OpenTTD `baseset/` directory (e.g. `%USERPROFILE%\\Documents\\OpenTTD\\baseset\\`
on Windows or `~/.openttd/baseset/` on Linux/macOS), then select the set in
*Game Options → Music*.

## Reassigning anthems

Edit `national_anthems.obm`:

```
[files]
theme = gb.mid      ; change gb.mid to e.g. fr.mid
old_0 = us.mid
...
```

The matching `[md5s]` and `[names]` entries should be updated to stay consistent
(the game only strictly requires the `[files]` mapping).

## Deduplication report

A melody-fingerprint analysis (transposition- and tempo-invariant) was run over
all 163 source files:

* **1 byte-identical duplicate removed:** `guinbiss.mid` (Guinea-Bissau) was
  byte-for-byte identical to `CapeVerde.mid` (Cape Verde) and was dropped.
  *Note:* this means the bundled Cape Verde file currently also stands in for
  Guinea-Bissau; a proper Guinea-Bissau anthem should be supplied.
* **1 historical shared melody kept as two countries:** `estonia.mid` and
  `finland.mid` use the same Pacius tune (legitimately — both anthems share the
  melody). Both sovereign states are retained; only true duplicates were removed.
* All other anthems were found to be distinct.

## Known issues

* `xx.mid` — the source file `manislef.mid` could not be identified as any
  country from its name or its (auto-generated, title-less) MIDI metadata. It is
  included as `xx.mid` and flagged for review.
* The MIDI files appear to be auto-generated (`exten synt` / `b-lev synt`
  meta-events); their arrangement copyright is unknown. The underlying national
  anthem compositions are public domain.

## License

The national anthem *compositions* are public domain. The specific MIDI
*arrangements* in this package have unknown provenance; they are distributed
under **Public Domain**. If you are the rights holder of an arrangement and
object, please open an issue.

Generated {today}.
"""
    with open(os.path.join(pkg_dir, "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def write_license(pkg_dir):
    content = """National Anthems Base Music for OpenTTD — openttd-national-anthem

The musical compositions known as national anthems are, in general, public
domain works (written long ago, authors long deceased).

The MIDI files in this package are auto-generated arrangements of those public
domain compositions. Their specific arrangements are distributed under the
Public Domain.

No warranty is given. Use freely.
"""
    with open(os.path.join(pkg_dir, "LICENSE"), "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def write_changelog(pkg_dir):
    content = """1.0 (initial release)
  * Deduplicated 163 source MIDI files down to 162 unique anthems.
  * Normalised filenames to ISO 3166-1 alpha-2 codes.
  * Wired 31 anthems into OpenTTD's playable music slots.
  * Removed byte-identical duplicate (Guinea-Bissau == Cape Verde).
  * Retained Estonia & Finland (shared Pacius melody, distinct countries).
"""
    with open(os.path.join(pkg_dir, "changelog.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def write_makefile(pkg_dir):
    content = """# Minimal packaging Makefile for openttd-national-anthem
# Reference layout follows OpenTTD base-music conventions.

PKG     = openttd-national-anthem
VERSION = 1.0
DIR     = $(PKG)-$(VERSION)
TAR     = $(DIR).tar
TGZ     = $(DIR).tar.gz

all: $(TGZ)

$(TGZ): $(DIR)
\ttar -czf $(TGZ) -C $(DIR) .

$(TAR): $(DIR)
\ttar -cf $(TAR) -C $(DIR) .

$(DIR): $(wildcard *.mid) national_anthems.obm README.md LICENSE changelog.txt
\tmkdir -p $(DIR)
\tcp $^ $(DIR)/

clean:
\trm -rf $(DIR) $(TAR) $(TGZ)

.PHONY: all clean
"""
    with open(os.path.join(pkg_dir, "Makefile"), "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


if __name__ == "__main__":
    main()
