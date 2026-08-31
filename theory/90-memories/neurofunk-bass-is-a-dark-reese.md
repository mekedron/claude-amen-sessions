---
name: neurofunk-bass-is-a-dark-reese
description: What a neurofunk bass measures as - a very dark, hugely detuned, notched saw stack - and the two ways of building one that get rejected
type: preference
date: 2026-09-01
---

The main bass of a neurofunk track is a **detuned sawtooth stack through a low
resonant filter and a notch**, and its numbers are nothing like a synth-bass
preset. Two reference samples the user supplied (`_Do_You_Even_Witch_A1.mp3`,
`_Witch_House_Reese_G1.mp3`) measure:

| | Witch A1 (55 Hz) | Reese G1 (49 Hz) |
|---|---|---|
| under 120 Hz | 44% | 67% |
| 120-400 Hz | 48% | 28% |
| 400-1500 Hz | 6.7% | 4.5% |
| **above 1500 Hz** | **1.1%** | **0.7%** |
| detune (beat rate per partial) | ~32 cents | ~55 cents |
| side energy | 78% | 110%, and 54% of it below 120 Hz |

Three consequences: the filter cutoff belongs at **270-980 Hz**, not in the
mids; the detune is **30-55 cents**, three times a supersaw's; and the notch
is audible as a 4-6 dB dip through the fifth to the fourteenth partial that
comes back afterwards - one gap travelling through the harmonics.

Two constructions the user has rejected by ear:

1. **Hard sync and FM as the body of the sound.** Stepping the sync ratio,
   phase-distortion warp and cutoff on every sixteenth gives a timbre rebuilt
   from scratch each step: "как будто ты делаешь скретчи пластинкой... только
   очень ровные скретчи". Sync and FM belong on two or three accent steps a
   bar, mixed in by their own lanes so a step that does not ask for them
   hears none of them at all.
2. **One saw.** "Он какой-то простой и не глубокий" - a single stack is thin.
   Three stacks at 0.4x, 1x and 1.8x the detune, crossfaded per step, give
   the oscillator itself a width that moves.

**Why:** every complaint he has made about a bass has been about the *core
oscillator*, never about the filter movement or the arrangement. The genre's
sound is a saw - "обычным стандартным классическим звуком - saw" - and the
processing is what is done to it, not what replaces it.

**How to apply:** `reese()` in `src/machinelib.py` is built to these numbers;
`sawspread()` is the stereo stack it is made of. Layer three parts that never
share a band - `subbar` under 105 Hz mono, `reese` from there to ~4 kHz, and a
highpassed `bassbar` gated to the accent steps only.

Related: [[bar-rendered-parts-must-overhang]]
