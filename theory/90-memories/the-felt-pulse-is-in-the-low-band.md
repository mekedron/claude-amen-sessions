---
name: the-felt-pulse-is-in-the-low-band
description: verify.py measures the pulse under 160 Hz, so a backbeat with no low content leaves a track reading as pulseless however busy the top is
type: pitfall
date: 2026-09-01
---

`verify.py`'s pulse grid lowpasses at 160 Hz, and it is right to: what the
body counts is the rate of the **low** events, not the number of things
happening. A kit with kicks on beats 1 and 3 and snares on 2 and 4 has an
event on every beat and still measures as pulseless, because the snare puts
nothing under 160 Hz. The first pass of `zaika` read

    1.00 0.93 0.83 0.57 | 0.51 0.49 0.65 0.62 | 1.00 0.96 0.88 0.61 | ...
    on-beat / off-beat = 1.04   (NO PULSE)

- steps 4 and 12, the backbeat, were the two *quietest* on-beat steps, while
the bass's passing notes on steps 2 and 10 were louder than them.

The fix is not a second kick. It is a **95 Hz thud inside the snare**, 50 ms
long, under the crack - which is what a layered drum & bass snare has anyway,
and which every one-shot library ships. `idmlib.crack(bottom=…)` is that
layer, and it moved the ratio from 1.04 to 1.16 without adding an event.

**Why:** the ratio compares steps 0/4/8/12 against 2/6/10/14, so anything
sustained that moves on the offbeats - a rolling sub, a passing note, a bass
that answers the kick - actively pushes it below 1. A track can therefore lose
its pulse by having a *busier* bass, which is the opposite of the instinct.

**How to apply:** print the pulse grid before mixing anything. If steps 4 and
12 sit below 0.65 while 0 and 8 are at 1.00, the backbeat has no bottom.
Related: [[section-contrast-belongs-in-level]].
