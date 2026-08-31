---
name: section-contrast-belongs-in-level
description: A breakdown that measures within 1 dB of the drops is not a breakdown, however different its instrumentation - measure the per-section RMS before calling an arrangement finished
type: pitfall
date: 2026-09-01
---

Before a track is finished, measure **RMS per section** and look at the curve.
`src/analyze.py` prints it. The lowest section must sit **3-6 dB under** the
drops, and the lowest of all must be the one immediately before the biggest.

A first pass of `descarga` had a sixteen-bar breakdown in which the drums
stopped entirely, the piano switched from the guajeo to a written solo, and
the break vanished. It measured **-13.2 dB against the drop's -12.5** - a
difference of 0.7 dB, which is inaudible. Every part had been *changed* and
none had been *turned down*, so the percussion, congas, bass and piano
between them refilled the hole the drums left within one bar.

**Why:** contrast is relative and the ear judges the drop against what it
just heard. Removing an element only reads as removal if the total energy
drops with it; a section that swaps a loud thing for another loud thing reads
as a variation, not as a fall. And a drop is only big because the thing
before it was small - so a breakdown that fails to fall also spends the drop
that follows it.

The fix was a gain ramp across the whole section rather than a different
arrangement: every part entering at 0.55 of its drop level and climbing back
over sixteen bars. That moved it to -16.2 dB, 3.7 dB under the drop, and the
band curve moved with it - the 3-16 kHz content fell 11 dB, because that is
where the break lives and the break was gone.

**How to apply:** print the section table before mixing anything. Check three
things: the curve rises overall, the minimum precedes the maximum, and the
peak lands 60-90% of the way through. Fix a flat curve with section gains,
not with EQ or with more parts. See [[bar-rendered-parts-must-overhang]].
