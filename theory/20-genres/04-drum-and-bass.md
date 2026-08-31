# Drum & Bass

**Identity:** fast breakbeats at 170–178 BPM over a slow, heavy bassline. The
drums run at double time while the bass and harmony move at half — a permanent
two-speed feeling that no other genre has.

## Numbers

| Parameter | Value |
|---|---|
| Tempo | 170–178 (standard 174; liquid 172–175; jungle 160–175; halftime 85–90 felt, written at 170–174) |
| Meter | 4/4 |
| Key | Minor (F, G, A, D minor). Dorian for liquid, Phrygian for neuro |
| Swing | Usually 50%, but the break's internal groove carries the swing |
| Track length | 5–6 min |
| Loudness | −8 to −6 LUFS |

## Drums — the "two-step" foundation

```
kick:   x - - - | - - - - | - - x - | - - - -
snare:  - - - - | x - - - | - - - - | x - - -
hat:    x - x - | x - x - | x - x - | x - x -
ghost:  - - . . | - . - . | . - . - | - . . -
```

The core: **kick on 1, snare on 2, kick on the "and" of 3, snare on 4.** That
displaced third kick is the entire feel of drum & bass.

Variations:

```
"two-step"    K - - - | S - - - | - - K - | S - - -
"amen-style"  K - K - | S - . . | - - K K | S - - -
"rolling"     K - - K | S - - - | - K - - | S - K -
"halftime"    K - - - | - - - - | S - - - | - - - -
"jump-up"     K - - - | S - - - | K - K - | S - - -
```

- **Breakbeat sampling** is the tradition: chop a funk break (Amen, Think,
  Apache, Funky Drummer), re-sequence it, layer with clean one-shots.
- Modern D&B layers a sampled break under programmed drums for texture.
- Ghost notes between the main hits are essential — they are what make D&B drums
  feel like drumming rather than a pattern.
- Hats and rides at 16ths, sometimes 32nds in fills.
- The **snare is the most important sound in the genre** — bright, layered,
  cutting, usually at 200 Hz + 1.5 kHz + 8 kHz.

## Bass

Two-layer, always:

1. **Sub** — a clean sine at MIDI 28–38, long notes, following the chord roots,
   usually one or two notes per bar. This is the weight.
2. **Mid bass** — the character: reese, growl, wobble, or a plucky riff, from
   100 Hz to 3 kHz, high-passed off the sub.

Bass rhythm typically works *against* the drums: long sub notes across the bar
while the drums are busy, or a syncopated riff filling the drum gaps.

```
sub:    x - - - - - - - | - - - - x - - -      (two notes per bar)
midbass:- - x - x - - x | - x - - x - x -      (riff filling the gaps)
```

## Neurofunk: what the bassline measures

The gesture itself — one long note whose modulation rate changes inside it —
is in **Signature techniques** below and in
`../30-patterns/11-signature-techniques.md`. This section is the numbers: what
finished records in this subgenre actually measure, so a version of it can be
checked rather than guessed at.

| What to measure | A finished neurofunk record |
|---|---|
| Attacks per bar in the mid bass (200 Hz–1.2 kHz) | **4 to 6** |
| Fraction of the bar the low end is sounding | **81–85%** |
| Distinct sub notes across sixteen bars | **2 or 3**, one held ~40% of the time |
| Modulation of the 200 Hz–1.2 kHz envelope sitting at 10–90 Hz | **40–48%** |
| Energy in 60–120 Hz | **a quarter of the whole mix** |
| Side energy at 400–1200 Hz / below 120 Hz | **95–135% / 5–7%** |
| Spectrum from 300 Hz to 11 kHz | **flat within 3 dB** |

A bass written as a run of short notes measures 15–25% in that 10–90 Hz band
and 12–18 attacks a bar, and the gap between those numbers and these is
exactly what people mean when they say a track "sounds like a preset".

### Implementing the rate curve

Two details decide whether it accelerates or stutters:

1. **Integrate the rate; never restart the modulator.** Its phase must be the
   running integral of the rate (`phase += 2π·rate/SR` per sample), so a rate
   that triples across a note glides up to it. Recomputing per step makes it
   jump.
2. **Smooth the rate itself** over 30–60 ms before integrating, or the curve
   reads as a gear change.

Note lengths should not divide the bar evenly. 10 + 6 steps, or 5 + 3 + 3 + 5,
sounds stretched; 4 + 4 + 4 + 4 sounds sequenced.

### Three layers, and they never share a frequency

| Layer | Range | What it is |
|---|---|---|
| Sub | 30–60 Hz | One clean sine, mono, monophonic, no distortion, no reverb |
| Body | 60–120 Hz | An octave up, filtered, **no hard sync** — a sync edge at 33 Hz is a buzz once per cycle, not a growl |
| Character | 130 Hz up | Everything: sync, FM, formants, distortion, the rate curve |

The body layer is the one people leave out, and it is a quarter of the mix.

### Aggressive rather than merely loud

| Property | Measure it as | A hit wants |
|---|---|---|
| Front edge | Peak of the first 10 ms over the 75th percentile of the body | **+10 to +18 dB** |
| Teeth | Energy above 1 kHz minus energy below | **−4 to +2 dB** |
| Depth | How far the filter travels, not how fast | **14–20 dB** of swing |
| Hardness | Odd-harmonic energy minus even | **+4 to +12 dB** |

Put a real 5 ms transient on the front and add it **after** every zero-phase
filter in the chain — a forward-backward filter smears a transient in both
directions. Use a **wavefolder** for the last stage rather than a saturator:
`tanh` stops generating partials once it is flat and folding does not. Put a
square in the source, because even-order distortion is warm (octaves and
fifths) and odd-order is hollow and hard.

For width, render the character layer **twice with different oscillator
phases** and put one in each channel. That is decorrelation, not delay: a Haas
delay reads as width on headphones and puts a fixed null in the low mids the
moment a club system sums the bass.

### Neurofunk-specific hazards

- **Counting attacks is the quickest test.** More than about eight a bar and
  it is a sequence, not a bassline.
- **FM at a non-integer ratio on a bass note.** A ratio of 1.5 puts sidebands
  at 0.5, 2.5 and 5.5 times the note — the harmonic series of the octave
  *below* — so half the energy lands between the note's own harmonics and the
  ear reads it as out of tune rather than as driven. Integer ratios (2, 3)
  keep a pitch while sounding just as violent.
- **Confusing rate with depth.** A fast LFO over a 6 dB filter swing is a
  flutter; the growl is the swing.
- **Hard sync at the sub's octave** is a buzz. Sync belongs two octaves up.
- **Shelving the whole bass off above 2.5 kHz** to keep the snare clear works,
  and removes the teeth. Carve narrowly at the snare's crack instead and get
  the beat back in *time*, by ducking the bass on the snare as well as on the
  kick.

## Harmony

- Liquid: **m9, maj9, add9, ii–V** — genuinely jazz-influenced, 4- or 8-bar
  progressions, rhodes and pads.
- Neuro/techstep: often one chord or none; the harmony is in the bass timbre.
- Jump-up: minimal — a riff and a sub.
- Common progressions: `i–bVI–bIII–bVII`, `i–iv–bVII–bIII`, `im9–IVmaj9`
  (Dorian), `i–bVII–bVI–bVII`.
- Chords change every 2 or 4 bars — slowly, against the fast drums.

## Arrangement (the two-drop structure, ~6 min at 174 BPM)

```
0-15     Intro: atmosphere, filtered drums, DJ-friendly.
16-31    Beat in, half the elements.
32-63    FIRST DROP: full drums + bass. 32 bars.
64-79    Breakdown: drums out or halftime, pads, melody, reverb.
80-95    Build: rolling drums return, riser, sub drop.
96-127   SECOND DROP: bigger — new bass, extra layers, more energy.
128-143  Third section or a variation.
144-175  Outro: subtract, drums last.
```

**Key convention:** the drop is where the *drums* start, not where the bass
drops out. And the **sub-drop** (a sine sweeping from ~80 Hz down to ~30 Hz over
half a bar) marks the moment before the drop.

## Subgenres

| Subgenre | Feature |
|---|---|
| **Liquid** | Jazz/soul chords, rhodes, vocals, warm, melodic, rolling |
| **Neurofunk** | Complex modulated basses, dark, technical, minimal harmony — **deep dive: `04a-neurofunk.md`** |
| **Techstep** | Dark, industrial, sparse, 90s |
| **Jump-up** | Big cartoonish basslines, party-oriented, simple |
| **Jungle** | Chopped breaks, ragga vocals, 90s, sub-heavy (see own file) |
| **Halftime / 170 halftime** | Snare on 3 only, trap-influenced, spacious |
| **Drumfunk** | Extreme breakbeat editing, no straight patterns |
| **Minimal / autonomic** | Sparse, dubby, atmospheric, 160–170 |
| **Jazzstep** | Live jazz instrumentation |
| **Ragga jungle** | Reggae/dancehall vocals, dub sirens, soundsystem culture |
| **Dancefloor / mainstream** | Big drops, EDM structure, festival |
| **Deep / atmospheric** | Ambient pads, long, hypnotic (LTJ Bukem lineage) |
| **Rollers** | One relentless groove, minimal change, hypnotic |

## Production notes

- **Drum processing is the craft.** Layer, transient-shape, parallel-compress,
  saturate, and EQ each drum element separately. D&B drums are usually the most
  processed drums in music.
- **The break's pitch matters.** Speeding a 140 BPM break to 174 raises it by
  ~3.8 semitones and thins it — that brittle, bright quality is a genre marker.
- Sub bass mono, clean, no reverb, no distortion.
- Mid bass can be as distorted, modulated and wide as you like above 150 Hz.
- Reese basses: two detuned saws, filtered, with notch and phaser movement.
- **Sidechain the sub to the kick** lightly (2–4 dB) so the kick has room.
- Reverb tails at 174 BPM must be short (< 1.5 s) or everything washes out.

## Clichés (use knowingly)

The sub-drop before the drop; the Amen break; the "wooo" rave sample; the
Reese bass; the halftime section at 2/3 through; the vinyl crackle intro;
the ragga MC "bo bo bo"; the filtered-break-into-full-break transition.

## Signature techniques

- **The bass is one long note, not an arpeggio.** This is the single most
  misunderstood thing about the genre. In neurofunk and techstep the defining
  bass is a *sustained* note — often one pitch for a whole bar — whose
  **internal modulation rate changes**: slow at the start, doubling and
  redoubling, then releasing. `vzhuuuu → VZHU-ZHU-ZHU → zhuzhuzhuzhu`.
  Writing it as a run of short notes through an arpeggiator produces something
  busy that is not the genre. **Do not retrigger the note** — retriggering
  resets the envelope and kills the continuity the sound depends on. See
  `../30-patterns/11-signature-techniques.md` for the full implementation.
- **Automate the LFO rate, not the pitch.** Step it 1/4 → 1/8 → 1/16 → 1/8T
  across bars, or ramp it continuously. The pitch stays put.
- **Layer independent modulators.** Filter LFO, wavetable position, two formant
  band-passes and a notch/phaser each move on their own curve. Their
  interference is the "impossible" quality.
- **Resample, then process again.** Bounce the modulated bass to audio, re-pitch
  and re-distort it, twice or three times.
- **The sub is separate, clean and unmodulated** — mono sine, no retrigger, no
  distortion. All the movement happens above 100 Hz.
- **Two-speed writing.** Drums move at 174; bass and harmony move at 87. Chords
  change every 2 or 4 bars against 16th-note drums.
- **Ghost notes carry the break.** The quiet hits between kick and snare are what
  separate a programmed pattern from a played one. Edit them, do not quantise
  them away.
- **The sub-drop before the drop:** a sine sweeping 80 → 25 Hz over half a bar.
- **Pitch gestures are rare and deliberate** — an octave drop, a slide into the
  next phrase, a bend at the end of 4 bars. Not every note.
- **Liquid inverts the emphasis**: the bass sustains simply and the *chords*
  carry the movement, with rolling ghost-note drums and jazz voicings.

## Hazards

- Drums too quiet. D&B is a drum genre — the break should be loud and forward.
- Sub and mid bass not separated in frequency, so the low end is mush.
- Reverb too long for the tempo.
- Harmony changing too fast; chords should move at half the drums' speed.
- A drop that is only 16 bars — 32 is the standard.
- Programmed drums with no ghost notes; the result sounds like a drum machine,
  not a break.
