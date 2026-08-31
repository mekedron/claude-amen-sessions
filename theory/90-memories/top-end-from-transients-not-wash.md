---
name: top-end-from-transients-not-wash
description: A sustained ride or open-hat layer owning the top end reads to him as painful; the brightness should come from the snare
type: pitfall
date: 2026-09-01
---

He hears a sustained cymbal layer as fatiguing - "ударники на фоне... слишком
много шума добавляют", then "тарелки как-то по ушам бьют" - and the fix is not
a shelf on the master. It is which *source* owns the band.

Measure it: sum the 3-16 kHz energy of one bar's worth of each voice, weighted
by how many times it plays and by its mix gain. On the first pass of `razryv`
the ride owned **63%** of the top end - eight hits a bar, each a 300 ms
broadband wash. After shortening its partial decays, cutting its noise layer
from 0.30 to 0.11 and dropping its level, the snare owns **82%** and the ride
2.7%.

That is the right shape. Two snare hits a bar are transients: the ear takes
them as events and they do not accumulate. A ride sustaining under the whole
groove is a noise bed, and a noise bed at 6-9 kHz is what hurts after ninety
seconds.

**How to apply:** before EQ'ing the top end, run the ownership sum. If a
sustained voice is above about 20% of it, fix the voice - shorter decay, less
noise, lower level - rather than the bus. And when brightness has to come
back, take it from transient sources (the snare's crack, short metal, the
chord layer) and not from the wash.

Related: [[pitched-metal-reads-as-cheerful]]
