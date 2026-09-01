---
name: one-oscillator-cut-in-half-not-two-oscillators
description: Layer a bass by splitting one oscillator across two buses rather than by putting a separate sine under it, and reach for a played instrument before a synth
type: decision
date: 2026-09-01
---

He asked for the bass line on a **double bass** - "ты можешь сделать с
контрабасом? она сейчас как будто это всё равно клавишными наигрывается" -
after three passes of a drawbar `organbass` doubling a `subbar`. Two separate
things were wrong and the fix for both was the same shape.

## A synth bass reads as a keyboard

An organ stack has one decay rate, exact integer harmonics and no attack that
is not a click, and no EQ makes that a plucked instrument. `junglelib.contrabass`
is the list of things that do, and every item is physical behaviour rather
than spectrum:

| | Why it is not optional |
|---|---|
| `f_k = k·f0·sqrt(1 + B k^2)` | Exact harmonicity is what an organ has |
| A decay per mode, plus a second polarisation at 0.55x | One exponential is what a synth has - a real string drops several dB at once and then rings for two seconds |
| Four body resonances (60, 105, 200-450, 520-950 Hz) | A wooden box is why a note played at 49 Hz is heard through a speaker that stops at 80 |
| A finger burst and a fingerboard thud at every attack | Most of what identifies a double bass is not the string |
| One phase track, `_ftrack` glide | Portamento between notes is a fretless slide, and an attack re-excites a string that never stopped |
| The pitch a few cents sharp for 40 ms | The pluck stretches the string. This is the difference between played and switched on |

## And do not put a second oscillator under it

The instinct is to keep `subbar` underneath for the weight. Do not: two
continuous oscillators at the same pitch with unrelated phases cancel, and the
cancellation moves as the glide moves.

**Split one oscillator instead.** `contrabass(..., sub=0.22)` puts harmonic
one back on the *same phase track*, then `core.split(y, 130)` cuts the finished
instrument in two and the halves go to different buses - so the low half can be
collapsed to mono and ducked hard against the kick while the wood keeps its
width, and the two still sum back to exactly what came out of the oscillator.

**How to check it:** print the strongest peak under 200 Hz of the part in
isolation and compare it with the note being played. `ruffneck`'s bass reads
49.3 Hz against a written G1 of 49.0. A body resonance louder than the
fundamental means the box is over-mixed, and the ear will report the wrong
note however the band percentages look.

Related: [[bass-must-keep-its-own-fundamental]], [[a-bassline-written-as-notes-is-an-arpeggio]]
