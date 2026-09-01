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

## And the highpass is only half of it: check the octave

On `tvar` the same complaint came back twice - "оно стало ниже, но ноты всё
равно кажутся высокими" - while the mix measured *fatter* every time: 50% of
the energy under 120 Hz, 27% in 60-120, exactly the reference proportions. The
numbers were right and the ear was still right, because **perceived pitch is
the fundamental of the character layer**, and no amount of energy underneath it
changes what note the listener thinks they are hearing.

The character layer was playing F2, 87 Hz. He handed over the reference he had
in mind - `samples/reese_witch_a1_56hz.wav` - and it measures a fundamental of
**55.87 Hz**, with 28.8% of its energy under 60 Hz and no separate sub anywhere
in it. The reese *is* the bass, fundamental and all. Moving the note down an
octave to F1 fixed in one edit what three rounds of EQ had not touched.

So the layer split is not sub / mid / character. It is:

| | What it is |
|---|---|
| the creature | ONE oscillator carrying h1 upward, its own fundamental included |
| the sub bus | only the sections where the creature is absent or sparse |

Two continuous oscillators at 43.65 Hz with unrelated phases cancel, so if the
character layer has its own fundamental the separate sub has to get out of the
way rather than reinforce it. Building the low partials from the **same phase
track** as the character makes that impossible by construction.

**How to test it:** print the fundamental of the part in isolation and compare
it with the reference's, before touching a filter. A part an octave high reads
as "too high" through any EQ curve, and the band percentages will not say so.

**Why:** "deep" is not a frequency, it is whether the fundamental of the note
you are playing is present. Adding sub *underneath* a thin bass makes two
instruments; letting the bass keep its own bottom makes one.

Related: [[neurofunk-bass-is-a-dark-reese]], [[dnb-bass-is-gestures-not-notes]]
