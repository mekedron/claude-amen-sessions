---
name: a-drifting-machine-must-land-on-an-eighth
description: A polymetric cycle of an EVEN number of steps drifts against the bar and still puts every hit on an eighth
type: decision
date: 2026-09-01
---

`walzwerk` is three machines running at once, and a machine shop only sounds
like one if they do not agree - which is the coprime-cycle trick the theory
recommends, and which [[parts-must-be-anchored-to-the-grid]] says produces
"a second machine playing badly" the moment the part has a pitch and a ring.

Both are right, and the way through is the **parity of the cycle**, not its
length.

A cycle of an **even** number of steps only ever lands on even steps, and
every even step is a beat or an offbeat eighth - the top two metrical tiers.
So a 6-step cycle hits 0, 6, 12 in bar one, 2, 8, 14 in bar two and 4, 10 in
bar three: it comes home after three bars, drifts against the bar the whole
way, and never once falls between the eighths. 10 steps gives five bars and
14 gives seven, and the three of them agree with each other again after 105.

An **odd** cycle - 5, 7, 13, the numbers a coprime rule suggests first -
spends half its life on weak sixteenths, which is exactly the figure that was
rejected in `otrazhenie`.

**How to apply:** for anything pitched that repeats on its own period, pick
the cycle from 6, 10, 14, 18 and put the accent of the cycle on its first
step. Odd cycles stay available for short dry unpitched ticks, which are the
one thing allowed to fall anywhere. `industriallib.mill()` takes `cycle` in
steps and says this in its docstring, because the parameter looks free and is
not.
