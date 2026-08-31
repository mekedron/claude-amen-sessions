# World and Modal Traditions

Musical systems outside the Western common practice. Each is a complete grammar,
not a scale. This file gives enough to use them respectfully and to know what
you are not capturing.

**A note on approach:** a note set is the smallest part of any of these
traditions. Ornamentation, phrase vocabulary, tuning, instrumentation and
context carry most of the meaning. Either implement the behaviour or describe
what you did honestly.

## Arabic and Turkish maqam

A **maqam** is a melodic mode: a scale, plus characteristic phrases, plus rules
for ascent and descent, plus a hierarchy of important notes.

- Built from **ajnas** (tetrachords/trichords) joined at a shared note.
- Uses **quarter tones** — intervals of roughly 150 and 350 cents that do not
  exist in 12-TET. Turkish theory divides the tone into 9 commas.
- Modulation happens by moving to a maqam sharing a jins.

| Maqam | Approximate degrees (semitones, `.5` = quarter tone) | Character |
|---|---|---|
| Rast | 0, 2, 3.5, 5, 7, 9, 10.5 | Dignified, "major-like" |
| Bayati | 0, 1.5, 3, 5, 7, 8, 10 | The most common; plaintive |
| Hijaz | 0, 1, 4, 5, 7, 8, 10 | The famous "Arabic" sound; playable in 12-TET |
| Nahawand | 0, 2, 3, 5, 7, 8, 10 | ≈ natural minor |
| Kurd | 0, 1, 3, 5, 7, 8, 10 | ≈ Phrygian |
| Saba | 0, 1.5, 3, 4, 7, 8, 10 | Distinctive, sorrowful; a diminished-ish 4th |
| Ajam | 0, 2, 4, 5, 7, 9, 11 | ≈ major |
| Sikah | −0.5, 1.5, 3.5, 5.5, 7.5, 9, 11 | Built on a quarter-tone degree |

**Rhythm (iqa'at)**: cyclic patterns of dum (low) and tak (high) strokes.

| Iqa | Beats | Pattern (D = dum, T = tak, `-` = rest) |
|---|---|---|
| Maqsum | 4/4 | D T - T D - T - |
| Baladi | 4/4 | D D - T D - T - |
| Saidi | 4/4 | D - T D D - T - |
| Masmoudi | 8/4 | D - - D - - T - D - T - T - - - |
| Ayyub | 2/4 | D - T D - - T - |
| Chiftetelli | 8/4 | D - - T - T D - D - T - T - - - |
| Samai thaqil | 10/8 | D - - T - D D - T - |

## Indian classical (Hindustani and Carnatic)

- **Raga**: a melodic framework — an ascending form (aroha), descending form
  (avaroha, often different), a dominant note (vadi), a secondary note (samvadi),
  characteristic phrases (pakad), and an associated time of day or season.
- **Tala**: a cyclic rhythmic framework counted in beats with internal groupings.
- **Shruti**: 22 microtonal divisions of the octave; the tuning is just, not
  equal-tempered.
- A performance moves from free-time exposition (alap) through increasing
  rhythmic density to a fast climax.

| Raga | Approximate semitones | Time / mood |
|---|---|---|
| Bhairav | 0 1 4 5 7 8 11 | Dawn; serious |
| Yaman | 0 2 4 6 7 9 11 (= Lydian) | Evening; romantic |
| Bhairavi | 0 1 3 5 7 8 10 (= Phrygian) | Closing piece; devotional |
| Kafi | 0 2 3 5 7 9 10 (= Dorian) | Spring |
| Bhimpalasi | 0 3 5 7 9 10 asc / 0 2 3 5 7 9 10 desc | Afternoon |
| Malkauns | 0 3 5 8 10 (pentatonic) | Late night; meditative |
| Darbari Kanada | 0 2 3 5 7 8 10 with specific oscillation | Night; grave |
| Todi | 0 1 3 6 7 8 11 | Morning |

| Tala | Beats | Grouping |
|---|---|---|
| Teental | 16 | 4+4+4+4 |
| Jhaptal | 10 | 2+3+2+3 |
| Rupak | 7 | 3+2+2 |
| Ektal | 12 | 2+2+2+2+2+2 |
| Adi tala (Carnatic) | 8 | 4+2+2 |

Essential features that a note list misses: **meend** (glides between notes),
**gamaka** (ornamental oscillation, central to Carnatic music), the constant
**drone** (tanpura on Sa and Pa), and the fact that ascent and descent use
different notes.

## Gamelan (Java and Bali)

- Two tuning systems, **neither of which is 12-TET**:
  - **Slendro**: 5 nearly equal divisions of the octave (~240 cents each).
  - **Pelog**: 7 unequal steps; usually 5 are used in a given piece.
- Each gamelan ensemble is tuned uniquely — instruments from different sets do
  not play together.
- **Colotomic structure**: the form is marked by gongs at nested intervals — the
  large gong every 16 or 32 beats, smaller gongs subdividing.
- **Stratified density**: low instruments play slowly, high instruments play the
  same melody at 2×, 4×, 8× the density.
- **Interlocking (kotekan)**: two players alternate notes to produce a line
  neither could play alone. Balinese music is built on this.

To evoke it in 12-TET: use `0 2 7 9` or `0 1 3 7 8` note sets, inharmonic
metallic timbres, slight detuning between paired instruments (real gamelans are
tuned in pairs a few Hz apart to create a shimmering beating), and a nested
gong structure.

## Flamenco

- **Phrygian dominant** (`0 1 4 5 7 8 10`) and the **Andalusian cadence**
  (`i–bVII–bVI–V`, descending) are the core.
- The final chord is the **major V**, treated as home — flamenco's tonic is the
  Phrygian's V, not its i.
- **Compás**: cyclic rhythms with accent patterns, often 12 beats.

| Palo | Compás | Accents |
|---|---|---|
| Soleá | 12 | 3, 6, 8, 10, 12 |
| Bulerías | 12 | 12, 3, 6, 8, 10 (fast) |
| Alegrías | 12 | as soleá, major key |
| Seguiriya | 12 | 1, 3, 5, 8, 11 (asymmetric) |
| Tangos | 4 | strong on 2 and 4 |
| Fandango | 3 or 6 | |

## Balkan and Eastern European

- **Aksak (limping) meters**: 7/8 (2+2+3), 9/8 (2+2+2+3), 11/8 (2+2+3+2+2),
  5/8 (2+3). The unequal beat is the identity.
- Scales with augmented seconds (harmonic minor, Hungarian minor, double
  harmonic).
- Close-harmony singing with major/minor seconds held as consonances (Bulgarian
  women's choir).
- Ornamented, fast melodic lines; drone accompaniment.

## Klezmer

- Scales: **Freygish** (Phrygian dominant), **Misheberakh** (Ukrainian Dorian,
  `0 2 3 6 7 9 10`), and natural/harmonic minor.
- Ornamentation: krechts (a sobbing catch), bends, glissandi, trills.
- Rhythms: freylekhs (fast 2/4), bulgar, hora (3/8 limping), doina (free-time
  rubato).

## East Asian

| Tradition | Scale material | Notes |
|---|---|---|
| **Chinese** | Pentatonic (gong `0 2 4 7 9`, and its rotations) | Guzheng, erhu, pipa; heterophonic texture |
| **Japanese** | Hirajōshi `0 2 3 7 8`, In-sen `0 1 5 7 10`, Yo `0 2 5 7 9` | Koto, shakuhachi, shamisen; ma (space) is structural |
| **Korean** | Pentatonic with heavy vibrato (nonghyeon) | Gayageum; strong rhythmic cycles (jangdan) |
| **Mongolian** | Pentatonic | Overtone (throat) singing, morin khuur |

## Celtic and Northern European folk

- Modal: Ionian, Dorian, Mixolydian, Aeolian. The b7 is everywhere.
- Tune types: reel (4/4, fast), jig (6/8), slip jig (9/8), hornpipe (4/4, swung),
  polka (2/4), waltz (3/4), air (free).
- Ornaments: cuts, rolls, cranns, triplets — rhythmic, not melodic, decoration.
- **Drone accompaniment** (pipes) rather than chordal harmony; modern
  arrangements add chords.
- Structure: AABB, 8 bars each, repeated, with sets of tunes played back to back.

## Practical guidance for using these materials

1. **Use the rhythm, not just the scale.** A Phrygian dominant scale over a
   4/4 club beat is a flavour, not a tradition.
2. **Use a drone** where the tradition uses one — it changes how every note is
   heard.
3. **Use ornamentation.** These traditions live in the space between notes:
   glides, bends, oscillations, grace notes.
4. **Respect tuning.** If you cannot do quarter tones or non-equal scales, say
   so, and know that the result is an approximation.
5. **Instrumentation carries identity** as much as pitch. A shakuhachi phrase on
   a saw wave is not the same gesture.
6. **Name what you did honestly.** "Inspired by maqam Hijaz" is accurate;
   "a Hijaz piece" implies rules you did not follow.

## Related

- Scale tables: `../00-foundations/04-scales-and-modes.md`
- Odd meters: `../00-foundations/02-rhythm-and-time.md`
