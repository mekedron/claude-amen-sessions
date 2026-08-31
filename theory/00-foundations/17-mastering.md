# Mastering

Mastering is the last stage: taking a finished stereo mix and preparing it to
sound its best, at competitive loudness, consistently, everywhere it will be
played. It is **not** a rescue operation and it is **not** "make it loud".

## What mastering actually does

1. **Tonal balance** — small, broad EQ moves so the track translates on every
   system.
2. **Dynamic control** — gentle compression for cohesion, limiting for level.
3. **Loudness** — hit a target that suits the genre and the delivery platform.
4. **Stereo image** — small width and mono-compatibility adjustments.
5. **Consistency** — across an album/EP, so tracks sit at the same level and
   tone.
6. **Delivery** — sample rate, bit depth, dither, metadata, track spacing, fades.

**The rule of small moves:** mastering EQ is typically ±0.5 to ±2 dB. If you
need more than 3 dB anywhere, go back to the mix.

## Before you master

Requirements for the mix you are handed:

| Requirement | Value |
|---|---|
| Peak level | −6 to −3 dBFS, no clipping |
| Format | 24-bit or 32-bit float, at the session sample rate |
| Processing | **No limiter or heavy bus compression on the master** |
| Fades | None at the start/end (leave a little silence instead) |
| Mono compatibility | Already checked |
| Low end | Already mono below ~120 Hz |

If you produced the track yourself, **take a break before mastering it**. A day
is ideal; an hour is the minimum. Master with fresh ears at a moderate volume.

## The chain

A standard order, each stage optional:

```
1. Corrective EQ        (surgical: remove resonances, DC, rumble)
2. Dynamic EQ / multiband  (control problem bands that only misbehave sometimes)
3. Compression          (glue, 1–2 dB GR maximum)
4. Tonal EQ             (broad shelves: warmth, air, tilt)
5. Saturation / harmonic exciter  (density, perceived loudness, glue)
6. Stereo adjustment    (mono the lows, gentle widening of the highs)
7. Clipper              (shave the sharpest transients — usually the kick)
8. Limiter              (final level, true-peak ceiling)
9. Dither               (only when reducing bit depth)
```

Alternative valid order: compression before EQ if you want the compressor
reacting to the raw balance; saturation before compression if it *is* the sound.

### 1. Corrective EQ

- High-pass at **20–30 Hz**, gently (12 dB/oct), to remove subsonic energy that
  eats limiter headroom and does nothing audible.
- Notch out any narrow resonance you can hear ringing. Sweep with a high-Q boost
  to find it, then cut −2 to −4 dB with Q 6–12.
- Look for a build-up at 200–400 Hz (mud) and 3–5 kHz (harshness). Wide, gentle
  cuts.

### 2. Dynamic EQ / multiband

Use only for problems that are **intermittent**:
- Low end that only gets flabby in the drop → dynamic cut at 60–100 Hz.
- Harshness that only appears in the loud chorus → dynamic cut at 3 kHz.
- Sibilance surviving from the mix → dynamic cut at 6–9 kHz.

**HAZARD:** static multiband compression across the whole track flattens the
natural spectral movement between sections. Use narrow, dynamic, and sparingly.

### 3. Compression

| Setting | Value |
|---|---|
| Ratio | 1.2:1 to 2:1 |
| Threshold | So that GR is **1–2 dB** on peaks, 3 dB maximum |
| Attack | 10–30 ms (slow enough to let transients through) |
| Release | Auto, or tempo-matched (one beat is a good starting point) |
| Knee | Soft |

The goal is cohesion, not level. If you can clearly *hear* the compressor, it is
doing too much. Test by bypassing with matched gain: the compressed version
should sound slightly more "together", not obviously different.

Optional: **parallel compression** on the master (heavily compressed copy blended
at 10–20%) adds density without squashing transients.

### 4. Tonal EQ

Broad shelves and wide bells only:

| Move | Typical amount |
|---|---|
| Low shelf at 80–120 Hz | ±0.5 to ±1.5 dB — weight |
| Wide bell at 200–400 Hz | −0.5 to −1.5 dB — clarity |
| Wide bell at 800 Hz–1.2 kHz | ±0.5 dB — body vs hollowness |
| Wide bell at 2.5–4 kHz | ±0.5 to −1.5 dB — presence vs harshness |
| High shelf at 8–12 kHz | +0.5 to +2 dB — air, "expensive" |

Use Q values of 0.5–1.0. If a move needs Q > 2, it is corrective, not tonal.

### 5. Saturation

Gentle harmonic distortion at the master stage:
- Adds harmonics → the ear perceives more loudness at the same peak level.
- Rounds transients → the limiter works less.
- Glues elements → they share a distortion character.

Amount: barely audible. 1–3% THD. Tape and tube emulations are the usual choices;
a soft-clip stage is the modern one.

### 6. Stereo adjustment

- **Mono the low end** below 100–150 Hz if the mix has not already.
- **Mid/side EQ**: a small high-shelf boost on the sides widens without
  hollowing the centre.
- Widening beyond ~110% is almost always a mistake. Always check mono.
- Check correlation: a phase-correlation meter should stay positive (above 0),
  ideally 0.3–0.9. Persistent negative correlation = mono problems.

### 7. Clipping before limiting

Modern loud masters use a **soft clipper before the limiter** to shave the
sharpest peaks (usually the kick and snare transients), which are inaudible when
clipped by 1–3 dB but which otherwise force the limiter into audible pumping.

Order: clipper (1–3 dB of peak reduction) → limiter (2–4 dB of GR). This gets you
loud with far fewer artefacts than the limiter alone.

### 8. Limiting

| Setting | Value |
|---|---|
| Ceiling | **−1.0 dBTP** for streaming (−0.3 for CD/download only) |
| GR | 2–5 dB typical; more than 6 dB means the mix is not ready |
| Release | Fast enough to avoid pumping, slow enough to avoid distortion; auto is usually fine |
| Lookahead / true-peak detection | On |
| Style/character | Transparent for most genres; "aggressive" for EDM |

**Test for over-limiting:** bypass the limiter and turn the output down to match.
If the unlimited version has noticeably more punch and depth, back off.

### 9. Dither

Only when reducing bit depth (e.g. 24-bit → 16-bit for CD). Add noise-shaped
dither as the **absolute last** process. Do not dither if delivering 24-bit or
32-bit float. Never dither twice.

## Loudness targets

Streaming platforms normalise playback, so mastering far above their target
gains you **nothing but lost dynamics** — it just gets turned down.

| Platform | Normalisation target | True-peak ceiling |
|---|---|---|
| Spotify | −14 LUFS | −1 dBTP |
| Apple Music | −16 LUFS | −1 dBTP |
| YouTube | −14 LUFS | −1 dBTP |
| Tidal | −14 LUFS | −1 dBTP |
| Amazon Music | −14 LUFS | −2 dBTP |
| SoundCloud | −14 LUFS (approximately) | −1 dBTP |
| Broadcast (EBU R128) | −23 LUFS | −1 dBTP |
| Broadcast (US ATSC A/85) | −24 LKFS | −2 dBTP |
| Club / DJ playout (no normalisation) | −8 to −6 LUFS is common | −0.3 to −1 dBTP |
| CD / download (no normalisation) | −10 to −6 LUFS is common | −0.1 to −0.3 dBFS |

Practical targets by genre (integrated LUFS):

| Genre | Target |
|---|---|
| EDM / big room / hardstyle | −8 to −6 |
| Techno / house (club) | −9 to −7 |
| Drum & bass / dubstep | −8 to −6 |
| Trap / hip-hop | −9 to −7 |
| Pop | −10 to −8 |
| Rock / metal | −10 to −8 |
| Indie / singer-songwriter | −12 to −10 |
| Lo-fi / chillhop | −14 to −11 |
| Ambient | −18 to −14 |
| Jazz | −16 to −13 |
| Classical | −23 to −16 |

**How to choose:** master for the *context*, not for the platform. A club track
needs the density and saturation that come with loud mastering, even though
Spotify will turn it down — the density is part of the sound. A ballad mastered
to −7 LUFS just sounds crushed.

**HAZARD:** if you exceed the platform target, the platform turns you down, and
your track will sound *quieter and flatter* than a competitor mastered at −10
with real dynamics. The loudness war is over on streaming; density and punch
still matter.

## Reference matching

1. Choose 2–3 released tracks in the genre.
2. Load them alongside your master.
3. **Level-match by LUFS** (this is non-negotiable).
4. Compare, switching every 5–10 seconds:
   - Low-end weight and extension
   - Mid-range fullness (200 Hz–1 kHz)
   - Brightness (5–12 kHz)
   - Width
   - Punch (does the kick still hit?)
5. Make small adjustments. Re-match levels after every change.

A spectrum analyser with a long average is useful, but the goal is to sound
*like* the reference in balance, not to match its curve exactly — the curve is a
product of that track's arrangement.

## Album / EP mastering

- **Relative levels between tracks** matter more than absolute levels. The album
  should feel level-consistent while preserving the intended dynamics of a quiet
  interlude.
- **Tonal consistency**: if track 3 is noticeably brighter than tracks 2 and 4,
  fix it even if track 3 sounds good alone.
- **Spacing and fades**: 2–4 seconds between tracks is typical; shorter for
  continuous mixes; gapless/crossfade for DJ mixes.
- Master the loudest track first and use it as the benchmark.

## Delivery formats

| Destination | Format |
|---|---|
| Streaming / distribution | 24-bit WAV, session sample rate (44.1 or 48 kHz), −1 dBTP |
| CD | 16-bit / 44.1 kHz WAV, dithered, with correct track IDs |
| Vinyl | **Different master required**: no heavy limiting, mono below ~150–300 Hz, de-essed (sibilance causes cutting problems), reduced stereo width in the lows, and a peak ceiling around −3 dBFS. Long/loud low end reduces the achievable playing time per side. |
| Video / broadcast | −23 LUFS (EBU) or −24 LKFS (US), −2 dBTP |
| Club / DJ | 24-bit WAV, loud, −1 dBTP; also supply a 320 kbps MP3 |
| Games | Often normalised per-asset; check the engine's requirements |

**Never master from an MP3 or any lossy source** — the encoder artefacts get
amplified by limiting.

**Sample rate conversion**, if needed, happens before the final limiter, using a
high-quality converter. Peaks can rise after SRC, so limit afterwards.

## Codec considerations

Lossy encoders (MP3, AAC, Opus) can **raise peaks** by up to 1–2 dB and produce
artefacts in heavily limited, bright material.

- A −1 dBTP ceiling exists precisely for this.
- Excessive high-frequency energy and heavy limiting are what make a master fall
  apart after encoding.
- Test: encode to 128 kbps AAC and listen. If it becomes harsh or gritty, back
  off the limiter and the top end.

## Mastering checklist

Before you call it done:

- [ ] Integrated LUFS measured and appropriate for genre/platform
- [ ] True peak ≤ −1.0 dBTP
- [ ] No clipping anywhere in the chain (check inter-sample peaks)
- [ ] Low end mono below ~120 Hz
- [ ] Phase correlation positive
- [ ] Checked in mono
- [ ] Checked on: monitors, headphones, laptop speaker, phone speaker
- [ ] Checked at low volume and at loud volume
- [ ] Limiter GR under 6 dB
- [ ] Bypass A/B with matched gain: the master is better, not just louder
- [ ] Start and end are clean (no clicks, correct silence, deliberate fades)
- [ ] Correct sample rate and bit depth for the destination
- [ ] Dithered only if reducing bit depth, and only once
- [ ] Encoded to lossy and re-checked
- [ ] Compared to references at matched loudness

## HAZARDS

- **Mastering to fix a mix.** Go back to the mix. Every time.
- **Over-limiting.** The most common failure, by far. Symptoms: no punch, the
  kick disappears when the bass plays, pumping, a "wall" with no depth.
- **Boosting highs to sound "hi-fi".** Ear fatigue and codec artefacts.
- **Widening for the sake of it.** Costs mono compatibility.
- **Chasing a reference's loudness** without its arrangement and mix density.
- **Mastering when tired.** The last hour of a session is where masters are
  ruined.
- **Multiple limiters in series without intent** — cumulative squashing.
- **Not leaving the room and coming back.**

## Related

- What the mix should deliver: `16-mixing-process.md`
- The EQ moves in detail: `13-frequency-and-eq.md`
- Compression theory: `14-dynamics-and-compression.md`
- Loudness perception: `18-psychoacoustics-and-tension.md`
