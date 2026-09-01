---
name: an-accelerating-click-train-can-diverge
description: A geometric accelerando converges, so a while-loop waiting for it to reach the end of the segment never terminates
type: pitfall
date: 2026-09-01
---

`industriallib.servo()` places clicks whose repetition rate accelerates:

    ts, cur, r = [], 0.0, rate
    while cur < dur_s:
        ts.append(cur); cur += 1.0 / r; r *= accel ** (1.0 / max(rate * dur_s, 1))

The gaps are `1/r` and `r` grows geometrically, so **the gaps are a geometric
series and it converges.** If it converges to less than the segment's length,
`cur` never reaches `dur_s`, the loop never exits, and `ts` grows until the
process is killed.

`rate=11, accel=3.2, dur=2.14 s` converges at 1.9 s and hangs. `rate=8,
accel=5.0, dur=8.57 s` converges at 5.4 s and hangs. `rate=15, accel=2.6,
dur=1.43 s` sums to 1.52 s and is fine - which is why this survived in four
tracks and six calls before it was hit.

**The failure gives you nothing to go on.** No exception, no traceback, no
partial output: the render dies with exit code 0 and an empty log, because
everything the script prints comes at the end. Three renders were lost to it
before the cause was found by bisecting on section markers.

**How to apply:** the fix is a ceiling rather than a guard, because a real
stepper motor has one - `r = min(r * accel ** (...), rmax)` with `rmax=340`.
Once `r` is bounded, `1/r` is bounded below and the loop always advances.

The general form is worth keeping: **any loop whose step size shrinks
multiplicatively needs a floor on the step, not a cap on the iterations.** A
cap on the iterations hides the bug; a floor on the step fixes it and is
usually the physically correct behaviour anyway.

Related: [[smoothers-return-tiny-negatives]]
