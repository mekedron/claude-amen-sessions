# Vocals, Topline and Lyrics

The human voice is the element listeners attend to first and forgive least. Even
in instrumental electronic music, vocal fragments carry disproportionate weight.

## Vocal ranges

| Voice | Comfortable range | Full range | MIDI |
|---|---|---|---|
| Bass | E2–D4 | C2–E4 | 40–62 |
| Baritone | A2–F4 | F2–A4 | 45–65 |
| Tenor | C3–A4 | Bb2–C5 | 48–69 |
| Countertenor | G3–E5 | E3–G5 | 55–76 |
| Alto | F3–D5 | E3–F5 | 53–74 |
| Mezzo-soprano | A3–F5 | G3–A5 | 57–77 |
| Soprano | C4–A5 | B3–C6 | 60–81 |
| Typical untrained | ~1.5 octaves | 2 octaves | — |

**Always choose the key from the vocal range**, before anything else. The rule:
put the *chorus* melody in the upper-middle of the singer's comfortable range —
that is where a voice sounds most powerful and emotional — and let the verse sit
lower. If the verse is already high, the chorus has nowhere to go.

**Break points / passaggio**: most voices have a register transition around
E4–G4 (male) and E5–G5 (female). Melodies that repeatedly cross it are hard to
sing. Melodies that *climax* just above it sound thrilling.

## Writing a topline

1. **The rhythm first.** Speak the lyric out loud in time with the beat. The
   natural stresses of the words must land on the strong beats. Every great
   topline is a rhythm you could speak.
2. **Start off the downbeat.** Almost all sung phrases begin with a pickup.
3. **Breathe.** Leave a rest of at least a beat every 2–4 bars. A topline with
   no gaps is unsingable and exhausting to hear.
4. **Contrast verse and chorus:**

| | Verse | Chorus |
|---|---|---|
| Register | Lower | Higher (usually a 3rd to a 5th above) |
| Rhythm | Busier, more words, more syncopation | Longer notes, fewer words |
| Range | Narrow | Wider |
| Melody | Conversational, repetitive | Arching, memorable |
| Harmony | May avoid the tonic | Lands on the tonic |

5. **The chorus should contain the title**, usually in the first or last line.
6. **Repetition is not a weakness.** The most successful choruses repeat one
   phrase two to four times with small variation.

## Melodic and harmonic fit

- Sung notes on strong beats should be chord tones or safe tensions
  (see `08-melody.md`).
- The **9th and 6th** are the sweetest non-chord tones for a vocal.
- The **4th over a major chord** is the one to avoid on a long note.
- Vocals sit best when the chords beneath them are voiced **below** the melody —
  leave the top of the harmony at least a third under the top note, or the
  arrangement will crowd the voice.

## Lyric craft, briefly

| Principle | Explanation |
|---|---|
| **Concrete over abstract** | "Your coat still on my chair" beats "I miss you" |
| **One idea per song** | A song is not an essay |
| **Prosody** | Stressed syllables on strong beats; long vowels on long notes; the melody's shape should match the sentence's emotional shape |
| **Singable vowels** | Open vowels (ah, oh, ay) on high/long notes. "Ee" and "oo" on a high sustained note are hard to sing and harsh to hear |
| **Avoid consonant clusters** on fast passages |
| **Rhyme is a tool, not a requirement** | Perfect rhyme = pop/closure; slant rhyme = modern/conversational; no rhyme = folk/art |
| **Line length** | Match line lengths across parallel sections so the melody can repeat |
| **The title** | Should be the most memorable phrase and appear where the melody peaks |

Common song-lyric structures: verse (situation) → pre-chorus (build/turn) →
chorus (the point) → verse 2 (development) → chorus → bridge (new angle,
contradiction, or zoom out) → final chorus (same words, new weight).

## Recording and editing (the essentials)

- **Comping**: assemble the best take line-by-line, or word-by-word.
- **Tuning**: correct pitch, but leave micro-variation — fully quantised pitch
  sounds robotic unless that is the aesthetic (and in hyperpop and trap it is).
  Retune speed is the parameter that decides between "invisible" and "the
  T-Pain effect".
- **Timing**: align to the grid loosely. Vocals slightly ahead sound urgent;
  slightly behind sounds relaxed. Fully quantised sounds dead.
- **Breaths**: reduce them by 6–12 dB rather than deleting them. Removed breaths
  sound uncanny.
- **De-essing** before compression, not after.
- **Double-tracking**: a second real performance panned opposite the first
  (or at ±30%) thickens far better than any plugin. Triples and quads for
  choruses.
- **Harmonies**: a third above (bright), a third below (warm), a fifth above
  (powerful), and an octave (weight). Stack them and pan.

## Vocal mixing chain

```
gate/clean-up → subtractive EQ → de-esser → compressor 1 (fast, 3–5 dB)
  → compressor 2 (slow, 2–3 dB) → tonal EQ → saturation → sends (delay, reverb)
```

Key moves:

| Move | Value |
|---|---|
| High-pass | 90–120 Hz (male), 100–150 Hz (female) |
| Cut proximity boom | 200–300 Hz, −2 to −4 dB |
| Cut nasal | 800 Hz–1 kHz, −2 to −3 dB if honky |
| Boost presence | 2–4 kHz, +2 to +4 dB |
| De-ess | 5–9 kHz, dynamic, only on triggers |
| Boost air | 10–14 kHz shelf, +2 to +3 dB |
| Compression total | 6–10 dB GR across two stages |
| Reverb | Plate, 1.2–2 s, pre-delay 20–40 ms, high-passed at 300 Hz |
| Delay | 1/8 dotted or 1/4, filtered, ducked by the dry vocal |

**Volume automation, word by word, is the single most important vocal move.**
Compression evens out dynamics; automation puts every syllable exactly where it
should be. Professional vocals are automated before and after compression.

## Vocals as an instrument (electronic music)

| Technique | Description | Genres |
|---|---|---|
| **Vocal chop** | Slice a phrase into 16ths, re-pitch and re-sequence | Future bass, garage, house |
| **Formant shift** | Change perceived vocal-tract size without changing pitch | Everywhere; "chipmunk" avoidance, gender shift |
| **Pitched vocal stab** | One syllable mapped across a keyboard, played as a chord | House, garage, jungle |
| **Vocoder** | Voice modulates a synth's spectrum via a filter bank | Funk, electro, Daft Punk |
| **Talkbox** | The mouth physically filters a synth | Funk, G-funk |
| **Autotune as effect** | Extreme retune speed on a discrete scale | Trap, hyperpop, pop |
| **Reversed vocal** | Play it backwards, or reverse the reverb tail | Transitions, psychedelia |
| **Granular / freeze** | Sustain a single vowel indefinitely | Ambient, IDM |
| **Whisper / ASMR layer** | A quiet doubled whisper track under the lead | Modern pop, hyperpop |
| **Ad-libs** | Short responses panned wide, delayed | Hip-hop, trap, drill |
| **Acapella sample** | A borrowed vocal, filtered and chopped | House, jungle, bootlegs |
| **Formant choir / vowel synth** | Band-pass filters at vowel formants over a saw | D&B, cinematic, ambient |

Vowel formant frequencies (F1/F2), useful for synthesised voices:

| Vowel | F1 | F2 |
|---|---|---|
| "ee" (beet) | 270 Hz | 2290 Hz |
| "ih" (bit) | 390 | 1990 |
| "eh" (bet) | 530 | 1840 |
| "ae" (bat) | 660 | 1720 |
| "ah" (father) | 730 | 1090 |
| "aw" (bought) | 570 | 840 |
| "oo" (boot) | 300 | 870 |
| "uh" (but) | 640 | 1190 |

A third formant around 2500–3000 Hz and a "singer's formant" around 2800–3200 Hz
(which is how an opera voice cuts through an orchestra) complete the picture.

## HAZARDS

- **Key chosen before the singer** — the most common and most damaging error.
- **Chorus melody in the same register as the verse** — no lift.
- **No breathing space** in the topline.
- **Vocal buried by a pad or lead in the same 1–4 kHz band** — carve the
  instrument, do not boost the voice.
- **Over-tuning and over-compressing** until the performance is gone.
- **Reverb without pre-delay** — the words blur.
- **Sibilance left untreated** — becomes painful after limiting.
- **Sampling a recognisable acapella without clearance** if the result is going
  to be released commercially. Legally, sampling a recording requires permission
  from both the recording owner and the composition owner.

## Related

- Melody writing: `08-melody.md`
- Fitting the voice into the mix: `13-frequency-and-eq.md`, `16-mixing-process.md`
- Genre-specific vocal treatment: `../20-genres/`
