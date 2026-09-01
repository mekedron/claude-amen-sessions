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

**And then it went too far the other way.** The first repair opened the
sections to 9.6 dB and the 8-bar rows to 12, and he heard that as the record
changing volume rather than as structure - which is what
[[section-contrast-belongs-in-level]] already says the window is for. Pulled
back, the body of the record spans **6.3 dB**, the holes are 0.17 of a bar at
-10 dB rather than a full beat at -22, and the intro and outro are the only
things outside it because they are fades.

The lesson is not the number. It is that **the two faults have different
fixes and only one of them is the ride**: the palette differences and the
bass instrument are what make a drop, and the level is what stops it being a
jump.

**A fifty-six bar drop needs its own re-drop.** ABSTICH measured a 0.4 dB
plateau across its whole length until bars 182-183 were stripped to the kick
and the beam with a hole after them.

Related: [[section-contrast-belongs-in-level]], [[bass-must-keep-its-own-fundamental]]
