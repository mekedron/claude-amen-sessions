---
name: a-breakdown-must-keep-its-kick
description: Removing the backbeat to make a section feel emptier reads as beats being skipped, not as space; drop layers, never the pulse
type: preference
date: 2026-09-01
---

Two places in `ruffneck` took the drums apart to create contrast: four bars
of halftime snare inside the ragga section, and a dub breakdown with the kick
moved off beats 1 and 3. Both are textbook arrangement moves. He heard them
as a fault: **"в середине там есть именно такой ещё ломаный момент, где
пропускаются какие-то доли. Мне не очень это нравится."**

The distinction that matters is between **removing a layer** and **removing
the pulse**. A breakdown with no pad, no skank, no top break and no hats is
space. A breakdown that takes the kick off beat 3 and the snare off beats 2
and 4 is not quieter, it is *missing*, and the ear reports the gap as an
error rather than as a rest - because it was still counting.

So the contrast in a quiet section is made of everything except the beat:

| Take away | Keep |
|---|---|
| The break, the hats, the ghosts | The kick on 1 and 3 |
| The skank, the pad, the top layer | The backbeat on 2 and 4 |
| Six dB of level, via the ride | The bass line, even if only its first note |

This is also what dub actually does - the phrase is "drum **and** bass",
and the two things it never mutes are the two things in the name.

**How to apply:** verify it rather than trusting the arrangement. `verify.py`
prints the low band's energy per sixteenth; if any of steps 0, 4, 8 or 12
falls below about 0.5 of the bar's loudest step in a section, something has
been taken away that should not have been. And a halftime cell is only safe
if the *kick* stays on 1 and 3 while the snare moves - halftime in both at
once is a slow record whatever the tempo says.

Related: [[the-felt-pulse-is-in-the-low-band]], [[section-contrast-belongs-in-level]]
