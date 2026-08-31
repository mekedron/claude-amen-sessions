# Sound Design Recipes

Concrete construction methods. Values are starting points.

## Drums

### Kick (electronic)
```
Layer 1 (sub):    sine, pitch 150 Hz → 50 Hz over 30 ms, decay 200-500 ms
Layer 2 (punch):  sine or triangle at 80-120 Hz, decay 80-150 ms, slight distortion
Layer 3 (click):  noise burst or a high sine, 2-6 kHz, decay 5-15 ms
Processing:       saturate layers 2-3, EQ each separately, align transients
```
| Genre | Fundamental | Decay | Character |
|---|---|---|---|
| House | 50–60 Hz | 300–500 ms | Round, soft click |
| Techno | 55–65 Hz | 400–700 ms | Distorted, long |
| Trance | 55–65 Hz | 200–350 ms | Bright click |
| D&B | 50–60 Hz | 100–200 ms | Short, punchy |
| Trap (808) | 30–50 Hz | 500 ms–2 s | Long, tuned, distorted |
| Hardstyle | tuned to key | 300–400 ms | Extremely distorted tail |

### Snare
```
Layer 1 (body):   triangle/sine 180-250 Hz, pitch drop over 30 ms, decay 100-200 ms
Layer 2 (noise):  white noise, band-pass 1-8 kHz, decay 100-250 ms
Layer 3 (snap):   noise high-passed at 6 kHz, decay 30-60 ms
Processing:       compress hard, add a short room reverb, transient shape
```

### Clap
```
4 short noise bursts (band-pass 800 Hz - 4 kHz), spaced 8, 12, 16 ms apart,
each ~15 ms long, followed by a longer body burst with a 100-200 ms decay.
Slight stereo spread between the bursts. High-pass at 300 Hz.
```

### Hi-hat
```
Closed:  white noise, band-pass 6-12 kHz, decay 20-50 ms
Open:    same, decay 200-600 ms
Metallic: 6 square waves at inharmonic frequencies through a high-pass filter
```

### 808
```
Sine oscillator
Pitch:     start 2-4 semitones above the target, glide down over 20-60 ms
Amplitude: instant attack, exponential decay 400 ms - 2 s
Click:     separate 5 ms noise/triangle transient at 1-3 kHz
Saturation: soft clip or tube; generates harmonics at 2f, 3f for phone audibility
Glide:     40-150 ms portamento between notes
```

## Bass

### Reese
```
2-3 sawtooth oscillators
Detune:    10-30 cents apart (and one an octave down, clean)
Filter:    low-pass 200-800 Hz, 24 dB/oct, resonance moderate
Movement:  slow LFO on cutoff, plus a phaser or notch filter sweeping
Sub:       a separate clean sine an octave below, mono
HAZARD:    check mono - detuned saws cancel. The sine sub is what saves it.
```

### Wobble
```
Sawtooth or wavetable
Filter:    low-pass, 24 dB/oct, resonance 30-60%
LFO:       on cutoff, tempo-synced (1/4, 1/8, 1/8T, 1/16, 1/32)
LFO shape: sine for smooth, saw-down for rhythmic drops, square for gating
Sub:       separate clean sine
Arrangement: change the LFO rate every 1-2 bars - that IS the composition
```

### Growl / neuro
```
1. Wavetable oscillator with the position modulated by a fast LFO (10-60 Hz)
2. Distortion
3. Comb filter or phaser
4. RESAMPLE to audio
5. Re-pitch, filter, distort again
6. Repeat 4-5 two or three times
7. Layer with a clean sine sub
```

### Talking / formant bass
```
Saw or growl source
Two band-pass filters at vowel formant frequencies:
  "ee" 270/2290 Hz   "eh" 530/1840   "ah" 730/1090   "oh" 570/840   "oo" 300/870
Automate the filter frequencies to move between vowels over 1-2 bars
Add a third formant at 2500-3000 Hz for realism
```

### Funk / plucked bass
```
Sawtooth + a little square
Filter:    low-pass with an envelope: 4 kHz -> 400 Hz in 80 ms
Amp:       instant attack, decay 200 ms, sustain 0.2, release 60 ms
Add:       slight distortion, and a "pop" transient for slap
```

## Leads

### Supersaw
```
7 sawtooth oscillators
Detune:    symmetric, +-5 to +-25 cents
Phase:     randomised per voice
Pan:       spread across the stereo field (voice 1 centre, others outward)
Filter:    low-pass 8-14 kHz
High-pass: 200-300 Hz (essential - otherwise it eats the bass)
Sub layer: a sine or square an octave down
Play:      3 notes maximum
```

### Pluck
```
Saw or square
Amp:       attack 0-2 ms, decay 150-400 ms, sustain 0, release 100 ms
Filter:    envelope from 6 kHz down to 800 Hz in 100 ms, resonance 20-40%
FX:        1/8 dotted delay, short reverb, slight chorus
```

### Hoover
```
3-5 detuned saws (or a saw + PWM square)
Pitch:     envelope sweeping DOWN 5-12 semitones over 200-600 ms
FX:        heavy chorus, then phaser, then a resonant low-pass
Play:      as short stabs, or as long held notes with the sweep repeating
```

### Acid (303)
```
Saw or square, monophonic
Filter:    low-pass 24 dB/oct, resonance 50-80%
Envelope:  short decay (100-300 ms) on the filter, amount modulated per note
Accent:    on accented notes, raise both the level and the envelope amount
Slide:     portamento (40-80 ms) between selected notes only
Post:      overdrive AFTER the filter
```

### Bell
```
Additive: partials at 1, 2.76, 5.40, 8.93, 13.34 x fundamental
          each with its own decay time (higher = shorter)
or FM:    carrier:modulator ratio 1:1.41 or 1:3.5, index envelope decaying fast
Amp:      attack 0, decay 1-4 s, sustain 0
FX:       long reverb, slight chorus
```

### Vocal-like pad / choir
```
Source:    3-5 detuned saws, or filtered noise + saws
Formants:  band-pass filters at 730/1090 Hz ("ah") with a third at 2600 Hz
Vibrato:   5-6 Hz, depth 10-25 cents, fading in after 300 ms
Amp:       attack 200-600 ms, long release
FX:        big reverb, chorus, slight pitch drift between voices
```

## Pads and atmosphere

### Warm pad
```
3-5 detuned saws or a wavetable
Amp:       attack 300 ms - 2 s, sustain 1.0, release 1-3 s
Filter:    low-pass 2-5 kHz with a slow LFO (0.05-0.2 Hz) on the cutoff
High-pass: 150-250 Hz
FX:        chorus, then a large reverb (3-6 s), high-passed at 300 Hz
```

### Drone
```
1-3 oscillators at the same pitch, detuned by 3-10 cents
Slow random modulation on pitch (+-5 cents) and filter
Layer octaves and fifths for weight
Add filtered noise for texture
No envelope - just a very long fade in and out
```

### Riser
```
Band-passed noise, centre frequency 200 Hz -> 8 kHz (exponential)
Volume rising exponentially
Resonance moderate to high
Optional: pitch steps synced to 1/8 or 1/16 for a "stepped" riser
Reverb, cut dead at the drop
```

### Impact
```
Layer 1: sine 60 Hz -> 30 Hz, decay 1-2 s
Layer 2: low-passed noise burst, decay 1-3 s
Layer 3: a distorted transient click
Layer 4: a reversed reverb tail placed BEFORE the hit
Compress heavily; mostly mono
```

## Texture

### Vinyl crackle
```
Sparse random impulses (Poisson process, ~20-80 per second)
Each impulse: 0.5-3 ms, band-passed 1-6 kHz, random amplitude
Plus continuous low-level pink noise
Plus a periodic "thump" once per rotation (33 rpm = every 1.8 s)
```

### Tape hiss / wow / flutter
```
Hiss:    pink noise at -50 to -40 dB
Wow:     pitch modulation, 0.3-1 Hz, depth 5-20 cents
Flutter: pitch modulation, 6-15 Hz, depth 2-8 cents
Plus:    gentle high-frequency rolloff and soft saturation
```

### Wind / atmosphere
```
Pink or brown noise
Band-pass filter with the centre frequency slowly randomised (0.05-0.3 Hz)
Amplitude modulated by a slow random envelope
Wide stereo (two independently modulated copies)
```

### Rain
```
Dense random impulses (thousands per second), high-passed at 2 kHz
Plus a low continuous rumble
Plus occasional larger single drops
```

## Processing chains that make things sound expensive

| Goal | Chain |
|---|---|
| Fat bass | EQ (cut mud) → saturation → compression → multiband → limiter |
| Big lead | Unison → high-pass → chorus → delay → reverb → compression |
| Punchy drums | Transient shaper → EQ → compression → parallel compression → saturation |
| Wide pad | Detune → chorus → stereo reverb → mid/side EQ (boost side highs) |
| Lo-fi anything | Bit reduction → sample-rate reduction → low-pass → tape saturation → wow |
| Aggressive bass | Distortion → band-split → per-band processing → recombine → clip |
| Vintage warmth | Tape saturation → gentle low-pass → light compression → subtle wow |

## The universal technique: resampling

1. Build a sound.
2. Render it to audio.
3. Process the audio (pitch, filter, distort, reverse, stretch).
4. Render again.
5. Repeat.

Each pass introduces artefacts and relationships that no synthesiser can produce
in one step. This is how modern bass music, hyperpop and neurofunk sound
designers work.

## Related

- The theory: `../00-foundations/12-timbre-and-synthesis.md`
- Effects: `../00-foundations/15-stereo-and-space.md`
