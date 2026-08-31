# Virtual Analog and the 1990s

Digital machines that modelled analog behaviour in real time — and in doing so
invented sounds analog synths had never made.

---

## Roland JP-8000 / JP-8080 (1996/1998) — the Supersaw

**Type:** virtual analog polysynth. Its historical importance rests almost
entirely on one oscillator waveform.

### The Supersaw
A single oscillator setting that generates **seven detuned sawtooth waves**
internally, with two dedicated controls:

| Control | Effect |
|---|---|
| **Detune** | The spread of the seven saws — but on a *non-linear* curve: the outer pairs spread much further than the inner ones |
| **Mix** | The level of the six side saws relative to the centre saw |

The detune curve is the secret. The seven saws are not evenly spaced; the
distribution (roughly: centre, then ±small, ±medium, ±large in an accelerating
curve) plus the fact that each has a random start phase produces a sound that is
simultaneously wide, thick and still pitched.

### What it changed
**Trance.** Every uplifting trance lead from 1998 onwards, plus hardstyle
screeches, festival EDM leads, hands-up, and eventually future bass chords.
It is probably the single most-imitated waveform in electronic music.

### Rebuild
```
7 sawtooth oscillators
Detune offsets in cents, scaled by a "detune" parameter d (0..1):
    0, ±(d·10), ±(d·22), ±(d·38)          # accelerating spread, not linear
Random start phase per oscillator (essential - otherwise they cancel)
Levels: centre saw at 1.0, the six others at 0.4-0.8 ("mix")
Pan: centre saw centred, the pairs spread progressively outward
Then: high-pass at 200-300 Hz, low-pass at 8-14 kHz
Add a square or sine an octave down for weight
PLAY AT MOST 3 NOTES - a 5-note supersaw chord is 35 oscillators of mud
```

---

## Access Virus (1997–)

**Type:** German virtual analog, progressively expanded across models (A, B, C,
TI). Three oscillators, two filters with several models, a deep modulation
matrix, and — crucially — **on-board effects** (distortion, chorus, phaser,
delay, reverb, ring mod) as part of the patch.

### Why it matters
The Virus is the sound of **trance, neurofunk drum & bass, and 2000s
electronica**: aggressive, complex, modulated, and very loud in the mid-range.
Its **HyperSaw** (its supersaw variant) and its ability to modulate almost
anything from anything made it the sound-design instrument of a generation.

Neurofunk bass design in particular — modulated, screaming, formant-shifted —
was largely developed on Virus hardware before Massive and Serum existed.

**Rebuild:** wavetable or multi-saw oscillators → a resonant multimode filter →
a saturation stage → a phaser → a short delay, with 3–4 LFOs assigned to
oscillator mix, filter cutoff, phaser rate and pan.

---

## Clavia Nord Lead (1995)

**Type:** the first commercially successful virtual analog synth, in a bright red
case with a knob for every function.

Its importance is conceptual: it proved that a DSP model of an analog synth was
good enough, cheap enough and *more reliable* than the real thing. Everything in
this file follows from it.

Character: clean, bright, slightly clinical — much less "warm" than the analogs
it modelled, which made it excellent for cutting leads.

---

## Novation Bass Station / Supernova / Nova (1993–2000)

- **Bass Station** (1993) — an affordable analog-modelled mono; acid and
  bass duties.
- **Supernova / Supernova II** (1998/2000) — massively multitimbral VA with
  per-part effects. Its huge detuned pads and leads are the sound of late-90s
  trance and big-beat.

---

## Korg MS2000 / microKORG (2000/2002)

VA with a built-in **vocoder** and a step arpeggiator. The microKORG's
affordability and its vocoder put that sound into indie, electro-pop and
bedroom production for a decade.

---

## Waldorf Q / Micro Q (1999)

Wavetable-plus-VA hybrid with a distinctive digital edge; heavily used in
trance, industrial and IDM.

---

## Grooveboxes: Roland MC-303 / MC-505 / Korg Electribe

**Type:** all-in-one sequencer + sound module + effects, designed to make a
dance track in one box.

- **MC-303** (1996) — mediocre sounds, but it introduced a generation to
  pattern-based composition and to the idea that you could make techno on a
  £500 box.
- **Korg Electribe** series (1999–) — ER-1 (analog-modelled drums), EA-1
  (analog-modelled synth), ES-1 (sampler); knob-per-function, immediate,
  performance-oriented. A huge influence on minimal techno and electro.

Their real legacy is the **workflow**: 16 steps, knobs, instant pattern
switching, and effects you perform with.

---

## Yamaha QY / Roland W-30 / Akai MPC — the "one box" tradition

The 90s bedroom producer's setup was often a single sequencer-sampler. That
constraint shaped jungle, hardcore and early UK garage: limited polyphony,
limited memory, so **every element had to earn its place** — which is why those
records are sparse and hit hard.

---

## Korg Kaoss Pad (1999)

**Type:** an XY touchpad controlling an effects processor (and later, sample
playback).

Why it matters: it made **effects a performance instrument**. Filter, delay,
pitch, gate, loop — all controlled by dragging a finger. Its influence runs
through live electronic performance, glitch, dubstep, and the whole idea of
"the effect as the arrangement".

**Rebuild:** map two continuous parameters (typically filter cutoff and delay
feedback, or grain size and pitch) to a 2D control, and automate a path through
that space over a section.

---

## The 1990s lesson

The decade's instruments made two lasting contributions:

1. **The supersaw** — a single waveform that carries an entire genre.
2. **Effects as part of the patch.** Before the Virus and the D-50, effects were
   separate rack units applied to a finished sound. Once distortion, chorus,
   delay and reverb became part of the preset, sound design and mixing merged.
   That is the modern norm: a Serum patch includes its own reverb and its own
   distortion, and the "sound" is the whole chain.

## Related

- The supersaw recipe in detail: `14-iconic-patch-recipes.md`
- Trance: `../20-genres/03-trance.md`
- Neurofunk bass: `../20-genres/04-drum-and-bass.md`
