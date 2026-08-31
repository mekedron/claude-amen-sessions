# Quick Decision Tables

For when you need an answer, not an explanation.

## "I need to write a track. Where do I start?"

1. **Genre** → look it up in `../20-genres/`.
2. **Tempo and key** → take the genre's defaults. Minor, and a root between
   MIDI 29 and 40 for the bass, unless there is a vocalist.
3. **Length in bars** = `target_seconds * BPM / 240`.
4. **Draw the arrangement matrix** (`../30-patterns/10-arrangement-templates.md`).
5. **Write the highest-energy section first.** Derive everything else by
   subtraction.
6. **Groove, then bass, then harmony, then melody, then fx.**

## Which mode for which mood?

| Mood | Mode |
|---|---|
| Happy, resolved, simple | Ionian (major) |
| Bright, magical, floating | Lydian |
| Rooted, bluesy, folky | Mixolydian |
| Cool, groovy, not-quite-sad | Dorian |
| Sad, serious, dramatic | Aeolian (natural minor) |
| Menacing, exotic, Spanish | Phrygian |
| Theatrical, neoclassical | Harmonic minor |
| Aggressive, Middle-Eastern-flavoured | Phrygian dominant |
| Weightless, dreamlike | Whole tone |
| Suspenseful, horror | Diminished, chromatic |
| Safe, cannot go wrong | Pentatonic |

## Which chord progression?

| Want | Use |
|---|---|
| Universal, pop, uplifting | `I–V–vi–IV` |
| Minor anthem, EDM | `i–bVI–bIII–bVII` |
| Dramatic descent | `i–bVII–bVI–V` (Andalusian) |
| Cool loop, never resolves | `im7–IVmaj7` (Dorian) |
| Sophisticated, jazzy | `ii–V–I` with 9ths |
| Nostalgic | `I–vi–IV–V` |
| Modern J-pop / future bass | `IV–V–iii–vi` |
| Menace, trap | `i–bII` |
| Epic, cinematic | chromatic mediants: `I–bVI`, `i–bVI–bIII` |
| Endless motion | `i–bVII–bIII–bVI` |

## Which key?

| Situation | Choice |
|---|---|
| There is a singer | Their range decides. Nothing else matters. |
| Club music | F, G, A minor — roots at MIDI 29, 31, 33 |
| Guitar-based | E, A, D, G, C |
| Bright and open | Major keys with few accidentals |
| Emotional/dark | Any minor; the key itself does not change the mood in 12-TET |
| Harmonic DJ mixing | Use the Camelot wheel in `02-scale-and-chord-formulas.md` |

## Fixing a mix

| Symptom | First thing to try |
|---|---|
| Muddy | High-pass everything but kick/bass; cut 200–500 Hz |
| Boomy | Cut 60–120 Hz on the non-bass elements; check mono |
| Harsh | Cut 2–5 kHz on the loudest offender; reduce distortion |
| Thin | Stop high-passing so aggressively; reinstate 150–400 Hz |
| No punch | Slower compressor attacks; less gain reduction |
| Vocal buried | Cut 1–4 kHz on the competing elements |
| Bass gone on phones | Saturate the bass to create harmonics above 100 Hz |
| Kick disappears | Sidechain the bass, or split their frequencies |
| Small / narrow | Widen the non-core elements; add depth with reverb sends |
| Washy | High-pass the reverb returns; add pre-delay; use delay instead |
| Cluttered | Delete a layer. It is an arrangement problem |
| Sounds amateur but nothing is wrong | Automate something |

## Compression starting points

| Source | Ratio | Attack | Release | GR |
|---|---|---|---|---|
| Kick | 4:1 | 10–20 ms | 60–150 ms | 3–6 dB |
| Snare | 4:1 | 5–20 ms | 100–200 ms | 3–8 dB |
| Bass | 4:1 | 5–15 ms | 100–200 ms | 4–8 dB |
| Vocal | 3–4:1 | 5–15 ms | 40–100 ms | 3–6 dB |
| Drum bus | 2–4:1 | 10–30 ms | auto | 2–4 dB |
| Mix bus | 1.5–2:1 | 10–30 ms | auto | 1–3 dB |
| Sidechain pump | 4:1–∞ | 0.1–1 ms | 1/16 note | 6–20 dB |

## High-pass frequencies

| Element | Hz |
|---|---|
| Kick | 25–35 |
| Bass | 25–30 |
| Snare | 100–150 |
| Clap | 200–300 |
| Hats | 300–600 |
| Vocal | 90–150 |
| Guitar | 80–120 |
| Pads | 150–300 |
| Leads | 200–400 |
| Reverb/delay returns | 200–500 |
| FX and risers | 200–500 |

## Loudness targets (integrated LUFS)

| Context | Target |
|---|---|
| Streaming (Spotify/YouTube/Tidal) | −14 |
| Apple Music | −16 |
| Club / DJ / no normalisation | −8 to −6 |
| Pop | −10 to −8 |
| Rock | −10 to −8 |
| Lo-fi | −14 to −11 |
| Ambient | −18 to −14 |
| Classical | −23 to −16 |
| Broadcast (EBU R128) | −23 |

True-peak ceiling: **−1.0 dBTP** for anything going to a lossy codec.

## Element count per section

| Section | Simultaneous elements |
|---|---|
| Intro | 2–4 |
| Verse | 4–6 |
| Build | 5–8 |
| Drop / chorus | 6–10 |
| Breakdown | 2–5 |
| Outro | 2–4 |

More than ~10 and the mix stops being legible regardless of balance.

## Humanisation amounts

| Parameter | Amount |
|---|---|
| Timing jitter (non-foundational) | ±3–8 ms |
| Snare laid back | +10 to +25 ms |
| Snare pushed | −5 to −15 ms |
| Velocity variation | ±8–20% |
| Ghost note velocity | 20–40% of accent |
| Note-length variation | ±10–25% |
| Chord roll | 5–25 ms between voices |
| Pitch drift (acoustic-style) | ±3–10 cents |

Never jitter: the kick, the sub bass, or layers that must stay phase-aligned.

## Frequency ownership

| Band | Owner |
|---|---|
| 20–60 Hz | Sub bass (one element only) |
| 60–120 Hz | Kick and bass, split between them |
| 120–300 Hz | Body: snare, low vocal, guitar warmth |
| 300–800 Hz | The crowded band; cut here first |
| 800 Hz–2.5 kHz | Intelligibility: vocal, snare crack, lead |
| 2.5–6 kHz | Definition and attack; also where harshness lives |
| 6–12 kHz | Hats, cymbals, air, sibilance |
| 12 kHz+ | Sparkle, space |

## Checklist before calling a track finished

- [ ] Something changes every 8 bars, and something big every 16 or 32
- [ ] The lowest-energy section immediately precedes the highest
- [ ] Every section boundary lands on a multiple of 8 bars
- [ ] The peak is 60–75% of the way through
- [ ] Something is removed as well as added at each seam
- [ ] Checked in mono
- [ ] Checked on a phone speaker
- [ ] Checked at low volume
- [ ] Sub is mono, monophonic, un-reverbed
- [ ] Nothing clips; true peak ≤ −1 dBTP
- [ ] Level-matched A/B against a reference
- [ ] Intro and outro are appropriate for the destination (DJ, streaming, album)
