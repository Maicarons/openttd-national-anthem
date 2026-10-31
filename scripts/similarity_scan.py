#!/usr/bin/env python3
"""Broad all-pairs melody similarity scan (transposition/tempo invariant)."""
import os, sys, glob, json
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from midi_analysis import parse_midi, parse_track, fingerprint, seq_similarity

MIDI_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "midi")

def main():
    files = sorted(glob.glob(os.path.join(MIDI_DIR, "*.mid")))
    seqs = {}
    for path in files:
        name = os.path.basename(path)
        try:
            fmt, division, tracks = parse_midi(path)
            notes = []
            for tr in tracks:
                ns, _ = parse_track(tr, division)
                notes.extend(ns)
            seqs[name] = fingerprint(notes, division)
        except Exception as e:
            print("ERR", name, e, file=sys.stderr)

    # bucket by rounded length to limit comparisons
    buckets = defaultdict(list)
    for n, s in seqs.items():
        buckets[round(len(s) / 12)].append(n)

    results = []
    for b, members in buckets.items():
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                a, c = members[i], members[j]
                sa, sc = seqs[a], seqs[c]
                if min(len(sa), len(sc)) < 8:
                    continue
                sim = seq_similarity(sa, sc)
                if sim >= 0.80:
                    results.append((round(sim, 3), a, c))
    results.sort(reverse=True)
    print("Similar pairs (sim>=0.80):", len(results))
    for sim, a, c in results:
        print(f"  {sim:.3f}  {a}  <->  {c}")

if __name__ == "__main__":
    main()
