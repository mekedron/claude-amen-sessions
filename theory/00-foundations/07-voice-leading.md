# Voice Leading

Voice leading is the difference between a chord progression and *music*. Same
chords, different note-by-note motion — one sounds like a beginner pressing
buttons, the other sounds professional. It costs nothing to fix.

## The core principle

**Treat every note in a chord as a singer with a memory.** Each voice should move
as little as possible from one chord to the next, and should move for a reason.

Concretely, going from chord A to chord B:

1. Keep any **common tones** in the same voice at the same pitch.
2. Move the remaining voices to the **nearest** available chord tone.
3. Prefer **contrary motion** between the bass and the top voice.
4. Let the **bass** move freely and boldly — it is the exception; it is allowed
   to leap by 4ths and 5ths because that is what makes harmony sound rooted.

## Worked example

`Cmaj7 → Am7 → Dm7 → G7` in root position, close voicing:

```
Cmaj7  60 64 67 71     C E G B
Am7    57 60 64 67     A C E G
Dm7    50 53 57 60     D F A C
G7     55 59 62 65     G B D F
```

Total motion: enormous, and the top line jumps around aimlessly.

Voice-led (bass separate, three upper voices moving minimally):

```
bass:  36 (C)   33 (A)   38 (D)   31 (G)
upper: 64 67 71 | 64 67 69 | 65 69 72 | 65 67 71
       E  G  B  | E  G  A  | F  A  C  | F  G  B
```

Every upper voice moves by 0, 1 or 2 semitones. The progression now *flows*.

## Guide tones — the cheapest professional trick

In any 7th chord, the **3rd and the 7th** define its quality. In a ii–V–I those
two notes alone resolve by half-step:

```
Dm7   F  and  C     (3rd, 7th)
G7    B  and  F     (7th of Dm7 becomes 3rd of G7 — common tone F; C→B by a half-step)
Cmaj7 E  and  B     (B is a common tone; F→E by a half-step)
```

Play only guide tones and the harmony is fully legible. Add the root in the
bass and the 9th/13th on top for colour. This is how jazz pianists, house
producers and liquid drum'n'bass writers voice chords.

## Motion types

| Type | Description | Use |
|---|---|---|
| **Contrary** | Voices move in opposite directions | Strongest; use between bass and melody |
| **Oblique** | One voice holds, another moves | Smooth; pedal points, sustained pads |
| **Similar** | Same direction, different intervals | Neutral, fine in moderation |
| **Parallel** | Same direction, same interval | Thickens one line into a texture |

### The parallel-fifths rule, and when to ignore it

Classical part-writing forbids parallel perfect 5ths and octaves between voices,
because they collapse two independent voices into one thickened line.

**When it matters:** any texture pretending to be independent voices — string
quartets, choirs, contrapuntal pads, anything "classical" or "orchestral".

**When it is the point:** power chords (parallel 5ths *are* rock), organum,
parallel-4th quartal comping (McCoy Tyner, film scoring), parallel triads
sliding chromatically (Debussy, video game music), and every synth "unison"
patch ever made. Modern music runs on parallel motion.

**HAZARD:** the one place it always sounds bad is when *some* voices are
independent and one pair is accidentally parallel. Either commit to parallelism
as a texture or avoid it.

## Low interval limits

The lowest pitch at which an interval stays clear rather than turning into mud.
Approximate, and roughly a fourth lower for pure sine-ish timbres than for
saw-ish ones.

| Interval | Lowest usable bottom note | Approx. Hz |
|---|---|---|
| Minor 2nd | E3 (52) | 165 |
| Major 2nd | Eb3 (51) | 156 |
| Minor 3rd | C3 (48) | 131 |
| Major 3rd | Bb2 (46) | 117 |
| Perfect 4th | F2 (41) | 87 |
| Perfect 5th | Bb1 (34) | 58 |
| Minor 6th | G#2 (44) | 104 |
| Major 6th | F#2 (42) | 92 |
| Octave | E1 (28) | 41 |

**Practical rules that follow:**

- Below ~MIDI 40 (E2, 82 Hz): **one note at a time**. Octaves at most.
- Between MIDI 40 and 48: fifths and fourths are safe; thirds are risky.
- Above MIDI 48 (C3): anything works.
- Above MIDI 72 (C5): even clusters read as shimmer rather than dissonance.

This is a *mixing* rule as much as a theory rule — see `13-frequency-and-eq.md`.

## Spacing

Mirror the harmonic series: wide at the bottom, tight at the top.

```
GOOD:  36 ......... 55 62 65 69      (octave+ gap low, thirds on top)
BAD:   36 40 43 47 ................  (a cluster in the sub — mud)
BAD:   36 ....................... 84 (a hole in the middle — thin, weak)
```

Rule of thumb: **no gap larger than an octave between adjacent upper voices**,
and **at least a fifth between the bass and the next voice up**.

## The bass is not a voice

The bass line has its own grammar and does not obey minimal-motion rules:

- It plays roots and fifths, and leaps freely.
- Its job is to define the harmony's foundation and lock with the kick.
- **Inversions are a bass-line tool**: `C – G/B – Am – Am/G – F` gives a
  descending bass `C B A G F` from ordinary chords. Any progression can be made
  to feel like it is going somewhere by controlling the bass contour.
- Common bass shapes: descending stepwise (melancholy, "Air on a G string",
  every ballad), ascending stepwise (building), pedal (static, tense), alternating
  root–fifth (driving), chromatic descent (noir, jazz, "Hotel California").

## The top voice is a melody whether you meant it or not

The highest note of each chord is what people hum. Design it:

- **Static top note** across changing chords = the chords "colour" a held note.
  Extremely effective; the note becomes a different tension on each chord
  (e.g. hold G over `Cmaj7 (5th) – Am7 (b7) – Fmaj7 (9th) – G7 (root)`).
- **Descending top line** = resignation, resolution.
- **Ascending top line** = building, opening.
- **Arch** = the classic phrase shape; rise then fall.

## Common tone tables

The number of shared pitch classes between two triads determines how smooth the
change is.

| Relationship | Common tones | Example (C major) | Smoothness |
|---|---|---|---|
| Same root, major↔minor | 2 | C ↔ Cm | Very smooth, big emotional change |
| Up/down a 3rd (diatonic) | 2 | C ↔ Am, C ↔ Em | Very smooth |
| Up/down a 5th | 1 | C ↔ G, C ↔ F | Strong, functional |
| Up/down a step | 0 | C ↔ Dm, C ↔ Bb | Bold, fresh, "lifting" |
| Tritone apart | 0–1 | C ↔ F# | Alien |
| Chromatic mediant | 1 | C ↔ Ab, C ↔ E | Magical (one held note carries it) |

**Technique:** when a progression has zero common tones (step motion), use
contrary motion in the outer voices to keep it smooth. When it has two common
tones, hold them and move only one voice — the change becomes a colour shift.

## Voice leading for pads and synth chords

Electronic music has extra concerns:

1. **Voice count consistency.** If chord 1 has 4 notes and chord 2 has 6, the
   loudness jumps. Keep the count constant or compensate with gain.
2. **Detuned/unison patches multiply everything.** A 7-voice supersaw playing a
   5-note chord is 35 oscillators. Use 3 notes maximum for supersaws; the
   detune supplies the thickness.
3. **Long release times smear voice leading.** With a 2-second release, chord 1
   is still sounding under chord 2 — so the *union* of consecutive chords must
   also be consonant. Either shorten the release at chord changes or choose
   chords with common tones.
4. **Filter cutoff is a voice.** A moving cutoff over a static chord does the
   job of a voice-led progression in techno and psytrance.
5. **The sub bass is monophonic**, always. Two sub notes at once produce
   intermodulation mud and destroy headroom.

## Counterpoint in 90 seconds

If you want two independent melodic lines rather than a melody plus chords:

1. Move mostly by step; leaps are events.
2. Prefer contrary motion; avoid parallel 5ths/octaves.
3. On strong beats, prefer consonances (3rds, 6ths, 5ths, octaves).
4. Dissonances happen on weak beats as **passing tones** (stepwise between two
   chord tones), **neighbour tones** (step away and back), **suspensions** (hold
   a note from the previous chord, then resolve down by step), **anticipations**
   (arrive early), and **escape tones**.
5. **Suspensions are the workhorse**: 4–3, 7–6 and 9–8 suspensions are how
   baroque music generates continuous tension. In modern terms: hold the pad
   note through the chord change, then let it fall a step.
6. Give the two lines different rhythms — if they move together, they are one
   line in harmony, not counterpoint.
7. End on a unison, octave or fifth.

Canon/round: the same line against a delayed copy of itself. It works when the
line is built so that beats N and N+delay are consonant — easiest with
pentatonic material, which is why pentatonic canons always work.

## Related

- The chords being led: `05-chords.md`
- What the bass does on its own: `09-bass.md`
- Register limits and mud: `13-frequency-and-eq.md`
