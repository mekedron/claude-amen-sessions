# Effects and Processors

The devices that shaped records as much as the instruments did. In electronic
music the effect is frequently the instrument.

---

## Echo and delay

### Roland RE-201 Space Echo (1974)
**Type:** tape echo with three playback heads and a spring reverb.

| Control | Effect |
|---|---|
| **Mode selector** | Which combination of the three heads is active — different rhythmic patterns |
| **Repeat rate** | Tape speed; changing it while echoes are ringing **pitch-shifts them** |
| **Intensity** | Feedback; past ~7 it self-oscillates into howling chaos |
| **Bass/Treble** | Tone of the repeats |
| **Reverb** | The spring, mixable |

Why it matters: tape saturation, wow and flutter, and progressive high-frequency
loss mean each repeat is darker, warmer and slightly detuned. **Dub was built on
this box** (King Tubby, Lee "Scratch" Perry used similar units), and so was a
great deal of techno, psychedelia and ambient.

**Rebuild:** a delay line with (1) a low-pass in the feedback path that gets
darker each pass (start at ~4 kHz, drop ~15% per repeat), (2) saturation in the
feedback path, (3) ±5–15 cents of slow random pitch drift, (4) feedback capable
of exceeding 100% with a limiter after it.

### Other landmark delays
| Unit | Contribution |
|---|---|
| **Echoplex EP-3** (tape) | The warm rockabilly/Hendrix slapback |
| **Binson Echorec** (magnetic drum) | Pink Floyd's multi-head rhythmic echoes |
| **Electro-Harmonix Memory Man** (BBD) | Analog chorus-echo; The Edge, post-punk |
| **Roland SDE-3000** (digital, 1983) | Clean, tempo-set delays; the 80s |
| **Boss DD-3** | The pedal standard |

---

## Reverb

| Unit | Year | Character | Use |
|---|---|---|---|
| **EMT 140 plate** | 1957 | Bright, dense, no early reflections | Vocals, snares — the classic pop reverb |
| **EMT 250** | 1976 | The first digital reverb; lush, distinctive | Everything expensive in the late 70s |
| **Lexicon 224** | 1978 | Wide, smooth, slightly grainy | The 80s "big" sound; ambient |
| **Lexicon 480L** | 1986 | The studio standard for 20 years | Pop, film |
| **AMS RMX16** | 1982 | Its **"NonLin"** program is the gated reverb | Phil Collins's drum sound; all of 80s pop |
| **Yamaha SPX90** | 1985 | Cheap, characterful; reverse and gated presets | 80s everything |
| **Alesis Microverb/Quadraverb** | 1986/89 | Affordable digital; grainy | Early house, hip-hop |
| **Spring reverb** (Fender, Roland) | 1960s | Boingy, metallic, splashy | Surf, dub, lo-fi |
| **Valhalla Shimmer** (software) | 2010 | Pitch-shifted feedback | Modern ambient, worship, cinematic |

### Gated reverb — the 1980s in one effect
A large, bright reverb followed by a **noise gate keyed to the dry signal**, so
the tail is chopped off abruptly after 200–400 ms.

**Rebuild:** reverb (decay 2–4 s, bright, no pre-delay) → gate with a hold of
150–300 ms and a very fast release → mix well up, sometimes louder than the dry
snare.

### Shimmer reverb
Pitch-shift the reverb's **feedback path** up an octave (and sometimes down one
too). Each pass rises, producing an infinite ascending choir.

**Rebuild:** reverb → +12 semitone pitch shift → back into the reverb input at
40–70% → low-pass in the loop to stop it screaming.

---

## Modulation

| Unit | Effect | Notes |
|---|---|---|
| **Roland Dimension D** (1979) | Chorus | Four fixed settings, no controls to get wrong; adds width without obvious warble. On countless 80s records |
| **Juno / Solina BBD chorus** | Chorus | Noisy, wide, the definition of "warm analog" |
| **MXR Phase 90 / Small Stone** | Phaser | Funk keys, Van Halen, krautrock |
| **A/DA Flanger, Electric Mistress** | Flanger | Jet-plane sweeps |
| **Leslie** | Rotary | See `04-electromechanical-keyboards.md` |
| **Uni-Vibe** | Rotary-ish phaser | Hendrix, Pink Floyd |

**Chorus rebuild:** 2–3 delay lines of 10–30 ms, each modulated by an LFO at a
different slow rate (0.3–2 Hz) and depth (2–8 ms), panned apart, mixed with dry.
**Flanger:** one delay of 0.5–10 ms, modulated, **with feedback**. **Phaser:**
4–12 all-pass stages with modulated centre frequencies, mixed with dry.

---

## Pitch and frequency manipulation

| Unit | Contribution |
|---|---|
| **Eventide H910 Harmonizer** (1975) | The first practical pitch shifter; David Bowie's *Low* snare (shifted down with feedback), doubling |
| **Eventide H3000** (1986) | Micro-pitch detuning (±7–20 cents on each side) for width; "crystal" reverse pitch effects; the sound of 80s/90s big productions |
| **Publison Infernal Machine** | Early pitch/delay; French electronic music |
| **DigiTech Whammy** | Extreme real-time pitch bends |
| **Antares Auto-Tune** (1997) | See `11-chips-trackers-and-voices.md` |
| **Celemony Melodyne** (2001/2009) | Polyphonic pitch editing |

**Micro-pitch widening** is worth knowing: duplicate a mono signal, pitch one
copy +8 cents and the other −8 cents, delay them by ~15 and ~22 ms, pan hard
left and right. This is how vocals and leads are widened on professional records
without a chorus's obvious warble.

---

## Distortion and saturation

| Type | Character | Typical use |
|---|---|---|
| **Tube / valve** | Even harmonics, warm, compressing | Warmth, glue |
| **Tape** | Soft compression, high-frequency loss, hysteresis | Cohesion, vintage |
| **Transformer** | Low-frequency saturation | Weight |
| **Transistor / op-amp clipping** | Odd harmonics, hard | Aggression |
| **Fuzz** | Extreme square-wave clipping | Guitar, lo-fi |
| **Bitcrush** | Inharmonic quantisation noise | Digital grit |
| **Wavefolder** | Inharmonic, metallic | West coast, screech design |
| **Multiband distortion** | Per-band aggression, controlled low end | **Bass music — essential** |

**The bass-music rule:** never distort the sub. Split at ~100 Hz, keep the low
band clean, destroy the upper band, recombine. Plugins like Ohmicide,
Camel Crusher and Trash exist for exactly this.

---

## Dynamics with a character

| Unit | Why it matters |
|---|---|
| **Fairchild 670** (1959) | Vari-mu; the most expensive glue in existence |
| **Teletronix LA-2A** (1965) | Opto; slow, smooth, program-dependent. Vocals, bass |
| **UREI 1176** (1967) | FET; very fast attack, aggressive. Drums, vocals; the "all-buttons-in" mode is a distortion effect |
| **dbx 160** | VCA; punchy, snappy. Snares, kicks |
| **SSL bus compressor** | The "mix glue" sound of the 80s onward |
| **Ableton OTT / multiband upward compression** | The modern EDM density sound |

---

## Performance and rhythmic effects

| Device | Idea |
|---|---|
| **Korg Kaoss Pad** (1999) | XY-pad control of effects as performance |
| **Pioneer DJM / Allen & Heath Xone filters** | The DJ mixer's filter knob as a compositional tool |
| **Gross Beat** (FL) | Time and volume curves on a bar grid: stutter, freeze, scratch, reverse |
| **Effectrix / ShaperBox / Portal** | Step-sequenced effect chains — gate, reverse, stretch, granular per 16th |
| **Beat repeat / stutter** | Retrigger the last fraction of a bar with pitch and rate changes |
| **Turntablism** | The record itself as an instrument: scratching, the crab, the transformer, the baby scratch |

---

## The dub technique, generalised

Dub engineers in 1970s Kingston invented a way of working that now underlies
most electronic music:

1. **Mute and unmute parts live**, as the arrangement.
2. **Throw single hits into long echo** — the effect send is played like an
   instrument.
3. **Push the delay feedback into self-oscillation**, then pull it back.
4. **Sweep a high-pass filter across the whole mix.**
5. **Keep drums and bass constant** while everything else appears and vanishes.
6. **Use the reverb as a place**, not as a coating.

Any loop-based track becomes an arrangement if you do these six things to it.

---

## Effect order matters

| Chain | Result |
|---|---|
| Distortion → filter | Controlled: the filter tames the harmonics distortion created |
| Filter → distortion | Aggressive: distortion acts on the filtered shape, creating new harmonics above the cutoff |
| Reverb → distortion | The reverb tail itself distorts — dense, gritty, unnatural, useful |
| Distortion → reverb | Normal, clean space around a dirty sound |
| Delay → reverb | Repeats get progressively more distant — huge and controlled |
| Reverb → delay | Each echo carries a full reverb — washy, often too much |
| Compression → modulation | Even, consistent modulation depth |
| Modulation → compression | The compressor fights the modulation, creating pumping |

## Related

- Effect theory: `../00-foundations/15-stereo-and-space.md`
- Compression theory: `../00-foundations/14-dynamics-and-compression.md`
- Transitions: `../30-patterns/06-transitions-and-fx.md`
