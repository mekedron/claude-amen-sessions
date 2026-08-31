# Analog Monosynths

One note at a time, and every one of them defined a genre.

---

## Moog Minimoog Model D (1970)

**Type:** 3-VCO subtractive monosynth. The first portable, playable synthesiser.

### Signal path
```
VCO1 (saw/tri/pulse ×3 widths) ┐
VCO2 (same, detunable)         ├→ Mixer (+ noise, + external in) → Ladder LPF (24 dB/oct)
VCO3 (same, or LFO below 20 Hz)┘                                    ↓
                                                          Loudness Contour (VCA)
Two ADS envelopes: one for the filter, one for the amplifier (attack/decay/sustain, no release —
the release is the decay knob with the "decay" switch on)
```

### The controls that matter
| Control | Effect |
|---|---|
| **Oscillator detune** | VCO2 and VCO3 detuned ±5–20 cents against VCO1 — the entire "fat" |
| **Cutoff + Emphasis (resonance)** | Emphasis past ~8 self-oscillates into a sine |
| **Filter contour amount** | How far the envelope sweeps the cutoff — the "wow" of every Moog bass |
| **VCO3 → filter/pitch** | Osc 3 as an LFO for vibrato or filter wobble |
| **External input feedback** | Patch the output back into the external in → overdrive, the "Moog growl" |
| **Glide** | Portamento; essential for lead lines |

### Why it sounds like that
The **ladder filter** (four cascaded transistor pairs) is not a clean 24 dB/oct
low-pass. It loses low end as resonance rises, and it saturates non-linearly when
driven — the bass "compresses" and the harmonics fold. The oscillators drift
against each other continuously because they are temperature-dependent, so the
detune is never static.

### What it changed
The synthesiser as a *lead and bass instrument*: Stevie Wonder, Kraftwerk,
Parliament/Funkadelic, Gary Numan, Giorgio Moroder ("I Feel Love" — a sequenced
Moog bass through a delay is the origin of all sequenced dance music).

### Rebuild
```
3 saw oscillators: 0 cents, +7 cents, -9 cents (one optionally an octave down)
Low-pass 24 dB/oct, resonance 20-35%
Filter envelope: attack 0, decay 250-600 ms, sustain 30%, amount 40-70%
Amp envelope: attack 2 ms, decay 400 ms, sustain 70%, release 150 ms
Saturation AFTER the filter (tanh, moderate)
Slight random pitch drift (±3 cents, 0.2 Hz) on each oscillator
```

---

## ARP 2600 (1971)

**Type:** semi-modular. Pre-wired signal path, overridable with patch cables.

### Signal path
```
3 VCOs (one usable as LFO) + noise + ring modulator
   → VCF (early units: a Moog ladder clone, later: ARP 4072 4-pole)
   → VCA → built-in spring reverb → built-in speakers
Plus: sample & hold, envelope follower, lag processor, two envelopes
```

### The controls that matter
Everything is a slider with a normalled connection, so you can hear the change
before you patch. The **ring modulator**, the **sample & hold** and the
**envelope follower** are the three modules that make it a sound-design tool
rather than a keyboard.

### What it changed
Sound design as a discipline. R2-D2 (Ben Burtt), the Doctor Who and BBC
Radiophonic tradition, Herbie Hancock, Jean-Michel Jarre, Vince Clarke, and
most of the "electronic sound effect" vocabulary of the 1970s–80s.

### Rebuild
Ring modulation (`out = a * b`) between two oscillators at non-harmonic ratios
plus a sample & hold modulating pitch or cutoff gets you 80% of the way to
"vintage sci-fi".

---

## ARP Odyssey (1972)

**Type:** duophonic (two notes) monosynth; the aggressive, thinner answer to
the Minimoog.

Key features: **oscillator sync**, **PWM**, a high-pass filter alongside the
low-pass, sample & hold, and a much snappier envelope. The Rev 1 filter (a Moog
ladder clone) was replaced after litigation; Rev 2 and Rev 3 have ARP's own
4075 filter — brighter and more aggressive.

Used by: Herbie Hancock, Ultravox, 808 State, Portishead, and a great deal of
90s techno.

**Rebuild the "sync lead":** oscillator 2 hard-synced to oscillator 1, with an
envelope sweeping oscillator 2's pitch up 1–2 octaves over 200–600 ms. The
timbre tears upward without the pitch changing.

---

## Korg MS-20 (1978)

**Type:** semi-modular monosynth with a patch bay and, crucially, an
**external signal processor**.

### Signal path
```
VCO1 (saw/pulse/tri/noise) + VCO2 (detunable, can be ring-modulated)
  → HIGH-PASS filter (12 dB/oct, resonant)
  → LOW-PASS filter (12 dB/oct, resonant)
  → VCA
Patch bay: modulation wheel, S&H, envelope follower, pitch-to-voltage converter
```

### Why it sounds like that
**Two resonant filters in series, one high-pass and one low-pass**, both able to
self-oscillate and both extremely aggressive when pushed. The MS-20 does not
sound "warm" — it screams. The original (Korg 35) filter distorts hard at high
resonance in a way the later (Korg 135) revision does not.

### What it changed
Acid, industrial, electro and modern techno leads. Aphex Twin, Daft Punk, Nine
Inch Nails, Boards of Canada.

**Rebuild:** band-pass by putting a resonant HPF *before* a resonant LPF, both
12 dB/oct, both with resonance at 60–80%, and drive between them.

---

## Roland SH-101 (1982)

**Type:** single-VCO monosynth with a sub-oscillator, arpeggiator and a
100-step sequencer. Cheap, portable (it had a guitar strap and a handgrip).

### Signal path
```
VCO (saw + pulse/PWM, mixable) + SUB-OSC (square, -1 or -2 octaves) + noise
  → 24 dB/oct LPF (resonant, self-oscillating)
  → VCA
1 envelope (ADSR), 1 LFO
```

### The controls that matter
| Control | Effect |
|---|---|
| **Sub-osc level** | The weight; this is why one oscillator sounds huge |
| **Saw + pulse mixed** | Both at once = the classic thick SH bass |
| **Filter env amount + decay** | The plucky attack |
| **PWM by LFO** | The "moving" pad character |

### What it changed
Acid house and techno basslines (as the cheaper 303 alternative), and the
entire "bedroom sequenced dance track" workflow.

**Rebuild:** saw + square-one-octave-down at equal levels, 24 dB LPF, filter
envelope decay 150–300 ms with 50% amount, no sustain. Instant SH-101 bass.

---

## Roland TB-303 Bass Line (1981)

**Type:** single-VCO monosynth with a step sequencer, intended to replace a bass
guitarist for practising guitarists. It failed commercially and was discontinued
in 1984. Second-hand units were cheap. Chicago producers found them.

### Signal path
```
VCO (saw OR square, one at a time) → 18 dB/oct (3-pole) diode ladder LPF → VCA
Envelope: a single decay-based envelope, modulating the filter
Accent: a per-step switch that raises level AND filter envelope AND adds a
        "wow" from a shared power-supply sag
Slide: a per-step switch that ports smoothly to the next note
```

### The controls that matter
| Control | Effect |
|---|---|
| **Cutoff** | The performance control — you play the filter, not the keyboard |
| **Resonance** | Near maximum for the "squelch" |
| **Env Mod** | How much the decay envelope opens the filter |
| **Decay** | How fast it closes again — the length of each "wow" |
| **Accent** | Per-step; changes level, envelope depth and adds compression sag |
| **Slide** | Per-step portamento; makes the line liquid rather than stepped |

### Why it sounds like that
1. **18 dB/octave, not 24.** The 3-pole slope leaves more high end above the
   cutoff, so the resonant peak sits on top of an audible harmonic bed.
2. **The accent circuit is shared with the power supply.** An accented note
   momentarily starves the circuit, producing a level and timbre artefact that
   cannot be separated from the accent.
3. **The envelope is not an ADSR.** It is a single non-linear decay whose shape
   changes with the Env Mod setting.
4. **The sequencer's slide** re-triggers or does not re-trigger the envelope
   depending on context, which creates the characteristic uneven articulation.

### What it changed
**Acid house.** Phuture's "Acid Tracks" (1987) is a 303 being tweaked in real
time. From there: acid techno, psytrance, Hardfloor, the entire Rotterdam and
Detroit acid lineage, and every "303-style" plugin since.

### Rebuild
```
Oscillator: saw (or square), monophonic, 1 voice
Filter:     low-pass, 18 dB/oct if available (else 24 with reduced resonance)
            resonance 55-85%
Filter env: attack 0, decay 100-400 ms, sustain 0, amount 40-90%
Amp env:    attack 0-3 ms, decay/sustain near full (the filter does the shaping)
Accent:     on accented steps, +6 dB level AND +30% envelope amount
Slide:      portamento 60 ms, applied only on slid steps, without retriggering
Post:       overdrive AFTER the filter (this is essential - most of the
            recognisable "acid" aggression is distortion, not the synth)
Perform:    automate the cutoff continuously; the pattern stays fixed
```
**The pattern is not the sound.** A 303 line is 16 fixed steps with the cutoff,
resonance and env-mod knobs being moved for four minutes.

---

## EMS VCS3 / Synthi AKS (1969/1971)

**Type:** briefcase modular with a **pin matrix** instead of patch cables.

Three oscillators (with unusually wide ranges), a ring modulator, a
distinctive 18 dB/oct filter that self-oscillates beautifully, spring reverb,
and a joystick. Notoriously unstable tuning — which is why it was used more for
texture than for melody.

Used on: Pink Floyd's *Dark Side of the Moon*, Roxy Music, Brian Eno, the Doctor
Who theme's later arrangements, Aphex Twin.

**Rebuild:** the sound is unstable pitch plus ring modulation plus spring reverb.
Add ±20 cents of slow random drift to everything and put a short, boingy spring
reverb across the output.

---

## Related

- Filter theory: `../00-foundations/12-timbre-and-synthesis.md`
- Bass design: `../00-foundations/09-bass.md`
- Acid patch: `14-iconic-patch-recipes.md`
