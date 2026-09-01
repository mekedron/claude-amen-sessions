---
name: a-sliced-break-must-not-be-jittered
description: Timing jitter on a chopped break flams against the clean kick layered under it, and redrawn every bar it reads as the drums drifting out of tempo
type: pitfall
date: 2026-09-01
---

`idmlib.edit()` nudges every hit it places by `humanise=0.0035` of a bar -
about fourteen milliseconds at 166 BPM, redrawn from the seed each time. In
drill'n'bass that is correct: the break is the only kit on the record and the
scatter is the aesthetic. In `ruffneck` it produced the one complaint that was
about the drums: **"у барабанов какой-то рассинхрон... как будто они все не
сочетаются в темп друг с другом."**

The mechanism is layering, not the jitter itself. Under the break sit `thump`
on beats 1 and 3 and `crack` on 2 and 4, placed at `s.pos(b, k)` - exactly on
the grid. So the break's own kick lands up to fourteen milliseconds either
side of the clean one that is reinforcing it, and the offset is a different
random number every bar. Two transients that far apart are heard as a flam,
and a flam whose size changes bar to bar is heard as two players who are not
counting the same tempo.

Fourteen milliseconds is also inside the Haas window, so it moves the
perceived position of the hit rather than thickening it.

**How to apply:** the moment anything clean is layered against a sliced
break - a kick under its kick, a snare under its snare - pass
`humanise=0.0`. A break is a recording of a person playing drums; its feel
arrived with it, and adding jitter to a sampled performance does not humanise
it, it smears it. Save the jitter for the layers that have nothing doubling
them: shakers, ghosts, percussion, a second break.

Related: [[the-felt-pulse-is-in-the-low-band]], [[a-breakdown-must-keep-its-kick]]
