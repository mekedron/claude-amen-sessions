# FM and Phase Distortion

The 1980s digital revolution. These machines could make sounds no analog synth
could — bells, electric pianos, metallic basses, glass — and they were almost
impossible to programme, which is why their presets became the decade's sound.

---

## Yamaha DX7 (1983)

**Type:** 6-operator FM (technically phase modulation), 16-voice, fully digital.
Over 160,000 sold — it made analog synths temporarily worthless.

### How FM works, practically

An **operator** is a sine oscillator with its own envelope. When operator B
modulates operator A's phase at audio rate, sidebands appear at
`carrier ± n × modulator` for all integer n.

Two numbers control everything:

| Parameter | Effect |
|---|---|
| **Ratio** (modulator freq ÷ carrier freq) | *Which* sidebands appear — the harmonic identity |
| **Index** (modulation depth) | *How many* sidebands, i.e. the brightness |

| Ratio | Result |
|---|---|
| 1:1 | Sawtooth-like harmonic spectrum; electric pianos, basses |
| 2:1 | Square-like, hollow, clarinet |
| 3:1, 4:1 | Bright, brassy, harmonic |
| 1:2, 1:3 | Fundamental-weak, hollow |
| 1:1.41, 1:3.5, 1:7 | **Inharmonic** — bells, metal, glass, gongs |
| 0.5:1 | Sub-octave content |

**The critical insight: envelope the index, not a filter.** The DX7 has no
filter at all. Its sounds evolve because each operator has its own 8-stage
envelope, so the modulator's level (the brightness) falls faster than the
carrier's — exactly like a struck physical object.

### The 32 algorithms
An "algorithm" is a wiring diagram: which operators are carriers (heard) and
which are modulators (unheard), and how they stack.

| Shape | Sound |
|---|---|
| Algorithm 1 (two 3-operator stacks) | Complex, evolving, classic |
| Algorithm 5 (three 2-operator pairs) | Three simple FM voices layered — the E.PIANO topology |
| Algorithm 32 (all six as parallel carriers) | Additive synthesis — organs, pure tones |
| Deep stacks (4+ operators in series) | Aggressive, chaotic, noisy |

**Feedback** on one operator (routing it into itself) turns a sine progressively
into a sawtooth, and then into noise. This is the DX7's only "dirt".

### The controls that matter
| Control | Effect |
|---|---|
| Operator frequency ratio (coarse/fine) | The harmonic identity |
| Operator output level | The index — brightness |
| Operator envelope rates/levels | How the timbre evolves |
| Algorithm | The whole architecture |
| Feedback | Adds harmonics/noise |
| Key scaling | Brightness changes across the keyboard (essential for realism) |
| Velocity → operator level | Harder = brighter, as in real instruments |

### Why it sounds like that
The DX7's 12-bit DAC and its particular sine-table quantisation add a
characteristic grainy "crunch" in the high end, and its envelopes are
exponential in a distinctive stepped way. It is cold, glassy and slightly
brittle — qualities that were mocked in 1995 and prized now.

### What it changed
The entire sound of 1984–1990 pop: the **E.PIANO 1** preset on countless
ballads, **BASS 1** (the "slap bass"), tubular bells, and the marimba/vibraphone
presets. Later: Aphex Twin, Autechre, and modern FM-based bass design.

### Rebuild: the DX7 electric piano
```
Operator pair A (the "tine"):
  carrier ratio 1.0, modulator ratio 1.0 (or 14.0 for the attack "ping")
  modulator envelope: instant attack, decay to zero in 100-300 ms
  carrier envelope:  instant attack, decay 2-4 s
Operator pair B (the body):
  carrier ratio 1.0, modulator ratio 1.0, low index
  slower decay
Velocity -> modulator output level (the harder the strike, the more index)
Add: chorus, a little tremolo/auto-pan, and a plate reverb
```

### Rebuild: an FM bell
```
Carrier 1.0, modulator 1.41 (or 3.5, or 7.0 - non-integer is the point)
Index envelope: instant attack, decay to zero in 300-800 ms
Amp envelope:   instant attack, decay 2-6 s, no sustain
```

### Rebuild: an FM bass
```
Carrier 1.0, modulator 1.0, index ~3 with a 40-80 ms decay to ~0.5
Add a second carrier an octave down for weight
Slight feedback for grit
```

**HAZARD:** FM aliases readily. High index at high pitch folds sidebands back
down as inharmonic noise. Limit the index in the upper register, or oversample.

---

## Yamaha TX81Z (1987) — the "Lately Bass"

**Type:** 4-operator FM, rack-mount, cheap — but with one crucial difference:
its operators can produce **eight waveforms**, not just sines.

Non-sine modulators produce far more sidebands for the same index, so a 4-op
TX81Z can sound richer and dirtier than a 6-op DX7.

Its factory patch **"Lately Bass"** — a hollow, hard, slightly detuned FM bass —
became the bass sound of house, UK garage, jungle and early techno. If a 90s
dance record has a bass that is neither a sub nor a saw but something woody and
metallic, this is usually it.

**Rebuild:** carrier at ratio 1.0 with a **square or "saw-ish" modulator** at
ratio 1.0, index around 2–4 decaying quickly, plus a detuned second layer 7–12
cents away, low-passed around 2 kHz, short envelope.

---

## Casio CZ series (1985) — Phase Distortion

**Type:** Casio's patent-avoiding alternative to FM, sold cheaply (CZ-101,
CZ-1000, CZ-5000).

### How it works
Instead of modulating frequency, PD **warps the phase readout of a sine table**.
Reading the first half of the sine faster and the second half slower turns a
sine progressively into a saw or a square. Sweeping the amount of warping is
equivalent to sweeping a resonant filter — **without having a filter**.

The "resonance" waveforms restart a sine cycle at each period of the
fundamental, producing a hard-synced formant peak that tracks the pitch. That is
why CZ sounds have a distinctive vocal/formant quality.

### Character
Thin, glassy, slightly cheap, with an unmistakable digital edge. 8-stage
envelopes with arbitrary rates and levels give unusual, non-analog shapes.

Used by: Vince Clarke, Aphex Twin, Autechre, and a great deal of early UK
electronica. **The Reese bass is frequently credited to a CZ-5000** (Kevin
Saunderson's "Just Want Another Chance", 1988) — detuned oscillators through
its distinctive PD waveforms.

**Rebuild:** take a sine and apply a waveshaping phase warp:
`out = sin(2π · warp(phase))` where `warp` compresses the first portion of the
cycle. Sweeping the warp amount 0→1 morphs sine→saw and sounds like a filter
opening, but brighter and more digital than any real filter.

---

## FM in software

| Instrument | Notes |
|---|---|
| **Native Instruments FM8** | 6-op with a free routing matrix, filters and effects the DX7 never had |
| **Dexed** | A faithful, free DX7 emulation; loads original DX7 patch banks |
| **Ableton Operator** | 4-op FM with filters; the practical modern FM workhorse |
| **Image-Line Sytrus** | FM + ring mod + filters per operator; deeply flexible |
| **Arturia DX7 V** | Modelled, with a modern interface |
| **Elektron Digitone** | 4-op FM with a sequencer; the modern hardware standard |
| **Serum/Vital/Phase Plant** | All do FM between oscillators alongside wavetables |

## When to reach for FM instead of subtractive

| Want | FM is better because |
|---|---|
| Bells, metal, glass | Inharmonic ratios produce genuinely inharmonic spectra; filters cannot |
| Electric pianos | The attack/decay spectral evolution is inherent |
| Aggressive, digital bass | Sidebands create mid-range content that survives small speakers |
| Growls and screams | Modulating the index at audio rate is chaotic in a controllable way |
| Sounds that cut through | FM's spectrum is dense in the 1–5 kHz region |

| Want | Subtractive is better because |
|---|---|
| Warm pads | Filtered saws are smooth; FM is not |
| Classic analog bass | The filter's non-linearity is the sound |
| Anything needing a resonant sweep | FM has no resonance |

## Related

- Synthesis fundamentals: `../00-foundations/12-timbre-and-synthesis.md`
- Sound design recipes: `../30-patterns/08-sound-design-recipes.md`
