# Frequency, EQ and the Spectrum

Mixing is mostly **allocating frequency space**. Two sounds that occupy the same
band fight; the loser becomes inaudible even though its fader is up. EQ is how
you assign each element a home.

## The audible spectrum, band by band

| Band | Range | Name | What lives there | Too much | Too little |
|---|---|---|---|---|---|
| Sub-bass | 20–60 Hz | Rumble | Sub bass, kick fundamental, room noise | Muddy, boomy, wastes headroom | Thin, no weight on big systems |
| Bass | 60–120 Hz | Weight | Kick body, bass fundamentals, low toms | Boomy, one-note bass | Weak, small |
| Low-mid | 120–300 Hz | Warmth / mud | Bass harmonics, snare body, low vocals, guitar body | **Mud, boxy, congested** | Thin, hollow, cold |
| Mid | 300–800 Hz | Body / boxiness | Everything's fundamentals; the crowded band | Boxy, cardboard, honky | Hollow, "scooped" |
| Upper-mid | 800 Hz–2.5 kHz | Presence, attack | Vocal intelligibility, snare crack, guitar bite | Harsh, nasal, fatiguing | Distant, veiled, no definition |
| High-mid | 2.5–6 kHz | Definition / harshness | Consonants, attack transients, pick noise | **Painful, sibilant, ear-fatiguing** | Dull, lifeless |
| High | 6–12 kHz | Brilliance | Hats, cymbals, sibilance, "expensive" sheen | Sibilant, brittle, hissy | Dark, muffled |
| Air | 12–20 kHz | Air | Space, sparkle, sense of "hi-fi" | Fizzy, harsh (and inaudible to many adults) | Closed-in, dull |

Two bands deserve special attention because they are where nearly every amateur
mix fails:

- **200–500 Hz — the mud zone.** Every instrument has energy here, and it adds
  up. Most mixing is subtractive cuts in this band.
- **2–4 kHz — the fatigue zone.** The ear is most sensitive here. A boost feels
  like "clarity" for thirty seconds and like a headache after five minutes.

## Instrument frequency map

Fundamentals (F) and the band where the character/definition lives (C).

| Instrument | F range | C range | Notes |
|---|---|---|---|
| Kick | 40–100 Hz | 2–5 kHz (click) | Also 150–250 Hz "thump" |
| Sub bass / 808 | 30–90 Hz | 100–300 Hz (harmonics that make it audible on phones) | |
| Bass guitar / synth bass | 40–400 Hz | 700 Hz–2.5 kHz (string/definition) | |
| Snare | 150–250 Hz | 1.5–3 kHz crack, 6–10 kHz snap | |
| Clap | 500 Hz–1 kHz | 1–4 kHz | Almost no low content |
| Toms | 80–300 Hz | 3–6 kHz | Floor tom 60–100 Hz |
| Hi-hat | — | 6–12 kHz | Body around 300–800 Hz can be cut |
| Ride | 300 Hz–1 kHz (ping) | 3–8 kHz | |
| Crash | — | 300 Hz–15 kHz | Broadband; masks everything |
| Piano | 30 Hz–4 kHz | 1–5 kHz | Widest range of any instrument |
| Electric piano (Rhodes) | 80 Hz–2 kHz | 2–5 kHz (bark) | |
| Acoustic guitar | 80 Hz–1.2 kHz | 2–5 kHz | Body boom at 200–250 Hz |
| Electric guitar | 80 Hz–1.2 kHz | 1.5–4 kHz | Almost nothing above 6 kHz |
| Strings (ensemble) | 60 Hz–1.5 kHz | 2–8 kHz | Rosin/air at 8–12 kHz |
| Brass | 100 Hz–1.5 kHz | 1–5 kHz | Blat at 800 Hz–2 kHz |
| Male vocal | 90–350 Hz | 1–4 kHz (intelligibility), 5–9 kHz (sibilance) | Boom at 200–300 Hz |
| Female vocal | 160–600 Hz | 1.5–5 kHz, 5–10 kHz sibilance | |
| Pads / strings synth | 100 Hz–2 kHz | 2–8 kHz | Usually high-passed at 150–250 Hz |
| Lead synth | 250 Hz–2 kHz | 2–8 kHz | |
| Supersaw | 200 Hz–8 kHz | broadband | The great masker; high-pass it |

## The essential EQ moves

### 1. High-pass everything except the kick and bass

The single most effective action in mixing. Every element has low-frequency
content it does not need and which is stealing headroom.

| Element | High-pass at |
|---|---|
| Kick | 25–35 Hz (only to remove DC/rumble) |
| Bass / 808 | 25–30 Hz |
| Snare | 100–150 Hz |
| Clap | 200–300 Hz |
| Hats / cymbals | 300–600 Hz |
| Percussion | 150–400 Hz |
| Vocal | 80–120 Hz (male), 100–150 Hz (female) |
| Guitar | 80–120 Hz |
| Pads | 150–300 Hz |
| Leads | 150–400 Hz |
| Strings | 80–150 Hz |
| Reverb/delay returns | 200–500 Hz |
| FX, risers, atmospheres | 200–500 Hz |

Use a gentle slope (12 dB/oct) for musical elements and a steep one (24–48) for
surgical removal. **HAZARD:** steep high-pass filters cause phase shift and
pre-ringing near the cutoff; on a kick or bass this audibly weakens the attack.
Use linear-phase or a gentle slope there.

### 2. Cut before you boost

Subtractive EQ (cutting an offending band) sounds more natural than additive.
The workflow: boost a narrow band by +10 dB, sweep it until the ugly resonance
jumps out, then invert to a cut of −3 to −6 dB with a moderate Q.

### 3. Carve for the important element

If two elements fight, **cut the less important one** in the band where the more
important one lives, rather than boosting the important one.

| Pair | Move |
|---|---|
| Kick vs bass | Cut the bass 3–5 dB at the kick's fundamental (50–70 Hz), or vice versa |
| Vocal vs synth | Cut the synth 2–4 dB at 1–3 kHz |
| Snare vs guitar | Cut the guitar around 2 kHz |
| Bass vs guitar | Cut the guitar below 120 Hz completely |
| Pad vs vocal | Cut the pad at 200–500 Hz and 2–4 kHz |
| Hats vs cymbals | Split: hats 8–12 kHz, ride 3–6 kHz |

### 4. Complementary EQ

If you boost element A at 3 kHz, cut element B at 3 kHz by a similar amount.
The perceived separation is far greater than either move alone.

## Typical starting EQ per element

These are *starting points*, not truths. Always listen in context.

### Kick
| Move | Frequency | Amount |
|---|---|---|
| High-pass | 30 Hz | 12 dB/oct |
| Boost (weight) | 50–70 Hz | +2 to +4 dB, Q 1.0 |
| Cut (mud/box) | 200–400 Hz | −3 to −6 dB, Q 1.5 |
| Boost (click) | 2–5 kHz | +2 to +5 dB, Q 1.0 |
| Low-pass (optional) | 10 kHz | to keep it out of the hats' band |

### Bass
| Move | Frequency | Amount |
|---|---|---|
| High-pass | 30 Hz | |
| Cut where the kick sits | 50–70 Hz | −2 to −4 dB, Q 2 |
| Boost (fundamental) | 80–110 Hz | +2 dB |
| Cut (mud) | 250–400 Hz | −2 to −4 dB |
| Boost (definition, phone audibility) | 700 Hz–1.5 kHz | +2 to +4 dB |

### Snare
| Move | Frequency | Amount |
|---|---|---|
| High-pass | 120 Hz | |
| Boost (body) | 180–250 Hz | +2 to +3 dB |
| Cut (box) | 400–600 Hz | −2 to −4 dB |
| Boost (crack) | 1.5–3 kHz | +2 to +4 dB |
| Boost (snap/air) | 7–10 kHz | +2 to +3 dB, shelf |

### Hi-hats
| Move | Frequency | Amount |
|---|---|---|
| High-pass | 400–600 Hz | |
| Cut (harshness) | 3–5 kHz | −2 to −4 dB if brittle |
| Boost (air) | 10–12 kHz | +2 dB, shelf |

### Vocal
| Move | Frequency | Amount |
|---|---|---|
| High-pass | 90–120 Hz | |
| Cut (boom/proximity) | 200–300 Hz | −2 to −4 dB |
| Cut (nasal) | 800 Hz–1 kHz | −2 to −3 dB if honky |
| Boost (presence) | 2–4 kHz | +2 to +4 dB |
| De-ess (dynamic) | 5–9 kHz | −3 to −8 dB, only when it triggers |
| Boost (air) | 10–14 kHz | +2 to +3 dB, shelf |

### Pads and chords
| Move | Frequency | Amount |
|---|---|---|
| High-pass | 150–300 Hz | Aggressively — pads do not need low end |
| Cut (space for vocal/lead) | 1–3 kHz | −2 to −4 dB, wide |
| Low-pass | 8–12 kHz | to sit behind the leads |

### Lead synth
| Move | Frequency | Amount |
|---|---|---|
| High-pass | 200–400 Hz | |
| Cut (mud) | 300–600 Hz | −2 to −3 dB |
| Boost (presence) | 2–5 kHz | +2 to +4 dB |

## Q, slopes and filter types

| Type | Shape | Use |
|---|---|---|
| **Bell / peaking** | boost or cut around a centre frequency | The general-purpose tool |
| **Low shelf** | everything below a point up/down | Broad warmth or thinning |
| **High shelf** | everything above a point | Air, brightness, darkening |
| **High-pass (low-cut)** | removes lows | Cleaning, the most-used filter in mixing |
| **Low-pass (high-cut)** | removes highs | Distance, warmth, taming |
| **Notch** | very narrow deep cut | Killing a resonance or hum |
| **Tilt** | rotates the whole spectrum | Global brightness |

**Q** = centre frequency / bandwidth. Higher Q = narrower.

| Q | Bandwidth | Use |
|---|---|---|
| 0.4–0.7 | ~3 octaves | Broad tonal shaping; sounds "natural" |
| 1.0–1.4 | ~1–1.5 octaves | General-purpose |
| 2–4 | ~1/2 octave | Corrective |
| 8–20 | very narrow | Surgical notch: hum, ring, resonance |

**Rule of thumb: broad boosts, narrow cuts.** A wide +2 dB shelf is invisible;
a wide −6 dB cut removes an instrument's character.

## Dynamic EQ and multiband

- **Dynamic EQ**: a bell that only engages when the band exceeds a threshold.
  Use for: sibilance, boomy vocal notes, a bass that gets muddy only on certain
  pitches, a resonance that appears only when loud. Preferable to static EQ
  whenever the problem is intermittent.
- **Multiband compression**: splits into bands and compresses each. Use for
  controlling low end on a master bus, or taming a mix's harsh 3 kHz band. Easy
  to overuse — it flattens the mix's natural spectral movement.
- **Sidechain EQ**: duck a specific band of element B when element A plays.
  Ducking 60–120 Hz of the bass on every kick is cleaner than ducking the whole
  bass.

## Linear phase vs minimum phase

- **Minimum phase** (normal EQ): introduces phase shift around the cutoff. Sounds
  natural; can smear transients slightly; cheap.
- **Linear phase**: no phase shift, but adds latency and **pre-ringing** — a
  faint artefact *before* transients. Best on mastering EQ and on parallel/
  multi-mic sources where phase relationships matter; worst on percussive
  material with steep cuts.

Default: minimum phase everywhere except mastering and mid/side surgery.

## Mid/side EQ

Process the mono (mid) and stereo (side) content separately.

| Move | Effect |
|---|---|
| High-pass the **side** at 150–300 Hz | Tightens the low end; the standard mastering move |
| Boost highs in the **side** | Widens without affecting the centre |
| Cut 200–500 Hz in the **mid** | Clears space for the vocal without narrowing |
| Boost 2–4 kHz in the **mid** | Brings the vocal/lead forward |

## Resonances and problem frequencies

Common offenders worth knowing:

| Frequency | Problem |
|---|---|
| 50 or 60 Hz | Mains hum (and its harmonics at 100/120, 150/180…) |
| 120–250 Hz | Boominess, proximity effect on vocals |
| 300–500 Hz | Boxy, "cardboard" room resonance |
| 800 Hz–1 kHz | Nasal, honky, "telephone" |
| 2–4 kHz | Harsh, fatiguing, "ice-pick" |
| 5–8 kHz | Sibilance (s, t, sh sounds) |
| 8–12 kHz | Cymbal wash, hiss, digital brittleness |

## Reference spectra

A finished, full-range modern mix roughly follows a **pink-noise-like slope**:
about **−3 to −4.5 dB per octave** above 1 kHz, with a low end that is flat or
slightly raised from 40–120 Hz. Genre variations:

| Genre | Low end (20–120 Hz) | Mids | Highs (8 kHz+) |
|---|---|---|---|
| EDM / trap / dubstep | Very strong, +3 to +6 dB over a pink slope | Scooped | Bright |
| Techno / house | Strong, tight | Present | Controlled |
| Rock / metal | Moderate | Strong 1–4 kHz | Moderate |
| Pop | Strong, controlled | Vocal-forward 2–4 kHz | Very bright |
| Jazz / classical | Natural, unhyped | Natural | Natural, extended |
| Lo-fi | Rolled off below 60 | Warm 200–800 | Rolled off above 8 k |

## Practical EQ workflow

1. **Fix the arrangement first.** If two parts occupy the same band and both must
   be heard, the real fix is transposing one, changing its timbre, or removing
   it. EQ is a last resort for an arrangement problem.
2. **High-pass everything** per the table above.
3. **Cut the mud** (200–500 Hz) on the elements that do not need it.
4. **Balance with faders**, not EQ, first.
5. **Carve** where things clash, by cutting.
6. **Boost** only for character, at the end, and gently.
7. **Check in mono.** Mono reveals masking that stereo hides.
8. **Check at low volume.** If the balance holds at a whisper, it holds anywhere.

## HAZARDS

- **Boosting to fix a balance problem** — turn a fader instead.
- **High-passing the kick or bass too high** — 40 Hz is already too high for
  club music.
- **EQ'ing in solo** — masking only exists in context. Always EQ while the full
  mix plays.
- **Matching a "reference EQ curve" blindly** — the curve is a consequence of
  good arrangement, not a cause.
- **Too many EQ bands** — if an element needs 8 bands of correction, the source
  is wrong. Re-record or re-synthesise it.
- **Forgetting that filters have gain** — resonant filters and shelves change
  loudness; the "better" version may just be the louder one. Level-match before
  judging.

## Related

- What creates the frequency content: `12-timbre-and-synthesis.md`
- Level control: `14-dynamics-and-compression.md`
- The full mixing process: `16-mixing-process.md`
- Mastering EQ specifically: `17-mastering.md`
