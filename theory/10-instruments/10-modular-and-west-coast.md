# Modular and West Coast Synthesis

Two philosophies emerged in the 1960s and never merged. Knowing the difference
is the fastest route to sounds that do not sound like everyone else's.

---

## East Coast (Moog) vs West Coast (Buchla)

| | East Coast — Moog, ARP, Roland | West Coast — Buchla, Serge |
|---|---|---|
| **Method** | Start bright, **subtract** with a filter | Start simple, **add** complexity by folding and modulating |
| **Interface** | Keyboard | Touch plates, sequencers, random voltage |
| **Core module** | VCF (resonant low-pass) | **Wavefolder** and **low-pass gate** |
| **Timbre control** | Filter cutoff | Timbre/index of a complex oscillator |
| **Amplitude** | VCA (linear) | **Low-pass gate** — level and brightness fall together |
| **Musical result** | Playable, tonal, familiar | Percussive, organic, unpredictable |
| **Genres** | Everything popular | Ambient, experimental, sound design, modern electronic |

### The wavefolder
Instead of removing harmonics with a filter, a **folder** adds them by reflecting
the waveform back on itself when it exceeds a threshold:

```
out = sin(g · π/2 · clip(x, -2, 2))     # a simple sine folder
```

Raising the fold amount on a sine produces increasingly complex, **inharmonic**
spectra that no filter can create. It is bright without being buzzy — the
characteristic "west coast" bell-metallic quality.

### The low-pass gate (LPG)
A vactrol-based circuit that acts as a filter and an amplifier at once: as it
closes, the sound gets both **quieter and darker**, with a slow, non-linear
"bounce" from the vactrol's response.

This is why west-coast percussion sounds like struck physical objects: real
objects lose high frequencies as they decay. An ordinary VCA does not do this.

**Rebuild the LPG:** apply an envelope to **both** the amplitude and a low-pass
cutoff simultaneously, with the cutoff following a slightly slower, non-linear
version of the amplitude curve (e.g. `cutoff = 200 + 8000 · env^1.6`, with the
envelope having a 20–80 ms exponential decay and a slight lag).

---

## Moog modular (1964)

Bob Moog's system established the vocabulary everything else uses: **VCO, VCF,
VCA, envelope generator, LFO**, all connected with 1V/octave control voltage.

Wendy Carlos's *Switched-On Bach* (1968) proved a synthesiser could make music
people wanted to hear, and it is monophonic multitracking — every voice recorded
separately.

---

## Buchla 100/200 (1963–)

Don Buchla refused keyboards, considering them a limitation imported from the
past. Instead: **touch-sensitive capacitance plates**, sequencers, and sources
of randomness.

Key modules and their ideas:
| Module | Idea |
|---|---|
| **259 Complex Oscillator** | Two oscillators, one modulating the other, with a wavefolder — a whole voice in one module |
| **292 Low Pass Gate** | See above |
| **266 Source of Uncertainty** | Structured randomness: fluctuating voltages, quantised random, sample & hold |
| **281 Function Generator** | Envelopes that can loop, becoming LFOs |

Morton Subotnick's *Silver Apples of the Moon* (1967) is the canonical Buchla
record and still sounds unlike anything else.

---

## Serge (1974)

Modules designed to be patched in unconventional ways — most can act as
oscillator, filter, envelope or slew depending on how they are used. The
"patch-programmable" philosophy: the distinction between audio and control is
deliberately blurred.

---

## Eurorack (1995–)

Doepfer's small, cheap format opened modular synthesis to a mass market. There
are now thousands of modules from hundreds of makers.

Modules whose *concepts* are worth stealing, whatever tools you use:

| Module | Concept | How to apply it anywhere |
|---|---|---|
| **Make Noise Maths** | A function generator that is an envelope, LFO, slew, and mixer at once, with looping and end-of-cycle triggers | Use one modulation source to drive several destinations at different scalings |
| **Mutable Plaits** | A dozen synthesis models (analog, FM, wavetable, granular, physical, drums) with the same three controls | Design a sound with only "harmonics / timbre / morph" and see how far it gets you |
| **Mutable Rings** | Modal/physical resonator — excite it with anything | Feed noise or drums into a resonant bank tuned to a chord |
| **Mutable Clouds** | Granular texture processor | Freeze and stretch any incoming audio into a pad |
| **Make Noise Morphagene** | Tape-splicing granular | Reorder and vary-speed slices in real time |
| **Turing Machine** | A looping shift register that can be made more or less random | Generate melodies that repeat but occasionally mutate |
| **Quantizers** | Force any voltage into a scale | Random modulation that is always in key |
| **Clock dividers/multipliers** | Polyrhythm generation | Run layers at /3, /5, /7 of the clock |

---

## What modular thinking gives a composer

Even with no hardware, three habits transfer:

1. **Modulate everything from everything.** In a modular there is no distinction
   between an LFO, an envelope and an audio signal; any output can go to any
   input. Try envelope → LFO rate, audio → filter cutoff, random → note length.

2. **Use feedback.** Route an output back into an earlier stage. Delay feedback
   into a filter into distortion into the same delay produces sounds no preset
   contains. Keep a limiter after it.

3. **Generate rather than programme.** A clocked random source through a
   quantiser, with a slowly changing probability, will produce melodies for
   hours. Curate the output rather than writing every note. See
   `../20-genres/15-idm-and-glitch.md` for the constraint systems that make this
   musical rather than random.

## Rebuild: a west-coast voice
```
1. Sine oscillator (the "principal")
2. Second sine (the "modulator") at a non-integer ratio (1.47, 2.7, 3.3)
   -> FM the principal, with the index driven by an envelope
3. Wavefolder on the output, fold amount also enveloped
4. LOW-PASS GATE: one envelope drives both amplitude and a low-pass cutoff,
   cutoff = 200 + 8000 * env^1.6, decay 30-300 ms, slight lag on the cutoff
5. Optional: a spring or plate reverb
6. Trigger it from an irregular clock (Euclidean, or random with a quantiser)
```
That patch produces the "modern ambient / generative" percussion-and-bell
palette heard across contemporary electronic music.

## Related

- Synthesis theory: `../00-foundations/12-timbre-and-synthesis.md`
- Generative systems: `../20-genres/15-idm-and-glitch.md`
- Ambient construction: `../20-genres/14-ambient-and-drone.md`
