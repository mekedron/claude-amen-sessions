# Melody, Motif and Hooks

A melody is a rhythm that happens to have pitches. If the rhythm is not
memorable, no sequence of pitches will save it — and if the rhythm *is*
memorable, remarkably poor pitch choices will still work.

## The four parameters of a melody

| Parameter | Question | Why it matters |
|---|---|---|
| **Rhythm** | When do notes start and how long are they? | Recognition happens here first |
| **Contour** | What is the shape of the up/down motion? | What listeners actually remember |
| **Interval content** | Steps or leaps? Which ones? | Emotional colour, singability |
| **Harmonic placement** | Which note lands on which chord? | Whether it sounds intentional |

Design them in that order.

## Contour: the shape

| Shape | Description | Effect |
|---|---|---|
| **Arch** | Up then down | The default; balanced, complete, singable |
| **Inverted arch** | Down then up | Reflective, then hopeful |
| **Ascending** | Rising overall | Building, opening, unresolved |
| **Descending** | Falling overall | Resolution, sighing, sadness, finality |
| **Static / axial** | Circles one note | Hypnotic, insistent, rap-like, minimal |
| **Terraced** | Steps up in plateaus | Escalating; great for build-ups |
| **Zigzag** | Alternating direction | Playful, mechanical, chiptune |

A phrase almost always has **one high point (the climax)**, placed roughly 2/3
of the way through, and it is usually approached by step and left by a leap
downward, or vice versa. Two climaxes in one phrase = no climax.

## Range and tessitura

- **Range**: total span. A singable melody spans ~an octave; up to a 12th is
  common; beyond two octaves is instrumental.
- **Tessitura**: where it spends most of its time. Keep this in the comfortable
  middle of whatever is playing it, and reserve the extremes for the climax.
- For synth leads: MIDI 72–88 cuts through everything. MIDI 60–72 sits with
  vocals and pads and needs EQ carving. Below 60, a "lead" becomes a mid-bass.

## Rhythm of the melody

The most important and most neglected dimension.

- **Contrast with the drums.** If the drums are busy 16ths, the melody should be
  long notes. If the drums are sparse, the melody can be busy. Two busy layers
  cancel.
- **Start off the downbeat.** A melody that starts on step 0 of bar 1 sounds
  square. Start on the "and" of 4 of the previous bar (an anticipation), or on
  step 2, or on beat 2. This one change makes generated melodies sound written.
- **Use one distinctive rhythmic cell** and repeat it. The whole hook of most
  famous melodies is a rhythm you could clap.
- **Leave holes.** Rests are where the ear consolidates. A melody with no rests
  is a stream, not a phrase.
- **Long final note.** Phrases end with a note held across the bar line, or with
  silence. Both signal "that was a phrase".

## Motif and development

A **motif** is the smallest recognisable unit — often 2 to 5 notes. Everything
else is what you do to it.

| Operation | Description |
|---|---|
| **Repetition** | Play it again. Underrated; repetition creates identity. |
| **Sequence** | Repeat at a different pitch level (usually up/down a step or third). Diatonic sequences keep the key; real sequences transpose exactly and leave it. |
| **Inversion** | Flip the intervals (up 3 becomes down 3). |
| **Retrograde** | Play it backwards. |
| **Augmentation** | Double all durations. |
| **Diminution** | Halve all durations. |
| **Fragmentation** | Use only part of it. |
| **Extension** | Add notes to the end. |
| **Ornamentation** | Add passing tones, grace notes, turns. |
| **Rhythmic displacement** | Same notes, shifted to different beats. |
| **Intervallic expansion** | Keep contour, widen the leaps. |
| **Truncation** | Chop the last note; creates urgency. |

A whole 8-bar melody can be: motif (2 bars) → sequence of the motif a step down
(2 bars) → fragment repeated and building (2 bars) → cadence figure (2 bars).
That is the classic **sentence** structure and it is inexhaustible.

The other classic structure is the **period**: 4-bar antecedent ending on a half
cadence (a question), 4-bar consequent that begins the same and ends on an
authentic cadence (an answer).

## Which notes over which chord

A melody note on a strong beat should be a **chord tone** or a **legal tension**.
Non-chord tones belong on weak beats and must resolve by step.

### Available tensions by chord type

| Chord | Safe melody notes (offsets from chord root) | Avoid on strong beats |
|---|---|---|
| `maj7` | 0, 2(9), 4, 7, 9(13), 11 | 5 (the 11 — clashes with the 3rd) |
| `maj7#11` | 0, 2, 4, 6(#11), 7, 9, 11 | 5 |
| `m7` | 0, 2(9), 3, 5(11), 7, 10 | 9 (13) if it implies Dorian when you meant Aeolian |
| `m7b5` | 0, 2, 3, 5, 6, 8(b13), 10 | 9 |
| `7` (dominant) | 0, 2(9), 4, 7, 9(13), 10 | 5 (11) |
| `7alt` | 1(b9), 3(#9), 4, 6(#11), 8(b13), 10 | 2, 7, 9 |
| `dim7` | 0, 2, 3, 5, 6, 8, 9, 11 | — (any whole step above a chord tone works) |
| `sus4` | 0, 2, 5, 7, 9, 10 | 4 (the 3rd — it kills the sus) |

**The one universal rule:** the **b9 relationship is the problem**. Any melody
note a semitone above a chord tone (other than the 3rd above the root of a maj7,
i.e. the maj7 itself) will sound like a mistake on a strong beat.

### Non-chord tones and how to use them

| Type | Motion | Feel |
|---|---|---|
| **Passing tone** | step between two chord tones | Invisible glue |
| **Neighbour tone** | step away and back | Decoration, singable |
| **Suspension** | held from previous chord, resolves down by step | Aching, the most expressive |
| **Anticipation** | chord tone of the *next* chord, arriving early | Groove, drive, funk |
| **Appoggiatura** | leap in, resolve by step | Dramatic, "sob" |
| **Escape tone** | step away, leap back | Light, playful |
| **Pedal tone** | note held while harmony changes underneath | Tension, hypnosis |
| **Blue note** | b3/b5/b7 over major harmony | Grit, soul, humanity |

## Tension and release inside a line

The scale degrees, ranked by how badly they want to move:

| Degree | Stability | Wants to go |
|---|---|---|
| 1 (tonic) | Home | Nowhere |
| 5 | Very stable | Nowhere, or to 1 |
| 3 | Stable, defines mode | To 1 or 2 |
| 6 | Mild tension | Down to 5 |
| 2 | Mild tension | Down to 1 or up to 3 |
| 4 | Strong tension | Down to 3 |
| 7 (leading tone) | Maximum tension | **Up to 1** |
| b7 | Modal, relaxed | Down to 6 or 5 |
| b2, #4 | Extreme colour | Resolve by half-step |

**A melody's emotional arc is a walk through this table.** Ending a phrase on 1
closes it; on 5 leaves it open; on 7 makes it urgent; on 2 or 4 leaves it
hanging (good for a loop that must repeat).

## Hooks

A hook is the part a listener can reproduce after one listen. Properties:

1. **Short** — 1 to 4 bars.
2. **Rhythmically distinctive** — you could clap it and it would still be
   recognisable.
3. **Small range** — often a fifth or less.
4. **Repetitive** — the hook usually repeats within itself.
5. **One surprise** — one interval or one note that is not what you expect.
6. **Register-isolated** — nothing else occupies its frequency band.

Hook archetypes:

| Archetype | Description | Example genre |
|---|---|---|
| **Riff** | Rhythmic pitched pattern, repeated exactly | Rock, funk, metal, big beat |
| **Topline** | Sung phrase over the chords | Pop, house, trance |
| **Lead melody** | Synth line in the drop | EDM, trance, future bass |
| **Arp hook** | Arpeggiated pattern with a shape | Trance, synthwave, chiptune |
| **Vocal chop** | Sampled voice used as an instrument | Future bass, garage, house |
| **Bass hook** | The riff *is* the bass | Drum'n'bass, dubstep, funk, drill |
| **Timbral hook** | A *sound*, not a pitch pattern | Dubstep growls, Amen break, cowbell |
| **Rhythmic hook** | A drum pattern that is the identity | Dembow, Amen, boom-bap |

In electronic music, **the timbral and rhythmic hooks usually outrank the
melodic one**. A memorable sound repeated on the beat beats a forgettable
melody every time.

## Call and response

Two phrases where the second answers the first. It is the deepest structure in
melody, older than harmony.

Implementations:
- Melody phrase → drum fill.
- Lead phrase → the same phrase an octave up or with a different timbre.
- Vocal phrase → instrumental stab.
- High register statement → low register answer.
- Question ending on 5 or 2 → answer ending on 1.

**A melody that plays continuously for 16 bars is exhausting.** Alternate: 2
bars of melody, 2 bars of space (filled by drums, bass, an fx sweep, or a
counter-line).

## Arpeggios and pattern-generated melody

For electronic music, much "melody" is generated from a chord plus a pattern.

| Pattern | Note order (chord `[0,3,7,10]`) | Feel |
|---|---|---|
| Up | 0 3 7 10 | Rising, classic |
| Down | 10 7 3 0 | Falling, resigned |
| Up-down (inclusive) | 0 3 7 10 7 3 | Circular, trance |
| Up-down (exclusive) | 0 3 7 10 10 7 3 0 | Symmetric, hypnotic |
| Random / order | shuffled | Generative, IDM |
| Thumb / alternating | 0 7 3 7 10 7 | Bass-note anchored, baroque, Alberti |
| Octave-spread | 0 7 12 15 19 | Wide, glittering |
| Trance gate | one note, gated rhythm | Not melody but reads as one |

**Make an arp into a hook**: add one note outside the chord, use a non-power-of-2
pattern length (5 or 7 notes over a 16-step bar), or accent one step
differently. A plain 16th-note up-arp is wallpaper.

## HAZARDS in generated melody

- **Random walk within a scale** — in key, no shape, forgettable. Always impose a
  contour and a motif.
- **Even 8ths for 16 bars** — no rhythmic identity.
- **Every note a chord tone** — sterile. You need passing tones and suspensions.
- **Melody in the same octave as the pad and vocal** — masked.
- **No repetition** — an ever-changing melody is not a melody; it is a solo, and
  a bad one. Repeat, then vary.
- **Starting every phrase on the downbeat with the tonic** — the tell of
  algorithmic writing.
- **Ignoring the drums** — melody rhythm and drum rhythm must interlock, not
  duplicate.

## Related

- Which notes are available: `04-scales-and-modes.md`
- Chord tones and tensions: `05-chords.md`
- Hook placement in a track: `11-form-and-arrangement.md`
- Ready-made shapes: `../30-patterns/05-melodic-hooks-and-riffs.md`
