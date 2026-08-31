# Scales and Modes

A scale is a set of pitch classes, given as semitone offsets from a tonic. Its
job is to define what is "in" and what is "out" — and the "out" notes are half
of what makes music expressive.

## The major scale and its modes

The major scale: `[0, 2, 4, 5, 7, 9, 11]` — the step pattern **W W H W W W H**
(2 2 1 2 2 2 1).

Rotate the starting point and you get the seven modes. All contain the same
notes; what changes is which note is home, and therefore which intervals are
measured against it.

| Mode | Offsets | Character note | Feel | Where you hear it |
|---|---|---|---|---|
| **Ionian** (major) | 0 2 4 5 7 9 11 | — | Bright, resolved, plain | Pop, classical, EDM anthems |
| **Dorian** | 0 2 3 5 7 9 10 | **natural 6** (9) | Minor but hopeful, cool | House, funk, jazz, drum'n'bass, Santana |
| **Phrygian** | 0 1 3 5 7 8 10 | **b2** (1) | Spanish, dark, exotic, menacing | Flamenco, metal, trap, hard techno |
| **Lydian** | 0 2 4 6 7 9 11 | **#4** (6) | Floating, wondrous, cinematic | Film score, dream pop, prog |
| **Mixolydian** | 0 2 4 5 7 9 10 | **b7** (10) | Major but bluesy, folky, rooted | Rock, funk, Britpop, Celtic |
| **Aeolian** (nat. minor) | 0 2 3 5 7 8 10 | **b6** (8) | Sad, serious, default minor | Everything in a minor key |
| **Locrian** | 0 1 3 5 6 8 10 | **b5** (6) | Unstable, no home | Almost unused as a key; metal riffs |

### Brightness ordering

Sort the modes by how many raised degrees they have:

```
brightest  Lydian → Ionian → Mixolydian → Dorian → Aeolian → Phrygian → Locrian  darkest
```

Each step down the list lowers exactly one note. This is a compositional tool:
to darken a section without changing key, flat the next degree in that chain
(major → mixolydian by flatting the 7th → dorian by flatting the 3rd → aeolian
by flatting the 6th → phrygian by flatting the 2nd). Modal *interchange*
between two adjacent brightness levels is nearly seamless.

### Relative vs parallel

- **Relative**: same notes, different tonic. A minor is the relative minor of C
  major (tonic 9 semitones up, or 3 down). Formula: `relative_minor = major + 9`.
- **Parallel**: same tonic, different notes. C major and C minor. Switching
  between parallel major and minor is the single most emotionally direct move
  available in tonal music.

## Minor scales — three of them

Minor is not one scale. It is a family, because the natural minor's b7 is too
weak to make a strong cadence.

| Scale | Offsets | Notes |
|---|---|---|
| **Natural minor** (Aeolian) | 0 2 3 5 7 8 10 | The default. Cadence V is minor → weak pull. |
| **Harmonic minor** | 0 2 3 5 7 8 **11** | Raised 7th creates a real dominant V7. The b6→7 gap is an augmented second — the "Arabic"/"neoclassical" sound. |
| **Melodic minor** (ascending) | 0 2 3 5 7 **9 11** | Raised 6 *and* 7 — smooths the gap. Classically descends as natural minor; in jazz it stays raised both ways ("jazz minor"). |

**Practical rule:** write your melody in natural minor, and raise the 7th only
inside the dominant chord at a cadence. That gives you the pull without the
neoclassical flavour bleeding everywhere.

### Modes of harmonic minor (the useful ones)

| Mode | Offsets | Character |
|---|---|---|
| Phrygian dominant (5th mode) | 0 1 4 5 7 8 10 | Major 3rd + b2. Flamenco, klezmer, metal, psytrance, Egyptian-sounding leads. |
| Ukrainian Dorian (4th mode) | 0 2 3 6 7 9 10 | Dorian with #4. Eastern European, dark-bright. |
| Hungarian minor (harm. minor #4) | 0 2 3 6 7 8 11 | Two augmented seconds. Maximum "gypsy scale" drama. |

### Modes of melodic minor (the jazz workhorses)

| Mode | Offsets | Use |
|---|---|---|
| Lydian dominant (4th mode) | 0 2 4 6 7 9 10 | Over dominant 7#11. Bright, floating, funk and fusion. |
| **Altered / Super-Locrian** (7th mode) | 0 1 3 4 6 8 10 | Over an altered dominant (7alt: b9 #9 b5 #5). Maximum tension before resolution. |
| Locrian ♮2 (6th mode) | 0 2 3 5 6 8 10 | Over half-diminished (m7b5) chords. |

## Pentatonics — five notes, zero wrong answers

| Scale | Offsets | Notes |
|---|---|---|
| **Major pentatonic** | 0 2 4 7 9 | Major without 4 and 7 — removes both half-steps, so nothing clashes. Folk, country, pop hooks, Asian traditional. |
| **Minor pentatonic** | 0 3 5 7 10 | Relative of the above (same set, tonic moved). Rock, blues, hip-hop, everything. |
| **Blues scale** | 0 3 5 **6** 7 10 | Minor pentatonic + the b5 "blue note". The b5 is a passing tone; land on it and it sounds wrong, pass through it and it sounds essential. |
| **Major blues** | 0 2 3 4 7 9 | Major pentatonic + b3 passing tone. Country, gospel, rockabilly. |
| **Japanese (Hirajōshi)** | 0 2 3 7 8 | Sparse, austere, immediately "Eastern". |
| **In Sen** | 0 1 5 7 10 | Dark Japanese pentatonic. |
| **Egyptian / suspended pent.** | 0 2 5 7 10 | Fourths-flavoured, ambiguous, great for ambient. |

**Why pentatonics matter for generated music:** with a pentatonic you can pick
notes at random over almost any diatonic progression and it will not sound
wrong. It is the safety net. The cost is that it also cannot sound *specific* —
you lose the leading tone and the character notes that give a mode its identity.

## Symmetric scales

Scales that repeat at an interval smaller than an octave. They have no strong
tonic, which is exactly why they are used for suspense, transition and magic.

| Scale | Offsets | Repeats every | Sound |
|---|---|---|---|
| **Chromatic** | all 12 | 1 semitone | No centre at all |
| **Whole tone** | 0 2 4 6 8 10 | 2 semitones | Dreamlike, weightless, Debussy, "dissolve" transitions |
| **Diminished (H-W)** | 0 1 3 4 6 7 9 10 | 3 semitones | Over dim7 and altered dominants; horror, chase scenes |
| **Diminished (W-H)** | 0 2 3 5 6 8 9 11 | 3 semitones | Over dominant 7b9; jazz, neo-soul |
| **Augmented** | 0 3 4 7 8 11 | 4 semitones | Eerie, Twin-Peaks, sci-fi |
| **Tritone scale** | 0 1 4 6 7 10 | 6 semitones | Petrushka-ish, angular |

Only 2 unique whole-tone scales, 3 unique diminished scales, 4 unique augmented
scales exist — which is why they blur tonality: any transposition lands you back
in the same note set.

## Scales from other traditions

Use these for colour, and know that in their home traditions they carry rules
(ornament, direction, time of day, characteristic phrases) that a bare note set
does not capture.

| Scale | Offsets | Origin / feel |
|---|---|---|
| Hijaz / Phrygian dominant | 0 1 4 5 7 8 10 | Arabic maqam Hijaz, Jewish Ahava Rabbah. |
| Nahawand | 0 2 3 5 7 8 10 | ≈ natural minor, Arabic phrasing |
| Bayati | 0 1.5 3 5 7 8 10 | Uses a **quarter tone** on the 2nd — not playable in 12-TET |
| Rast | 0 2 3.5 5 7 9 10.5 | Quarter tones on 3rd and 7th |
| Raga Bhairav | 0 1 4 5 7 8 11 | Indian; b2 and b6 with major 3rd and 7th |
| Raga Yaman | 0 2 4 6 7 9 11 | = Lydian; evening raga |
| Raga Bhairavi | 0 1 3 5 7 8 10 | = Phrygian |
| Pelog (approx.) | 0 1 3 7 8 | Javanese gamelan; real pelog is not 12-TET |
| Slendro (approx.) | 0 2 5 7 9 | Gamelan, near-equal 5-division of the octave |
| Hungarian major | 0 3 4 6 7 9 10 | Bartók; wild, bright-dark |
| Enigmatic | 0 1 4 6 8 10 11 | Verdi's puzzle scale; genuinely strange |
| Prometheus | 0 2 4 6 9 10 | Scriabin; mystic, hovering |
| Double harmonic (Byzantine) | 0 1 4 5 7 8 11 | Two augmented 2nds; "Misirlou" |

**HAZARD (respect):** if you are reaching for maqam or raga names, either
implement their behaviour (characteristic phrases, microtones, ascent/descent
asymmetry) or describe what you did honestly as "a scale borrowed from". A note
list is not a maqam.

## Choosing a scale

A short decision procedure:

1. **Major or minor?** Minor is the default for almost all modern electronic and
   hip-hop music. Major reads as pop, house, gospel, anthemic, or naive.
2. **Which flavour of minor?**
   - Aeolian → serious, neutral sadness (trance, D&B, cinematic)
   - Dorian → groove-forward, cool, not tragic (house, funk, liquid D&B, garage)
   - Phrygian → menace and exotic edge (trap, hard techno, metal, drift phonk)
   - Harmonic minor / Phrygian dominant → theatrical, neoclassical, psytrance
3. **Do you want a character note to be audible?** If yes, make sure the chord
   progression *contains* it. Dorian without an audible natural 6 is just minor.
   The classic way: use a **IV major** chord in a minor key (that is the natural
   6), or **bII** for Phrygian, or **II major** for Lydian.
4. **Pentatonic for the melody, full scale for the harmony** is a safe default
   that almost never fails.

## Which key?

In equal temperament, all keys are transpositions — the "character of C# minor"
is a myth from unequal temperaments. What is *not* a myth:

- **Register**: the key decides where your parts land relative to the sweet
  spots of instruments and of human hearing. F minor puts a bassline in a
  fatter place than B minor.
- **Convention**: club music clusters around A, F, G, C, D minor because those
  put the root sub between ~40 and 75 Hz where systems reproduce it best.
  Roots at MIDI 33 (A1, 55 Hz), 29 (F1, 43.7 Hz), 31 (G1, 49 Hz) are the
  workhorses.
- **Vocals**: pick the key from the singer's range, always, before anything else.

**Practical default for electronic music: F minor, G minor, or A minor.**

## Related

- Chords built on these scales: `05-chords.md`
- How scale choice becomes a progression: `06-harmony-function.md`
- Formula tables in machine-friendly form: `../40-reference/02-scale-and-chord-formulas.md`
