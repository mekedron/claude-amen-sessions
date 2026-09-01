---
name: shimmer-is-the-only-reverb-that-adds-notes
description: A reverb with a transposition inside its feedback path returns octaves that were never played; damping in the loop is what stops them stacking into a whistle
type: decision
date: 2026-09-01
---

`core.shimmer()` exists because `reverb()` cannot make a record sound like
morning. A convolution returns what went in, darker and later. Put a pitch
shift **inside the feedback path** and each pass comes back an octave above
the one before it, so a held chord grows a choir of its own harmonics that
nobody played - arriving late, in tune, and from further away every time.

Measured on one `ens` chord:

| | dry | through shimmer |
|---|---|---|
| 200-800 Hz | 78% | 26% |
| 800-3000 Hz | 22% | **73%** |
| rings for | 2.0 s | **6.3 s** |

Three things make it work rather than howl:

1. **Re-reverberate each pass.** The tail does not merely rise in pitch, it
   spreads: pass three has been through the room three times and has no
   transient left in it at all. Transposing the dry signal and mixing it in
   is a different, much worse effect.
2. **Damp inside the loop.** `damp` is not a tone control. Without a lowpass
   in the feedback path the top pass runs away and the whole thing becomes a
   whistle, which is the failure mode of every shimmer ever built.
3. **Highpass the return.** The octaves are the point; the fundamentals are
   already in the dry signal, and letting them round the loop puts mud where
   the bass is.

`shift` is a parameter and the octave is not the only useful value: 1.5 is a
fifth and stacks into a dominant ninth over four passes - bright and slightly
wrong; 0.5 is an octave DOWN and turns the same device into weight instead of
air.

**How to apply:** it is expensive - four convolutions per call, and a
six-second decay makes a segment four times longer than its input - so render
it per chord and cache it, never across a whole bus. And watch the ownership:
on `heimweg` it owns half of everything above 3 kHz, which is fine for a
sustained pitched consonance and would not be for noise
([[top-end-from-transients-not-wash]]).
