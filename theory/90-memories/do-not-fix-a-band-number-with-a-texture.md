---
name: do-not-fix-a-band-number-with-a-texture
description: Chasing "not enough above 3 kHz" by turning up a scattered click layer produces audible crackle; the band number was right and the cure was worse than the complaint
type: pitfall
date: 2026-09-01
---

On `heimweg` the record measured 0.6% of its energy above 3 kHz, which
[[industrial-techno-measures-too-dark]] correctly calls a fault. The fix
applied was to turn up `minimallib.dust` - and `dust`'s own docstring says
what it is: *"micro-clicks scattered across a bar. Individually inaudible."*

Across four separate edits it received:

    dustg x2.1  .  placement gain x1.6  .  bus gain x2.33  .  +5 dB shelf
    = about +23 dB, with the density raised from 14 clicks a bar to 26

The band number moved from 0.6% to 1.4%. The user's report was
*"какие-то потрескивания появились"*, and measured, the record had gone from
**0.2 isolated high-band ticks per second to 19.5** against 6.4 for
`finsternis` and 0.0 for `blendung` and `nebel`. The extra brightness WAS the
crackle; removing it put the band back to 0.85%.

**Two lessons, and the second is the general one.**

A texture of random short bursts and a played part can occupy the same band
at the same level and be completely different things. `verify.ticks()`
separates them by **grid lock** - the resultant vector length of each tick's
phase within a sixteenth. Validated on the two extremes:

| | ticks/s | grid lock | verdict |
|---|---|---|---|
| the dust layer at the level that crackled | 60.9 | **0.10** | CRACKLE |
| a shaker line, same band, same density | 0.0 | — | clean |
| `finsternis` (sixteenth hats at 142 BPM) | 9.3 | **1.00** | played |

Nine ticks a second is a hi-hat line by design. Nine scattered ones is a
fault, and no count alone can tell them apart.

**And: a band-balance number is a symptom, never a target.** The right
response to an empty top was a brighter INSTRUMENT - the open hat, the
shaker, the shimmer's `tone`, all of which are events or pitched sustains -
not more of a layer whose entire purpose is to be beneath notice. When a
measurement is bad, fix the thing the measurement is describing.

Related: [[top-end-from-transients-not-wash]],
[[a-repeated-hit-must-not-be-identical]]
