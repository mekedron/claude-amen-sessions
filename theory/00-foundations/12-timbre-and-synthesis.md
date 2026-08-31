# Timbre and Synthesis

Timbre is why a violin and a synth playing the same note are different. It is
made of three things: the **spectrum** (which harmonics, at what levels), the
**envelope** (how those levels change over time), and the **noise/transient**
content at the attack.

Of the three, **the envelope matters most for recognition** — strip the attack
off a piano note and most listeners cannot name the instrument.

## The spectrum

| Waveform | Harmonics | Amplitude of nth | Sound | Use |
|---|---|---|---|---|
| Sine | 1st only | — | Pure, invisible in a mix | Sub bass, bells, FM operators |
| Triangle | odd only | 1/n² | Soft, hollow, flute | Soft leads, retro bass, chiptune |
| Square | odd only | 1/n | Hollow, woody, clarinet | Chiptune, reedy leads, hollow bass |
| Pulse 25% | all, notched | varies | Nasal, thin | Plucks, funky leads |
| Pulse 10% | all, notched | varies | Very thin, buzzy | Chiptune, harpsichord-ish |
| Sawtooth | all | 1/n | Bright, brassy, rich | The workhorse: pads, leads, bass, strings |
| Noise (white) | all, random | flat | Hiss | Hats, snares, wind, texture |
| Noise (pink) | all, random | −3 dB/oct | Fuller hiss | Natural noise, rain, room tone |

Rules of thumb: **more harmonics = brighter and more present, but also more mask­ing
and more aliasing.** A sawtooth cuts through a mix; a sine disappears unless it
owns its band.

**Pulse-width modulation (PWM)**: slowly sweeping a pulse wave's duty cycle
between ~10% and ~50% makes the notched harmonics move, producing a rich,
chorus-like motion from a single oscillator. The classic 80s string/pad sound.

## The amplitude envelope (ADSR)

| Stage | What it controls | Typical ranges |
|---|---|---|
| **Attack** | Time from silence to peak | 0–5 ms percussive, 5–50 ms plucked, 100 ms–2 s pads |
| **Decay** | Time from peak down to sustain | 20 ms–2 s |
| **Sustain** | Level held while the note is on | 0 for plucks, 0.6–1.0 for pads |
| **Release** | Time to silence after note-off | 10 ms staccato, 200 ms–5 s ambient |

Envelope shapes and what they sound like:

| A | D | S | R | Result |
|---|---|---|---|---|
| 0 | 80 ms | 0 | 50 ms | Pluck, stab |
| 0 | 800 ms | 0 | 800 ms | Piano/bell |
| 0 | 20 ms | 0.9 | 40 ms | Organ, sub bass |
| 300 ms | — | 1.0 | 1.5 s | Pad, strings |
| 1.5 s | — | 1.0 | 4 s | Ambient swell |
| 0 | 200 ms | 0.3 | 100 ms | Electric piano |
| 5 ms | 30 ms | 0.7 | 100 ms | Brass |

**HAZARD:** an attack of exactly 0 ms on any oscillator produces a click, because
the waveform starts mid-cycle at a non-zero value. Use 1–5 ms, or start the
oscillator at phase 0, or apply a 2–5 ms fade. This is the single most common
artefact in programmatically generated audio.

**HAZARD:** the same applies at the end. Cutting a sustained tone dead produces
a click. Always fade the last 2–5 ms.

## The filter envelope — where character lives

A second envelope applied to filter cutoff is what makes a synth sound *played*
rather than switched on.

- **Pluck**: cutoff starts at 8 kHz, falls to 400 Hz in 150 ms. The note is
  bright at the attack and dark afterwards — exactly how physical instruments
  behave.
- **Sweep-in pad**: cutoff rises from 200 Hz to 4 kHz over 2 seconds.
- **Acid**: cutoff envelope with high resonance, and the envelope amount
  modulated per note (accents). This *is* the 303 sound.
- **Wobble**: cutoff driven by a tempo-synced LFO instead of an envelope.

**Rule:** brightness should fall as a note decays. A note whose spectrum stays
constant sounds synthetic (which may be what you want).

## Filters

| Type | Passes | Use |
|---|---|---|
| **Low-pass (LP)** | below cutoff | 90% of all filtering; darkening, distance, drama |
| **High-pass (HP)** | above cutoff | Removing mud; build-ups; making room for the bass |
| **Band-pass (BP)** | a band | Telephone/radio effects, isolation, formants |
| **Notch** | everything except a band | Phaser-like sweeps, removing a resonance |
| **All-pass** | everything (phase only) | Phasers, reverb building blocks |
| **Comb** | periodic peaks | Flanger, resonator, physical modelling |

**Slope** (6, 12, 18, 24 dB/octave) determines how sharply the filter acts.
12 dB/oct is gentle and musical; 24 dB/oct is the classic "moog" ladder sound.

**Resonance (Q)** boosts frequencies at the cutoff. Low Q = tonal shaping.
High Q = a whistling, self-oscillating peak that becomes a pitched element in
itself. Acid, psytrance and drum'n'bass live on high resonance.
**HAZARD:** high resonance can add 12–20 dB at the cutoff frequency. Compensate
the level, or a filter sweep will destroy your headroom.

## Modulation

| Source | Typical destinations |
|---|---|
| **LFO** (0.01–20 Hz) | pitch (vibrato), amplitude (tremolo), cutoff (wobble), pan, PWM |
| **Envelope** | cutoff, pitch, FM amount, amplitude |
| **Velocity** | amplitude, cutoff, FM amount, sample choice |
| **Key tracking** | cutoff (so high notes stay bright), envelope times |
| **Random / S&H** | cutoff, pitch, pan — for movement without pattern |
| **Audio-rate modulation** | becomes FM/AM — a timbre change, not a movement |

**LFO shapes**: sine (smooth), triangle (linear), saw down (rhythmic drops),
saw up (rising), square (on/off gating), S&H (stepped random), noise (drift).

**Tempo-synced LFO rates** matter enormously. Free-running LFOs sound loose and
organic; synced LFOs sound tight and modern. See `02-rhythm-and-time.md` for the
Hz conversions.

## Synthesis methods

### Subtractive
Start rich (saw, square, noise), remove with filters. The default of analogue
synths and 90% of electronic music.

`oscillator(s) → mixer → filter (with envelope) → amplifier (with envelope) → fx`

### Additive
Build a sound by summing sines with individual amplitudes and envelopes. Total
control, expensive, and the basis of band-limited oscillator generation. Best
for bells, organs, evolving pads and anything where each partial needs its own
decay (real bells have inharmonic partials that decay at different rates).

### FM (frequency modulation)
One oscillator (the **modulator**) modulates another's (the **carrier**)
frequency at audio rate. Produces sidebands at `carrier ± n × modulator`.

- The **ratio** of modulator to carrier frequency determines the character:
  integer ratios (1:1, 2:1, 3:2) = harmonic and pitched; non-integer ratios
  (1:1.41, 1:2.76) = inharmonic, metallic, bell-like.
- The **index** (modulation depth) controls brightness. Envelope the index and
  you get an instrument whose spectrum evolves — this is why FM electric pianos
  and bells sound alive.
- Classic FM sounds: DX7 electric piano (ratio 1:1, index envelope), bells
  (inharmonic ratios), bass (ratio 1:2 with a fast index decay), brass (index
  rises with velocity).
- **HAZARD:** FM aliases very easily. High index at high pitch folds sidebands
  back down. Limit the index in the upper register.

### AM / ring modulation
Multiply two signals. Ring mod produces only the sum and difference frequencies
(`|c−m|` and `c+m`), removing the originals — instantly inharmonic and metallic.
Robot voices, dalek, gongs, industrial percussion.

### Wavetable
Store a series of single-cycle waveforms and sweep a "position" pointer between
them. The position becomes a modulation destination, so timbre morphs continuously.
The dominant method in modern EDM (growls, evolving pads, complex leads).

### Granular
Chop audio into 5–100 ms grains and replay them with independent position, pitch,
density and pan. Enables time-stretching without pitch change, freezing, clouds
and textures. The basis of ambient, IDM and modern sound design.

- Grain size < 20 ms → the grain rate itself becomes a pitch (buzzy).
- Grain size 40–100 ms with high overlap → smooth, "frozen" texture.
- Randomising grain position ±50 ms removes the periodicity artefacts.

### Physical modelling
Simulate the physics: a **Karplus–Strong** plucked string is a burst of noise
fed through a delay line of length `SR/frequency` with a small amount of
low-pass filtering in the feedback loop. Cheap, and instantly recognisable as a
string. Extends to tubes (waveguides), membranes and modal resonators.

### Sampling
Play recorded audio. Pitch by playback rate (which changes duration) or by
time-stretching (which does not). Multi-sampling (one recording per few
semitones) avoids the "chipmunk"/"munchkinisation" of formants.

## Building specific sounds

### Supersaw / hypersaw (trance, festival EDM)
7 sawtooth oscillators, detuned symmetrically ±5 to ±25 cents, random start
phases, spread across the stereo field, low-passed around 8–12 kHz, then a
high-pass at 200–300 Hz to keep it out of the bass. Layer with a sine or square
an octave down for weight. **Play at most 3 notes at once.**

### Reese bass
2–3 saws detuned 10–30 cents, low-passed at 200–800 Hz, plus a clean sine sub.
Movement from a slow filter LFO, a phaser, or notch sweeps.

### Pluck
Saw or square, amplitude decay 100–400 ms with zero sustain, filter envelope
falling from 6 kHz to 800 Hz in 100 ms, a touch of reverb, short delay.

### Pad
3–5 detuned saws or a wavetable, attack 200 ms–2 s, full sustain, release 1–3 s,
low-pass 2–5 kHz with a slow LFO, chorus, and a large reverb. High-pass at
150–250 Hz so it does not crowd the bass.

### Bell
FM with an inharmonic ratio (e.g. 1:1.41 or 1:3.5), or additive with partials at
1, 2.76, 5.4, 8.9 × the fundamental, each with a different decay time (higher
partials decay faster). Zero attack, long decay, no sustain.

### Hoover (rave, hardcore)
A detuned saw stack with a **pitch envelope sweeping down** over 200–600 ms,
heavy chorus/phaser, played as a stab. The pitch sweep is the whole sound.

### 808 kick / bass
Sine oscillator, pitch envelope from ~120 Hz falling to the target note in
20–60 ms, amplitude decay 200 ms–2 s, saturation for harmonics, a click layer
(1–3 kHz noise burst, 5 ms) for attack.

### Snare
Two layers: a pitched body (sine or triangle at 180–250 Hz with a fast pitch
drop and a 100–200 ms decay) plus noise (band-passed 1–8 kHz, 100–250 ms decay,
sometimes gated). Blend to taste.

### Hi-hat
Band-passed white noise (6–12 kHz), decay 20–60 ms closed / 200–600 ms open.
For metallic realism, use several square waves at inharmonic frequencies
(the classic 808 hat uses six) through a high-pass.

### Acid (303)
Saw or square, 24 dB low-pass with high resonance, filter envelope with a short
decay, accent notes that increase both level and envelope amount, and slide
(portamento) between selected notes. Overdrive after the filter.

## Distortion and saturation

Distortion adds harmonics that were not there. Which harmonics depends on the
transfer curve:

| Type | Curve | Harmonics added | Character |
|---|---|---|---|
| **Soft clip / tanh** | smooth compression | odd, gentle | Warmth, "analogue", glue |
| **Hard clip** | flat above threshold | odd, harsh | Loud, aggressive, digital |
| **Tube / asymmetric** | asymmetric curve | even + odd | Rich, musical, "fat" |
| **Wavefolder** | folds back on itself | many, inharmonic-ish | Metallic, screaming, west-coast |
| **Bitcrush** | amplitude quantisation | inharmonic noise | Lo-fi, digital, gritty |
| **Sample-rate reduction** | decimation | aliased mirror images | Chiptune, harsh, robot |
| **Rectification** | abs() | strong even harmonics | Octave-up, ring-mod-ish |

**Even harmonics** (2nd, 4th) sound "warm" and musically consonant (octaves and
fifths above). **Odd harmonics** (3rd, 5th) sound "hard" and aggressive.

Practical: run a signal through a low-pass *before* distorting to control which
harmonics get generated, and a low-pass *after* to tame the fizz. Distortion
before filtering sounds different from filtering before distortion — both are
valid, and the order is a creative choice.

## Noise as an instrument

- **White**: flat power per Hz. Hats, snares, harshness.
- **Pink**: −3 dB/octave. Rain, wind, natural, less fatiguing.
- **Brown/red**: −6 dB/octave. Rumble, thunder, ocean.
- **Filtered noise** is the basis of: risers (band-pass sweeping up), wind
  (band-pass with slow random movement), breath, vinyl crackle (sparse impulses),
  and every cymbal.

## Stereo from mono

| Technique | How | Risk |
|---|---|---|
| **Detune spread** | Multiple detuned voices panned differently | Safe, the standard |
| **Haas delay** | Delay one channel 5–35 ms | Collapses in mono; use sparingly |
| **Mid/side EQ** | Boost highs in the side channel | Safe |
| **Chorus/ensemble** | Modulated short delays, opposite phase per channel | Some mono loss |
| **Stereo reverb** | Different IR per channel | Safe |
| **Inverted phase** | Left = −right | **Never** — vanishes in mono |

**Rule:** everything below ~150 Hz stays mono. Width above that is free.

## HAZARDS in synthesis

- **Clicks** from zero-length attacks/releases and from cutting at non-zero
  amplitude. Fade 2–5 ms.
- **Aliasing** from naive oscillators, FM at high index, or distortion of
  high-frequency content. Band-limit or oversample.
- **DC offset** from asymmetric distortion or non-zero-mean waveforms. High-pass
  at 20 Hz at the end of the chain.
- **Resonance blowing the headroom** on filter sweeps.
- **Phase cancellation** when layering the same waveform at the same pitch —
  randomise start phase.
- **Uncompensated gain** when adding oscillators: summing 7 saws is +17 dB.
  Divide by the voice count, or by `sqrt(n)` for uncorrelated sources.

## Related

- Frequency consequences of these choices: `13-frequency-and-eq.md`
- Concrete patch recipes: `../30-patterns/08-sound-design-recipes.md`
- Effects in depth: `15-stereo-and-space.md`
