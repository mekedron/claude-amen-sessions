---
name: a-spark-is-a-click-with-no-body
description: A repeated click reads as electrical rather than mechanical when it has no struck body, no low end and too high a top rate
type: pitfall
date: 2026-09-01
---

Of `servo()` in `walzwerk` he said: *"он как разряды тока... он как будто не
очень вписывается. Потому что у нас типа звучат какие-то колокола... они
скорее типа звучат, как будто мы бьем по каким-то бидонам. И вот это
электрический разряд с этими бидонами как-то не связывается."*

He is describing a category error, not a mix problem. Everything else in that
palette is a **struck object** - `anvil` is a plate, `pipe` is a tube, `mill`
bites metal - and `servo` is the only thing in it that nobody hit.

Three properties, and all three have to be wrong at once:

| | `servo` (arc) | `ratchet` (pawl) |
|---|---|---|
| what makes the click | a band-passed noise burst | four inharmonic partials, top ones dying first |
| 20-300 Hz | **0.0%** | 21% |
| 300-2000 Hz | **1.7%** | 72% |
| 2-11 kHz | **95%** | 7% |
| top rate | 340 clicks/s | 88 |

The low end is the one that matters most. A mechanism has **mass**: a
spring-loaded catch thuds at a pitch of its own that does not change as the
wheel speeds up, and that fixed low thud under a rising click rate is most of
what says "machine". Take it away and there is nothing for the room to
answer, which is exactly what an arc is - energy with no object in it.

The rate is the second: past about a hundred clicks a second the ear stops
resolving separate impacts and hears a buzz, and a buzz at 2-11 kHz is
electrical whatever it is made of. Bounding the accelerando at 88/s keeps it
countable. (Bounding it at all is also required - see
[[an-accelerating-click-train-can-diverge]].)

**How to apply:** `servo()` is correct where a record wants an electrical
event and four other tracks use it that way. In a shop, use `ratchet()`, and
before adding any repeated click ask what struck it and what has the mass.
The same test catches the wider version of this: a percussion voice belongs
with the others when it shares their **mechanism**, not when it shares their
band.

Related: [[struck-metal-needs-modes-not-squares]], [[bells-are-not-a-default-top-layer]]
