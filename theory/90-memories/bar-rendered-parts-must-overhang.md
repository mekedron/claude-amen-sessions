---
name: bar-rendered-parts-must-overhang
description: A part rendered one bar at a time has to render PAST the bar line, or every note that was meant to ring into the next bar is silenced exactly where it should land
type: pitfall
date: 2026-09-01
---

Any voice that renders a whole bar as one segment - `punklib.bassbar`,
`minimallib.line`, `neurolib.phrase`, `latinlib.tumbao`, `latinlib.montuno` -
must be given a length **longer than the bar**, with the note edges still on
the bar's grid. Six to eight sixteenths of overhang is enough at 174 BPM.

Rendering exactly `dur_steps=16` truncates every tail at the bar line, and
the segment's own end-fade then wipes the last few milliseconds as well. The
symptom is not an obvious click: it is a **hole in the first half of every
bar**, because the note that was supposed to be ringing through it stopped.

In `descarga` the cost was the whole idea of the track. The bass plays a
tumbao, so beat 4 carries the root of the *next* chord - the anticipation,
which is the reason the music leans forward. Cut at the bar line, that note
died at the moment it was meant to arrive. The low-band energy per sixteenth
measured `0.51 0.18 0.08 0.14 0.26 0.16 1.00 ...` - the first six steps of
every bar nearly empty, all the weight in the second half. Adding seven steps
of overhang moved it to `0.86 0.50 0.39 0.37 0.48 0.31 1.00 ...` and took the
on-beat/off-beat ratio from 1.00 to 1.15.

**Why:** the bar is a unit of *notation*, not of sound. Nothing an instrument
does respects it - a piano string rings for a second and a half, a plucked
bass for half of one - and the places composers most want a note to cross the
line (anticipations, ties, suspensions, the pickup into the next phrase) are
exactly the places this destroys.

**How to apply:** give every bar-at-a-time renderer a `tail=` parameter,
default it to 5-8 steps, and let the segments overlap when they are placed -
`Session.place` sums, so nothing else needs to change. Verify with the
per-sixteenth low-band grid in `src/analyze.py`: if the bar starts quiet and
ends loud, a tail is being cut. See [[section-contrast-belongs-in-level]].
