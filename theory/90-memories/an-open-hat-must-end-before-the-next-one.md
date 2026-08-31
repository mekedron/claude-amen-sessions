---
name: an-open-hat-must-end-before-the-next-one
description: Four 909 open hats a bar with a real exponential tail is 1.6 seconds of noise inside a 1.95 second bar, which the ear hears as constant sand rather than as an offbeat
type: pitfall
date: 2026-09-01
---

The offbeat open hat is house's signature, so it gets written on all four
offbeats and given a 909's own decay. At 123 BPM that is four hits 488 ms
apart, each falling 26 dB in 470 ms - so every hat is still sounding when the
next one starts. Add a sixteenth-note shaker in the same octave and the top
of the record never stops. He heard it exactly: **"эти хай-хеты такие длинные,
они как будто занимают всё пространство... как будто вот этот песочный шум
всегда"**.

Two fixes, and the second one matters more:

1. **Truncate the hat.** A 909's open hat is a SAMPLE, and a sample ends. An
   exponential that is merely long leaves a tail under every following hit.
   130 ms of decay and then a raised-cosine window to silence by 300 ms
   measures -26 dB in 224 ms - under two sixteenths - and the offbeat becomes
   an event with air after it.
2. **Do not play four of them.** Open hats on the "and" of 1 and 3 with the
   other two offbeats closed is still unmistakably house, and it leaves the
   density of all four as something the arrangement can spend later. The same
   applies to the shaker: eighths for most of the record, sixteenths only for
   the two loudest sections.

**The number to check:** hat length at -26 dB, divided by the step length
(`15000 / BPM` ms). Above about 2.0 the hats overlap; above 3 the record is
sand. And two noise sources in the same octave - a hat high-passed at 5.4 kHz
over a shaker band-passed at 4.2-11.5 kHz - are one noise source twice as
loud, so move one of them (the shaker now sits at 3.4-9.5 kHz).

See [[minimal-means-fewer-voices]].
