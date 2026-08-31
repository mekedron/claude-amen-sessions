# Humanisation and Groove

Programmed music sounds programmed for specific, fixable reasons. This file is
the checklist of what to vary and by how much.

## The four dimensions of humanisation

| Dimension | What to vary | Typical range |
|---|---|---|
| **Timing** | Onset position | ±3–20 ms |
| **Velocity** | Loudness per hit | ±8–20% |
| **Duration** | Note length | ±5–25% |
| **Timbre** | Brightness, sample choice | correlated with velocity |

Vary all four. Varying only velocity produces "loud and quiet robot".

## Timing

### Swing
Applied to **odd subdivisions only** (the offbeat 16ths or 8ths).

```
offset_ms = (swing_pct/100 - 0.5) * 2 * ms_per_step
ms_per_step = 15000 / BPM        (one 16th in 4/4)
```

| Swing | Genre |
|---|---|
| 50% | Techno, trance, hyperpop, most EDM |
| 52–54% | House, subtle |
| 54–58% | Deep house, afrobeats, disco |
| 56–62% | UK garage, hip-hop, R&B |
| 58–66% | Boom bap, neo-soul |
| 66.7% | Full triplet: shuffle, blues, gospel, swing jazz |
| 68–75% | Drunken, lurching, dub |

### Microtiming offsets

| Element | Offset | Feel |
|---|---|---|
| Snare | +10 to +25 ms | Laid back (hip-hop, neo-soul, trip-hop) |
| Snare | −5 to −15 ms | Urgent (punk, jump-up, hardcore) |
| Hats | +3 to +8 ms | Behind the beat |
| Hats | −3 ms | Pushing |
| Bass | −5 to −10 ms vs the kick | The bass "leads"; funk |
| Bass | +5 ms vs the kick | The bass "follows"; relaxed |
| Chords/comping | ±10–30 ms, irregular | Live playing |
| Melody | −10 ms on phrase starts | Expressive anticipation |

### Random jitter

Apply per hit: `offset = gaussian(0, sigma)` clipped to ±3σ.

| σ | Result |
|---|---|
| 1–3 ms | Barely perceptible; removes machine perfection |
| 4–8 ms | Clearly human |
| 9–15 ms | Loose, sloppy in a good way |
| 15+ ms | Actually sloppy |

**Do not jitter the kick** in dance music — it destroys the pulse. Jitter the
ghost notes, hats, percussion and inner voices.

## Velocity

### Base tables

| Role | Velocity | Linear gain |
|---|---|---|
| Accent | 110–127 | 0.86–1.0 |
| Normal | 85–105 | 0.67–0.83 |
| Soft | 60–80 | 0.47–0.63 |
| Ghost | 25–50 | 0.20–0.39 |

`gain ≈ (velocity / 127) ** 1.5` is a reasonable perceptual curve for drums.

### Patterns that work automatically

```
Alternating hats:      100, 70, 90, 70, 100, 70, 90, 70
Downbeat emphasis:     +15 on steps 0, 4, 8, 12
Phrase crescendo:      linear ramp across a 4-bar fill from 60 to 127
Backbeat emphasis:     snare on 2 and 4 at 120; ghosts at 35
Random walk:           v[n] = clamp(v[n-1] + gaussian(0, 6), 40, 127)
```

### Velocity should change timbre

A hard-hit snare is brighter and longer. If your instrument does not model this:
- Brighten accented hits (+2–4 dB shelf at 4 kHz).
- Shorten quiet hits.
- Use different samples for accent / normal / ghost.

## Note duration

| Style | Duration relative to the step |
|---|---|
| Staccato | 30–50% |
| Normal | 70–90% |
| Legato | 100–110% (overlapping) |
| Varied (human) | 60–100%, randomised |

**Duration variation is the most neglected humanisation.** A bass line where
every note is exactly one 16th long sounds mechanical even with perfect timing
and velocity variation.

## Groove templates

A groove template is a per-step offset (timing and velocity) applied to
everything. Some useful ones, expressed as `(ms offset, velocity multiplier)`
per 16th step:

### MPC 16-swing 58%
```
step:  0        1        2        3        4        5        6        7
time:  0,       +18,     0,       +18,     0,       +18,     0,       +18
vel:   1.0,     0.80,    0.92,    0.78,    1.0,     0.80,    0.92,    0.78
```

### Laid-back (neo-soul)
```
time:  +4, +20, +8, +22, +6, +20, +8, +22, ...
vel:   1.0, 0.7, 0.85, 0.7, 0.95, 0.7, 0.85, 0.7, ...
```

### Pushed (punk / jump-up)
```
time:  -3, -6, -2, -6, -3, -6, -2, -6, ...
vel:   1.0, 0.85, 0.95, 0.85, ...
```

### Machine (techno)
```
time:  all 0
vel:   1.0, 0.85, 0.92, 0.85, ...   (velocity only)
```

## Melodic and harmonic humanisation

| Element | Technique |
|---|---|
| **Chords** | Roll/strum: offset each note by 5–25 ms, lowest first (or highest for a "flick") |
| **Piano** | Vary velocity across the chord (melody note loudest, inner voices quieter) |
| **Strings** | Slow attacks that vary per note; slight pitch drift; vibrato that fades in |
| **Guitar** | Strum offsets, string-dependent velocity, occasional fret noise |
| **Brass** | Pitch scoop into the note (10–30 cents over 30 ms) |
| **Vocals** | Timing ±20 ms, pitch drift ±10 cents, breaths |
| **Bass** | Slide into some notes, vary note length, ghost notes |
| **Synth arps** | Velocity pattern, occasional missed step, slight cutoff variation per note |

**Pitch humanisation:** ±3–10 cents of random detune per note on acoustic-style
instruments. On synths, per-voice random phase and ±2–5 cents.

## Structural humanisation

Real performances vary at a larger scale too:

- **Section-to-section energy**: verse quieter and looser, chorus louder and
  tighter.
- **Fills are not perfect** — a real drummer's fill has a rushed or dragged
  quality.
- **The last chorus is played harder** than the first.
- **Tempo variation**: ±0.5–2 BPM over a section (rubato) for acoustic styles;
  none for electronic.
- **Instrumental "mistakes"**: an occasional extra ghost note, a slightly
  early entry, a note held too long. One per 16 bars is plenty.

## Random number practice

- **Use a seeded RNG** so a track is reproducible.
- **Gaussian, not uniform**, for timing and velocity — real deviation clusters
  around a centre.
- **Correlated randomness**: a random walk (each value depends on the previous)
  sounds far more human than independent samples, because real performers drift.
- **Different seeds per instrument** so their deviations are independent.
- **Quantise the randomness where it matters**: a kick can be jittered by 2 ms;
  a lead can be jittered by 15 ms.

## When NOT to humanise

| Situation | Why |
|---|---|
| Techno, trance, hardstyle kicks | The grid is the aesthetic |
| Hyperpop, chiptune | Artificiality is the point |
| Layered drums (kick sub + click) | The layers must stay phase-aligned |
| Sub bass | Timing shifts change the phase relationship with the kick |
| Anything doubling another part in unison | Offsets create flamming |
| Quantised vocal chop rhythms | The rhythm is the hook |

## Checklist

- [ ] Velocity varies across every repeated element
- [ ] Hats alternate loud/soft
- [ ] Ghost notes exist where the genre calls for them
- [ ] Swing applied to the right subdivision at the right percentage
- [ ] Note durations vary
- [ ] Timing jitter on non-foundational elements
- [ ] Chords are rolled, not block-simultaneous (where appropriate)
- [ ] Something differs between bar 1 and bar 2 of every 2-bar loop
- [ ] Velocity affects timbre, not just level
- [ ] The kick and the sub are NOT jittered

## Related

- Groove theory: `../00-foundations/02-rhythm-and-time.md`, `../00-foundations/10-drums-and-groove.md`
