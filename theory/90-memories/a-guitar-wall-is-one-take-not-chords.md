---
name: a-guitar-wall-is-one-take-not-chords
description: A chord-per-segment rhythm guitar reads as a synth patch; the fix is one take through one amp, and it measures
type: feedback
date: 2026-09-01
---

The rhythm wall of the first two punk records was `gtr()`: every chord its
own segment, its own pass of the amp, normalised to the same peak. He heard
it precisely: **"он не похож на гитару... похож именно на электронную гитару,
которая типа именно синтезированная, синтезаторная, классическая"** - and
asked for more distortion to fix it.

The distortion was not the problem. The measurement that is: take the same
four-bar riff and smooth the low-passed envelope over 20 ms -

    chord-per-segment wall    envelope floor between chords = 0.000
    one take, one amp pass    envelope floor between chords = 0.519

**The wall was falling to digital zero between every pair of chords.** A
sound that starts from silence at an identical loudness a few hundred times
is a sampler playing a patch, whatever the string model behind it cost. No
amount of gain changes that, because the silence is not in the amp.

What a recorded rhythm track has instead, all of which `punklib.riff()` now
does and none of which fits a per-chord render:

1. **Ring-over.** Strings ring INTO the next chord until the fretting hand
   chokes them - and a restrike of the same chord only dips them (~0.34),
   because the pick passes through strings that never stopped.
2. **One amp pass per phrase.** The sag has memory across chords, the
   ring-over intermodulates with the new strum, and there is no per-chord
   `norm()` flattening the dynamics.
3. **A noise floor.** Hiss and mains hum go through the amp's gain, so a
   rest is a room, not a zero.
4. **The mistakes.** Pick scrapes at changes, per-stroke velocity that
   shades the SPECTRUM (`tilt`), strum-direction timing.

Do not chase the old sound's band shares when making this change: the
per-segment version measured brighter per time-average only because every
segment was cut at the note-off - all attack, no sustain. The attack bite is
what to compare, not the average.

Same lesson one level up from [[a-chord-must-not-arrive-as-one-event]] -
there the notes of one chord must not share a start; here the chords of one
phrase must not each start from nothing.

Related: [[a-chord-must-not-arrive-as-one-event]]
