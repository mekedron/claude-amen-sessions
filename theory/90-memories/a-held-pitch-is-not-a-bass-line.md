---
name: a-held-pitch-is-not-a-bass-line
description: One note under a moving filter reads as low-frequency noise, and a second bass on complementary steps fills the gaps of the first
type: pitfall
date: 2026-09-01
---

`walzwerk`'s first bass was `shear()` playing ONE pitch for eight bars with a
wavefolder ramping and a resonant filter sweeping on it. Everything about the
timbre was moving and he heard no instrument at all: *"она не раздельная...
просто какая-то низкая частота трещит, и всё"*.

**Timbral movement is not articulation.** A gesture that carries a drum &
bass line ([[dnb-bass-is-gestures-not-notes]]) carries it because the LINE is
already established by pitch and by gaps; strip both and the same gesture is
a texture, and what the ear reports about a texture in the sub is noise.
`shear()` now takes `(step, midi, length)`, builds its frequency from
`core._ftrack` so the oscillator stays continuous and the changes glide, and
builds its gate from the note lengths so the gaps are real.

**And then the mix filled the gaps anyway.** Written alone the line left 25%
of its sixteenths below -12 dB in 60-400 Hz. In the render that was **2%**,
because three other things were playing in the same band:

- `distbass` on 2, 6, 10 and 14 against a line answering on 6, 10 and 14 -
  two bass instruments on complementary steps are one continuous bass;
- `rumble` at 0.85 s decay, whose tail spans two beats and therefore every
  hole the line is made of;
- the machines, high-passed at 95 Hz, sitting on the line's own octave.

Removing the offbeat bass wherever the line plays, shortening the rumble to
0.52 s there and moving the machines' high-pass to 138 Hz is what made it
audible. The fix was never in the bass.

**How to apply:** write the part, measure its own duty cycle, then measure it
again in the mix. If the second number is much smaller than the first, the
problem is what else is in the band and not the part. And `bitcrush` with
`downsample=2` has no place on a bass at all - decimating without an
anti-alias filter folds everything above 11 kHz back down, which on the
lowest element of a record is not grit, it is a crackle.

Related: [[a-bassline-written-as-notes-is-an-arpeggio]], [[bass-must-keep-its-own-fundamental]]
