---
name: industrial-techno-measures-too-dark
description: Both finished industrial techno records came out with under 2% of their energy above 3 kHz and 13% of their sub in the side channel; an air shelf does not fix either
type: pitfall
date: 2026-09-01
---

`industrial_morgengrauen_152` and `industrial_untertage_136` were written
eight months apart, by different routes, and they measure almost identically
in the two places the genre is easiest to get wrong:

| | morgengrauen | untertage | what a rig does with it |
|---|---|---|---|
| above 3 kHz | **1.7% + 1.2%** | **1.0% + 0.9%** | a blanket over the record |
| under 120 Hz | 32% | 36% | thin against 120-300 Hz at 38% / 33% |
| side below 120 Hz | **12.8%** | **14.3%** | a club system that sums the bass throws it away |
| true peak | +0.83 dBTP | +0.82 dBTP | distorts in an encoder and in a DAC |

None of the four is a taste decision, and all four have the same cause: the
palette. Everything in an industrial kit is dark by construction - the kick
is a driven sine, the rumble is a reverb tail band-limited to the growl, the
grind is noise through resonators tuned to the root, and the brightest
instrument in the whole module is a closed hat.

**The three fixes, in the order they matter:**

1. **Put something above 3 kHz rather than lifting what is there.** An air
   shelf multiplies a band that is empty. `industriallib.sheet()` is the
   answer: broadband noise through a bank of high resonant bands, drifting
   against each other. It must be **untuned** - `grind()` is the same
   construction two octaves down tuned to the root, and a bright ringing
   pitched thing above 3 kHz reads as a glockenspiel
   ([[pitched-metal-reads-as-cheerful]]). An untuned bright object is a room.
2. **The kick needs a third layer.** techkick is the punch and rumble is the
   growl, and neither is the weight - both records ended up with more energy
   in 120-300 Hz than under 120. A clean mono sine at the root, 100 ms,
   ducked with everything else, moves it: `blendung` measures 40% under
   120 Hz and 19% in 120-300.
3. **`mono_below(150)` is not enough.** A 4th-order crossover leaks, and
   reverb tails and Haas offsets keep refilling the side. Cross over at
   **170 Hz**, and narrow the buses that had no business being wide down
   there in the first place. That took the side content from 13% to 3.6%.

And the true peak is [[loud-masters-need-a-true-peak-limiter]]: both records
used `limit=` alone, which averages its gain curve and cannot hold a ceiling.

Related: [[section-contrast-belongs-in-level]]
