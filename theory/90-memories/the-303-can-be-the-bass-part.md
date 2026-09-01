---
name: the-303-can-be-the-bass-part
description: A 303 written as the bassline needs its overdrive split off the fundamental, or the low end turns to mud - and it comes out low-middle unless the line's own octave is added under it
type: decision
date: 2026-09-01
---

`industriallib.deepacid()` exists because there are two different instruments
called a 303 and this engine only had one of them.

The one it had - `industriallib.acidline`, `minimallib.acidline` - is a hook.
It high-passes at 165-240 Hz on the principle that the sub belongs to the
kick, and it measures **74% of its energy in 300-800 Hz**. Correct for a line
riding over a bassline.

The other is the bass. It sits at the second octave, the filter rests below
150 Hz, and the resonant peak crawls through the low harmonics. Two things
have to change for that to work and neither is obvious:

1. **Split the drive off the fundamental.** The overdrive after the filter is
   most of what makes a 303 sound like one, and applied to a 60 Hz
   fundamental it generates intermodulation across the whole sub. So the
   signal splits at ~105 Hz: the low band passes clean and the band above it
   is driven and folded. Same rule as every bass in this engine - one clean
   thing at the bottom - applied to a 303 for the first time.
2. **Add the line's own octave down.** A 303 written at D#2 has its
   fundamentals at 78-185 Hz, which IS the 120-300 band, so a record whose
   bass is the 303 comes out low-MIDDLE and measures 48% there against 29%
   under 120 Hz. `sub_oct` is a clean tracked sine at half the phase; it has
   to be a sine and it has to be clean.

It keeps three things from `minimallib.acidline`, which is the most faithful
303 here and was the right starting point: the **three-pole** filter (the
fourth pole every imitation adds puts the resonant peak on silence instead of
on a bed of harmonics), the overdrive **after** the filter, and `cutoff` and
`envmod` as two independent knobs so the resting point and the throw can be
turned against each other while the pattern stays fixed.

**How to apply:** `deepacid(pattern, bars, knob=(...))` renders a phrase, not
a bar - the oscillator never restarts, so the slides slide - and `knob` is the
hand on the cutoff across the whole phrase. Watch the balance: with the kick
at 38.89 Hz, the sub layer, the rumble and `sub_oct` all stacked, this record
measured 53% under 120 Hz on the first pass, which is not dark, it is muffled.
`sub_oct` is the one that gives.

Related: [[dark-is-register-and-mode-not-key]], [[note-envelopes-need-a-release]]
