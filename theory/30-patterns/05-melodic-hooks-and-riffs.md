# Melodic Hooks, Riffs and Arps

Concrete shapes. Degrees are given relative to the tonic (`1 2 b3 4 5 b6 b7 8`),
so they transpose to any key.

## Hook archetypes

### The three-note hook
The smallest thing that can be a hook. Pick three notes with one distinctive
interval.
```
1 – 5 – b3        heroic then sad
1 – b3 – 4        blues-tinged, catchy
5 – 4 – 1         resolving, satisfying
1 – 2 – 5         open, questioning
b6 – 5 – 1        yearning
1 – b7 – 5        modal, cool
```

### The repeated-note hook
The same pitch, rhythmically distinctive, with the harmony changing beneath.
```
melody: 5 5 5 5 - 5 5 -
chords: i        bVI
```
The note is the 5th of i and the maj7 of bVI. One note, two meanings.

### The arch
```
1 – 2 – b3 – 5 – b3 – 2 – 1
```
Rise to a peak two-thirds through, then fall. The default phrase shape.

### The falling hook
```
8 – b7 – 5 – 4 – b3 – 1
```
Resignation, resolution, closure. Common in minor-key EDM leads.

### The rising sequence
```
1 – b3 – 4    then    b3 – 5 – b6    then    5 – b7 – 8
```
The same 3-note shape moved up the scale. Builds without new material.

### The call and response
```
call (bars 1-2):  1 – 5 – b3 – 2      (ends on 2 = unresolved)
resp (bars 3-4):  1 – 5 – b3 – 1      (ends on 1 = resolved)
```

## Genre-typical lead shapes

| Genre | Shape | Notes |
|---|---|---|
| **Trance lead** | Long notes, arch, 8 or 16 bars | `1 – 2 – b3 – 5 | 4 – b3 – 2 – 1` |
| **Big room** | Two or three notes, rhythmically punched | `1 1 - 1 | b3 - 1 -` |
| **Future bass** | Chord-tone melody over rich chords | Follows the top voice of the chords |
| **Synthwave** | Singable, nostalgic, mid-range | `5 – 8 – b7 – 5 – 4 – 5` |
| **D&B / liquid** | Sparse, jazzy, leaves space | `b3 – 5 – b7 – 9 | 5 – 4 – b3` |
| **Trap melody** | 2-bar loop, dark, narrow range | `1 – b2 – 1 – b7(low) – 1` |
| **Drill melody** | Pizzicato, angular, sparse | `1 – 5 – b6 – 5 – b3` |
| **Techno** | Not a melody; a filtered, resonant motif | one or two pitches |
| **House** | Vocal-derived, soulful | `5 – b7 – 8 – b7 – 5 – 4` |
| **Pop chorus** | Higher than the verse, few words, long notes | `5 – 6 – 5 – 3 – 1` (major) |
| **Metal riff** | Chromatic, rhythmic, low | `1 – 1 – b2 – 1 – 1 – b5` |
| **Funk riff** | 16ths, syncopated, pentatonic | `1 – b3 – 4 – 5 – 4 – b3` |

## Arpeggio patterns

Given a chord `[0, 3, 7, 10]` (m7):

| Pattern | Sequence | Feel |
|---|---|---|
| Up | 0 3 7 10 | Rising, classic |
| Down | 10 7 3 0 | Falling |
| Up-down (inclusive) | 0 3 7 10 7 3 | Circular |
| Up-down (exclusive) | 0 3 7 10 10 7 3 0 | Symmetric |
| Up 2 octaves | 0 3 7 10 12 15 19 22 | Wide, trance |
| Thumb / Alberti | 0 7 3 7 | Baroque, classical |
| Octave-alternating | 0 12 3 15 7 19 10 22 | Glittering |
| Random-in-chord | shuffled | Generative |
| Converging | 0 22 3 19 7 15 10 12 | Complex, IDM |
| Pedal + moving | 0 3 0 7 0 10 0 12 | Insistent, ostinato |

### Making an arp into a hook

1. **Break the length symmetry.** Use a 3, 5, 6 or 7-note pattern over a 16-step
   bar so it displaces every bar.
2. **Add one non-chord note.** The 9th or the 4th, once per cycle.
3. **Accent one step differently.** Velocity, filter, or pan.
4. **Change one note when the chord changes**, keeping the rest.
5. **Gate it** with a rhythmic pattern rather than playing every 16th.
6. **Octave-jump one note** per cycle.

## Ostinato and riff construction

An ostinato is a short figure repeated unchanged. Rules for one that survives
100 repetitions:

- **1 or 2 bars.** Never 4.
- **A distinctive rhythm** — one you could clap.
- **A small range** — a fifth or less.
- **One "hook" interval** — a leap, a chromatic step, a repeated note.
- **A gap.** At least one beat of rest, so the ear can breathe.

Examples:
```
Rhythm:  x - - x | - - x - | x - - - | - - - -
Pitch:   1     5   b3        1
```
```
Rhythm:  x x - x | - x - - | x x - x | - - - -
Pitch:   1 1   b3   4       1 1   5
```

## Counter-melody

A second line that fits against the main one.

Rules:
1. **Different rhythm.** Move when the melody rests.
2. **Different register.** At least a sixth away.
3. **Mostly consonant** with the melody at strong beats (3rds, 6ths, 5ths,
   octaves).
4. **Simpler than the melody**, or the ear cannot decide what to follow.
5. **Contrary motion** where possible.

The easiest effective counter-melody: hold long notes on chord tones that move by
step every 2 bars, while the melody is busy.

## Vocal chop patterns

Slice a sung phrase into 8 or 16 pieces, then re-sequence:

| Pattern | Description |
|---|---|
| **Chord player** | Map slices across a keyboard; play the progression with one syllable |
| **Rhythmic stutter** | One slice repeated on 16ths with pitch changes |
| **Melodic re-write** | Re-order the slices to make a new melody |
| **Reverse-in** | A reversed slice leading into a forward one |
| **Formant sweep** | Same slice, formant automated across the bar |
| **Gate/chop** | The whole phrase played through a 16th-note gate |

## Motif development template

Given a 2-bar motif M:

```
bars 1-2    M                       (statement)
bars 3-4    M transposed up a step  (sequence)
bars 5-6    fragment of M, repeated (fragmentation, building)
bars 7-8    cadence figure          (resolution)
```

That is a complete 8-bar melody built from one idea. Vary by:
- Sequencing down instead of up.
- Inverting M in bars 3–4.
- Augmenting M (doubling note lengths) in bars 5–6 for a "big" feeling.
- Extending bars 7–8 into a 4-bar cadence for a 10-bar phrase (unsettling, good).

## Tension-note reference (what to land on)

| Over | Sweet | Spicy | Avoid on a long note |
|---|---|---|---|
| `maj7` | 1, 3, 5, 7, 9, 13 | #11 | 4 (natural 11) |
| `m7` | 1, b3, 5, b7, 9, 11 | 13 | b9, b13 |
| `7` | 1, 3, 5, b7, 9, 13 | b9, #9, #11, b13 | 4 |
| `m7b5` | 1, b3, b5, b7, 11 | 9, b13 | — |
| `sus4` | 1, 2, 4, 5, b7 | — | 3 |
| `dim7` | any chord tone, +2 above each | — | — |

## Hazards

- A melody with no repetition — nothing to remember.
- A melody that never rests.
- A melody in the same octave as the pad, the vocal or the mid bass.
- Every phrase starting on the downbeat with the tonic.
- Random-walk pitch selection within a scale.
- Arpeggios as a substitute for a melody.

## Related

- Melody theory: `../00-foundations/08-melody.md`
- Chords to build hooks over: `../00-foundations/05-chords.md`
