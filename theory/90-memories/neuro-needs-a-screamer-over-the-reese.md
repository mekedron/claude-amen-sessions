---
name: neuro-needs-a-screamer-over-the-reese
description: A reese measures dark because that is what a reese is; matching one and calling it the bass leaves the record with a shelf falling off a cliff at 1 kHz
type: pitfall
date: 2026-09-01
---

A reese one-shot out of a sample pack is a **foundation layer**, not a bass.
The one this engine is calibrated against - `samples/reese_witch_a1_56hz.wav` -
has **4% of its energy above 800 Hz**, and it is supposed to: that is what
makes it a reese.

On `tvar` the whole bass was built to match it, and the record measured a
**7.5 dB spread across 300 Hz - 11 kHz** with everything above 1 kHz sitting
5-6 dB down. He heard it as "глухой... не создаёт чувство наполненности", and
adding sub, opening the filter and shelving the master all failed, because the
energy was never generated.

**What was missing was a second bass layer**, and the genre's own build notes
say so: `abysslib.fang()` - hard sync two octaves up, FM at an integer ratio, a
wavefolder rather than a saturator, and **four resonances that TRACK the note**
(21x, 36x, 62x, 108x the fundamental) each sweeping half an octave on its own
rate. It shares the reese's phase track, so it is the same note and can never
disagree about tuning, and it shares the gesture lanes, so it moves with it
rather than beside it.

That closed 800-3000 Hz from 5.3% of the mix to 13.6% and 3-10 kHz from 4.3%
to 9.0%, and took the spread from 7.5 dB to under 5.

## Two things that cost a round trip each

- **Low and bright are different knobs.** Opening the cutoff for brightness
  raises the whole spectrum and the ear then hears a HIGHER NOTE - that is how
  this patch first ended up an octave up. A separate band-limited layer over an
  unchanged low end adds presence and moves no pitch. That is the entire reason
  the genre stacks layers instead of turning one filter.
- **Resonances parked at fixed harmonics are a comb**, and a comb's gaps
  measure as clearly as its peaks: with four of them nailed down the mix read
  -4 to -5 dB at 600, 1200 and 3800 Hz, exactly halfway between each pair.
  Swept on unrelated rates they cross the gaps and the time-average fills in.

**How to apply:** measure the third-octave spectrum from 300 Hz to 11 kHz on a
drop. The genre's own target is flat within 3 dB. If it tilts down past 1 kHz,
the answer is a source, not an EQ.

Related: [[bass-must-keep-its-own-fundamental]], [[neurofunk-bass-is-a-dark-reese]],
[[a-timbre-figure-must-not-repeat-exactly]]
