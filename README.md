# National Anthems of the World — OpenTTD Base Music

A collection of **national anthems** packaged as [OpenTTD](https://www.openttd.org/)
**Base Music** sets, released as a split set of volumes.

Because OpenTTD's music system has exactly **31 fixed track slots**, the 162
unique anthems are published across **6 volumes** (27 anthems each). Each volume
is an independent GitHub repository and an independent Bananas base-music package,
so you can install just the volumes you want — or all of them for the complete
set.

## Volumes

| Volume | Repository | Anthems |
|--------|------------|---------|
| 1 | [openttd-national-anthem-1](https://github.com/Maicarons/openttd-national-anthem-1) | 27 |
| 2 | [openttd-national-anthem-2](https://github.com/Maicarons/openttd-national-anthem-2) | 27 |
| 3 | [openttd-national-anthem-3](https://github.com/Maicarons/openttd-national-anthem-3) | 27 |
| 4 | [openttd-national-anthem-4](https://github.com/Maicarons/openttd-national-anthem-4) | 27 |
| 5 | [openttd-national-anthem-5](https://github.com/Maicarons/openttd-national-anthem-5) | 27 |
| 6 | [openttd-national-anthem-6](https://github.com/Maicarons/openttd-national-anthem-6) | 27 |

**Total: 162 anthems** (deduplicated; see below).

## Installation

**Via Bananas (recommended):** in OpenTTD, open *Content Download → Music* and
search for `openttd-national-anthem`. Each volume appears as a separate
base-music package — subscribe to all six for the full set.

**Manual:** copy every `national_anthems_volN.obm` and all `*.mid` files from the
six volume repositories into your OpenTTD `baseset/` directory (e.g.
`%USERPROFILE%\Documents\OpenTTD\baseset\` on Windows or
`~/.openttd/baseset/` on Linux/macOS), then select each set in
*Game Options → Music*.

## Building

Each volume repository contains a `scripts/build_package.py` and a GitHub Actions
workflow that builds the Bananas package (`dist/openttd-national-anthem-N-1.0.tar.gz`)
on every push. Locally:

```
python scripts/build_package.py
```

## Deduplication

A transposition/tempo-invariant melody analysis over the source files found:

- **1 byte-identical duplicate removed:** Guinea-Bissau (`guinbiss.mid`) was
  byte-for-byte identical to Cape Verde (`CapeVerde.mid`) and was dropped.
- **1 historical shared melody kept as two countries:** Estonia and Finland use
  the same Pacius tune (legitimately — both anthems share the melody). Both
  sovereign states are retained.
- All other anthems are distinct.

## License

**Creative Commons Attribution 4.0 International (CC BY 4.0).** You may share and
adapt for any purpose, including commercially, provided appropriate credit is
given. License text: <https://creativecommons.org/licenses/by/4.0/>

> Note: the national-anthem *compositions* are public domain; the specific MIDI
> *arrangements* in this collection are distributed under CC BY 4.0.
