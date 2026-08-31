# Intervals

An interval is the distance between two pitches. It is the atom of everything:
scales are interval patterns, chords are interval stacks, melodies are interval
sequences, and consonance is an interval property.

## The table — learn this cold

| Semitones | Name | Short | Sound | Example from C4 (60) |
|---|---|---|---|---|
| 0 | Unison | P1 | Same note | C4 (60) |
| 1 | Minor second | m2 | Grinding, fear, dissonance | Db4 (61) |
| 2 | Major second | M2 | Step, mild tension, "next" | D4 (62) |
| 3 | Minor third | m3 | Sad, soft, minor | Eb4 (63) |
| 4 | Major third | M3 | Bright, happy, major | E4 (64) |
| 5 | Perfect fourth | P4 | Open, suspended, heroic | F4 (65) |
| 6 | Tritone | TT (A4/d5) | Unstable, evil, jazz colour | F#4 (66) |
| 7 | Perfect fifth | P5 | Hollow, powerful, stable | G4 (67) |
| 8 | Minor sixth | m6 | Yearning, dark-sweet | Ab4 (68) |
| 9 | Major sixth | M6 | Warm, nostalgic, pastoral | A4 (69) |
| 10 | Minor seventh | m7 | Bluesy, groovy, wants to fall | Bb4 (70) |
| 11 | Major seventh | M7 | Dreamy, sophisticated, sharp | B4 (71) |
| 12 | Octave | P8 | Same note, new register | C5 (72) |

Beyond the octave (compound intervals): add 12.

| Semitones | Name | Also called |
|---|---|---|
| 13 | Minor ninth | b9 — the harshest colour in tonal music |
| 14 | Major ninth | 9 — the sweetest colour |
| 15 | Minor tenth | #9 in a dominant chord (the "Hendrix" sound) |
| 16 | Major tenth | M3 an octave up — the safe wide voicing |
| 17 | Eleventh | 11 (sus/quartal) |
| 18 | Sharp eleventh | #11 — lydian brightness, the "film" interval |
| 20 | Thirteenth | 13 — same pitch class as M6, but functions upward |

## Consonance and dissonance, ranked

Roughly by how "at rest" two simultaneous tones sound:

```
most consonant   P8  P5  P4  M3  m3  M6  m6  m7  M2  M7  m2  TT   most dissonant
```

Two caveats that matter more than the ranking:

1. **Register changes everything.** A minor second at C5 is a shimmer; the same
   interval at C1 is mud. Below ~150 Hz, anything closer than a perfect fifth
   turns into a rumble. See the *low interval limit* in `07-voice-leading.md`.
2. **Context changes everything.** In 1400, the third was a dissonance. In 1900,
   the m7 was. Today a maj7#11 is a pop chord. Dissonance is a
   *statistical expectation*, and genre sets the statistics.

## What each interval does emotionally

Useful when you are choosing a melodic leap or a top-note colour.

| Interval | Emotional reading | Typical use |
|---|---|---|
| m2 | Threat, insect, pain | Horror, tension risers, chromatic bass |
| M2 | Motion, neutral | Melodic steps, sus2 openness |
| m3 | Melancholy, tenderness | Minor-key hooks, blues, lullabies |
| M3 | Confidence, warmth, arrival | Major-key hooks, fanfares |
| P4 | Call, question, openness | Sus chords, quartal pads, horn calls |
| TT | Instability, menace, wit | Dominant chords, metal, jazz alterations |
| P5 | Power, emptiness, ancient | Power chords, drones, organum, sub bass |
| m6 | Longing | Minor-key climaxes, romantic score |
| M6 | Nostalgia, sweetness without sugar | Pop toplines, 6th chords, city pop |
| m7 | Groove, laid-back tension | Every funk and house chord |
| M7 | Dream, sophistication, ache | Lo-fi, neo-soul, ambient, bossa |
| P8 | Confirmation, strength | Doubling, octave bass, hook emphasis |
| b9 | Panic, dread, spice | Altered dominants, horror stabs |
| #11 | Wonder, magic, "sky" | Lydian film cues, EDM pads |

## Inversion

Invert an interval (move the lower note up an octave) and the two sizes sum to
12: `inverted = 12 - n`.

| Original | Inverted |
|---|---|
| m2 (1) | M7 (11) |
| M2 (2) | m7 (10) |
| m3 (3) | M6 (9) |
| M3 (4) | m6 (8) |
| P4 (5) | P5 (7) |
| TT (6) | TT (6) |

Two consequences: perfect intervals invert to perfect, major inverts to minor,
and **the tritone is its own inversion** — which is why tritone substitution
works and why a dominant 7th chord has an ambiguous, rotatable core.

## Melodic vs harmonic

- **Harmonic interval** — simultaneous. Governed by consonance and register.
- **Melodic interval** — successive. Governed by singability and momentum.

Melodic rules of thumb:

- Steps (1–2 semitones) are free; use them for most of a line.
- Leaps of a 4th, 5th or octave are events — spend them deliberately.
- A large leap **wants to be followed by stepwise motion in the opposite
  direction**. This is not superstition; it is what makes a line feel resolved.
- Leaps of a 7th or a tritone read as "difficult", "modern", or "wrong" unless
  the harmony explains them.
- Repeated notes are not filler — a repeated note with changing harmony
  underneath is one of the strongest hook devices there is.

## Interval maths you will actually use

```
interval        = abs(note_a - note_b)
pitch_class_gap = (note_a - note_b) % 12          # ignores octave
is_consonant    = pitch_class_gap in (0, 3, 4, 5, 7, 8, 9)
inversion       = 12 - (interval % 12)
```

**Interval vector / chord flavour**: to know whether a set of notes will sound
harsh, count how many semitone-1 and semitone-6 relationships it contains
between *any* pair. Zero m2s and zero tritones = consonant. Two or more m2s in a
low register = mud, regardless of what the chord is called.

## Interval-based construction

Whole families of sounds are just "stack interval X repeatedly":

| Stack | Result | Use |
|---|---|---|
| 3 or 4 (thirds) | Standard triads and 7th chords | All tonal music |
| 5 (fourths) | Quartal harmony | Modal jazz, ambient, sci-fi score |
| 7 (fifths) | Power chords, organum | Rock, metal, sub bass, drone |
| 2 (seconds) | Cluster | Tension, horror, texture pads |
| 6 (tritones) | Symmetric, unstable | Diminished/whole-tone colour, dread |
| 1 (semitones) | Chromatic cluster | Sound design, not harmony |

## Related

- Scales as interval patterns: `04-scales-and-modes.md`
- Chords as interval stacks: `05-chords.md`
- Register limits for close intervals: `07-voice-leading.md`
