# Wavetable, Vector and LA Synthesis

The bridge between analog warmth and digital strangeness: machines that store
waveforms and move between them.

---

## PPG Wave 2.2 / 2.3 (1982/1984)

**Type:** the first commercially significant **wavetable** synthesiser. German,
expensive, and the source of a timbre nobody had heard before.

### How it works
A **wavetable** is a table of 64 single-cycle waveforms. An oscillator reads one
of them; a modulation source (envelope, LFO, key position, or the mod wheel)
sweeps the **wavetable position**, morphing continuously from one waveform to
the next.

The PPG's waveforms were stored at **8-bit resolution** and its interpolation
between adjacent waves was crude, which produces a characteristic **glassy,
grainy, slightly aliased** sound. Analog filters (SSM) sat after the digital
oscillators, so it is a digital-source/analog-filter hybrid.

### The controls that matter
| Control | Effect |
|---|---|
| **Wavetable select** | Which family of 64 waves |
| **Wave position** | Where in the table you are — the primary timbre control |
| **Envelope → wave position** | The sound morphs as the note evolves |
| **LFO → wave position** | Continuous shimmer |
| **Analog filter** | Tames the digital harshness |

### What it changed
The 80s "digital but organic" palette: Depeche Mode, Tangerine Dream,
Thomas Dolby, Rush, Trevor Horn productions. And it is the direct ancestor of
Massive, Serum and Vital — the dominant architecture in modern electronic music.

**Rebuild:** build a table of 8–64 single-cycle waveforms that vary
progressively (sine → saw → harmonically complex → noisy). Reduce them to
8-bit. Interpolate linearly (not smoothly) between adjacent waves. Sweep the
position with an envelope. Follow with a resonant analog-style low-pass.

---

## Waldorf Microwave (1989) / Microwave XT (1998) / Blofeld

PPG's continuation. The original Microwave uses the PPG wavetables with analog
filters (Curtis chips); the XT is fully digital with a famous
knob-per-function orange panel.

The XT's **"wavetable + analog-modelled filter + heavy modulation"** approach is
the sound of a lot of trance, D&B and electronica from 1998–2005.

---

## Sequential Prophet VS (1986) — Vector synthesis

**Type:** four digital oscillators, each assigned to a corner of a square, with a
**joystick** mixing between them — and the joystick movement can be **recorded
and looped** as an envelope.

That is vector synthesis: a timbre that travels a path through four sound
sources over time.

Only about 3,000 were made, but the idea outlived the machine: it went into the
Yamaha SY22/TG33 and, most importantly, the Korg Wavestation.

**Rebuild:** four oscillators with different waveforms; two crossfade
parameters (X and Y) driven by a looping multi-segment envelope; the four
levels are `(1−x)(1−y)`, `x(1−y)`, `(1−x)y`, `xy`.

---

## Korg Wavestation (1990) — Wave sequencing

**Type:** vector synthesis plus **wave sequencing**, which is the real
innovation.

### Wave sequencing
Instead of one waveform per oscillator, you define a **list of waveforms with
individual durations and crossfade times**. The oscillator steps through them.

| Setting | Result |
|---|---|
| Short durations, no crossfade | A rhythmic pattern — the sound has a built-in groove |
| Long durations, long crossfades | A slowly evolving pad that never repeats |
| Durations synced to tempo | Wave sequences as arpeggios and rhythm parts |

This is why Wavestation pads sound alive in a way sampled pads do not: the
timbre is a *sequence*, not a static snapshot.

Heard on: Depeche Mode, film and TV scores of the 90s, and the enormous
"Ka Waves" / "Motion Pad" style of ambient-trance pad.

**Rebuild:** define a list of 4–16 short samples or single-cycle waves; step
through them with per-step durations of 30–500 ms and crossfades of 10–100%;
layer four such sequences and vector between them with a slow looping envelope.

---

## Roland D-50 (1987) — Linear Arithmetic (LA)

**Type:** the machine that beat the DX7, using a genuinely clever shortcut.

### The insight
**The identity of an instrument lives in its attack transient**, not its
sustain. So: use a **short digital PCM sample for the attack** (a few hundred
milliseconds — a struck string, a breath, a mallet) and a **synthesised
subtractive waveform for the sustain**. You get realism where it matters, at a
fraction of the memory cost.

### Architecture
```
Partial 1: PCM attack transient  ┐
Partial 2: synth (saw/pulse) + TVF (filter) + TVA  ├→ mixed → onboard chorus → onboard reverb
(×2 tones, so up to 4 partials per voice)          ┘
```

The D-50 was also **the first synth with built-in digital effects**, and its
chorus and reverb are a big part of why the presets sound finished.

### The presets that mattered
**"Fantasia"**, **"Digital Native Dance"**, **"Soundtrack"**, **"Pizzagogo"** —
these are on an enormous number of late-80s records, film scores and TV themes.
Enya, Jean-Michel Jarre, Vangelis-adjacent production, and the whole
"new age / 80s dream" aesthetic.

**Rebuild:** layer a short, bright, noisy attack sample (10–300 ms — a mallet, a
breath, a pluck, a metallic tick) over a warm sustained synth pad that has
almost no attack of its own. Add chorus and a large bright reverb. That is 90%
of the D-50 formula, and it works with any sound.

---

## Ensoniq ESQ-1 / SQ-80 (1986/1987)

Digital wavetable-ish oscillators (a set of fixed waveforms and short samples)
through **analog Curtis filters**, with a genuinely powerful modulation matrix
and a sequencer. Cheap, characterful, and popular in early industrial and
electronic music.

---

## Modern wavetable — the lineage

| Instrument | Notes |
|---|---|
| **NI Massive** (2007) | Wavetable oscillators + a very musical filter section; the sound of dubstep and 2010s EDM |
| **Xfer Serum** (2014) | Visual wavetable editing and import; drag-and-drop modulation; high-quality anti-aliased oscillators; the current standard |
| **Vital** (2020) | Free, spectral wavetable editing, similar workflow to Serum |
| **Kilohearts Phase Plant** (2019) | Modular: stack any number of wavetable, sample, noise and analog generators |
| **Ableton Wavetable** (2018) | Built-in, clean, two wavetable oscillators with sub |
| **Waldorf Iridium / Quantum** | Modern hardware wavetable with granular and resonator engines |

### What to do with a wavetable that you cannot do otherwise
1. **Envelope the position** so the timbre evolves like a physical sound.
2. **LFO the position slowly** for pads that never settle.
3. **Modulate the position at audio rate** — this is a form of FM and produces
   growls and screams (the dubstep bass technique).
4. **Import your own wavetables** from any audio: a vocal, a field recording, a
   rendered synth line. A wavetable made from a voice keeps its formants.
5. **Use position + unison detune together**: each unison voice reads a slightly
   different table position, producing a chorus that is timbral rather than
   pitch-based.

## Related

- Synthesis theory: `../00-foundations/12-timbre-and-synthesis.md`
- Modern software: `12-software-instruments.md`
- Growl design: `../30-patterns/08-sound-design-recipes.md`
