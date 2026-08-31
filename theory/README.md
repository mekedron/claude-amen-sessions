# The Theory Library

A complete, self-contained music-theory and production reference written for an
AI agent that composes — not for a student with an instrument in their hands.

It is deliberately **tool-agnostic**. Nothing here assumes a particular DAW,
synth, library or API. Every rule is stated as something you can turn into
numbers — MIDI note numbers, semitone offsets, positions on a 16-step bar,
hertz, decibels, milliseconds — so it can be translated into whatever engine is
in front of you.

## How to read it

Four kinds of file, answering four different questions.

| Folder | Question it answers |
|---|---|
| `00-foundations/` | **Why** does this work? Pitch, rhythm, scales, chords, harmony, voice leading, melody, form, timbre, mixing, perception. |
| `10-instruments/` | **Which machine made that sound?** The landmark synths, drum machines, samplers, effects and plugins — how they worked and how to rebuild their sounds. |
| `20-genres/` | **What** does this style actually do? One file per genre: tempo, grid, harmony habits, sound palette, arrangement map, clichés to use and clichés to avoid. |
| `30-patterns/` | **Give me one now.** Cookbooks: progressions, drum grids, basslines, drops, transitions, sound-design recipes. |
| `40-reference/` | **What is the number?** Lookup tables: MIDI/frequency, scale and chord formulas, delay times per BPM, glossary. |

## The short version

If you read nothing else, read these four:

1. `00-foundations/02-rhythm-and-time.md` — the grid is the instrument.
2. `00-foundations/06-harmony-function.md` — why one chord follows another.
3. `00-foundations/11-form-and-arrangement.md` — a track is an energy curve.
4. `30-patterns/02-drop-and-buildup.md` — the most reusable device in modern music.

## Conventions used everywhere in this library

- **Pitch** is a MIDI note number. `60` = middle C = C4 = 261.63 Hz.
- **Chords** are semitone offsets from the root: a minor 7th is `[0, 3, 7, 10]`.
  Add the root's MIDI number to get real notes.
- **Scales** are semitone offsets from the tonic: natural minor is
  `[0, 2, 3, 5, 7, 8, 10]`.
- **Rhythm** is written on a 16-step bar (one step = one 16th note) unless
  stated otherwise. `x` = hit, `-` = rest, `.` = ghost/quiet hit, `o` = open,
  `|` = beat boundary. Steps are numbered 0–15.

      kick:  x - - - | - - - - | x - - - | - - - -     kicks on beats 1 and 3
      step:  0 1 2 3 | 4 5 6 7 | 8 9 . . | . . . 15

- **Roman numerals** are uppercase for major, lowercase for minor:
  `I ii iii IV V vi vii°`. A `b` prefix lowers the degree: `bVI` in C major = Ab.
- **Levels** are given in dB when the point is relative loudness, and as linear
  gains in `0.0–1.0` when the point is a mixer setting.
- Anything marked **HAZARD** is a mistake that sounds bad and is easy to make by
  accident when music is generated programmatically rather than played.

## The one rule that outranks the rest

Theory is a description of what listeners have already been trained to expect.
It is a prediction engine, not a law. Every entry here is worth breaking the
moment breaking it is *the point* — but break it deliberately, in one dimension
at a time, while the rest of the track stays legible. A track that violates
everything at once is not experimental, it is noise.

## Full index

### `00-foundations/` — Foundations — the why

- [`01-pitch-and-tuning.md`](00-foundations/01-pitch-and-tuning.md) — Pitch, MIDI and Tuning
- [`02-rhythm-and-time.md`](00-foundations/02-rhythm-and-time.md) — Rhythm, Meter and Time
- [`03-intervals.md`](00-foundations/03-intervals.md) — Intervals
- [`04-scales-and-modes.md`](00-foundations/04-scales-and-modes.md) — Scales and Modes
- [`05-chords.md`](00-foundations/05-chords.md) — Chords
- [`06-harmony-function.md`](00-foundations/06-harmony-function.md) — Harmony and Function
- [`07-voice-leading.md`](00-foundations/07-voice-leading.md) — Voice Leading
- [`08-melody.md`](00-foundations/08-melody.md) — Melody, Motif and Hooks
- [`09-bass.md`](00-foundations/09-bass.md) — Bass
- [`10-drums-and-groove.md`](00-foundations/10-drums-and-groove.md) — Drums and Groove
- [`11-form-and-arrangement.md`](00-foundations/11-form-and-arrangement.md) — Form and Arrangement
- [`12-timbre-and-synthesis.md`](00-foundations/12-timbre-and-synthesis.md) — Timbre and Synthesis
- [`13-frequency-and-eq.md`](00-foundations/13-frequency-and-eq.md) — Frequency, EQ and the Spectrum
- [`14-dynamics-and-compression.md`](00-foundations/14-dynamics-and-compression.md) — Dynamics and Compression
- [`15-stereo-and-space.md`](00-foundations/15-stereo-and-space.md) — Stereo, Depth and Space
- [`16-mixing-process.md`](00-foundations/16-mixing-process.md) — The Mixing Process
- [`17-mastering.md`](00-foundations/17-mastering.md) — Mastering
- [`18-psychoacoustics-and-tension.md`](00-foundations/18-psychoacoustics-and-tension.md) — Psychoacoustics, Expectation and Tension
- [`19-vocals-and-lyrics.md`](00-foundations/19-vocals-and-lyrics.md) — Vocals, Topline and Lyrics

### `10-instruments/` — Instruments — the machines that made the sounds

- [`01-overview.md`](10-instruments/01-overview.md) — Landmark Instruments — Overview
- [`02-analog-monosynths.md`](10-instruments/02-analog-monosynths.md) — Analog Monosynths
- [`03-analog-polysynths.md`](10-instruments/03-analog-polysynths.md) — Analog Polysynths
- [`04-electromechanical-keyboards.md`](10-instruments/04-electromechanical-keyboards.md) — Electromechanical Keyboards
- [`05-fm-and-phase-distortion.md`](10-instruments/05-fm-and-phase-distortion.md) — FM and Phase Distortion
- [`06-wavetable-vector-and-la.md`](10-instruments/06-wavetable-vector-and-la.md) — Wavetable, Vector and LA Synthesis
- [`07-samplers-and-workstations.md`](10-instruments/07-samplers-and-workstations.md) — Samplers and Workstations
- [`08-drum-machines.md`](10-instruments/08-drum-machines.md) — Drum Machines
- [`09-virtual-analog-and-90s.md`](10-instruments/09-virtual-analog-and-90s.md) — Virtual Analog and the 1990s
- [`10-modular-and-west-coast.md`](10-instruments/10-modular-and-west-coast.md) — Modular and West Coast Synthesis
- [`11-chips-trackers-and-voices.md`](10-instruments/11-chips-trackers-and-voices.md) — Sound Chips, Trackers and Voice Machines
- [`12-software-instruments.md`](10-instruments/12-software-instruments.md) — Software Instruments
- [`13-effects-and-processors.md`](10-instruments/13-effects-and-processors.md) — Effects and Processors
- [`14-iconic-patch-recipes.md`](10-instruments/14-iconic-patch-recipes.md) — Iconic Patch Recipes
- [`15-why-old-gear-sounds-like-that.md`](10-instruments/15-why-old-gear-sounds-like-that.md) — Why Old Gear Sounds Like That

### `20-genres/` — Genres — the what

- [`01-house.md`](20-genres/01-house.md) — House
- [`02-techno.md`](20-genres/02-techno.md) — Techno
- [`03-trance.md`](20-genres/03-trance.md) — Trance
- [`04-drum-and-bass.md`](20-genres/04-drum-and-bass.md) — Drum & Bass
- [`05-jungle-and-breakbeat.md`](20-genres/05-jungle-and-breakbeat.md) — Jungle and Breakbeat
- [`06-dubstep-and-bass-music.md`](20-genres/06-dubstep-and-bass-music.md) — Dubstep and Bass Music
- [`07-uk-garage-and-grime.md`](20-genres/07-uk-garage-and-grime.md) — UK Garage, 2-Step and Grime
- [`08-hardstyle-and-hardcore.md`](20-genres/08-hardstyle-and-hardcore.md) — Hardstyle, Hardcore and Hard Dance
- [`09-edm-and-future-bass.md`](20-genres/09-edm-and-future-bass.md) — Festival EDM, Future Bass and Melodic Bass
- [`10-hiphop-and-trap.md`](20-genres/10-hiphop-and-trap.md) — Hip-Hop and Trap
- [`11-drill.md`](20-genres/11-drill.md) — Drill
- [`12-phonk.md`](20-genres/12-phonk.md) — Phonk
- [`13-lofi-and-chillhop.md`](20-genres/13-lofi-and-chillhop.md) — Lo-fi Hip-Hop and Chillhop
- [`14-ambient-and-drone.md`](20-genres/14-ambient-and-drone.md) — Ambient, Drone and Sound Design Music
- [`15-idm-and-glitch.md`](20-genres/15-idm-and-glitch.md) — IDM, Glitch and Experimental Electronic
- [`16-synthwave-and-retro.md`](20-genres/16-synthwave-and-retro.md) — Synthwave, Retrowave and 80s Revival
- [`17-pop-songwriting.md`](20-genres/17-pop-songwriting.md) — Pop Songwriting
- [`18-rock-and-metal.md`](20-genres/18-rock-and-metal.md) — Rock and Metal
- [`19-funk-soul-and-rnb.md`](20-genres/19-funk-soul-and-rnb.md) — Funk, Soul, R&B and Neo-Soul
- [`20-jazz.md`](20-genres/20-jazz.md) — Jazz
- [`21-blues.md`](20-genres/21-blues.md) — Blues
- [`22-classical-and-orchestral.md`](20-genres/22-classical-and-orchestral.md) — Classical, Orchestral and Common-Practice Writing
- [`23-film-and-game-score.md`](20-genres/23-film-and-game-score.md) — Film, Trailer and Game Score
- [`24-latin-and-afro-cuban.md`](20-genres/24-latin-and-afro-cuban.md) — Latin, Afro-Cuban and Brazilian
- [`25-reggae-dub-and-dancehall.md`](20-genres/25-reggae-dub-and-dancehall.md) — Reggae, Dub and Dancehall
- [`26-afrobeats-and-amapiano.md`](20-genres/26-afrobeats-and-amapiano.md) — Afrobeats, Amapiano and African Popular Music
- [`27-world-and-modal-traditions.md`](20-genres/27-world-and-modal-traditions.md) — World and Modal Traditions
- [`28-hyperpop-and-experimental-club.md`](20-genres/28-hyperpop-and-experimental-club.md) — Hyperpop and Experimental Club
- [`29-disco-and-italo.md`](20-genres/29-disco-and-italo.md) — Disco, Italo, Hi-NRG and Nu-Disco
- [`30-country-folk-and-singer-songwriter.md`](20-genres/30-country-folk-and-singer-songwriter.md) — Country, Folk and Singer-Songwriter

### `30-patterns/` — Patterns — the ready-made

- [`01-progression-cookbook.md`](30-patterns/01-progression-cookbook.md) — Progression Cookbook
- [`02-drop-and-buildup.md`](30-patterns/02-drop-and-buildup.md) — The Drop and the Build-Up
- [`03-bassline-cookbook.md`](30-patterns/03-bassline-cookbook.md) — Bassline Cookbook
- [`04-drum-pattern-cookbook.md`](30-patterns/04-drum-pattern-cookbook.md) — Drum Pattern Cookbook
- [`05-melodic-hooks-and-riffs.md`](30-patterns/05-melodic-hooks-and-riffs.md) — Melodic Hooks, Riffs and Arps
- [`06-transitions-and-fx.md`](30-patterns/06-transitions-and-fx.md) — Transitions and FX
- [`07-sampling-and-breaks.md`](30-patterns/07-sampling-and-breaks.md) — Sampling, Chopping and Breaks
- [`08-sound-design-recipes.md`](30-patterns/08-sound-design-recipes.md) — Sound Design Recipes
- [`09-humanization-and-groove.md`](30-patterns/09-humanization-and-groove.md) — Humanisation and Groove
- [`10-arrangement-templates.md`](30-patterns/10-arrangement-templates.md) — Arrangement Templates

### `40-reference/` — Reference — the numbers

- [`01-note-frequency-midi-table.md`](40-reference/01-note-frequency-midi-table.md) — MIDI, Note Name and Frequency Table
- [`02-scale-and-chord-formulas.md`](40-reference/02-scale-and-chord-formulas.md) — Scale and Chord Formula Tables
- [`03-bpm-and-timing-tables.md`](40-reference/03-bpm-and-timing-tables.md) — BPM, Timing and Tempo Tables
- [`04-glossary.md`](40-reference/04-glossary.md) — Glossary
- [`05-quick-decision-tables.md`](40-reference/05-quick-decision-tables.md) — Quick Decision Tables

**79 files.** Everything is plain Markdown with no external dependencies.
