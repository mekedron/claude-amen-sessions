# Analog Polysynths

Polyphony plus patch memory turned the synthesiser from a specialist instrument
into the sound of popular music.

---

## Sequential Circuits Prophet-5 (1978)

**Type:** 5-voice analog polysynth. **The first fully programmable polysynth** —
you could save a patch and recall it. That single feature changed live
performance and studio work permanently.

### Signal path (per voice)
```
OSC A (saw/pulse, PWM) + OSC B (saw/tri/pulse, detunable, can be an LFO)
  → Mixer (+ white noise)
  → 24 dB/oct low-pass filter (resonant, self-oscillating)
  → VCA
2 ADSR envelopes (filter, amplifier), 1 LFO, plus the POLY-MOD section
```

### The controls that matter
**Poly-Mod** is the reason this synth sounds different from its imitators: it
routes **Oscillator B** and the **filter envelope** to Oscillator A's frequency,
Oscillator A's pulse width, and the filter cutoff — per voice. That gives you
per-voice FM and per-voice sync sweeps in a polyphonic instrument.

| Setting | Result |
|---|---|
| Osc B → Osc A freq (Osc B at audio rate) | Polyphonic FM; metallic, bell-like |
| Filter env → Osc A freq, with Osc A synced to B | The classic "sync sweep" lead |
| Osc B (low frequency) → PWM | Lush, moving pads |

### Revisions
Rev 1/2 used SSM chips, Rev 3 used CEM — Rev 3 is more stable and slightly
cleaner; Rev 1/2 are considered "fatter". The instability *is* the character.

### What it changed
The 1980s. Everything from Michael Jackson to Kraftwerk to Talking Heads to
Duran Duran to Radiohead. It is the default "warm analog polysynth" reference.

### Rebuild
```
2 saws, detune 6-12 cents, one with PWM from a 0.3 Hz LFO
24 dB LPF, resonance 15-30%
Filter env: attack 5 ms, decay 800 ms, sustain 40%, amount 45%
Amp env:   attack 10-300 ms depending on pad vs stab, release 400 ms
Per-voice random detune of ±4 cents (this is what "analog polysynth" means)
```

---

## Roland Jupiter-8 (1981)

**Type:** 8-voice analog flagship.

Two VCOs per voice with **cross-modulation** and **sync**, a low-pass filter
switchable between 12 and 24 dB/oct, a separate **high-pass filter**, and a
split/dual keyboard mode. Bright, glassy, hi-fi — noticeably cleaner than a
Prophet or an Oberheim.

Key features: the HPF (thinning a pad without touching the LPF), the 12/24 dB
switch (12 dB = softer, more "string-like"), and the arpeggiator.

Heard on: Duran Duran, Michael Jackson's *Thriller*, Howard Jones, Vangelis, and
almost all modern "80s revival" production.

**Rebuild:** two saws detuned 8 cents, 12 dB/oct LPF, high-pass at 150–250 Hz,
slow LFO to PWM, chorus, and a long release.

---

## Roland Juno-106 (1984)

**Type:** 6-voice, **one DCO per voice**, and the most-loved cheap polysynth
ever made.

### Signal path
```
DCO (saw and/or pulse with PWM, both mixable) + SUB-OSC (square, -1 oct) + noise
  → HPF (a 4-position slider, non-resonant)
  → 24 dB/oct resonant LPF
  → VCA → BBD CHORUS (I, II, or I+II)
1 ADSR, 1 LFO
```

### Why it sounds like that
1. **DCOs are digitally clocked**, so they never drift — the Juno is always in
   tune, which is why its chords sound "clean" rather than "fat".
2. **The chorus is a bucket-brigade delay** with audible noise and a specific
   modulation depth. Chorus I is subtle, Chorus II is wide and fast, both
   together is unstable and enormous. **The chorus is the instrument.** Bypass
   it and a Juno sounds thin and ordinary.
3. **One oscillator plus a sub** means the low end comes from the square sub, not
   from detuning.

### What it changed
Every 80s pad, and then house, techno, synthwave, chillwave, and modern indie.
It is the default "warm nostalgic pad" of the last twenty years.

### Rebuild
```
1 saw + 1 square one octave down at 50% level
HPF at 100-200 Hz (a fixed cut, not resonant)
24 dB LPF, resonance 10-25%
Attack 200-600 ms, sustain full, release 600 ms-1.5 s
CHORUS: two delay lines at 20-30 ms modulated at ~0.5 Hz (I) and ~2 Hz (II),
        depth ~5 ms, mixed 50/50, with a little noise added
```

---

## Oberheim OB-Xa / OB-8 (1980/1983)

**Type:** 8-voice analog. Big, brassy, aggressive.

Two VCOs per voice, a filter switchable between 12 and 24 dB/oct, and — the
Oberheim signature — **unison mode**, stacking all eight voices on one note with
detune. That is the sound of Van Halen's "Jump" and Rush's "Subdivisions".

Character: fatter and more mid-forward than a Jupiter; the 12 dB filter setting
is what gives it that "horn section" quality.

**Rebuild:** stack 6–8 saw voices on a single note, detune spread ±15 cents,
12 dB/oct LPF with a fast, deep filter envelope. Play block chords with heavy
attack.

---

## Yamaha CS-80 (1977)

**Type:** 8-voice, two complete synth layers per voice, **polyphonic
aftertouch**, and a weighted ribbon controller. 100 kg of it.

Unique features:
- **Polyphonic aftertouch**: pressing harder on one key in a chord changes only
  that note's brightness and level. Almost nothing else has ever had this.
- **The ribbon controller** for continuous pitch bends across the whole keyboard.
- Two independent layers (each with HPF and LPF) detunable against each other.

The Blade Runner soundtrack is a CS-80. So is much of Vangelis's work; also Toto,
Keith Emerson, and modern film scorers who use its emulations.

**Rebuild:** two detuned layers, each with its own filter; map aftertouch (or
per-note expression) to cutoff *and* level; add a slow ribbon-style pitch bend
of ±2 semitones on sustained notes; heavy chorus/ensemble.

---

## Korg Polysix (1981)

6-voice, one VCO plus sub, with built-in chorus/phase/ensemble effects and an
arpeggiator. Cheaper than a Prophet and consequently everywhere in early-80s
British synth-pop. Its **ensemble** effect is wider and more chaotic than a
Juno's chorus.

---

## Roland JX-3P / MKS-70 / Alpha Juno (1983–1986)

The JX series was Roland's "digital control, analog voice" line. The **Alpha
Juno-1/2 (1986)** matters for one reason: its factory patch **"What The"**,
a detuned pulse-wave stack with a downward pitch sweep and heavy chorus, became
the **hoover** — the defining sound of rave, hardcore and hardstyle. See
`14-iconic-patch-recipes.md`.

---

## String machines: Solina / ARP String Ensemble (1974)

Not a synth: a divide-down organ with a fixed voice and a **three-phase BBD
chorus**. Every note sounds at once from a single top-octave oscillator divided
down, so it is fully polyphonic with zero voice cards.

That chorus — three modulated delay lines at different rates — is the "string
machine" sound: Pink Floyd, Joy Division, Air, and the whole of ambient and
synthwave.

**Rebuild:** a saw wave with every note running continuously, through three
delay lines (15–25 ms) modulated at 0.4, 0.9 and 1.6 Hz with opposite phases,
mixed together. Add a slow attack and a gentle low-pass.

---

## What to take from this family

| Want | Use the model of |
|---|---|
| Fat, drifting, aggressive | Prophet-5, OB-Xa (many voices, wide detune, 12 dB filter) |
| Clean, glassy, hi-fi 80s | Jupiter-8 (DCO-stable, HPF, 24 dB filter) |
| Warm, nostalgic, simple | Juno-106 (one osc + sub + chorus) |
| Expressive, cinematic | CS-80 (per-note pressure, two layers, ribbon) |
| Huge unison lead | OB-Xa unison (8 voices on one note) |
| Lush strings | Solina (divide-down + triple chorus) |

**The common thread:** in every case the character comes from *instability* —
drift, chorus noise, filter non-linearity, per-voice variation. A digitally
perfect recreation sounds sterile. Add per-voice random detune (±3–8 cents),
per-voice random filter offset (±3%), and slow drift, and generic oscillators
start sounding like these machines.

## Related

- Voice-leading polysynth chords: `../00-foundations/07-voice-leading.md`
- Chorus and ensemble: `13-effects-and-processors.md`
