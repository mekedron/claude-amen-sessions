# Dynamics and Compression

EQ decides *where* in the spectrum something lives. Compression decides *when*
and *how consistently* it is heard. Together they are the whole of mixing.

## What a compressor does

Above a threshold, it reduces gain by a ratio. Below it, nothing happens.

| Control | What it does | Ranges |
|---|---|---|
| **Threshold** | Level above which compression starts | −40 to 0 dBFS |
| **Ratio** | Input:output above threshold. 4:1 means 4 dB in → 1 dB out | 1.5:1 to ∞:1 |
| **Attack** | How fast it clamps down after the signal crosses the threshold | 0.1–100 ms |
| **Release** | How fast it lets go once the signal drops | 10–1000 ms, or auto |
| **Knee** | How gradually the ratio engages around the threshold | 0 (hard) to 20 dB (soft) |
| **Makeup gain** | Level restored after compression | to taste |

**Gain reduction (GR)** is what you actually judge: how many dB the compressor is
pulling down at the peaks.

## The two things attack and release actually control

This is the part that matters and is usually explained badly.

- **Fast attack (0.1–5 ms)** catches the transient → the attack is *reduced* →
  the sound becomes softer, rounder, more "squashed", and the body sounds louder
  relative to the hit.
- **Slow attack (10–50 ms)** lets the transient through → the attack is
  *emphasised* → the sound becomes punchier and more aggressive.

Counterintuitive but true: **to make a drum punchier, use a slower attack.**

- **Fast release (10–80 ms)** → the compressor recovers between hits → more
  audible pumping and "life"; too fast causes distortion on bass content.
- **Slow release (200 ms–1 s)** → smooth, transparent, but can duck material
  that follows a loud peak.
- **Release should relate to the tempo.** A release that finishes just before the
  next beat sounds musical; one that is still recovering sounds like a mistake.

## Starting settings by source

| Source | Ratio | Attack | Release | GR | Purpose |
|---|---|---|---|---|---|
| Kick | 4:1 | 10–20 ms | 60–150 ms | 3–6 dB | Punch, consistency |
| Snare | 4:1 | 5–20 ms | 100–200 ms | 3–8 dB | Body, sustain |
| Drum bus | 2–4:1 | 10–30 ms | auto / 100–200 ms | 2–4 dB | Glue |
| Parallel drums | 10:1+ | 0.1 ms | 50–100 ms | 10–20 dB | Blend under the dry for weight |
| Bass | 4:1 | 5–15 ms | 100–200 ms | 4–8 dB | Even level, note-to-note consistency |
| Sub bass | 3:1 | 20 ms | 150 ms | 2–4 dB | Gentle; over-compressing kills the sub |
| Vocal | 3–4:1 | 5–15 ms | 40–100 ms | 3–6 dB | Intelligibility, front-of-mix |
| Vocal (serial 2nd stage) | 2:1 | 20 ms | 200 ms | 2–3 dB | Smoothing; two gentle stages beat one hard one |
| Piano / keys | 2–3:1 | 15–30 ms | 150–300 ms | 2–4 dB | Even dynamics |
| Guitar | 3:1 | 10–20 ms | 100 ms | 3–5 dB | Sustain |
| Pads / strings | 2:1 | 30 ms | 300 ms | 1–3 dB | Barely; they are already even |
| Mix bus | 1.5–2:1 | 10–30 ms | auto | 1–3 dB | Glue only |

**Rule:** if a compressor shows more than ~6 dB of gain reduction and you did
not intend an effect, the source level or arrangement is wrong.

## Compressor types and their sound

| Type | Behaviour | Character | Use |
|---|---|---|---|
| **VCA** | Fast, precise, flexible | Clean, punchy | Drums, bus glue |
| **FET** | Very fast attack, aggressive | Coloured, exciting | Vocals, drums, room mics |
| **Opto** | Program-dependent, slow, gentle | Smooth, musical | Vocals, bass, mix bus |
| **Vari-mu / tube** | Ratio increases with level | Warm, thick, saturating | Mix bus, mastering |
| **Digital / transparent** | Exactly what you set | Neutral, surgical | Anywhere precision matters |

## Serial and parallel compression

- **Serial**: two compressors doing 3 dB each sounds far more natural than one
  doing 6 dB. This is the professional default on vocals.
- **Parallel (New York) compression**: blend a heavily compressed copy under the
  dry signal. You get density and sustain without losing the transients. Standard
  on drums and vocals. Ratio 10:1+, fastest attack, 10–20 dB GR, blended at
  20–50%.
- **Parallel saturation** works the same way and is often better on bass.

## Sidechain compression (ducking)

The compressor listens to one signal and compresses another.

**The pump** (house, techno, trance, EDM): the kick ducks the bass, pads and
sometimes the entire mix.

| Setting | Value |
|---|---|
| Ratio | 4:1 to ∞:1 |
| Attack | 0.1–1 ms (as fast as possible) |
| Hold | 10–50 ms |
| Release | matched to the tempo: 1/16 or 1/8 note |
| Depth (GR) | 3–6 dB subtle, 10–20 dB obvious |

Release in ms for a 1/16 note = `15000 / BPM`. At 128 BPM that is 117 ms; at
174 BPM, 86 ms.

Alternatives to a true sidechain compressor:
- **Volume-shaper / envelope**: draw the duck shape explicitly. More controllable
  and the modern standard for EDM.
- **Sidechain only the low band** (multiband/dynamic EQ): the bass keeps its
  mid-range presence while the sub gets out of the kick's way. Cleaner.
- **Ghost kick**: sidechain from an inaudible kick track so the pump continues
  through sections where the real kick is absent.

Other sidechain uses:
- Vocal ducks the instrumental bus by 1–2 dB — invisible, and the vocal sits
  forward without being louder.
- Snare ducks the reverb return so the tail blooms after the hit.
- Lead ducks the pad.

## Transient shaping

A transient designer changes attack and sustain without a threshold — level
independent, so quiet hits get the same treatment as loud ones.

| Move | Effect |
|---|---|
| Attack + | Punchier, clickier, forward |
| Attack − | Softer, further back, blends |
| Sustain + | Bigger room, longer decay, fatter |
| Sustain − | Tighter, drier, more separation |

Extremely useful on programmed drums and on samples you cannot re-record.
Reducing sustain on a snare is a cleaner way to shorten it than gating.

## Gating and expansion

- **Gate**: silence below a threshold. Removes bleed and noise; shortens
  reverberant drums. Key parameters: threshold, attack (fast for drums),
  hold (10–100 ms to avoid chatter), release (50–300 ms).
- **Expander**: a gentler gate — reduces rather than mutes. Better for anything
  musical.
- **Gated reverb**: a big reverb followed by a hard gate. The 1980s snare.
  Still a valid, huge-sounding effect.
- **Trance gate / chopper**: rhythmic gating of a pad or chord at 1/16 notes,
  with a short attack/release shaping each slice. It converts a static pad into a
  rhythm part.

## Limiting

A limiter is a compressor with an ∞:1 ratio and a very fast attack, used to stop
peaks from exceeding a ceiling.

- **True-peak** limiting accounts for inter-sample peaks that appear after D/A
  conversion or lossy encoding. Set a ceiling of **−1.0 dBTP** for streaming
  (−0.3 to −0.1 is asking for encoder distortion).
- **Clipping vs limiting**: a soft clipper adds harmonics and preserves
  transients; a limiter preserves waveform shape but flattens dynamics. Modern
  loud masters use a clipper *before* the limiter to shave the sharpest peaks
  (especially kick transients) so the limiter has less work to do.
- **HAZARD:** heavy limiting causes pumping, loss of punch, and distortion of
  bass content. If your limiter is pulling more than 4–6 dB, fix the mix.

## Loudness and dynamics measurement

| Metric | What it measures | Use |
|---|---|---|
| **Peak (dBFS)** | Highest sample value | Avoiding clipping |
| **True peak (dBTP)** | Peak after reconstruction | The number streaming services care about |
| **RMS** | Average energy over a window | Rough loudness |
| **LUFS (integrated)** | Perceptual loudness over the whole track | The standard for streaming normalisation |
| **LUFS (short-term / momentary)** | 3 s / 400 ms windows | Section-to-section balance |
| **LRA (loudness range)** | Spread between quiet and loud passages | Dynamics of the whole piece |
| **PLR / crest factor** | Peak minus loudness | How squashed it is |

Typical PLR: 8–10 dB for a heavily limited EDM master, 12–16 dB for pop/rock,
18+ dB for jazz and classical.

## Dynamic range as a musical parameter

Compression is not only corrective. Deliberate uses:

- **Pumping as rhythm** — the sidechain *is* an audible part.
- **Sustain as size** — heavy parallel compression makes a room sound enormous.
- **Consistency as intimacy** — a heavily compressed vocal sits "in your ear".
- **Restraint as drama** — a breakdown with 20 dB of dynamic range makes the
  drop feel enormous even if the drop's peak level is identical.

**HAZARD:** the most common error in modern production is compressing everything
until the track has no dynamic contrast between sections. Loudness contrast
across the arrangement matters more than loudness within a bar.

## Order of operations

The classic chain, and why:

```
gate/expander → EQ (subtractive) → compressor → EQ (additive/tonal) → saturation → fx sends
```

- Gate first, so the compressor is not triggered by noise.
- Subtractive EQ before the compressor, so it does not react to frequencies you
  are about to remove (a boomy 200 Hz will otherwise trigger the compressor
  constantly).
- Additive EQ after, so the compressor does not undo the boost.
- Saturation late, so it acts on a controlled signal.

Valid variations: compressor before EQ when you want the compressor's character
on the raw sound; two compressors either side of the EQ; saturation first when
it *is* the sound.

## HAZARDS

- **Over-compression**: no transients, no life, fatiguing after 30 seconds.
- **Attack too fast on drums**: kills the punch you were trying to create.
- **Release too fast on bass**: the compressor tracks the waveform itself and
  produces distortion. Keep the release above one cycle of the lowest frequency
  (at 40 Hz, that is 25 ms — so use 50 ms+).
- **Compressing a sub bass hard**: the sub is already a near-constant level;
  compressing it just modulates it.
- **Not level-matching when comparing**: louder always sounds better for the
  first ten seconds. Match levels before you judge any processing.
- **Compressing the mix bus to "make it loud"**: that is mastering's job, and
  doing it during mixing hides the problems you need to hear.

## Related

- Frequency-domain control: `13-frequency-and-eq.md`
- Full process: `16-mixing-process.md`
- Loudness targets and delivery: `17-mastering.md`
