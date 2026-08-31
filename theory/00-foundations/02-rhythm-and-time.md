# Rhythm, Meter and Time

Harmony decides what a track *means*. Rhythm decides whether anyone stays in the
room. In every modern genre, rhythm is the primary parameter — get the grid
wrong and no chord progression will save it.

## The units

| Name | Fraction of a 4/4 bar | Steps (16ths) | US name |
|---|---|---|---|
| Whole note | 1 | 16 | semibreve |
| Half | 1/2 | 8 | minim |
| Quarter | 1/4 | 4 | crotchet — "the beat" |
| Eighth | 1/8 | 2 | quaver |
| Sixteenth | 1/16 | 1 | semiquaver |
| Thirty-second | 1/32 | 0.5 | demisemiquaver |
| Dotted note | ×1.5 | dotted 8th = 3 | |
| Triplet | ×2/3 | 8th triplet = 4/3 ≈ 1.333 | |

A **dot** adds half the value. A **tie** joins two values. A **tuplet** divides a
span into an unusual number of parts: a triplet fits 3 where 2 belong, a
quintuplet 5 where 4 belong.

## Tempo maths — memorise these four lines

```
seconds_per_beat  = 60 / BPM
seconds_per_bar   = 60 / BPM * beats_per_bar         # 4/4: 240 / BPM
seconds_per_step  = 60 / BPM / 4                     # one 16th in 4/4
ms_per_step       = 15000 / BPM
```

| BPM | 1 bar (4/4) | 1 beat | 1/8 | 1/16 | 1/16 triplet |
|---|---|---|---|---|---|
| 70 | 3.429 s | 857 ms | 429 ms | 214 ms | 143 ms |
| 85 | 2.824 s | 706 ms | 353 ms | 176 ms | 118 ms |
| 90 | 2.667 s | 667 ms | 333 ms | 167 ms | 111 ms |
| 100 | 2.400 s | 600 ms | 300 ms | 150 ms | 100 ms |
| 120 | 2.000 s | 500 ms | 250 ms | 125 ms | 83 ms |
| 128 | 1.875 s | 469 ms | 234 ms | 117 ms | 78 ms |
| 140 | 1.714 s | 429 ms | 214 ms | 107 ms | 71 ms |
| 150 | 1.600 s | 400 ms | 200 ms | 100 ms | 67 ms |
| 160 | 1.500 s | 375 ms | 188 ms | 94 ms | 63 ms |
| 174 | 1.379 s | 345 ms | 172 ms | 86 ms | 57 ms |
| 175 | 1.371 s | 343 ms | 171 ms | 86 ms | 57 ms |

Everything time-based in a mix should be derived from this table: delay times,
LFO rates, envelope releases, reverb pre-delay, riser lengths. A delay set to
"about 300 ms" is noise; a delay set to a dotted 8th is a part.

**LFO rate in Hz for a note value**: `hz = BPM / 60 / beats_per_cycle`.
At 140 BPM: 1/4 LFO = 2.333 Hz, 1/8 = 4.667 Hz, 1/2 = 1.167 Hz, whole bar =
0.583 Hz.

## Meter: how beats group

**Time signature** `n/d`: `n` units of a `1/d` note per bar.

| Signature | Feel | Where it lives |
|---|---|---|
| 4/4 | Square, universal | ~95% of popular and electronic music |
| 3/4 | Waltz, circular | Ballads, folk, some ambient |
| 6/8 | Two big beats each split in 3 | Blues shuffle, doo-wop, epic score |
| 12/8 | Four big beats split in 3 | Slow blues, gospel, some trap |
| 2/4 | March, cut, urgent | Latin, polka, punk, footwork |
| 5/4, 7/8 | Limping, alert | Prog, math rock, IDM, Balkan folk |
| 9/8, 11/8 | Additive, dance-y in context | Balkan, Turkish aksak, prog metal |

**Simple** meters divide the beat in 2 (4/4). **Compound** meters divide it in 3
(6/8, 12/8). **Additive** meters group unequal cells: 7/8 as 2+2+3 feels totally
different from 3+2+2.

### The 4/4 hierarchy of strength

```
strength:  4 . 1 . | 3 . 1 . | 3.5 . 1 . | 2 . 1 .     (approximate weights)
step:      0 1 2 3 | 4 5 6 7 | 8 9 10 11 | 12 13 14 15
           ^beat 1   ^beat 2   ^beat 3     ^beat 4
```

Beat 1 is strongest, beat 3 next, then 2 and 4, then the "and" of each beat
(steps 2, 6, 10, 14), then the remaining 16ths. **Placing an event on a strong
beat confirms the meter; placing it off one destabilises it.** All syncopation
is a game played against this table.

## Syncopation

Syncopation = accent where the hierarchy says there should not be one, or
silence where it says there should.

Devices, weakest to strongest:

1. **Backbeat** — accent on 2 and 4. Now so normalised it reads as neutral.
2. **Offbeat 8ths** — accents on steps 2, 6, 10, 14. The house offbeat hat.
3. **Pushed downbeat (anticipation)** — the chord or note arrives one 16th
   *early*, on step 15 of the previous bar. The single most effective
   groove trick in funk, house, samba and pop. Costs nothing, changes everything.
4. **Delayed downbeat** — the event lands on step 1 or 2 instead of 0. Lazy,
   dubby, hip-hop.
5. **Dotted-8th cycle (3-step)** — hits every 3 steps: 0, 3, 6, 9, 12, 15,
   then 2, 5 in the next bar. Resolves every 3 bars. Instant "modern" feel; the
   backbone of UK garage, dubstep hats, trap hats, and countless arps.
6. **Tresillo (3+3+2)** — hits on steps 0, 3, 6 in an 8-step half-bar; over a
   full bar: 0, 3, 6, 8, 11, 14. The most widespread rhythm on earth —
   reggaeton's dembow, Cuban son, trap 808 patterns, EDM chord stabs.
7. **The missing downbeat** — leave step 0 empty entirely and let the ear fill
   it. Terrifying and effective; the core of jungle and of half the drops in
   electronic music.

## Swing and microtiming

**Swing** delays every second subdivision. Expressed as a percentage of the pair:

| Swing % | Delay of the offbeat 16th | Feel |
|---|---|---|
| 50% | 0 (exactly on grid) | Straight, machine, techno |
| 54–56% | +8–12% of a step | Barely felt, "human", house |
| 58–62% | subtle-to-clear lilt | Classic MPC hip-hop, garage |
| 66.7% | full triplet | Shuffle, swing jazz, boogie |
| 70–75% | past triplet | Drunken, lurching, dub |

`swing_offset_ms = (swing_pct/100 - 0.5) * 2 * ms_per_step`

**HAZARD:** apply swing only to the offbeat subdivision (odd 16ths), never to
downbeats, or the whole track slides. And do not swing the kick and the hats by
different amounts unless you want flamming — but *do* consider swinging only the
hats and leaving the kick straight; that is the UK garage sound.

**Microtiming** is smaller than swing and it is where "feel" lives:

| Move | Offset | Effect |
|---|---|---|
| Snare late | +5 to +20 ms | Laid back, relaxed, hip-hop, D'Angelo |
| Snare early | −5 to −15 ms | Urgent, pushing, punk, drum'n'bass rolls |
| Hats slightly late | +3 to +8 ms | Behind-the-beat groove |
| Bass early vs kick | −5 to −10 ms | Bass "leads", funk |
| Everything quantised | 0 | Techno, trance, hyperpop — a valid choice |

Humanisation for programmed music: random timing jitter of ±3–8 ms and random
velocity of ±8–15% on non-accent hits. More than ~15 ms of jitter reads as
sloppy, not human.

## Polyrhythm vs polymeter

- **Polyrhythm**: two different divisions of the *same* span. 3-against-2 fits 3
  notes where 2 belong (hemiola). 3:4 and 5:4 are the useful ones in electronic
  music — an arp in 3 over a beat in 4.
- **Polymeter**: same pulse, different bar lengths. A 7-step loop over a 16-step
  bar realigns every 7×16/gcd = 112 steps = 7 bars. This is the cheapest way to
  make a static loop feel alive: give one element a cycle length coprime with 16
  (3, 5, 7, 9, 11).

Cycle length before repeat: `lcm(a, b)`.

| Loop A | Loop B | Realigns after |
|---|---|---|
| 16 | 3 | 48 steps (3 bars) |
| 16 | 5 | 80 steps (5 bars) |
| 16 | 6 | 48 steps (3 bars) |
| 16 | 7 | 112 steps (7 bars) |
| 16 | 12 | 48 steps (3 bars) |

## Euclidean rhythms

Distributing `k` hits as evenly as possible over `n` steps produces almost every
traditional rhythm on the planet. Notation `E(k, n)`:

| Pattern | Steps | Name / use |
|---|---|---|
| E(2,5) | `x-x--` | Khafif |
| E(3,4) | `xx-x` | Cumbia, calypso |
| E(3,8) | `x--x--x-` | **Tresillo** — dembow, trap, son |
| E(4,9) | `x--x-x-x-` | Turkish aksak |
| E(5,8) | `x-xx-xx-` | **Cinquillo** — Cuban |
| E(5,16) | `x--x--x--x--x---` | Bossa-ish clave feel |
| E(7,16) | `x-x-x-x--x-x-x--` | Busy but even; good for hats |
| E(9,16) | `x-xx-x-xx-x-xx-x` | Dense percussion layer |

Generation: `hit(i) = floor(i*k/n) != floor((i-1)*k/n)`. Rotating the pattern
(starting from a different index) changes its character completely — rotation is
as important as the pattern itself.

## Halftime, doubletime, and the tempo illusion

The *written* tempo and the *felt* tempo are different things.

- **Halftime**: keep the tempo, move the snare from step 4/12 to step 8 only.
  174 BPM drum'n'bass suddenly feels like 87 BPM hip-hop. The hats and bass
  still run at the fast grid, which is why it feels heavy rather than slow.
- **Doubletime**: double the subdivision density without changing the tempo.
- **Double-drop / tempo pun**: 85 BPM trap and 170 BPM drum'n'bass share a
  grid. 75 BPM and 150 BPM, 87.5 and 175 — any track can be re-heard at 2× or
  ½×. Producers exploit this to switch genres mid-track without a tempo change.
- **Triplet feel at speed**: 140 BPM with triplet 16ths ≈ 210 BPM straight.

## Phrase length — rhythm above the bar

Almost all popular and dance music is built in powers of two:

```
1 bar  → cell
2 bars → the smallest coherent loop
4 bars → a phrase
8 bars → a sentence; the standard unit of arrangement
16 bars → a section
32 bars → a "movement" (a full drop, a full verse-chorus)
```

The ear counts these unconsciously. **Something must change every 8 bars** and
something must change at every 16. A 4-bar loop repeated 8 times without
variation is not minimalism, it is an unfinished track.

Deviations that work:
- **The 6-bar phrase** — a truncated 8; sounds urgent, common in UK bass.
- **The 12-bar blues** — 3 groups of 4.
- **The turnaround bar** — bar 8 of an 8-bar phrase carries a fill and a
  harmonic push back to bar 1.
- **The dropped bar** — cut bar 16 to 15 to jolt the listener into a chorus.

## Groove: the thing that is not on the grid

A groove is the sum of four things, in order of importance:

1. **Which subdivisions carry accents** (the pattern itself).
2. **Velocity contour** — the difference between the loudest and quietest hit.
   A hat line with all hits at the same level is dead. Real drummers span
   30–40 dB across a bar. Alternating hats loud/soft (`x . x . x . x .`) is the
   single cheapest groove upgrade available.
3. **Microtiming** — see above.
4. **Note length / decay** — staccato vs sustained changes groove as much as
   placement. Shortening a bass note by 30 ms opens a hole the kick fills.

**Ghost notes** are hits at 10–30% of full velocity, usually snare, on weak
16ths. They are inaudible as events but change the feel completely. Funk,
neo-soul, jungle and liquid drum'n'bass are built on them.

## Rests, space and density

Silence is a rhythmic value with the same status as a note.

- **Density curve**: a track's excitement is largely `events per bar`. Build-ups
  raise it, drops often *lower* it violently (the classic dubstep drop is
  emptier than the build).
- **The one-bar hole**: removing everything for a beat or a bar before a section
  change is the most reliable attention grab in music. Do not overuse — twice
  per track.
- **HAZARD:** programmatically generated music is almost always too dense.
  When in doubt, delete a layer. If a pattern sounds boring when sparse, the
  problem is the pattern, and adding notes hides it rather than fixing it.

## Related

- Concrete grids per genre: `10-drums-and-groove.md`, `../30-patterns/04-drum-pattern-cookbook.md`
- Delay/LFO tables: `../40-reference/03-bpm-and-timing-tables.md`
- Phrase structure at track scale: `11-form-and-arrangement.md`
