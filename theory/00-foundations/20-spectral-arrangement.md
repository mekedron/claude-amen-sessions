# Spectral Arrangement — Which Bands Are Occupied, and When

**Filling the whole frequency spectrum for the whole track is not a goal. It is
one of the most common ways a production goes wrong.**

A spectrum analyser showing energy from 20 Hz to 20 kHz at every moment looks
like competence and is usually the opposite. This file is about treating
frequency space as something that is **budgeted across instruments** and
**spent differently across time**.

## Why "fill everything" fails

1. **Masking is zero-sum.** Two elements sharing a band do not both get heard;
   the quieter one is simply lost. A full spectrum at every moment guarantees
   maximum masking, so adding more content makes the mix *less* legible, not
   more.
2. **Contrast is the mechanism of arrangement.** A drop feels enormous because
   the build removed the low end. A chorus opens because the verse was narrow.
   **You cannot open a band that was never closed.** A permanently full spectrum
   throws away the single most powerful arrangement tool.
3. **Headroom is finite.** Every occupied band costs level. Energy spread across
   everything, all the time, means the limiter works harder and the master ends
   up flatter and *perceptually quieter* than a sparser mix at the same LUFS.
4. **Fatigue.** Constant full-range content — especially 2–5 kHz and above
   10 kHz — is exhausting after a minute, which is the opposite of what a track
   needs from a listener.
5. **It erases genre.** A very large amount of what identifies a style is what
   it *leaves out*.

## The spectrum as a budget

Each band has a **primary owner at any given moment**, and one or two supporting
parts. Not five.

| Band | Primary owner | Supporting | Rule |
|---|---|---|---|
| 20–60 Hz | Sub bass **or** kick | — | One element. Mono. Often empty entirely |
| 60–120 Hz | Kick and bass, split | Low toms | Two at most, separated in time or frequency |
| 120–300 Hz | Bass harmonics, snare body | Low vocal, guitar body | The mud zone; keep the count low |
| 300–800 Hz | Body of the lead instrument | Everything's fundamentals | The most crowded band; cut here first |
| 800 Hz–2.5 kHz | Vocal / lead intelligibility | Snare crack | Protect this for the focus element |
| 2.5–6 kHz | Attack and definition | Hats, presence | Also where harshness lives |
| 6–12 kHz | Hats, cymbals, air | Vocal sibilance | Thin content, easily overcrowded |
| 12 kHz+ | Sparkle | Reverb tails | Frequently empty, and fine |

**The test for any new element: which band does it own, and who has to give it
up?** If the answer is "none, it just fills things out", it is a candidate for
deletion — see `16-mixing-process.md` on the mute test.

## The spectrum over time

This is the part that gets missed. **Which bands are occupied should change
between sections.** Sketch it like an arrangement matrix:

```
band          intro  verse  build  DROP  breakdown  outro
20-60 Hz       -      x      -      X       -        -
60-120 Hz      -      x      -      X       -        x
120-300 Hz     x      x      x      X       x        x
300-800 Hz     x      x      x      X       x        x
800-2.5k       -      x      x      X       x        -
2.5-6k         x      x      X      X       -        x
6-12k          -      x      X      X       -        -
12k+           -      -      x      X       x        -
```

Read the low rows: the sub is **absent in the intro, absent in the build,
absent in the breakdown**, and that is exactly why the drop lands. The build
high-passes everything and the drop returns the bottom two octaves at once.

Techniques that follow:

- **High-pass the whole mix through a build**, rising to 400–800 Hz, then drop it
  back to 20 Hz on the downbeat.
- **Breakdowns are mid-range events.** Remove the sub and the extreme top; the
  return of both is the payoff.
- **Intros and outros are deliberately incomplete** — in club music because a DJ
  needs the space, and everywhere else because arriving at a full spectrum is
  more interesting than starting there.
- **Give the top octave somewhere to go.** If the hats are at full brightness
  from bar 1, the chorus has no lift available.

## Genres are defined by what they leave out

| Genre | Characteristically absent | Why |
|---|---|---|
| Lo-fi / chillhop | Below ~60 Hz and above ~8–12 kHz | Cassette and vinyl lineage |
| Boom bap | Extreme sub and extreme top | 12-bit samplers at 26 kHz |
| Reggae / dub | Bass harmonics above ~800 Hz; bright top | The bass is deliberately dark |
| Techno | Often little above 12 kHz | Mid-forward, mono-heavy, club-oriented |
| Jungle | Sub in the intro | It arrives with the drop, and that is the event |
| Ambient | 60–120 Hz, frequently | Weightlessness is the point |
| Jazz / classical | Sub-bass entirely | An acoustic ensemble has nothing below ~40 Hz |
| Folk / singer-songwriter | Sub, and hyped top | Natural, unhyped, small |
| Chiptune | Literally band-limited | The hardware could not produce it |
| Phonk / vaporwave | Clean top end | Tape and VHS degradation is the aesthetic |
| Black metal (trad.) | Low end | Thin and cold on purpose |
| Trap / drift phonk | Nothing — but the mids are hollowed | 808 and hats, with a gap between |

**A jazz trio recording with no content below 40 Hz is not deficient.** It is
correct. Adding a synth sub to it would be the error.

## The pink-noise slope, correctly understood

A finished full-range modern master tends toward roughly **−3 to −4.5 dB per
octave** above 1 kHz. That is:

- a **statistical tendency**, measured across a *whole track*;
- a **consequence** of good arrangement, not a cause;
- **specific to full-range genres** — it does not describe lo-fi, dub, chiptune
  or a solo piano recording;
- **not a per-moment target.** A track whose spectrum matches the curve at every
  instant has no spectral dynamics at all.

Matching a reference curve section by section is how a mix ends up sounding
technically fine and emotionally flat.

## How to check

1. **Look at a spectrogram of the whole track, not an analyser on a loop.**
   The question is *does the picture change over time?* A solid rectangle from
   start to finish is the failure this file is about.
2. **Per-section band map.** Fill in the table above for your own arrangement.
   Any row that is `x` in every column is suspicious.
3. **The subtraction test.** In each section, name one band that is emptier than
   in the previous section.
4. **Mono, quiet, and on a phone.** If the mix survives all three, the band
   budget is working.

## Rules

1. **Every band should be empty somewhere in the track.**
2. **One primary owner per band at a time.**
3. **Decide the band budget before writing**, not during mixing. Spectral
   problems are almost always arrangement problems.
4. **Sections differ in which bands they use**, not only in how loud they are.
5. **Silence in a band is a legitimate, permanent choice** when the genre asks
   for it.
6. **Do not add content to fill a gap.** Ask first whether the gap is the point.

## Hazards

- **Adding a layer because a band "looks empty" on the analyser.** The ear, not
  the display, decides.
- **A sub-bass in a genre that has never had one.**
- **Air-band shelves on everything**, which is fatiguing and codec-hostile.
- **Full-spectrum intros**, which leave nowhere to go and, in club music, make
  a track unmixable.
- **Identical spectra in verse and chorus.**
- **Treating a reference curve as a target rather than a symptom.**
- **Confusing "full" with "big".** Big comes from contrast and from clean
  ownership of a few bands, not from occupying all of them.

## Related

- Band-by-band detail and EQ moves: `13-frequency-and-eq.md`
- Arrangement contrast: `11-form-and-arrangement.md`
- Why contrast works on the ear: `18-psychoacoustics-and-tension.md`
- Genre tonal targets: `17-mastering.md`
