# Form and Arrangement

Form is the plan. Arrangement is which elements sound at which bar. Together they
are the single largest factor in whether a piece of music holds attention — much
larger than harmony, and larger than sound design.

## The universal principle: contrast

**A section only feels big because the previous one was small.** Every arrangement
technique reduces to managing contrast in four dimensions:

| Dimension | Low | High |
|---|---|---|
| **Density** | few elements, few notes | many elements, busy |
| **Register** | narrow band, no highs or lows | full spectrum |

Register is the most under-used of the four. Which *frequency bands* are
occupied should differ between sections — see `20-spectral-arrangement.md`.

| **Loudness** | quiet, headroom | loud, compressed |
| **Rhythmic energy** | long notes, sparse | fast subdivisions, syncopation |

You do not need all four to move together, and the most interesting moments
happen when they diverge (a quiet but rhythmically frantic section, a loud but
sparse drop).

## The bar-count skeleton

Almost all popular and electronic music is built from 8-bar units and their
multiples. Work in this vocabulary:

```
 1 bar   cell
 2 bars  loop
 4 bars  phrase
 8 bars  sentence  ← the fundamental unit of arrangement
16 bars  section
32 bars  a full drop / a verse-chorus pair
64 bars  half a track
```

At 128 BPM, 8 bars = 15 s, 16 bars = 30 s, 32 bars = 60 s.
At 174 BPM, 8 bars = 11 s, 16 bars = 22 s, 32 bars = 44 s.
At 90 BPM, 8 bars = 21 s, 16 bars = 43 s.

Use these to hit target durations. A 3:30 track at 128 BPM is ~112 bars.

## Song forms

### Pop / vocal forms

| Form | Structure | Notes |
|---|---|---|
| **Verse–Chorus** | I V C V C B C C | The default since 1960 |
| **AABA** | 32-bar song form: A A B A | Jazz standards, early pop, city pop |
| **Verse–Prechorus–Chorus** | I V P C V P C B C | The modern pop standard |
| **Strophic** | A A A A | Folk, ballads, storytelling |
| **Through-composed** | A B C D | Prog, art song, film |
| **Post-chorus / drop** | ... C D C D | Post-2010 pop; the "drop" replaces the instrumental chorus |

Modern pop timings: intro ≤ 8 s, first chorus by 0:50, total 2:30–3:20.

### Electronic dance forms

| Form | Structure |
|---|---|
| **Classic club** | Intro (16–32) – Build (16) – Drop (32) – Breakdown (16–32) – Build (16) – Drop 2 (32) – Outro (16–32) |
| **Two-drop EDM** | Intro – Verse – Build – Drop – Breakdown – Build – Drop 2 (bigger) – Outro |
| **Long-form techno** | 8-bar layer additions for 5–9 minutes, one or two breakdowns, gradual subtraction |
| **Liquid D&B** | Intro – 1st drop (32) – Breakdown (16–32) – 2nd drop (32, more elements) – Outro |
| **Ambient** | No sections; slow evolution, no beat, 6–20 minutes |

### Classical forms (still useful)

| Form | Structure | Modern application |
|---|---|---|
| **Binary** | A B (each repeated) | Two-part instrumental |
| **Ternary** | A B A | The "breakdown and return" of dance music |
| **Rondo** | A B A C A D A | Recurring hook with contrasting episodes |
| **Sonata** | Exposition (theme 1, theme 2 in new key) – Development – Recapitulation (both themes in tonic) | Film score, prog, long-form |
| **Theme and variations** | A A' A'' A''' | The literal model of loop-based electronic music |
| **Passacaglia / chaconne** | Repeating bass, varying material above | Exactly what a techno track is |
| **Fugue** | Subject imitated across voices | Rare; but "subject entries" = element introductions |

## The DJ-friendly club arrangement

For music intended to be mixed:

- **Intro**: 16–32 bars of drums (and little else) at the top, so a DJ can beat
  match. Kick from bar 1 or bar 9.
- **Outro**: 16–32 bars, mirroring the intro, elements subtracting.
- **Phrase alignment**: every structural change lands on a multiple of 8 (ideally
  16) from bar 1. No off-grid section starts.
- **No full-spectrum content in the intro/outro** — leave room for the other
  track. Keep the bass simple and the melody absent.

## The energy curve

Sketch the whole track as a number from 0 to 10 per 8-bar block *before* writing
anything. Example for a 128-bar club track:

```
bars:    0    16   32   48   64   80   96   112  128
energy:  2    4    8    9    3    5    9    10   4
section: int  bld  drp  drp  brk  bld  drp2 drp2 out
```

Rules that make a curve work:

1. **Never sustain 10.** If everything is maximum for 3 minutes, nothing is.
2. **The lowest point must come immediately before the highest.** The breakdown
   exists to make the second drop enormous.
3. **The second drop must exceed the first** — by one new element, a wider
   stereo image, an octave, a key lift, or a new rhythm, not by volume.
4. **The last 16 bars are a resolution or an exit**, not a new idea.
5. **Introduce elements one at a time** and each on a phrase boundary.

## The arrangement matrix

Write your track as a grid: elements × 8-bar blocks. This is the most useful
single artifact in arrangement.

```
bars:        0-7  8-15 16-23 24-31 32-39 40-47 48-55 56-63
kick          -    x     x     x     x     -     x     x
sub bass      -    -     x     x     x     -     x     x
hats          x    x     x     x     x     x     x     x
clap          -    -     x     x     x     -     x     x
pad           x    x     x     -     -     x     x     x
lead          -    -     -     x     x     -     x     x
vocal         -    -     -     -     x     x     x     -
riser         -    -     -     -     -     -     x     -
impact        -    -     x     -     -     -     x     -
```

Reading down each column tells you the density. Reading across each row tells you
whether an element is boring (all x) or wasted (one x).

**The subtraction test:** in every 8-bar block, at least one element that was
present in the previous block should be *absent*. Arrangements fail by
accumulation far more often than by sparseness.

## Transitions — how sections connect

| Device | Where | Effect |
|---|---|---|
| **Riser / uplifter** | Last 1–4 bars of a build | Rising pitch or filtered noise; raises expectation |
| **Downlifter** | First bar of a new section | Falling sweep; releases pressure |
| **Impact / boom** | On the downbeat of the new section | Marks arrival |
| **Reverse cymbal** | Last 1–2 beats | Classic, slightly dated, still works |
| **Snare roll** | Last 1–4 bars | Accelerating; the EDM standard |
| **Filter sweep** | Over 4–16 bars | Gradual opening or closing |
| **Silence / cut** | Last 1–2 beats | The most powerful of all; use twice per track |
| **Tape stop** | Last beat | Playful, hip-hop, breaks the illusion |
| **Vocal ad-lib / stab** | Last beat | Human, marks the seam |
| **Beat repeat / stutter** | Last 1–2 beats | Modern, digital |
| **Drum drop-out** | Last bar | Everything but the melody vanishes |
| **Crash + kick** | Downbeat | The plain, universal marker |

**Compound transitions** work best: silence for 1 beat, then impact + crash +
sub-drop + full mix. Layering 3–5 devices at one seam is normal.

## Build-ups

A build has to raise *at least three* of these simultaneously:

1. **Pitch** — riser, arpeggio ascending, filter cutoff opening.
2. **Rhythmic density** — snare roll accelerating 1/8 → 1/16 → 1/32.
3. **Loudness** — everything crescendos.
4. **Register** — high-passing the mix so the bass drops away and returns.
5. **Harmonic tension** — sit on the dominant, or on a sustained chord that
   cannot resolve until the drop.
6. **Space** — increase reverb/delay, then cut it dead at the drop.

Length: 8 bars for a normal build, 16 for a main-drop build, 4 for a fast reset.

**The last beat before the drop should be empty or nearly empty.** The gap is
what makes the drop land.

## Breakdowns

Breakdowns remove the drums. What replaces them:

- The main melody, exposed, with reverb.
- A new chord progression or a re-harmonisation of the existing one.
- A vocal.
- Atmosphere: pads, field recordings, noise, drones.
- Half-time or free-time material.

Length: 16–32 bars in dance music, 8–16 in pop. A breakdown that goes on too long
loses the room; one that is too short does not reset the ear.

## Intros

The first 8 seconds decide whether anyone hears the rest.

| Approach | Effect |
|---|---|
| **Cold open on the hook** | Streaming-era default; no time wasted |
| **Atmosphere first** | Cinematic; earns patience |
| **Drums only** | DJ-friendly, club standard |
| **Filtered version of the drop** | Promises what is coming |
| **Vocal a cappella** | Immediate human interest |

## Outros

| Approach | When |
|---|---|
| **Subtractive** | Club music; mirror the intro |
| **Sudden stop** | Punk, hyperpop, hip-hop; confident |
| **Fade out** | Deprecated in the streaming era, but correct for a groove that has no natural end |
| **Coda / new material** | Album context, prog |
| **Return of the intro material** | Circular, satisfying |

## Density and layer counts

A practical guide to how many simultaneous elements each section should have:

| Section | Elements | Example |
|---|---|---|
| Intro | 2–4 | drums + pad |
| Verse | 4–6 | drums, bass, chords, vocal |
| Build | 5–8 | + riser, roll, fx |
| Drop / chorus | 6–10 | everything |
| Breakdown | 2–5 | pad, vocal, fx |
| Outro | 2–4 | drums + one element |

**HAZARD:** more than about 10 simultaneous elements and the mix stops being
legible regardless of how well it is balanced. Frequency space, not track count,
is the limit.

## Repetition and variation — the loop problem

Loop-based music lives or dies on this. Techniques for keeping a 4-bar loop
interesting for 3 minutes:

1. **Filter automation** — the workhorse. Slow cutoff movement over 16–32 bars.
2. **Element rotation** — swap which layers are muted every 8 bars.
3. **Octave changes** — move the lead or bass up/down an octave for 8 bars.
4. **Rhythmic variation of one element** — the hats change pattern, nothing else.
5. **Harmonic variation** — the 4th repetition of a loop changes its last chord.
6. **Fills and edits** at phrase boundaries.
7. **Effect throws** — a delay or reverb send opened for one hit.
8. **Polymetric layers** — one element on a 5- or 7-step cycle so the combination
   never quite repeats.
9. **Timbral evolution** — a slowly opening filter, growing distortion, widening
   stereo.
10. **Sudden absence** — mute everything but one part for a bar.

## Writing an arrangement: a working procedure

1. Choose tempo, key and total length. Convert length to bars.
2. Draw the energy curve in 8-bar blocks.
3. Name the sections and assign bar ranges, all on multiples of 8.
4. Write the core loop (drums, bass, chords) for the highest-energy section
   first. **Write the drop before the intro.**
5. Derive every other section by *subtraction* from the drop, not by writing
   fresh material.
6. Add the one contrasting section (breakdown / bridge) with genuinely new
   material or a re-harmonisation.
7. Place transitions at every seam.
8. Run the subtraction test on the matrix.
9. Check that something changes at every 8-bar boundary and something big at
   every 16 or 32.

## Related

- Where these numbers come from: `02-rhythm-and-time.md`
- Genre-specific arrangement maps: `../20-genres/`, `../30-patterns/10-arrangement-templates.md`
- The drop in detail: `../30-patterns/02-drop-and-buildup.md`
