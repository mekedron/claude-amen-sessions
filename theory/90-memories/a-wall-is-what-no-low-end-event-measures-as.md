---
name: a-wall-is-what-no-low-end-event-measures-as
description: A hard record whose bass is only kick, rumble and sub has nothing for a drop to land on, and measures as a flat band
type: pitfall
date: 2026-09-01
---

The first pass of `walzwerk` had a correct arrangement, correct band balance
and a pulse ratio of 1.87, and measured **-9.8 to -6.3 LUFS from 0:22 to
5:31** - a five-minute wall inside a 3.5 dB band, with every section within
2.5 dB of the peak.

Two causes, and neither is a fader.

**1. Every section owned the same instruments.** Floor, tops, pipes, clinks,
plates, stabs, offbeat bass, three machines, hall, drone and girder played in
all of them. A section can only feel like an arrival if the previous one was
missing something, so the fix is written as a subtraction: WALZWERK now has no
stabs, no plates, no bass and no shear for thirty-two bars, and STANZE is
made of exactly the things it has been denied.

**2. There was no bass INSTRUMENT.** `techkick` is a transient, `rumble` is a
room and `weight` is a floor - none of them is an event, and a drop needs
something to land on. `shear()` is that: one oscillator split at 92 Hz, the
weight clean and untouched, everything above it through a wavefolder whose
amount ramps across the phrase and a resonant lowpass moved by a `scanlane`
that accelerates from a quarter to a sixty-fourth without retriggering.

The move that makes it a *drop* rather than a louder bar: **where the shear
plays, the kick's own clean sub comes almost all the way out** (`wg` 0.9 to
0.30). Two sines at 43 Hz with unrelated phases cancel anyway, and handing
the bottom over changes the character of the low end instead of its level.
It ends up owning 39% of 20-120 Hz against the drums' 52%.

**And the hole is not something the arrangement can make.** A gap means every
bus at once, so it belongs in the ride: a notch to -17 dB for the last beat
before each arrival, ramped over 40 ms. Measured, those beats sit 13-17 dB
under the record.

After both, the sections span **9.6 dB** and the curve reads -21 -> -7 ->
-18 -> -6.5 -> -12.6 -> -5.9 -> -13.

**A fifty-six bar drop needs its own re-drop.** ABSTICH measured a 0.4 dB
plateau across its whole length until bars 182-183 were stripped to the kick
and the beam with a hole after them.

Related: [[section-contrast-belongs-in-level]], [[bass-must-keep-its-own-fundamental]]
