---
name: a-repeated-hit-must-not-be-identical
description: Three voices drew their noise from a fixed RandomState, so every kick click and every hat in a record was bit-identical; the user hears that as a metronome, not a drum
type: pitfall
date: 2026-09-01
---

On `finsternis` the user reported a crackle: *"кик дает вот этот вот треск,
потому что она трещит, как будто как метроном какой-то... метронома всегда
какая-то высокий звук"*, and then located it exactly - *"ровно с десятой
секунды начинается тряск"*, which at 142 BPM is bar 6, the bar the kick's
lowpass came off and the open hat entered.

Two causes, both measurable, and the first one is systemic:

**1. The noise was the same every time.** `techkick`'s click layer drew from
`RandomState(7)`, `hat909` from `RandomState(seed + 77)` with `seed`
defaulting to 0 and never passed, and `distclap` from `RandomState(11)`. So
in a six-minute record every one of ~4000 kick transients and ~10000 closed
hats carried **bit-identical noise**. Nothing in a real kit repeats exactly,
and a short bright sound that does stops being heard as an instrument and
starts being heard as a tick - which is precisely what a metronome is.

The fix is a `seed` derived from the position: `cseed=(b * 16 + st) % 89`.
Bound it with a modulus so the segment cache stays finite.

**2. The grit layer was aliasing.** `techkick`'s grit is two waveshapers in
series - a hard `tanh` on a swept saw, then a wavefolder - and `saw_ph()`
chooses its harmonic count from the frequency it is handed. It was handed
`tune * 11`, the RESTING pitch, while the phase it renders starts
`(1 + rise)` times higher: at a 38.9 Hz kick the saw is momentarily at
163 Hz and its partials reach **68 kHz against a 22.05 kHz Nyquist**.

Measured against an 8x reference, computing that layer at 1x has **-21 dB of
aliasing error** - 9% of it arriving as inharmonic fizz on the attack of
every kick, identical every time. At 4x it is -34 dB.

**How to apply:**

- Any voice whose sound is noise or a transient takes a `seed`, and the
  caller varies it per hit. Check it: two calls with different seeds must
  differ, and `np.abs(a - b).max()` of 0.000 is the bug.
- Any waveshaper on a swept source is computed oversampled. The test is not
  "does the spectrum look odd" - a swept tone is smeared by construction, and
  that measurement lies. Render the same thing at 8x, decimate, and take the
  difference; that number is the aliasing and nothing else is.
- When brightness is added to a kick, `mid` is body and is safe; `click`,
  `grit` and `tone` are the tick. He asked for brighter kicks, got `click`
  1.55 and `grit` 0.36, and reported a metronome.

Related: [[an-open-hat-is-not-a-closed-hat-opened]],
[[top-end-from-transients-not-wash]]
