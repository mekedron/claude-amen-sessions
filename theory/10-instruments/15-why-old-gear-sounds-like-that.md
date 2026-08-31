# Why Old Gear Sounds Like That

A digitally perfect recreation of a vintage instrument sounds wrong, and the
reason is always the same: **the character is in the imperfection**. This file
lists the specific imperfections and how to reproduce them deliberately.

---

## 1. Analog drift and per-voice variation

Analog oscillators are temperature- and voltage-dependent. They never hold exact
tuning, they drift against each other continuously, and in a polysynth every
voice card has slightly different component tolerances.

**Reproduce:**
```
Per oscillator: slow random pitch drift, ±2-8 cents, at 0.05-0.5 Hz
Per voice (polysynth): a fixed random offset of ±3-8 cents and ±2-5% filter
                       cutoff, regenerated per note or per voice slot
Per note: a small random attack-time variation (±5%)
```
This single change does more to make a synth patch sound "analog" than any
filter model.

---

## 2. Filter non-linearity

A real ladder or diode filter is not a mathematical low-pass:
- It **loses low end as resonance rises** (the Moog ladder is famous for this).
- It **saturates** when driven, compressing and adding harmonics.
- Its resonance peak is asymmetric and its slope is not exactly 24 dB/oct.
- Its cutoff tracking is imperfect across the keyboard.

**Reproduce:** put a `tanh` saturation stage inside or immediately after the
filter; reduce the low band by 1–3 dB as resonance rises; add ±3% of random
cutoff error; drive the filter input so the saturation is audible.

---

## 3. Bit depth and sample rate

| Machine | Spec | Sonic consequence |
|---|---|---|
| Fairlight CMI | 8-bit / ~24 kHz | Gritty, aliased, harsh |
| PPG Wave | 8-bit wavetables | Glassy, grainy |
| SP-1200 | 12-bit / 26.04 kHz | The golden-age hip-hop crunch |
| MPC60 | 12-bit / 40 kHz | Warmer grit |
| Akai S950 | 12-bit, variable rate | Time-stretch smear |
| TR-909 hats | 6-bit samples | Splashy, broken |
| Amiga | 8-bit / ~28 kHz | The jungle/demoscene sound |

**Reproduce:**
```
Truncate (do NOT dither) to the target bit depth:
    q = 2 ** (bits - 1);  x = floor(x * q) / q
Downsample by decimation WITHOUT an anti-alias filter, then hold or repeat
    samples back up - the aliasing is the point
Low-pass at roughly (sample_rate / 2) afterwards to imitate the output filter
```
The critical detail: **do not anti-alias**. Modern converters filter before
downsampling; vintage samplers often did not, and the folded-back frequencies
are what you are trying to recreate.

---

## 4. Aliasing

Any frequency above Nyquist folds back to `sample_rate − f`. In vintage digital
gear this happens constantly: in FM at high index, in pitched-up samples, in
naive oscillators.

- **Unwanted:** aliasing on a modern clean lead sounds like a bug.
- **Wanted:** aliasing on a pitched-up 12-bit break is the sound of 1993.

**Reproduce:** generate a waveform with harmonics above Nyquist and do not
band-limit it (e.g. a naive `2*(f*t % 1) - 1` sawtooth above 500 Hz), or
pitch a sample up by varispeed with no filtering.

---

## 5. Varispeed pitching

Vintage samplers changed pitch by changing playback rate. Pitch and duration are
locked, and the timbre's **formants move with the pitch** — which is why a
pitched-up vocal sounds like a chipmunk and a pitched-down one sounds enormous.

Modern time-stretching preserves duration and (optionally) formants, and
therefore does **not** sound vintage. If you want the historical sound, use
varispeed.

```
rate = target_pitch_ratio
new_length = old_length / rate
semitones = 12 * log2(rate)
```

---

## 6. Tape

| Artefact | Cause | Value |
|---|---|---|
| **Wow** | Slow speed variation | Pitch modulation, 0.3–1 Hz, 5–20 cents |
| **Flutter** | Fast speed variation | Pitch modulation, 6–15 Hz, 2–8 cents |
| **Saturation** | Magnetic hysteresis | Soft compression, added even harmonics |
| **High-frequency loss** | Head gap, tape speed | Low-pass, more with each generation |
| **Hiss** | The medium itself | Pink noise at −50 dB |
| **Print-through** | Adjacent layers on the reel | A faint pre-echo |
| **Compression** | Tape's soft ceiling | Transients rounded, level evened |

Each repeat in a tape delay accumulates all of these — which is why tape echoes
decay into warm mush instead of digital copies.

---

## 7. Timing and quantisation resolution

Old sequencers had coarse timing grids and real, measurable jitter:

| Machine | Resolution | At 120 BPM |
|---|---|---|
| MPC60 | 96 ppq | ~5.2 ms per tick |
| TR-909 | 96 ppq | ~5.2 ms |
| Atari ST + MIDI | ~1 ms jitter | audible tightness |
| Modern DAW | sample-accurate | 0.02 ms |

**Reproduce:** quantise event positions to a 96-ppq grid, then add ±1–3 ms of
random jitter. And use the machine's swing implementation (delay the offbeat
16ths by a percentage) rather than a modern groove template.

---

## 8. Limited polyphony and memory

The Prophet-5 has 5 voices. The Amiga has 4 channels. The SP-1200 holds 10
seconds. The Mellotron holds 8 seconds per note.

These limits forced arrangement decisions that we now hear as style:
- Sparse arrangements, because you could not layer.
- Voice-stealing artefacts when a chord exceeded the polyphony.
- Tight sample chopping, because memory was measured in kilobytes.
- Bass and melody sharing one channel, alternating.

**Reproduce:** cap your polyphony at 4–8 and let notes steal. Cap your total
sample memory. Force yourself to pre-mix layers into a single sound.

---

## 9. Effects were always on

The Juno's chorus, the D-50's reverb, the Space Echo's spring, the Leslie's
rotor — on many classic instruments the effect could not be bypassed, or nobody
bypassed it. The "instrument" everyone remembers **is the instrument plus its
effect**.

If a recreation sounds thin, the missing part is usually the effect, not the
oscillator.

---

## 10. Noise floors and crosstalk

Analog gear hums, hisses, and leaks between channels. The 60/50 Hz mains hum,
the VCA feedthrough (a faint tone audible even when a note is off), the
bucket-brigade chorus's noise — all of it fills the space between notes, and
modern digital silence sounds unnaturally empty by comparison.

**Reproduce:** add a constant low-level noise bed (−60 to −50 dB), and let a
tiny amount of the oscillator through even when the envelope is closed.

---

## The generic "make it vintage" chain

Apply to any modern sound, in this order:

```
1. Per-voice random detune (±4 cents) and per-voice filter offset (±3%)
2. Slow pitch drift on each oscillator (±3 cents at 0.2 Hz)
3. Saturation before and/or inside the filter (tanh)
4. Bit reduction to 12 bits (truncated, no dither)
5. Decimate to 26-32 kHz without anti-aliasing
6. Low-pass at 8-12 kHz, high-pass at 40-80 Hz
7. Tape wow (0.5 Hz, 8 cents) and flutter (9 Hz, 3 cents)
8. Chorus or ensemble (the era's effect)
9. A noise bed at -55 dB
10. Gentle compression with a visible pump
```

Not all ten at once for every sound — pick the three or four that match the era
you want. Steps 1 and 3 alone cover "analog"; steps 4, 5 and 10 cover "sampler";
steps 6, 7 and 9 cover "tape".

---

## The counter-argument, stated fairly

None of this is required. A great deal of excellent modern music is clean,
precise, digitally perfect, and would be ruined by any of the above. Hyperpop,
big-room EDM, contemporary pop and much techno are *deliberately* artificial.

The point is to know which quality you are choosing, and to choose it — not to
apply vintage processing by reflex. **Sterility is a valid aesthetic; accidental
sterility is not.**

## Related

- Synthesis fundamentals: `../00-foundations/12-timbre-and-synthesis.md`
- Lo-fi recipes: `../30-patterns/08-sound-design-recipes.md`
- Humanisation: `../30-patterns/09-humanization-and-groove.md`
