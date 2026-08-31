---
name: a-chord-must-not-arrive-as-one-event
description: Block chords on any keyboard voice read to the user as a default preset pasted in; the fix is scattered entries, a moving spectrum and audible mechanism
type: feedback
date: 2026-09-01
---

A chord whose notes all start on the same sample, with the same spectrum and
the same envelope, reads as **a preset rather than an instrument** - however
good the voice underneath is. On `zaika` the user heard `core.ep()`, a
six-operator-style FM tine piano with velocity-dependent brightness and
per-note decay scaling, and rejected it in these terms: *"слишком древние,
какие-то слишком искусственные... как будто аккорд на самом простом обычном
синтезаторе без настроек нажал и вставил... как будто они лишние тут"*.

The complaint is not about the timbre. It is about four things that are true
of every block chord and of no real instrument:

1. **Simultaneity.** Ten fingers do not land on one sample. Scattering the
   entries over 20-90 ms in pitch order is most of the difference between "a
   chord" and "a chord being played".
2. **A fixed spectrum.** If the partials all fade at one rate the sound is a
   sample being faded out. Real strings shed their top first, and a bowed
   section changes colour as the bow leans in.
3. **No mechanism.** Hammer thud, key bed, bow noise, the box the strings sit
   in. Remove them and an instrument stops being an object.
4. **No role.** Two of the three chords on the first pass were doubling what
   the strings and the bass already said, which is what "лишние" means.

**How to apply:** `idmlib.felt()` is the answer built to those four points -
modal partials with stiffness, a fast prompt-sound layer, a second
polarisation, hammer noise and a `roll` parameter that staggers the notes. But
the more useful move on `zaika` was structural: **delete the chord instrument
entirely.** The harmony is a string section that has no attack at all
(`core.ens`, separate entries and independent intonation drift, with a filter
opening across the phrase) plus single felt notes dropped one at a time across
the bar. Nothing on that record ever plays a block.

Same underlying lesson as [[plucked-instruments-must-not-sound-synthetic]] and
[[hard-dance-needs-layers-and-effects]]: he hears physical behaviour and
processing depth, not correct notes.
