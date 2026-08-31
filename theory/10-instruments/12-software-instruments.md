# Software Instruments

From 1996, the studio moved inside the computer. These are the plugins that
changed what music sounded like — not merely what it cost to make.

---

## The turning points

| Year | Event | Consequence |
|---|---|---|
| 1996 | Steinberg opens the **VST** format (and ships **Neon**, the first VST instrument) | Third-party instruments inside a DAW |
| 1997 | **ReBirth RB-338** (Propellerhead) | A software 303 + 808 + 909; an entire generation learns acid without hardware |
| 1997 | **FruityLoops** | Pattern-based production for people who never read a manual |
| 1998 | **Reaktor** (NI) | A modular environment where the instrument itself is the project |
| 2001 | **Ableton Live** | Non-linear, clip-based composition and performance |
| 2002 | **Kontakt** | Sample libraries become scriptable instruments |
| 2007 | **Massive**, **Sylenth1** | The sound of the next decade of dance music |
| 2008 | **Omnisphere** | Hybrid sample+synth for film and texture |
| 2014 | **Serum** | Visual wavetable design; the current default |
| 2020 | **Vital** | A free, spectral-editing equivalent |

---

## Native Instruments Reaktor (1996)

Not an instrument but a **modular construction environment**. Its importance:
- Instruments are built from primitives (oscillators, filters, logic, DSP
  blocks) and shared as files — a huge public library exists.
- **Ensembles** like *Monark*, *Razor* (additive, with visually drawn spectra),
  *Form* and *Blocks* (a Eurorack-style environment) each define their own
  niches.
- **Razor** in particular — pure additive synthesis with hundreds of partials
  controlled by "filters" that are really spectral shapers — produces
  dissonance-free, aliasing-free sounds impossible in subtractive synthesis.
  Heavily used in neurofunk and modern bass music.

---

## Native Instruments Massive (2007)

**Type:** wavetable synth with two main oscillators, a noise source, two
filters (serial/parallel/mixed) and a very direct modulation system (drag a
handle from a source onto any knob).

### Why it defined a decade
- **The wavetables are aggressive.** Their spectral jumps make it easy to get
  bright, complex, mid-heavy sounds that survive a club system.
- **Modulating wavetable position at audio rate** produces the growl.
- **The performer section** (looped stepped modulators) allows rhythmic timbre
  changes synced to tempo — the wobble.
- **Feedback and "insert effects"** inside the voice path add distortion and
  ring modulation before the filters.

**It is the sound of dubstep, brostep and 2010–2015 EDM.** Skrillex-era bass
design is largely Massive plus resampling.

### Rebuild a Massive-style growl
```
Oscillator 1: wavetable with strong spectral variation, position modulated by
              a fast LFO (20-80 Hz) or by a stepped sequencer at 1/16
Oscillator 2: same table, detuned 12-20 cents, position offset
Insert:       hard sync or ring mod between them
Filter:       resonant low-pass, cutoff modulated by a tempo-synced stepped LFO
Distortion:   after the filter
Resample the result, then process again (see below)
```

---

## LennarDigital Sylenth1 (2007)

**Type:** a virtual-analog synth with four oscillator "units" (each up to 8
unison voices), two filters and a straightforward modulation matrix.

Its reputation rests on **oscillator and filter quality at low CPU cost**: the
unison detune sounds smooth rather than harsh, and the filters are musical.
It became the default trance, progressive house and EDM synth for a decade —
plucks, supersaw leads, and chord stacks.

**Rebuild:** the essential Sylenth move is 8-voice unison per oscillator with
moderate detune and a wide stereo spread, two such oscillators an octave apart,
gentle low-pass, and a short filter envelope for plucks.

---

## reFX Nexus (2007)

**Type:** a **ROMpler** — no synthesis controls to speak of, only presets and
effects.

Its historical role is honest and worth stating: it made professional-sounding
EDM leads, plucks and stabs available with no sound-design knowledge, which
accelerated the 2008–2014 EDM boom and simultaneously homogenised it. If a
festival record from that era has a lead you have heard elsewhere, this is often
why.

**The lesson:** a preset is a starting point. Presets used unmodified are the
fastest route to sounding like everyone else.

---

## Xfer Records Serum (2014) — the current standard

**Type:** wavetable synth with a **visual editor for everything**.

### Why it took over
| Feature | Why it matters |
|---|---|
| **Wavetable editing and import** | Draw a waveform, import audio, or generate a table from a formula. Any sound becomes an oscillator |
| **High-quality anti-aliased playback** | You can modulate the position fast without digital garbage |
| **Drag-and-drop modulation** | Any source onto any parameter, with visible depth rings |
| **Warp modes per oscillator** | Sync, bend, PWM, FM, RM, mirror, remap — a second layer of timbre control before the filter |
| **Noise oscillator with any sample** | Layer texture inside the voice |
| **Built-in effects with modulation** | The patch includes its distortion, reverb, delay, compression |
| **LFOs drawable and tempo-synced** | The rhythm of the timbre is drawn, not approximated |

### The techniques Serum made standard
1. **Resampling chains.** Design a sound, render it, import it as a wavetable,
   design again. Two or three passes produce timbres no synth can make directly.
2. **Wavetable position as the primary melody.** In a lot of modern bass music
   the *pitch* barely changes; the position and the filter do the moving.
3. **Audio-rate modulation of the position** for growls and screams.
4. **Custom wavetables from vocals** — the formants survive and the result
   sounds like a talking synth.

---

## Vital (2020)

Free, and architecturally close to Serum, with **spectral wavetable editing**
(morph a table in the frequency domain) and a clean modulation workflow. For an
agent generating music, its relevance is that its concepts and terminology are
the modern lingua franca and its file formats are open.

---

## Kilohearts Phase Plant (2019)

**Type:** a **modular** semi-modular: you stack generators (analog, wavetable,
sample, noise) and insert effects anywhere in the voice path, in any order,
with any number of them.

It represents the current direction of travel: the distinction between
"synthesiser" and "effects chain" has dissolved.

---

## u-he: Diva, Zebra2, Repro, Hive

- **Diva** (2011) — circuit-level modelling of classic analog filters and
  oscillators (Minimoog, Jupiter, MS-20, and more, mixable). It is CPU-expensive
  because it actually simulates the non-linearities. The best available answer to
  "make it sound analog".
- **Zebra2** — semi-modular, and the film-score workhorse (Hans Zimmer's team
  used it extensively on *Inception*, *The Dark Knight* and much else). Its
  strength is complex evolving textures.
- **Repro-1/5** — SH-101 and Prophet-5 models.
- **Hive** — fast, clean, EDM-oriented.

---

## Spectrasonics Omnisphere (2008)

**Type:** a hybrid of an enormous sample library and a full synthesis engine,
with granular processing and thousands of curated "psychoacoustic" sources
(including recordings of unusual objects).

Its role is texture and cinematic sound design rather than classic synth duties.
Also **Trilian** (bass) and **Keyscape** (electromechanical keyboards).

---

## Image-Line: Sytrus, Harmor, Gross Beat

- **Sytrus** — FM + ring modulation + subtractive, with per-operator filters.
  Very deep; the source of a lot of early hardstyle and psytrance sound design.
- **Harmor** — **additive resynthesis**: it converts audio into partials, then
  lets you filter, pitch, blur and reshape in the frequency domain. Time-stretch
  and pitch-shift become free and artefact-free, and "impossible" transformations
  are ordinary.
- **Gross Beat** — a real-time time and volume manipulator with 36 slots. It is
  responsible for the **stutter, gate, and pitch-drop effects** of trap and
  modern EDM; the "time" curves let you scratch, freeze and reverse audio on a
  bar grid.

---

## Ableton's built-ins (as ideas, not products)

| Device | Idea worth stealing |
|---|---|
| **Operator** | Compact 4-op FM — enough for most FM duties |
| **Wavetable** | Two tables plus sub, with a clean mod matrix |
| **Simpler / Sampler** | Warp modes; the "Beats" mode's transient slicing is a whole workflow |
| **OTT (a Multiband Dynamics preset)** | **Multiband *upward* compression** — it raises quiet parts in three bands. This is the single most recognisable modern EDM processing move; it makes a sound dense, bright and "finished", and overusing it flattens everything |
| **Max for Live** | Build the device you actually need |

---

## Effects plugins that changed sounds (see also `13-effects-and-processors.md`)

| Plugin | Contribution |
|---|---|
| **Auto-Tune** / **Melodyne** | Pitch as an editable, and abusable, parameter |
| **Soundtoys** EchoBoy, Decapitator, Crystallizer | Character effects modelled on hardware |
| **Valhalla** VintageVerb, Shimmer, Supermassive | Reverb as a compositional space; Shimmer defined modern ambient |
| **FabFilter** Pro-Q, Pro-C, Saturn | Precise, visual, transparent mixing tools |
| **iZotope** Ozone, RX | Mastering assistance and audio repair/restoration |
| **Camel Crusher**, **Ohmicide**, **Trash** | Multiband distortion — the core of bass music |
| **Paulstretch** | Extreme time-stretching; ambient from any source |
| **Portal / Thermal (Output)**, **Effectrix**, **ShaperBox** | Rhythmic, granular and gated effects as arrangement tools |

---

## How to use this knowledge without the plugins

Every technique above reduces to a signal path:

| "The sound of…" | The actual chain |
|---|---|
| Modern EDM chords | Detuned wavetable/saw stack → multiband upward compression → wide reverb → sidechain duck |
| Dubstep growl | Wavetable, position modulated at audio rate → distortion → resonant filter with a stepped LFO → resample → repeat |
| Trance lead | 7-saw supersaw → high-pass 250 Hz → unison spread → dotted-8th delay → big reverb |
| Ambient shimmer | Source → reverb with a +12 semitone pitch shift in the feedback path → low-pass → long decay |
| Trap stutter | Beat-repeat/time-warp on a bar grid, with pitch falling during the repeat |
| Lo-fi warmth | Bit reduction → sample-rate reduction → low-pass at 8 kHz → tape wow → saturation |
| Neuro bass | FM/additive source → multiband split → per-band distortion and formant filtering → recombine → resample |

## Related

- The theory: `../00-foundations/12-timbre-and-synthesis.md`
- Concrete recipes: `../30-patterns/08-sound-design-recipes.md`, `14-iconic-patch-recipes.md`
