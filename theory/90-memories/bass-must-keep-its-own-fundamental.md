---
name: bass-must-keep-its-own-fundamental
description: Highpassing the mid bass above its own fundamental is what makes it sound thin - "deep" means the note's first two harmonics are in the same instrument as the growl
type: pitfall
date: 2026-09-01
---

The mid-bass layer is highpassed at **~78 Hz, not at 105**. An F2 at 87 Hz cut
at 105 loses its own fundamental and its own second harmonic, and what is left
is a mid-range instrument sitting on top of a separate sub. He named it
exactly: "хотелось бы больше глубины, сделать их как-то ниже, глубже... они
должны быть более басистыми. Это же всё-таки основная бас-линия".

The three-layer split is still real - the sub is a clean mono sine and still
owns everything under about 70 Hz - but the crossover belongs *below* the
played note, not above it. Measured on `razryv`: moving the highpass from 105
to 78 Hz took 120-300 Hz from 12.5% to 17.4% of the mix and flattened the
low-band per-16th grid from 0.38-1.00 to 0.47-1.00, because the bass now
sustains through the bar in the band the grid measures.

Supporting moves that go with it: a low shelf at 190 Hz on the bass bus,
`mono_below` raised to 150 Hz so the extra weight is mono, and `reese(sub=…)`
adding a clean sine at the played note underneath the distortion.

**Why:** "deep" is not a frequency, it is whether the fundamental of the note
you are playing is present. Adding sub *underneath* a thin bass makes two
instruments; letting the bass keep its own bottom makes one.

Related: [[neurofunk-bass-is-a-dark-reese]], [[dnb-bass-is-gestures-not-notes]]
