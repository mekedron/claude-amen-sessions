# Stereo, Depth and Space

A mix is a three-dimensional image: **left–right** (pan and width),
**front–back** (depth), and **up–down** (frequency). This file covers the first
two, and the effects that create them.

## How the ear locates sound

| Cue | Mechanism | Frequency range |
|---|---|---|
| **ILD** (level difference) | One ear is louder | Above ~1.5 kHz |
| **ITD** (time difference) | One ear hears it first (up to ~0.7 ms) | Below ~1.5 kHz |
| **Precedence / Haas effect** | The first arrival within ~1–35 ms determines the perceived direction, even if the later one is louder | All |
| **Spectral cues (HRTF)** | The pinna filters differently by angle | Above ~5 kHz |
| **Direct/reverb ratio** | More reverb = further away | All |
| **High-frequency loss** | Air absorbs highs over distance | All |

Practical consequences: **panning by level works best above 1 kHz**; low
frequencies are inherently non-directional (hence mono bass); and **delay-based
widening breaks in mono** while level-based panning does not.

## Panning

| Position | Elements |
|---|---|
| Centre | Kick, snare, bass, sub, lead vocal, main hook |
| ±10–25% | Doubled vocals, secondary percussion, rhodes |
| ±30–50% | Guitars, pads, hats, arps, counter-melodies |
| ±60–100% | Ear candy, ad-libs, delays, one-shot fx, wide reverb |

Rules:

1. **The four foundations stay centre**: kick, snare, bass, lead vocal. Everything
   else is negotiable.
2. **Pan in pairs.** If something goes 40% left, something of similar weight goes
   40% right — otherwise the image tilts.
3. **Pan for arrangement, not for space.** Two competing mid-range parts panned
   apart are both audible; the same parts centred are mud.
4. **LCR mixing** (hard left, centre, hard right only) is a legitimate discipline
   that produces very clear mixes; it comes from classic rock and hip-hop.

**Equal-power panning** keeps perceived loudness constant across the pan
positions: `left = cos(θ)`, `right = sin(θ)`, where `θ = (pan+1) * π/4` for pan
in [−1, 1]. A naive linear pan law makes centred material sound quieter.

## Width and stereo image

| Technique | How | Mono safety |
|---|---|---|
| **True stereo source** | Recorded or synthesised in stereo | Depends |
| **Detune spread** | Multiple voices, different pitches, different pans | Excellent |
| **Haas / micro-delay** | Delay one side by 5–35 ms | **Poor** — comb filtering in mono |
| **Mid/side EQ** | Boost the side signal's highs | Good |
| **Chorus / ensemble** | Modulated delays, inverted per channel | Fair |
| **Stereo reverb** | Different early reflections per side | Good |
| **Ping-pong delay** | Echoes alternate channels | Good |
| **Double-tracking** | Two separate performances, panned apart | Excellent — the best method |
| **Polarity flip on one channel** | Left = −right | **Never.** Vanishes in mono |

**The width rule:** width is only perceptible by contrast. If everything is wide,
nothing is. Keep a narrow core (kick, snare, bass, lead) and let a few elements
be genuinely wide.

**Frequency and width:**

| Band | Width |
|---|---|
| Below 120 Hz | Fully mono, always |
| 120–300 Hz | Narrow |
| 300 Hz–3 kHz | Moderate; this is where the "core" lives |
| Above 3 kHz | Wide is fine and pleasant |

## Mono compatibility

Check every mix in mono. Reasons: club systems often sum the low end or the
whole signal, phone speakers are mono, Bluetooth speakers are mono, and a
significant fraction of listening is single-earbud.

What breaks in mono:
- Haas-delayed doubles (comb filtering, hollow sound).
- Out-of-phase stereo wideners (elements vanish entirely).
- Wide detuned basses (cancellation and level loss).
- Stereo reverb with inverted phase content.

If an element loses more than a couple of dB when summed to mono, fix it.

## Depth — front to back

Four independent tools, in order of importance:

1. **Level.** Quieter = further. The most powerful and most obvious.
2. **High-frequency content.** Distant sounds lose highs. A gentle low-pass at
   4–8 kHz pushes an element back.
3. **Reverb amount (direct/wet ratio).** More wet = further.
4. **Pre-delay.** *Short* pre-delay (0–10 ms) = the source is far away (its early
   reflections arrive almost with the direct sound). *Long* pre-delay (20–60 ms)
   = the source is close in a large room.
5. **Transient sharpness.** Softening the attack pushes an element back.

**A mix with everything at the same depth sounds flat.** Deliberately place:
one element right at the front (vocal, kick), a middle plane (chords, bass),
and a far plane (pads, atmosphere).

## Reverb

Reverb is the sum of thousands of reflections. What you control:

| Parameter | Effect | Typical values |
|---|---|---|
| **Type / algorithm** | The character of the space | see below |
| **Size** | Perceived room dimensions | small–hall |
| **Decay (RT60)** | Time to fall 60 dB | 0.2 s (room) to 10 s+ (cathedral/ambient) |
| **Pre-delay** | Gap before the reverb starts | 0–120 ms |
| **Damping / tone** | How fast highs decay | Low-pass 3–8 kHz on the tail |
| **Diffusion** | Density of reflections | Low = discrete echoes, high = smooth wash |
| **Early reflections** | The first distinct bounces | Define room size and character |
| **Wet/dry** | Blend | Use a send, not an insert, so it is shared |
| **Width** | Stereo spread of the tail | Usually wide |

### Reverb types

| Type | Character | Use |
|---|---|---|
| **Room** (0.3–0.8 s) | Small, natural, tight | Drums, glue, realism |
| **Chamber** (0.8–1.8 s) | Smooth, medium | Vocals, strings |
| **Hall** (1.5–4 s) | Large, lush, slow build | Orchestral, pads, epic |
| **Plate** (1–3 s) | Bright, dense, no early reflections | Vocals, snares — the classic pop reverb |
| **Spring** | Boingy, resonant, metallic | Dub, surf guitar, lo-fi |
| **Convolution** | An actual measured space | Realism, or exotic impulse responses |
| **Shimmer** | Reverb with pitch-shifted (+12) feedback | Ambient, cinematic, worship |
| **Non-linear / gated** | Truncated tail | 1980s drums |
| **Reverse** | Tail before the sound | Transitions, dreamlike |

### Reverb rules

1. **Use sends, not inserts.** Two or three shared reverbs (a short one for
   cohesion, a long one for depth) glue a mix; twenty separate reverbs do not.
2. **High-pass the reverb return** at 200–500 Hz. Low frequencies in a reverb
   tail are the fastest route to mud.
3. **Low-pass the return** at 5–10 kHz. Real rooms absorb highs.
4. **Pre-delay preserves clarity.** 20–40 ms of pre-delay lets the dry transient
   through before the wash arrives — the vocal stays intelligible *and* big.
   Sync it: a 1/32 or 1/16 note pre-delay locks the reverb to the groove.
5. **Duck the reverb** with a sidechain from the dry signal so the tail blooms
   between phrases.
6. **Never reverb the sub bass or the kick's low end.**
7. **Decay should fit the tempo.** A tail that has not died before the next hit
   creates a wash. RT60 ≈ one bar is a useful maximum for rhythmic material.

## Delay

| Type | Description | Use |
|---|---|---|
| **Slapback** (60–140 ms, 1 repeat) | A single close echo | Rockabilly, vocals, lo-fi |
| **Tempo-synced** (1/8, 1/8 dotted, 1/4) | Rhythmic repeats | Everything; dotted 1/8 is the "U2/EDM" delay |
| **Ping-pong** | Alternating channels | Width, movement |
| **Dub delay** | Long feedback, filtered, saturated, with the feedback pushed into self-oscillation | Dub, reggae, techno |
| **Multi-tap** | Several taps at different times/pans | Complex rhythmic space |
| **Reverse delay** | Repeats played backwards | Dreamlike, transitions |
| **Diffuse / blurred delay** | Heavily filtered and modulated | Ambient texture |

Delay times (see `../40-reference/03-bpm-and-timing-tables.md` for a full table):
`ms = 60000 / BPM × note_fraction × 4`. Dotted 8th = 0.75 of a beat.

**Delay vs reverb:** delay creates space without the density that clouds a mix.
For busy modern productions, a filtered tempo-synced delay is usually a better
depth tool than reverb. Combine them: delay into reverb (send the delay return
to the reverb) produces enormous, controlled space.

**Feedback filtering** is what makes delays sound professional: each repeat
should be darker than the last (low-pass 3–5 kHz in the feedback path, dropping
further with each repeat).

## Modulation effects

| Effect | Mechanism | Character |
|---|---|---|
| **Chorus** | Short delays (10–30 ms) modulated slowly, mixed with dry | Thick, wide, 80s |
| **Flanger** | Very short delay (0.5–10 ms) modulated, with feedback | Jet, whoosh, metallic |
| **Phaser** | All-pass filters creating moving notches | Swirling, less metallic than flanger |
| **Tremolo** | Amplitude LFO | Rhythmic pulsing |
| **Vibrato** | Pitch LFO | Expressive, or seasick |
| **Rotary / Leslie** | Doppler + amplitude modulation from a spinning speaker | Organ, psychedelic |
| **Ensemble** | Multiple chorus voices | Lush strings, Juno pads |

## Space as arrangement

Space is not decoration; it is structure.

- **Verse dry, chorus wet** — the most common depth arrangement in pop.
- **Breakdown = maximum reverb**, drop = almost none. The contrast makes the
  drop feel like the roof coming off.
- **Kill the reverb on the last beat before a drop.** Sudden dryness reads as
  "here it comes".
- **Throw** effects: send a single word, hit or note to a long delay/reverb, then
  close the send. The classic dub technique, and the easiest way to make a
  repetitive loop feel alive.
- **Reverse reverb into a downbeat** to signal an arrival.
- Depth also implies **era**: dry and close = modern/hip-hop; long plate =
  1970s; huge gated = 1980s; giant hall = cinematic.

## HAZARDS

- **Reverb on everything** — the mix loses focus and the low-mids fill up.
- **Reverb on the bass or kick sub** — mud, instantly.
- **Same reverb, same settings, on all elements** — everything sits at the same
  depth; the image is flat.
- **Stereo wideners on the master** — usually cost more in mono compatibility
  than they give in width.
- **Haas widening on anything that must survive mono.**
- **Long reverb at fast tempos** — at 174 BPM a 3-second tail is over four bars
  of wash covering everything.
- **Delays that are not tempo-synced in a rhythmic genre** — sounds accidental.

## Related

- Frequency and width interaction: `13-frequency-and-eq.md`
- Timing values: `../40-reference/03-bpm-and-timing-tables.md`
- Using space to build sections: `11-form-and-arrangement.md`
