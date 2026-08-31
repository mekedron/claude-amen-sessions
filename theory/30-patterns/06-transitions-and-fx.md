# Transitions and FX

The seams between sections carry a disproportionate share of a track's impact.
This is the toolbox.

## The transition inventory

| Device | Where | Length | Effect |
|---|---|---|---|
| **Riser / uplifter** | End of a build | 1–8 bars | Raises expectation |
| **Downlifter** | Start of a new section | 1–2 bars | Releases pressure |
| **Impact / boom** | On the downbeat | one hit | Marks arrival |
| **Sub-drop** | On or just before the downbeat | 1–2 beats | Physical weight |
| **Reverse cymbal** | Last 1–2 beats | 1–2 beats | Classic lead-in |
| **Reverse reverb** | Last 1–2 beats | 1–2 beats | Dreamlike lead-in |
| **Snare roll** | Last 1–4 bars | 1–4 bars | Rhythmic acceleration |
| **Filter sweep** | Over 4–32 bars | long | Gradual energy change |
| **Silence / cut** | Last 1–2 beats | short | The strongest device |
| **Tape stop** | Last beat | 1 beat | Playful, mechanical |
| **Vinyl rewind** | Last 1–2 bars | 1–2 bars | DJ culture, jungle, dub |
| **Beat repeat / stutter** | Last 1–2 beats | short | Digital, modern |
| **Drum drop-out** | Last bar | 1 bar | Exposes the melody |
| **Crash + kick** | Downbeat | one hit | The plain marker |
| **Vocal ad-lib** | Last beat | short | Human seam |
| **Delay throw** | Last hit of a section | tail | Dub, space |
| **White noise swell** | Over 2–8 bars | long | Fills and masks |
| **Pitch bend of the whole mix** | Last beat | short | Disorienting, hyperpop |
| **Gate/chop the last bar** | 1 bar | 1 bar | Rhythmic reset |

**Compound transitions are the norm.** A typical seam is: filter sweep (8 bars)
+ snare roll (4 bars) + riser (2 bars) + silence (1 beat) + impact + crash +
sub-drop + full mix.

## Building each element

### Noise riser
1. White or pink noise.
2. Band-pass filter, centre frequency sweeping from ~200 Hz to ~8 kHz over the
   riser's length (exponential curve).
3. Resonance moderate to high.
4. Volume rising, exponentially.
5. Optional: tempo-synced pitch steps for a "stepped" riser.
6. Add reverb, and **cut it dead at the drop**.

### Tonal riser
1. A saw or square sweeping up 1–3 octaves.
2. Low-pass filter opening alongside.
3. Vibrato depth increasing.
4. Ends on a note that is *not* in the drop's chord (a semitone below the tonic
   works well) so the drop resolves it.

### Shepard tone riser
Layer 4–6 copies of the same rising sweep, each an octave apart, with each
copy's volume following a bell curve — fading in at the bottom of its sweep and
out at the top. The result rises forever without going anywhere.

### Impact / boom
1. A low sine at 40–60 Hz with a fast pitch drop and a 0.5–2 s decay.
2. Plus a noise burst, low-passed, with a longer tail.
3. Plus a reversed reverb tail *before* it.
4. Plus a distorted transient click.
5. Heavily compressed and often mono.

### Sub-drop
A sine sweeping from ~80 Hz down to ~25 Hz over 0.5–2 beats, with a decaying
envelope, saturated. Best placed so the *bottom* of the sweep lands just before
the drop's downbeat.

### Downlifter
A tonal or noise sweep falling in pitch, usually 1 bar, placed on the first beat
of a new section. It "spends" the accumulated energy.

### Reverse reverb lead-in
1. Take the first sound of the new section.
2. Reverse it, add a long reverb, reverse the result.
3. Place it so the tail ends exactly on the downbeat.

### Tape stop
Read the audio at a rate falling from 1.0 to 0.0 over 200–600 ms, with the
pitch falling proportionally, and a volume fade.

### DJ rewind
Play the audio backwards while accelerating the playback rate. 1–2 bars.
A jungle, dub and garage convention; the track then restarts from a phrase
boundary.

### Beat repeat / stutter
Take the last 1/8 or 1/16 of the bar and repeat it 2, 4 or 8 times, optionally
accelerating (1/8 → 1/16 → 1/32) and/or pitching up.

## Filter automation as arrangement

| Move | Bars | Effect |
|---|---|---|
| Low-pass 200 Hz → 20 kHz | 16–32 | The classic opening; a whole section's worth of energy |
| High-pass 20 Hz → 500 Hz | 4–8 | The build; the bass vanishes |
| High-pass 500 Hz → 20 Hz | 1 | The drop; the bass returns |
| Band-pass sweeping | 8 | Radio/telephone effect passing through |
| Low-pass closing over the outro | 16 | The track walks away |

**Automate the filter on a bus, not on individual channels**, so the whole
section moves together.

## Silence — how to use it

| Placement | Effect |
|---|---|
| 1 beat before a drop | Sharpens the arrival |
| 1 bar before a chorus | Dramatic |
| Mid-phrase, unexpectedly | Startling; use once |
| At the very end of a track | Confident ending |
| Between two identical loops | Makes the second one feel new |

**Budget:** two true silences per track. More and they stop reading as events.

## Ear candy (small non-structural sounds)

These fill the gaps and reward repeat listening. One every 2–8 bars.

| Type | Examples |
|---|---|
| Reversed | Reversed hats, reversed vocal, reversed pad swells |
| Foley | Coins, matches, camera shutters, doors, glass |
| Vocal | Breaths, whispers, laughs, chopped syllables |
| Percussive | Rim clicks, wood blocks, tiny metallic hits |
| Synth blips | Short FM bells, zaps, glitches |
| Textural | Vinyl crackle, tape hiss, rain, crowd |
| Glitch | Bit-crushed fragments, buffer errors, stutters |

Place them **off the grid** (on 16ths that nothing else occupies) and **panned
away from the centre**.

## Section-change checklist

At every seam, verify:

- [ ] Something *leaves* as well as arrives.
- [ ] There is a marker on the downbeat (crash, impact, or a clear timbre change).
- [ ] The last beat before the change is thinner than the rest of the section.
- [ ] The new section differs in at least two dimensions (density, register,
      rhythm, timbre, harmony).
- [ ] The seam lands on a multiple of 8 bars from the start.
- [ ] Any reverb/delay tail from the old section is either cut or deliberately
      allowed to ring into the new one.

## Hazards

- Riser on every transition — they stop working.
- A riser with no impact at its end — the tension has nowhere to go.
- Reverb tails from the build washing over the first bar of the drop.
- The riser louder than the drop.
- Transitions that are not on the grid.
- Using an fx sample without EQ'ing it — most stock risers have far too much
  200–500 Hz.

## Related

- Structure: `../00-foundations/11-form-and-arrangement.md`
- Drops: `02-drop-and-buildup.md`
- Effects theory: `../00-foundations/15-stereo-and-space.md`
