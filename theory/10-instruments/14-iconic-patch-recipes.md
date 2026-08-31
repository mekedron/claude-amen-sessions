# Iconic Patch Recipes

Sounds that are so specific they function as genre signatures. Each one is given
as a build recipe you can follow with any synthesiser or with code.

---

## The Hoover (Alpha Juno "What The", 1986)

**Origin:** a factory patch on the Roland Alpha Juno-1/2, used by Human Resource
on "Dominator" (1991) and Second Phase on "Mentasm" (1991). It became the sound
of rave, hardcore, gabber, hardstyle and jump-up drum & bass.

```
Oscillators: a pulse wave with PWM + a detuned saw (or 3 saws, ±12 cents)
Pitch env:   START ~5-12 SEMITONES ABOVE the note, sweep DOWN to pitch
             over 200-600 ms   <- this sweep IS the hoover
PWM:         LFO at ~5 Hz, moderate depth, running throughout
Filter:      low-pass ~4-6 kHz, moderate resonance, slight downward env
Amp env:     attack 0-10 ms, sustain full, release 200 ms
FX:          heavy CHORUS (essential), then a phaser, then reverb
Play:        as short stabs on offbeats, or as long held notes with the
             sweep retriggering on each note
```
**The two non-negotiable parts:** the downward pitch sweep and the chorus.
Without either it is just a detuned saw.

---

## The Supersaw (Roland JP-8000, 1996)

The sound of trance. See `09-virtual-analog-and-90s.md` for the history.

```
7 saw oscillators
Detune (cents), for a detune amount d in 0..1:
    0, ±(10·d), ±(22·d), ±(38·d)        # non-linear, accelerating spread
Random start phase on every oscillator      # essential; otherwise they cancel
Levels: centre = 1.0, the six side saws = 0.4-0.8 (the "mix" control)
Pan:    centre saw centred; pairs spread progressively to ±30%, ±60%, ±90%
Filter: low-pass 8-14 kHz (just taming, not shaping)
EQ:     HIGH-PASS at 200-300 Hz    <- without this it destroys the bass
Layer:  add a square or sine one octave down at 30% for weight
Amp:    attack 5-20 ms for leads; 300 ms+ for pads
FX:     unison spread, 1/8-dotted delay, large reverb, sidechain to the kick
LIMIT:  3 notes maximum. A 5-note supersaw chord is 35 saws of mud
```

---

## The Reese Bass (1988)

**Origin:** Reese (Kevin Saunderson), "Just Want Another Chance" — commonly
credited to a Casio CZ-5000. Adopted by jungle and drum & bass, where it became
the foundation of the entire genre.

```
2-3 saw oscillators, detuned 10-30 cents apart
    (more detune = more movement and more mono cancellation)
Filter:  low-pass 200-800 Hz, 24 dB/oct, moderate resonance
Movement: a slow LFO on cutoff, PLUS a phaser or a swept notch filter
          - the phasing between the detuned saws is the sound
Sub:     a SEPARATE clean mono sine one octave down, NOT detuned
Amp:     long, sustained notes; legato with portamento
HAZARD:  detuned saws periodically cancel in mono. The clean sine sub is what
         keeps the low end alive. Always check in mono.
Modern:  split at 100 Hz - clean sub below, distortion/notching above
```

---

## The 808 Kick / Trap 808

```
Sine oscillator
Pitch env: start 2-5 semitones above the target note, glide down over 20-60 ms
Amp env:   instant attack, exponential decay 400 ms - 2 s (the decay IS the
           bass note length)
Tune:      to the track's root; it is a bass instrument, not a drum
Click:     a separate 3-8 ms layer - a noise burst or a triangle at 1-3 kHz
Saturation: soft clip / tube; this creates harmonics at 2f, 3f, 4f so the note
           is audible on phones (the ear reconstructs the missing fundamental)
Glide:     40-150 ms portamento between notes = the trap/drill gesture
Mix:       mono, no reverb; sidechain any separate kick against it
```

---

## The 909 Kick (house/techno)

```
Sine, pitch 220 Hz → 55 Hz over 15-30 ms      <- the fast sweep is the 909
Amp decay 200-400 ms
Click layer: 2-5 ms of noise or a filtered impulse at 2-4 kHz
Drive into soft clipping (this is most of the punch)
EQ: boost 50-60 Hz, cut 200-400 Hz, boost 2-4 kHz
```
Compare with the 808: same oscillator, but the 909's sweep is faster and higher,
its decay far shorter, and it has a real transient. Attack versus weight.

---

## The 808 Cowbell (phonk)

```
Two square waves at ~540 Hz and ~800 Hz (a ratio of about 1.48 - deliberately
    inharmonic)
Band-pass filter ~800 Hz - 6 kHz
Amp: instant attack, decay 100-400 ms, no pitch envelope
For drift phonk: TUNE it to the key, play a melodic riff with it, and drive it
    hard into tanh or a wavefolder until it screams
```

---

## The M1 House Piano (Korg M1, 1988)

```
A bright, hard-attack piano - strong 2nd and 3rd harmonics, weak fundamental
Decay 400-800 ms, no sustain pedal
EQ: high-pass at 200-300 Hz, boost 1-3 kHz
Play: SHORT STABS on offbeats (steps 2, 6, 10, 14), 7th and 9th chords
FX: plate reverb (1-1.5 s), slight chorus, gated tightly so the tail does not
    smear
```
It does not sound like a real piano. That is why it cuts through a club system.

---

## The Rave Organ Stab (M1 "Organ 2" / Korg)

```
A bright organ tone (stacked sines/squares at 1, 2, 3, 4× with the 3rd
    harmonic prominent)
Amp: instant attack, decay 150-300 ms, hard cut
Play: a minor or sus4 chord, stabbed on an offbeat
FX: reverb with the tail gated, slight pitch-up on the attack
```

---

## The Orchestra Hit (Fairlight ORCH5, 1979)

A sampled orchestral stab (originally from Stravinsky's *Firebird*), pitched
across a keyboard. "Planet Rock", then all of electro, rave, jungle and hip-hop.

```
A dense, bright orchestral chord: brass + strings + timpani, all attacking
    together
Very fast attack, 300-600 ms decay
Pitched by VARISPEED (so lower = longer and darker)
8-bit sample reduction for authenticity
Play: as a rhythmic figure, often in a rising or falling sequence
```

---

## The DX7 Electric Piano (1983)

```
Operator pair A ("tine"):
  carrier ratio 1.0; modulator ratio 14.0 (the attack ping) at low index
  modulator env: instant attack, decay to zero in 80-200 ms
Operator pair B ("body"):
  carrier ratio 1.0; modulator ratio 1.0, index ~1.5
  modulator env: decay to ~0.2 over 400 ms
Carrier env: instant attack, decay 2-4 s
Velocity → modulator output levels (harder = brighter, not just louder)
FX: chorus, stereo tremolo at 4-6 Hz, plate reverb
```

---

## The TX81Z "Lately Bass" (1987)

```
4-op FM. Carrier ratio 1.0 with a SQUARE (not sine) modulator at ratio 1.0
Index ~2-4, decaying to ~1 over 60-120 ms
Second layer detuned 7-12 cents
Low-pass at ~2 kHz
Amp: instant attack, decay 200-400 ms, low sustain
```
Hollow, woody, metallic. The bass of house, garage and jungle.

---

## The Amen Break

Not a synth patch — see `../30-patterns/07-sampling-and-breaks.md`. Summary:
The Winstons, "Amen, Brother" (1969); four bars; sped from ~136 to 160–175 BPM
(which raises it ~3–4 semitones); chopped and resequenced; the ghost notes are
what make it work.

---

## The Dubstep Growl / Talking Bass

```
1. Wavetable oscillator, position modulated by an LFO at 20-80 Hz
   (or a stepped sequencer at 1/16) - audio-rate modulation = the growl
2. A second detuned copy (12-20 cents), position offset
3. Ring mod or hard sync between them
4. Distortion
5. Two band-pass filters at VOWEL FORMANT frequencies, swept between vowels:
      "ee" 270/2290   "eh" 530/1840   "ah" 730/1090   "oh" 570/840   "oo" 300/870
6. Resonant low-pass with a tempo-synced stepped LFO on cutoff
7. RESAMPLE to audio, re-pitch, distort again - repeat 2-3 times
8. Multiband: keep 0-100 Hz as a CLEAN mono sine sub
```

---

## The Future Bass Chord

```
Supersaw or wavetable, voiced HIGH (MIDI 60-84), 4-5 note maj9/m9/add9 chords
Pitch modulation: an LFO or envelope bending the WHOLE chord ±10-50 cents,
    tempo-synced at 1/8 or 1/16 - the characteristic "wobble"
Heavy sidechain from the kick (the "breathing")
Multiband upward compression (OTT-style) at 30-60%
Wide stereo, big reverb, high-passed at 250 Hz
Often doubled by a formant-shifted vocal chop playing the same chords
```

---

## The Trance Pluck

```
Saw or square
Amp: attack 0-2 ms, decay 150-350 ms, sustain 0, release 100 ms
Filter env: 6 kHz → 800 Hz in 80-150 ms, resonance 20-40%
FX: 1/8-dotted ping-pong delay (feedback 40%), large reverb, sidechain
Play: 16th-note arpeggios or offbeat 8ths
```

---

## The Acid Line (TB-303)

```
Saw or square, MONOPHONIC
Low-pass 18 dB/oct (or 24 dB with less resonance), resonance 55-85%
Filter env: attack 0, decay 100-400 ms, sustain 0, amount 40-90%
Accent steps: +6 dB level AND +30% env amount, simultaneously
Slide steps:  60 ms portamento, WITHOUT retriggering the envelope
Overdrive AFTER the filter (most of the "acid" aggression is distortion)
PERFORM: automate cutoff, resonance and env-mod continuously over 16-32 bars
         while the 16-step pattern stays fixed
```

---

## The Gated Reverb Snare (1980s)

```
Snare → large bright reverb (2-4 s, no pre-delay, high-passed at 300 Hz)
      → NOISE GATE keyed to the dry snare: hold 150-300 ms, very fast release
Mix the gated reverb LOUD - often louder than the dry snare
```

---

## The Shimmer Pad (ambient)

```
Source: a pad, a held note, a vocal, or a guitar
Reverb with decay 6-15 s
In the reverb's FEEDBACK path: pitch shift +12 semitones (and optionally -12)
Feedback 40-70%, with a low-pass at 4-6 kHz in the loop to stop it screaming
Mix mostly wet; let it build over 20-60 seconds
```

---

## The Vinyl / Lo-fi Treatment

```
Bit depth → 10-12 bits (truncate, no dither)
Sample rate → 22-32 kHz
Low-pass at 6-12 kHz, high-pass at 60-100 Hz
Tape wow: pitch modulation 0.3-1 Hz, depth 5-20 cents
Tape flutter: 6-15 Hz, depth 2-8 cents
Vinyl crackle: sparse random impulses (20-80/s, 0.5-3 ms, band-passed 1-6 kHz)
Pink noise at -50 dB
Saturation, gentle compression with visible pumping
Narrow the stereo image
```

---

## The Trap Hi-Hat Roll

```
A single closed hat sample
Pattern: 1/8 → 1/16 → 1/32 → 1/16 triplets, changing every half-bar
Per-hit: pitch varies ±3 semitones, velocity varies 60-120, pan varies ±20%
Roll shape: velocity ramps up or down across the roll
Occasionally: a rate that accelerates continuously across a beat
```
Use **parameter-lock thinking**: every step gets its own pitch, decay and pan.

---

## Quick index

| Sound | Origin | File |
|---|---|---|
| Hoover | Alpha Juno | above |
| Supersaw | JP-8000 | above |
| Reese | Casio CZ-5000 (attributed) | above |
| 808 kick/bass | TR-808 | `08-drum-machines.md` |
| 909 kick | TR-909 | `08-drum-machines.md` |
| Cowbell | TR-808 | above |
| M1 piano | Korg M1 | `07-samplers-and-workstations.md` |
| Orchestra hit | Fairlight ORCH5 | `07-samplers-and-workstations.md` |
| DX7 e-piano | Yamaha DX7 | `05-fm-and-phase-distortion.md` |
| Lately Bass | Yamaha TX81Z | `05-fm-and-phase-distortion.md` |
| Growl | Massive/Serum | `12-software-instruments.md` |
| Gated snare | AMS RMX16 | `13-effects-and-processors.md` |
| Shimmer | Eventide/Valhalla | `13-effects-and-processors.md` |
| Acid | TB-303 | `02-analog-monosynths.md` |
| Amen break | The Winstons | `../30-patterns/07-sampling-and-breaks.md` |

## Related

- Generic recipes: `../30-patterns/08-sound-design-recipes.md`
- Where each belongs: `../20-genres/`
