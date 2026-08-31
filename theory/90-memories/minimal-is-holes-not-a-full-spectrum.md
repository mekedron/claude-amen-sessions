---
name: minimal-is-holes-not-a-full-spectrum
description: A balanced full-range mix is the wrong target for minimal house; he hears an always-occupied spectrum as heavy, and the fix is measured in how many bands are lit at once
type: preference
date: 2026-09-01
---

For anything he calls minimal, chill or light, **an evenly filled spectrum is
the defect, not the goal.** On `barhat` the mix was tuned band by band until
every octave was populated - the textbook move, and the reason he stopped it:
*"он какой-то не минимальный получается... как будто полностью все частоты
как будто заняты всегда... должен быть легким. Типа реально легким, как
перышко, как будто по воздуху плывешь."*

Band SHARES cannot see this. Two records with identical percentages sound
nothing alike if one of them plays all its bands all of the time. Measure
**occupancy** instead: band-pass into seven bands, take a 50 ms RMS envelope,
call a band "on" when it is within 12 dB of its own 90th percentile, and count
how many are on at each instant.

| | lit at once | all 7 lit | 3 or fewer |
|---|---|---|---|
| funk (`pyatnica`) | 6.20 / 7 | 53% | — |
| minimal techno (`maskarad`) | 5.89 | 50% | — |
| deep house (`terrasa`) | 5.29 | 31% | 17% |
| **light house (`barhat`)** | **4.51** | **11%** | **24%** |

Below about 4.6 lit and under ~15% all-lit is where "light" starts.

**What actually moved the number**, in order of effect - and none of it is EQ:

1. **Delete the redundant part.** A shaker on the eighths under closed hats on
   the eighths is one part twice as loud; both occupy the same octave and the
   same grid.
2. **Hats on the offbeats only.** Eight a bar spells out the subdivision; four
   leaves air between them.
3. **Holes in time, written in.** One bar in eight with no chords at all, and
   one with no percussion. The empty bar is the one that gets noticed.
4. **`hold` on the bass from 0.36 to 0.22**, so notes fall into a gap instead
   of holding a floor under the whole bar.
5. **Fewer events per bar everywhere** - four chords, not eight; four bass
   notes, not six; two percussion hits, not four.

**Why:** density is a time-domain property and every meter on the mastering
checklist is a frequency-domain one, so the thing he is listening for is
invisible to the tools unless it is measured on purpose. Chasing a flat
spectrum actively fights it - the instinct when a band measures thin is to put
something in it, and in this genre the thin band IS the genre.

Related: [[minimal-means-fewer-voices]], [[top-end-from-transients-not-wash]],
[[an-open-hat-must-end-before-the-next-one]]
