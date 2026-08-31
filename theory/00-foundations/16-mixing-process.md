# The Mixing Process

Mixing is turning a set of parts into one coherent object. It is 20% technical
correction and 80% deciding what matters.

## The one question

**At every moment of the track, what is the listener supposed to be paying
attention to?** Everything else exists to support that. A mix has exactly one
focus at a time; if two elements are equally important, neither is.

## Gain staging

Do this before touching a single processor.

1. **Peak levels of individual tracks**: aim for around **−12 to −18 dBFS**
   peak. Not because of headroom on the master (in floating point there is
   plenty) but because analogue-modelled processors are calibrated for it and
   because it leaves room to sum without constantly re-adjusting.
2. **Master bus should never clip during mixing.** Leave the master fader at 0
   and turn things down instead.
3. **Aim for the mix bus to peak around −6 dBFS** before mastering. This is the
   headroom the mastering stage needs.
4. **Level-match every A/B comparison.** Louder always wins for the first ten
   seconds. If you cannot match levels, you cannot judge processing.

Summing maths worth knowing:

| Situation | Level change |
|---|---|
| Two identical (correlated) signals | +6 dB |
| Two uncorrelated signals of equal level | +3 dB |
| `n` uncorrelated signals | +10·log10(n) dB |
| Doubling a fader value (linear gain ×2) | +6 dB |
| Halving perceived loudness | about −10 dB |

## The order of work

There is no single correct order, but this one fails least often:

1. **Fix the arrangement.** Mute-test every element. If nothing is lost when it
   is gone, delete it. Most "mix problems" are arrangement problems: too many
   elements in the same register at the same time.
2. **Gain stage** and set rough static levels with faders only, in mono.
3. **Balance the foundation**: kick, bass, snare, lead vocal/hook. If those four
   are right, the rest falls into place.
4. **Subtractive EQ**: high-pass everything, cut mud.
5. **Compression**: control the dynamics that need controlling.
6. **Panning and width.**
7. **Depth**: sends to reverb and delay.
8. **Additive EQ and saturation**: character, brightness, excitement.
9. **Automation**: the step that separates good from great.
10. **Bus processing and glue.**
11. **Reference and revise.**

## Balance: the numbers

There is no universal set of levels, but these relationships hold across most
modern productions:

| Element | Relative to the loudest element |
|---|---|
| Kick | 0 (reference) |
| Snare/clap | −1 to −4 dB |
| Bass | −2 to −5 dB (but higher RMS than anything) |
| Lead vocal | −2 to −5 dB (peak), and the most *consistent* level |
| Hats | −12 to −20 dB |
| Percussion | −15 to −22 dB |
| Chords / pads | −8 to −15 dB |
| Lead synth | −5 to −10 dB |
| Backing vocals | −8 to −14 dB below the lead |
| FX / risers | −10 to −20 dB, briefly louder at transitions |
| Reverb returns | −15 to −25 dB |

**Genre-defining balances:**

| Genre | What is loudest | What is quiet |
|---|---|---|
| Techno / house | Kick, then bass | Everything else, deliberately |
| Trap | 808 and kick | Everything; vocals sit *in* the beat |
| Pop | Vocal, always | Drums support, never compete |
| Rock | Vocal and snare | Bass supports |
| D&B | Break and bass equally | Melody is atmosphere |
| Dubstep | Bass, then drums | Melody is an intro device |
| Ambient | Nothing dominates | Everything is texture |
| Jazz / classical | Nothing — natural balance | Dynamics are the performance |

## Buses and groups

Organise before processing:

```
Master
├── Drum bus        (kick, snare, hats, perc) → glue compression, saturation
├── Bass bus        (sub, mid bass) → mono below 120 Hz, gentle compression
├── Music bus       (chords, pads, leads, arps) → shared EQ, sidechain from kick
├── Vocal bus       (lead, doubles, harmonies) → compression, de-ess, presence EQ
└── FX returns      (reverb short, reverb long, delay) → high-pass, tone
```

Advantages: one fader controls a whole section, glue compression across a group
sounds cohesive, and sidechaining a bus is cleaner than sidechaining ten tracks.

**Drum bus glue**: 2:1, 10–30 ms attack, auto release, 2–4 dB GR, plus gentle
saturation. This is the single most reliable "make the drums sound like a record"
move.

## Automation — the most underused tool

Static mixes sound static. Things worth automating:

| Parameter | Why |
|---|---|
| **Vocal level, word by word** | Even after compression; this is what makes vocals sit perfectly |
| **Filter cutoff over sections** | Builds and releases energy without changing arrangement |
| **Reverb/delay send amounts** | Wet in breakdowns, dry in drops |
| **Element levels per section** | The pad is louder in the breakdown than in the drop |
| **Panning** | Slow movement over 32 bars adds life |
| **Saturation / drive** | More distortion as the track intensifies |
| **Stereo width** | Narrow in the verse, wide in the chorus |
| **Master EQ tilt** | Slightly brighter in the final chorus |

Rule of thumb: **if a section repeats, something must be automated differently
the second time.**

## Referencing

1. Pick 2–3 commercially released tracks in your genre that you want to sit
   alongside.
2. Import them into the session, and **level-match to your mix using LUFS**, not
   peak.
3. Compare: low-end weight, vocal position, brightness, width, and how loud the
   drums are relative to everything.
4. Switch back and forth every few seconds. Long listens deceive.
5. **Reference on multiple systems**: monitors, headphones, laptop speaker,
   phone speaker, car if possible. Anything that survives a phone speaker is
   mixed. Especially check: is the bass still implied on a device with no bass?
   (That is what mid-range harmonics of the bass are for.)

## Common mix problems and their causes

| Symptom | Likely cause | Fix |
|---|---|---|
| Muddy | Too much 200–500 Hz across many elements | High-pass, cut mud, reduce layer count |
| Boomy | Too much 60–120 Hz, or room resonance | Cut, check the low end in mono |
| Harsh / fatiguing | 2–5 kHz build-up | Cut on multiple sources, reduce distortion |
| Thin | Over-high-passing, no low-mids, everything wide | Reinstate 150–400 Hz, narrow the core |
| No punch | Over-compression, fast attacks | Slower attacks, less GR, transient shaping |
| Vocal buried | Masking at 1–4 kHz | Carve the competing elements, not boost the vocal |
| Bass inaudible on small speakers | No harmonics above 100 Hz | Saturate the bass, add a mid layer |
| Kick disappears at loud volumes | Bass masking it | Sidechain, or split the frequencies |
| Small / narrow | Everything mono and dry | Add width to non-core elements, add depth |
| Washy | Too much reverb, no pre-delay | High-pass returns, add pre-delay, use delay instead |
| Cluttered | Too many elements | Arrangement fix; mute something |
| Amateur-sounding but nothing is "wrong" | No automation, no dynamic contrast between sections | Automate |

## Mixing in mono

Do the first hour of every mix in mono. Reasons:

- Masking is exposed; in stereo the ear separates things that will not separate
  on a phone or in a club.
- Phase problems become obvious.
- Balance decisions made in mono hold up everywhere.

Switch to stereo for panning, width and depth, then check mono again at the end.

## Listening practice

- **Low volume** reveals balance. If the mix works at conversation level, the
  balance is right.
- **Loud, briefly** reveals low end and harshness. Do not stay there — ear
  fatigue sets in within minutes and you will make everything too bright.
- **Take breaks.** Every 45–60 minutes. Fatigue is the biggest cause of bad
  decisions.
- **The next morning** is the best mix engineer you have.

## HAZARDS

- **Mixing while writing.** Separate the modes; you will fix compositional
  problems with EQ, which never works.
- **Soloing.** Almost all decisions should be made in context.
- **Chasing a reference's loudness during mixing.** Loudness is mastering's job.
- **Adding processing to every channel because it is there.** An untouched
  channel that sounds right is finished.
- **Mixing at one volume.** Vary it.
- **Never checking mono.**
- **Believing the meters over the ears** — or the ears over the meters. Use both.

## Related

- The EQ moves: `13-frequency-and-eq.md`
- The dynamics: `14-dynamics-and-compression.md`
- Space: `15-stereo-and-space.md`
- What comes after: `17-mastering.md`
