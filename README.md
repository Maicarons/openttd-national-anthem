# openttd-national-anthem

National anthems of the world, packaged as an **OpenTTD Base Music** set.

* **162** deduplicated MIDI anthems, one per country (ISO 3166-1 alpha-2
  filenames, e.g. `gb.mid`, `fr.mid`, `jp.mid`).
* A `national_anthems.obm` descriptor that wires **31 anthems** into OpenTTD's
  playable music slots (`theme`, `old_0..9`, `new_0..9`, `ezy_0..9`).
* All 162 MIDI files are shipped, so you can remap any slot to any anthem.

## How OpenTTD base music works

OpenTTD's music system has exactly **31 fixed track slots**: one `theme` plus
three groups of ten (`old_0..9`, `new_0..9`, `ezy_0..9`). A `.obm` file maps
each slot to a music file. Because of this engine limit, this collection
registers 31 anthems as playable and bundles the remaining 131 as data you
can reassign by editing `national_anthems.obm` (see below).

## Installation

**Via Bananas (recommended):** search for *openttd-national-anthem* in the
in-game Content Download, or upload the package on
<https://bananas.openttd.org/package/base-music>.

**Manual:** copy `national_anthems.obm` and all `*.mid` files into your
OpenTTD `baseset/` directory (e.g. `%USERPROFILE%\Documents\OpenTTD\baseset\`
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

Generated 2026-10-31.
