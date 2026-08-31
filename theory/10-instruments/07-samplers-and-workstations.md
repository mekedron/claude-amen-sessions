# Samplers and Workstations

The machines that turned recorded sound into a playable instrument — and whose
technical limits became hip-hop, jungle and house.

---

## Fairlight CMI (1979)

**Type:** the first commercially successful digital sampling workstation.
8-bit, ~24 kHz, and priced like a house.

Two things mattered:
1. **Sampling**: any recorded sound could be played across a keyboard.
2. **Page R** (1982): a graphical **pattern sequencer** — arguably the ancestor
   of every step sequencer and DAW arrangement view since.

Its low bit depth gives everything a gritty, aliased character that was
considered a flaw and is now an aesthetic.

**The ORCH5 sample** — an orchestral stab lifted from Stravinsky's *Firebird* —
became one of the most recognisable sounds in music through Afrika Bambaataa's
"Planet Rock" (1982) and then the whole of hip-hop, rave and jungle. See
`14-iconic-patch-recipes.md`.

Users: Kate Bush, Peter Gabriel, Trevor Horn, Jean-Michel Jarre.

---

## New England Digital Synclavier (1977–)

FM synthesis plus (later) high-quality sampling, sold at astonishing prices to
studios and film composers. Michael Jackson's "Bad" opens with one; Frank Zappa
composed entire albums on it. Its importance is as a workstation concept:
synthesis, sampling, sequencing and direct-to-disk recording in one system.

---

## E-mu Emulator / Emulator II (1981/1984)

The first affordable-ish sampler. 8-bit, with analog filters after the digital
playback — which is why it sounds warmer than the Fairlight. The Emulator II's
factory library (the "Shakuhachi" and "Marcato Strings" patches especially) is
all over 80s pop and film.

---

## E-mu SP-1200 (1987) — the sound of golden-age hip-hop

**Type:** 12-bit drum machine/sampler with a sequencer.

### The constraints
| Limit | Consequence |
|---|---|
| **10.07 seconds of total sampling time** | You chop tightly. No long loops |
| **12-bit, 26.04 kHz** | Everything gets quantisation noise and aliasing |
| **8 voices, 4 outputs with analog filters (SSM2044)** | Individual sounds get analog colour |
| **Pitch = varispeed** | Pitching down lengthens *and* darkens; pitching up adds aliasing |

### Why it sounds like that
The combination of 12-bit truncation (not dithered), a 26 kHz sample rate
(so anything above ~13 kHz is gone and aliasing folds down), and the analog
output filters produces a specific gritty warmth. Producers deliberately
**sampled at a higher pitch and played back lower** to add "SP grit".

### What it changed
Pete Rock, DJ Premier, Large Professor, RZA, Diamond D — the entire early-90s
New York sound. It is still bought at high prices for this reason.

**Rebuild:** resample to 26 kHz, truncate to 12 bits without dither, low-pass at
~12 kHz, add a gentle resonant analog-style filter, and do pitch changes by
varispeed rather than time-stretching.

---

## Akai MPC60 (1988) / MPC3000 (1994)

**Type:** sampler + drum machine + sequencer, designed by **Roger Linn** for
Akai. 12-bit/40 kHz (MPC60), 16-bit/44.1 kHz (MPC3000).

### Why it matters beyond the sound
**The 16 velocity-sensitive pads** made programming drums a *performance*
rather than a data-entry task. And Linn's **swing implementation** — quantise
strength expressed as a percentage, delaying every second 16th — became the
industry's definition of groove.

| MPC swing | Feel |
|---|---|
| 50% | Straight |
| 54% | Subtle push |
| 58% | The classic hip-hop feel |
| 62% | Heavy shuffle |
| 66% | Full triplet |

The MPC's internal timing also has a slight, consistent latency and jitter that
many producers describe as its "feel". Its sequencer resolution (96 ppq on the
MPC60) quantises everything to a grid coarser than a modern DAW's.

**Rebuild:** apply swing to the offbeat 16ths only, at 54–62%, quantise
positions to a 96-ppq grid (about 5.2 ms at 120 BPM), and let velocity vary
widely.

---

## Akai S900 / S950 / S1000 (1986–1988)

Rack samplers that defined UK dance music. The **S950** in particular: 12-bit
with a variable sample rate, and a **time-stretch algorithm** whose artefacts —
a granular, metallic smearing — became the sound of hardcore and jungle
vocal and break manipulation. The S1000 was 16-bit and cleaner.

If a 1992 rave record has a pitched-up vocal that sounds crunchy and slightly
broken, it is usually an S950.

---

## Ensoniq Mirage (1984) / ASR-10 (1992)

The Mirage was the first sub-$2000 sampler — 8-bit, difficult, and gritty. The
**ASR-10** added on-board effects and resampling and became a hip-hop staple
(used heavily by RZA and others) because you could process, resample and layer
inside the machine.

---

## Korg M1 (1988) — the best-selling synth in history

**Type:** PCM-based **workstation**: sample-playback oscillators, digital
filters, effects, and an 8-track sequencer, all in one keyboard. Over 250,000
sold.

### Why it mattered
It could produce a complete arrangement — drums, bass, piano, strings, brass —
from one box. That is the workstation concept, and it dominated the 90s.

### The presets that became genres
| Preset | What it became |
|---|---|
| **Piano 16'** | **The house piano.** Every piano stab in every early-90s house and rave record |
| **Organ 2 / "Universe"** | The rave organ stab |
| **Lore / Universe** pads | Ambient and dream-house pads |
| Brass and orchestral hits | Rave and jungle stabs |

The M1 piano is a short, bright, slightly unreal PCM sample with a fast decay —
it does not sound like a real piano, which is precisely why it cuts through a
club mix.

**Rebuild the house piano:** a bright, hard-attack piano sample (or an FM/
additive approximation with strong 2nd and 3rd harmonics), decay 400–800 ms,
band-passed to remove sub-200 Hz and boost 1–3 kHz, played as **short stabs on
offbeats**, with a plate reverb and a slight chorus.

---

## Roland D-50, JD-800, JV/XP series

- **D-50** (1987) — see `06-wavetable-vector-and-la.md`.
- **JD-800** (1991) — a knob-and-slider-covered digital synth, very bright and
  hyper-detailed. Its pads and bell sounds are all over 90s ambient, jungle and
  trance.
- **JV-1080 / XP-50** (1994–) — the workhorse ROMpler of the 90s; its
  "Hip Hop Kit" and pad patches are on thousands of records.

---

## Native Instruments Kontakt (2002) — the modern standard

Not a sound but a **platform**: a scriptable sampler that became the delivery
format for virtually all commercial sample libraries — orchestral, cinematic,
ethnic, drums, everything.

Its significance is that **sample libraries became software instruments** with
articulation switching, round robins, velocity layers and scripted behaviour.
Modern film and game scoring is largely Kontakt-based.

---

## The sampler's real lesson

Every one of these machines added character through **limitation**:

| Limit | Sonic result | Use it deliberately |
|---|---|---|
| Low bit depth (8/12-bit) | Quantisation noise, grit | Truncate without dither |
| Low sample rate (22–33 kHz) | Missing top, aliasing | Resample down and back up |
| Short sample memory | Tight chopping, creative looping | Restrict yourself to 5–10 s |
| Varispeed pitching | Pitch and length locked together | Avoid time-stretch |
| Analog output filters | Warmth on top of digital grit | Add a resonant LPF per voice |
| Coarse sequencer resolution | A specific rhythmic "feel" | Quantise to 96 ppq |
| Few voices | Forced arrangement decisions | Cap your polyphony |

## Related

- Chopping technique: `../30-patterns/07-sampling-and-breaks.md`
- Lo-fi processing: `../30-patterns/08-sound-design-recipes.md`
- Legal position on sampling: `../30-patterns/07-sampling-and-breaks.md`
