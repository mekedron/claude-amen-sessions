---
name: many-distorted-kicks-merge-into-noise
description: A hard-clipped kick fired eight times a bar stops being eight events and becomes one continuous rasp
type: pitfall
date: 2026-09-01
---

He found this one and named the cause in one sentence: *"это вот именно в
этом дисторшн кики... особенно когда этих киков происходит много, оно
сливается все просто в такой вот хриплый шум"*.

It measures exactly. Band-pass the drums at 2-9 kHz, take a 3 ms max
envelope, and ask how far it falls between hits:

| kicks per bar at 168 BPM | gap |
|---|---|
| 4 (357 ms apart) | silence |
| 8 (178 ms apart) | **-15.7 dB** |
| 16 (89 ms apart) | **-10.6 dB** |

`industrialkick` is hard-clipped twice and carries a noise exhale that decays
over 70 ms with an air layer at 5.2 kHz. At four a bar every one of those is
finished before the next starts. At eight they overlap, and clipping products
from consecutive kicks sum into a bed rather than a series of transients -
which is what "hoarse noise" is.

**Three fixes, and none of them is fewer kicks.**

1. **The offbeat kicks are a different voice**, not the same kick fired more
   often: half the decay, a quarter of the hiss, and a lowpass at 5 kHz.
   That alone takes eight a bar from -15.7 to -18.1 dB.
2. **Cap the main kick's own top.** The second hard clip is broadband by
   construction, and above about 7 kHz its products are not punch. Lowpass
   the kick at 6.8 kHz and let the hats own everything above it - the top
   that is lost comes back from transients, which is where it belongs.
3. **Back the bus stage off.** `drive_asym(1.5) -> softclip(1.10)` on a bus
   that already contains a doubly-clipped kick is not making the kit harder,
   it is intermodulating overlapping kicks with each other. 1.22 / 1.02.

**Why it is worth a memory:** every instinct when a record is asked to be
harder is to add kicks and add drive, and both of them make this worse. The
density is fine; what cannot survive it is a long, hissy, broadband kick.

Related: [[a-repeated-hit-must-not-be-identical]], [[industrial-techno-measures-too-dark]]
