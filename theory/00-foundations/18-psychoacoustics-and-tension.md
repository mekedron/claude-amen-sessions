# Psychoacoustics, Expectation and Tension

Music works because of how hearing and prediction work. This file is the "why"
underneath most of the rest of the library.

## Hearing is not a spectrum analyser

| Phenomenon | What it means | Practical consequence |
|---|---|---|
| **Equal-loudness contours** (Fletcher–Munson) | The ear is most sensitive around 2–5 kHz and much less sensitive to lows and extreme highs, and this changes with level | A mix balanced at low volume will sound bass-heavy loud, and vice versa. Mix at moderate level; check at several |
| **Critical bands** | The cochlea resolves frequency into ~24 bands; two tones in the same band interact | Two sounds within a critical band mask each other regardless of how you EQ them |
| **Masking (simultaneous)** | A loud sound hides a quieter one nearby in frequency, more so *above* it | Arrange so important elements do not share bands; this is the whole basis of EQ carving |
| **Masking (temporal)** | A loud sound hides quieter sounds ~5 ms before and up to 200 ms after it | You can hide artefacts just after a transient; and a kick genuinely erases what follows it |
| **Missing fundamental** | Given harmonics at 100, 150, 200 Hz, the ear hears a 50 Hz pitch that is not there | This is why a saturated bass sounds deep on a phone speaker |
| **Precedence / Haas effect** | The first arrival within ~35 ms determines perceived direction | Delay-based widening; also why early reflections define room size |
| **Loudness ≠ amplitude** | Perceived loudness depends on duration (integration ~200 ms), spectrum and density | A short peak can be much quieter than a sustained tone at the same dBFS |
| **Ear fatigue** | Sensitivity to highs falls after sustained loud listening | Mixes made late get progressively brighter and harsher |

### Practical loudness rules

- **+10 dB ≈ twice as loud** (subjectively). +3 dB is "slightly louder", +6 dB is
  "clearly louder".
- **A 1 dB change is roughly the smallest that matters** in a mix balance; 0.5 dB
  is audible on a solo element in a critical listen.
- **Density raises loudness more than level does.** A dense, saturated mix at
  −10 LUFS sounds louder than a sparse one at −8.
- **Brightness reads as loudness.** This is why the ear is fooled by an EQ boost
  and why level-matching must precede every A/B.

## Expectation: the engine of musical emotion

Listening is prediction. The brain constantly forecasts what comes next based on
everything it has heard — in this track, in this genre, and in its whole life.
**Emotion happens in the gap between prediction and outcome.**

Four outcomes, and what they feel like:

| Prediction | Outcome | Feeling |
|---|---|---|
| Confident | Confirmed | Satisfaction, groove, comfort |
| Confident | Violated | Surprise, shock, humour, drama |
| Uncertain | Confirmed | Relief, "aha", resolution |
| Uncertain | Violated | Confusion, unease, disorientation |

Great music alternates. Pure confirmation is boring; pure violation is noise.
The usual ratio is roughly **80% confirmation, 20% violation**, with the
violations placed at structurally important moments.

### How to build a confident prediction

Repetition. That is it. Four repetitions of a two-bar loop and the listener is
certain what bar 9 will be. Now you have something to break.

### How to violate it well

| Device | Level |
|---|---|
| A ghost note appears | Micro — texture |
| A chord arrives a beat early | Small — groove interest |
| The expected chord is replaced (deceptive cadence) | Medium — emotional |
| The downbeat is silent | Large — attention |
| The drop is halftime instead of the expected pattern | Large — structural |
| The key changes | Large |
| The genre changes | Extreme — use once |

**Rule:** the size of the violation should match the structural importance of
the moment. A shocking event in bar 3 of a verse is a mistake; the same event at
the drop is the point of the track.

## Tension and release

Tension is accumulated expectation that has not yet been satisfied. It can be
created in any dimension, and dimensions add:

| Dimension | Tension | Release |
|---|---|---|
| Harmony | Dominant, unresolved dissonance, pedal | Tonic, consonance |
| Melody | High register, leading tone, held note | Descent to the tonic, resolution |
| Rhythm | Syncopation, accelerating subdivisions, missing downbeat | Downbeat, straight pattern |
| Register | Rising, high-passed (no bass) | The bass returns, full spectrum |
| Loudness | Crescendo | Arrival, or a sudden drop to quiet |
| Density | Adding layers | Everything at once, or sudden sparseness |
| Space | More reverb, more delay | Dry, immediate |
| Timbre | Opening filter, growing distortion | The full sound |

**The build-up in dance music stacks all eight simultaneously.** That is why it
works, and why a build that raises only volume feels flat.

### The silence trick

A gap of 1 beat to 1 bar immediately before a big arrival is the single most
effective device in modern music. Reasons:

1. It removes masking, so the arrival hits a rested ear.
2. It removes the prediction's confirmation for a moment, maximising uncertainty.
3. Contrast: 0 dB against −10 dB feels enormous even if the arrival is not
   objectively loud.

Use it twice per track. Three times and it stops working.

## Groove and entrainment

Why the body moves:

- The brain **entrains** to a periodic pulse — internal oscillators lock to it.
  This is why a steady tempo matters more than a "correct" tempo.
- **Syncopation creates the urge to move.** A rhythm that is entirely on the
  beat is predictable and static; one that is entirely off the beat has no
  reference. The pleasure peak is at **moderate syncopation** — enough that the
  body must supply the missing beat itself.
- **The optimal tempo for movement is 120–130 BPM** — close to a fast walking
  pace and to the resonant frequency of the human body's natural motion. Genres
  cluster around it, or at 2× / ½× of it.
- **Low frequencies drive movement more than high ones.** The vestibular system
  responds to bass; this is measurable, and it is why sub bass is worth its
  headroom cost.

## Repetition and the "mere exposure" effect

- Familiarity increases liking, up to a point, then reverses (the inverted-U).
- This is why hooks repeat, why a loop can carry 6 minutes of techno, and why
  every song has a chorus that returns.
- It is also why the second half of a track must add *something* — the same
  material with no new information crosses the peak of the curve.
- **A listener needs to hear a hook 3–4 times before it is "theirs".** Structure
  the arrangement so the hook returns that many times.

## Emotional associations — a working table

These are cultural conventions, not universals. They are still reliable for
listeners raised on Western popular music.

| Element | Association |
|---|---|
| Major mode | Happy, bright, resolved, simple |
| Minor mode | Sad, serious, dramatic, "cool" |
| Fast tempo | Excitement, urgency, joy, anxiety |
| Slow tempo | Reflection, sadness, grandeur, intimacy |
| High register | Light, delicate, tense, distant, feminine-coded |
| Low register | Heavy, powerful, threatening, masculine-coded |
| Consonance | Peace, resolution, safety |
| Dissonance | Conflict, unease, complexity, modernity |
| Loud + dense | Power, aggression, celebration |
| Quiet + sparse | Intimacy, loneliness, suspense |
| Reverb, large | Space, awe, isolation, memory |
| Dry, close | Presence, intimacy, aggression, modernity |
| Rising line | Hope, effort, anticipation |
| Falling line | Resignation, resolution, sadness |
| Regular meter | Stability, march, machine |
| Irregular meter | Unease, cleverness, folk exoticism |
| Distortion | Aggression, energy, decay, authenticity |
| Clean / pure tone | Precision, cold, digital, purity |
| Wide stereo | Big, enveloping, "produced" |
| Mono / narrow | Focused, retro, direct, urgent |
| Lo-fi, filtered | Nostalgia, memory, distance, intimacy |
| Slow attack | Dreamlike, gentle, arriving |
| Fast attack | Immediate, percussive, real |

## Attention and the timeline

- **The first 5–15 seconds** decide whether a listener stays. Streaming skip
  rates are highest here.
- **Attention decays** after 30–40 seconds of unchanged material.
- **Novelty resets attention.** One new element every 8–16 bars is roughly the
  right rate for dance music; every 4–8 bars for pop.
- **The peak of a track should arrive around 60–75% of the way through.**
  This is where the second drop or final chorus belongs.
- **People remember beginnings and endings** (primacy and recency). Spend
  disproportionate effort on the intro and the last 15 seconds.

## Emotional arc design

A working method: write the emotional story in words first, then translate.

```
"Alone in a big empty space"     → sparse, high reverb, low density, minor, slow
"Something is approaching"       → rising line, accelerating subdivision, filter opening
"It arrives"                     → full spectrum, everything at once, dry
"Doubt"                          → drop to a breakdown, remove the bass, add dissonance
"Resolve, bigger than before"    → the drop, plus one new element and a wider image
"It's over"                      → subtraction, decay, silence
```

Every arrangement decision then has an answer to "why?" that is not "because
that's the template".

## HAZARDS

- **No contrast** — the mix is technically fine but nothing feels like anything.
- **Constant surprise** — every bar different; no predictions form, so no
  violations land.
- **Building tension and never releasing it** — exhausting.
- **Releasing without building** — the drop lands on nothing.
- **Mixing tired** — you will make it too bright, too loud, and too compressed.
- **Judging loudness without level-matching** — you will choose the louder
  version every time, regardless of quality.
- **Assuming the associations table is universal** — it describes a specific
  listening culture. If you are writing outside it, learn its conventions.

## Related

- Tension in harmony: `06-harmony-function.md`
- Tension in arrangement: `11-form-and-arrangement.md`
- The drop as a tension machine: `../30-patterns/02-drop-and-buildup.md`
- Loudness measurement: `17-mastering.md`
