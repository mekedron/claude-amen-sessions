---
name: note-envelopes-need-a-release
description: core._line_envs ended every note by stopping, so a 240 ms decay left the waveform stepping from 64% to zero in one sample - a click on most notes of every line it renders
type: pitfall
date: 2026-09-01
---

`core._line_envs` writes each note's amplitude into `amp[a:b]` and leaves
zero outside it. The envelope at `b` is `exp(-dur / decay)`, so with the
240 ms decay a bass 303 wants and a one-step note at 142 BPM, **the note is
still at 64% of its level when its span ends** - and the next sample is zero.

    worst amplitude step   0.644 -> 0.016      (release 6 ms)
    worst cutoff step      0.922 -> 0.005      (cut_smooth 4 ms)

That is a click on most notes, in every voice built on this function -
`core.line`, `minimallib.acidline` and `industriallib.deepacidline`. It went
unnoticed for a long time because in those tracks the 303 is a mid-range hook
under a loud kick and the kick masks it. Put the same renderer in the bass,
make it the loudest thing in the mix, and it is naked: the user's report was
*"как будто где-то щелкает... и в принципе на протяжении трека тоже"*.

The cutoff envelope has the same shape and the same problem - `morph_lp`
crossfades a bank of static filters by that value, so a step in it swaps
filters mid-waveform, which is a tick at the top of the spectrum.
`industriallib.acidline` already smoothed `cut` for exactly this reason;
nothing else did.

**How to apply:** both are now parameters of `_line_envs` with defaults that
are on - `release=0.006`, `cut_smooth=0.004`. Six milliseconds is far shorter
than any note and removes the step completely. When writing any new
envelope, the test is `np.abs(np.diff(env)).max()`: anything near the
envelope's own peak value is a cut, not a decay.

And when hunting a click, band-limit the detector. A big jump between two
samples finds every kick and every hat, because a transient IS a big jump and
is meant to be. `verify.clicks()` lowpasses at 2 kHz first: a 46 Hz sine at
full scale moves 0.0066 per sample, so any step down there is something that
was cut rather than something that was played, and percussion is invisible
to it.

Related: [[a-repeated-hit-must-not-be-identical]]
