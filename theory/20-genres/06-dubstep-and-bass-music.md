# Dubstep and Bass Music

**Identity:** halftime drums at 140 BPM over an enormous, modulated bass. Space
and weight; the drop is the destination and the bass is the melody.

## Numbers

| Parameter | Value |
|---|---|
| Tempo | 138–142 (standard 140); riddim 140; deep dubstep 138–140; future garage 130–140 |
| Meter | 4/4, felt as halftime (~70 BPM) |
| Key | Minor, Phrygian; often only 1–2 pitches matter |
| Loudness | −8 to −5 LUFS |

## Drums — the halftime skeleton

```
kick:   x - - - | - - - - | - - - - | - - - -
snare:  - - - - | - - - - | x - - - | - - - -
hat:    - - x - | - - x - | - - x - | - - x -
```

**Kick on 1, snare on 3.** That is the genre. Everything else is decoration.

Common variations:
```
kick:   x - - - | - - x - | - - - - | - - x -
snare:  - - - - | - - - - | x - - - | - - - -
perc:   - - - x | - x - - | - - - x | - x - x
```

- Snare on beat 3 must be **huge** — layered, long, with a reverb tail.
- Hats sparse and syncopated, often with a shuffled or dotted feel.
- The space between hits is as important as the hits. Dubstep drums are the
  sparsest in electronic music.

## Bass — the actual instrument

The bass carries melody, rhythm and timbre simultaneously.

| Type | Description |
|---|---|
| **Wobble** | LFO on the filter cutoff, tempo-synced. Changing the LFO rate per bar (1/4, 1/8, 1/8T, 1/16) *is* the composition |
| **Growl** | Fast modulation (20–100 Hz) or FM so the modulation becomes timbre |
| **Talking / formant** | Band-pass filters at vowel frequencies, swept between vowels |
| **Reese** | Detuned saws with phaser/notch movement |
| **Yoi / metallic** | Hard-synced oscillators, resampled and re-pitched |
| **Sub only** | Deep dubstep: a clean sine and nothing else |
| **Screech / laser** | High, fast-modulated, riddim style |

**Design method** (the standard workflow):
1. Start with a saw or a wavetable at MIDI 28–40.
2. Add a clean sine sub an octave down, mono, unmodulated.
3. Modulate the mid layer: filter LFO, wavetable position, FM index, distortion.
4. **Resample** the result to audio, then process the audio again (pitch,
   filter, distortion, reverse). This layered resampling is what makes modern
   bass sound "impossible".
5. Multiband: keep 0–100 Hz clean, mangle everything above.

## Harmony

Minimal. Often a single note or a two-chord loop. When present:
- `i–bVI`, `i–bII` (Phrygian), or a suspended drone.
- Intro/breakdown sections may have real chords (pads, piano) that vanish at the
  drop.

## Arrangement

```
0-15    Intro: atmosphere, filtered drums, a hint of the bass.
16-31   Groove: drums + sub, half energy.
32-47   Build: risers, snare roll, filter, then SILENCE for 1–2 beats.
48-79   DROP 1: 32 bars. Bass is the lead. Change the bass pattern every 4 bars.
80-95   Breakdown: chords, vocal, atmosphere, no bass.
96-111  Build 2.
112-143 DROP 2: different bass sound, more aggressive.
144+    Outro.
```

**The silence before the drop is mandatory.** One beat to one bar of nothing.

Within a drop, the standard structure is **call and response**: 2 bars of bass,
2 bars of a variation, repeated with escalation. A drop that plays the same
2-bar bass loop 16 times is a failure.

## Subgenres

| Subgenre | Feature |
|---|---|
| **Deep / original dubstep** | Sparse, dubby, sub-focused, 2005–2009 London |
| **Brostep** | Aggressive mid-range, huge growls, US festival, 2010– |
| **Riddim** | Minimal, repetitive triplet bass patterns, extremely sparse |
| **Melodic dubstep** | Emotional chords + big drop; crossover with future bass |
| **Tearout** | Maximum aggression, distorted, fast bass changes |
| **Future garage** | 2-step drums, dubstep sound design, melancholic, 130–140 |
| **Trapstep / hybrid trap** | Trap hats over dubstep drops |
| **Colour bass** | Melodic, tonal basses that play actual chords |
| **Drumstep** | D&B drums at 174 with dubstep-style bass |
| **Halftime** | 170 BPM written, felt at 85, dark and spacious |
| **UK bass / bassline** | House tempo, dubstep sound design |
| **Grime** | 140 BPM, square-wave basses, MC-led, sparse (see UK garage file) |

## Production notes

- **Multiband processing on the bass is essential.** Split at ~100 Hz. Below:
  clean mono sine. Above: distortion, modulation, width.
- **Mono the low end** absolutely. Anything below 120 Hz is mono or it disappears
  on a club system.
- **The drop's loudness comes from density**, not from the limiter. Layer 3–5
  bass sounds occupying different bands.
- Sidechain the bass to the kick and the snare.
- **Resampling** (bounce to audio, re-process, repeat) is the core technique.
- Reverb on the snare, never on the bass.
- The intro and breakdown should be significantly quieter than the drop — the
  dynamic range across the arrangement is the genre's main weapon.

## Clichés (use knowingly)

The one-bar silence; the sub-drop; the "riddim triplet" pattern; the pitched
vocal sample saying something ominous; the build with a rising siren; the second
drop being a different bass patch; the "growl that says a word".

## Hazards

- A busy drum pattern — dubstep drums are minimal by design.
- Bass without a clean sub — the drop will have no weight.
- Bass without mid-range content — it will be inaudible on phones and laptops.
- The same bass sound for the whole drop.
- No dynamic contrast between the breakdown and the drop.
- Distorting the sub layer.
