# Neurofunk

**Identity:** drum & bass stripped of everything organic and rebuilt as a
machine. Precision-engineered drums, minimal harmony, and a bass that is not
played so much as *operated* — a sound whose timbre changes faster than its
pitch. Dark, technical, biomechanical, science-fiction.

The deep dive for a subgenre summarised in `04-drum-and-bass.md`.

## Numbers

| Parameter | Value |
|---|---|
| Tempo | 170–178 BPM; **174 is the standard** |
| Meter | 4/4, drums at 174, bass and harmony felt at 87 |
| Key | Minor, Phrygian, or effectively none — one root note and a drone |
| Track length | 4:30–6:00 |
| Loudness | −8 to −6 LUFS |
| Drop length | 32 bars, in two 16-bar halves |

## Where it came from

Techstep (1995–1997) darkened drum & bass and replaced its sampled funk with
synthesised, industrial sound. **Simon Reynolds coined "neurofunk" in 1997** to
describe what came next, and **Ed Rush & Optical's *Wormhole* (1998)** is the
record that defined it — the point where the genre stopped sounding organic and
started sounding biomechanical.

The origin story that matters technically: the bassline of **"Alien Girl"
(1998)** was made by manipulating the knobs of an **Access Virus** preset in
real time. Not by writing notes — by *performing the timbre*. That is the whole
genre in one sentence, and it is why the Virus (`../10-instruments/09-virtual-analog-and-90s.md`)
is the instrument most associated with it.

| Era | Artists |
|---|---|
| Founders (1997–2002) | Ed Rush & Optical, Matrix, Cause 4 Concern, Bad Company, Konflict |
| Modern canon | Noisia, Black Sun Empire, Phace, Mefjus, Misanthrop, Emperor |
| Contemporary | Billain, Culprate, Teddy Killerz, Signal, Buunshin |
| Labels | Virus Recordings, Vision, Neosignal, Blackout, Eatbrain, Critical |

## The bass — the entire point of the genre

### The gesture

**One long sustained note whose internal modulation rate changes.** Not an
arpeggio. Not a run of short notes. The pitch may not move at all for a whole
bar while everything else about the sound does.

```
bar 1  |  vzhuuuuuuu        modulation slow  — the note breathes
bar 2  |  VZHU-ZHU-ZHU      rate doubles     — still ONE note
bar 3  |  zhuzhuzhuzhuzhu   rate doubles again — now it reads as texture
bar 4  |  zhu-zhu-ZHUUU     rate falls back, and the note finally releases
```

**Do not retrigger the note.** Retriggering resets the envelopes and destroys
the continuity the sound depends on. If you can write the part as a list of
`(step, pitch)` pairs and lose nothing, you have written something else.

### The synthesis sources

Subtractive synthesis alone cannot get there. The genre runs on:

| Method | What it contributes |
|---|---|
| **FM** | Metallic, inharmonic, aggressive mid-range that survives a club system. Noisia's reeses are largely FM8 |
| **Wavetable** | A position parameter that can be modulated at audio rate — the growl |
| **Phase distortion** | Formant-like resonance without a filter |
| **Reese (detuned saws)** | The ancestor; phase interference between near-unison voices |
| **Granular** | Texture and impossible transitions |

### The modulation stack

The characteristic "impossible" quality comes from **several modulators moving
on independent curves** inside one note:

```
filter cutoff      <- tempo-synced LFO, RATE automated 1/4 -> 1/8 -> 1/16 -> 1/8T
wavetable position <- its own slower envelope or LFO, different rate
FM index           <- a third curve
two formant bands  <- swept between vowels across the bar
notch / phaser     <- a fourth, unsynced
detune / phase     <- slow, producing beating
```

None of them share a rate. Their interference is the sound.

### Resampling — the core working method

This is not an optional polish step. Noisia, Evol Intent and Phace all describe
the same loop, repeated until the result is interesting:

```
1. Build a modulated sound in the synth.
2. Render it to audio.
3. Process the audio: re-pitch, distort, filter, reverse, stretch, EQ.
4. Load the result back as a wavetable or a sample.
5. Modulate it again.
6. Repeat 2-5, three to six times.
```

A specific Noisia technique: take an extensively processed waveform, **duplicate
it and detune the copies slightly** so they phase in and out of one another.

### A concrete build

```
OSC A     wavetable with strong spectral variation across the table
          position 40-45%, modulated by LFO1 at ~+55%
          LFO1: a complex shape (not a sine), 2-bar cycle, retrigger per note
          warp: "mirror" or hard sync, modulated by a slow envelope (1-2 s attack)
OSC B     the same table, detuned 12-20 cents, position offset by 10-20%
SUB       separate clean sine or rounded-rect, MONO, unmodulated, -1 octave
          (optionally its level inversely modulated by LFO1)
VOICING   monophonic, portamento ~200-250 ms
FILTER    resonant low-pass, cutoff driven by a tempo-synced stepped LFO
FORMANTS  two band-passes swept between vowel pairs:
          "ee" 270/2290  "eh" 530/1840  "ah" 730/1090  "oh" 570/840  "oo" 300/870
DRIVE     distortion after the filter; then a second, different distortion
BANDS     split at ~100 Hz: sub clean and mono below; everything else above
THEN      resample and do it again
```

### Rules the low end obeys

- **The sub is a separate, clean, mono sine.** It is never distorted, never
  modulated, never retriggered mid-note. All the drama happens above 100 Hz.
- **Check mono constantly.** Detuned and phase-processed layers cancel; the
  clean sub is what survives.
- **Pitch moves rarely and deliberately** — an octave drop, a slide into the
  next phrase, a bend at the end of 4 bars. Not every note.

## The drums

Precision, not rawness. This is the opposite of jungle: where jungle chops a
break and keeps its dirt, neurofunk builds a kit and machines it.

### The two-step foundation

```
step:   0 1 2 3 | 4 5 6 7 | 8 9 10 11 | 12 13 14 15
kick:   x - - - | - - - - | - - x  -  | -  -  -  -
snare:  - - - - | x - - - | -  - -  -  | x  -  -  -
hat:    x - x - | x - x - | x  - x  -  | x  -  x  -
ghost:  - - . . | - . - . | .  - .  -  | -  .  .  -
```

The second kick is **pushed late**, to the 8th note before the second snare —
that displacement is the "stepping" quality of the whole genre.

### Building the kit

| Element | Approach |
|---|---|
| **Kick** | Layered: sub body (50–60 Hz, short), punch (100–200 Hz), click (2–5 kHz). Tight, 100–200 ms |
| **Snare** | **Fundamental 180–200 Hz** with a crisp transient; layered from 2–4 sources — body, noise crack, top snap. The most important sound in the genre |
| **Ghosts** | Quiet snare/rim hits between the main strokes, heavily edited, never quantised flat |
| **Hats/rides** | 16ths with articulation and level detail; often from a break, high-passed |
| **Break layer** | A chopped break underneath the one-shots for texture, high-passed at 200–400 Hz |

### Processing

Transient shaping to sharpen attacks, parallel compression to lift the ghosts,
saturation for glue, tight gating, and per-hit EQ. The result should be **clean
and punchy**, not roomy. Drums sit loud and forward — as loud as the bass.

## Harmony and melody

Minimal by design. Frequently there is **no harmony at all** — one root note, a
drone, and atmosphere. When present:

- Minor or Phrygian; a b2 or a tritone for menace.
- Pads and atmospheres rather than chords; often a single sustained texture.
- Chords change every 4 or 8 bars if they change.
- **The melodic content is the bass's timbre.** The "hook" is a sound, not a
  tune — see `../00-foundations/08-melody.md` on timbral hooks.
- Film dialogue, sci-fi foley, mechanical and industrial samples supply the
  narrative in place of melody.

## Arrangement

```
0-15     Intro: atmosphere, sci-fi texture, filtered drums, a hint of the bass
16-31    Beat in: drums at half energy, sub only
32-47    Build: rolling drums, riser, a sub-drop in the last half-bar
48-79    DROP 1: 32 bars, in two 16-bar halves with different bass behaviour;
         a switch-up every 4 bars, a bigger one at 16
80-95    Breakdown: drums out or halftime; atmosphere, dialogue, tension
96-111   Build 2
112-143  DROP 2: a different bass patch, more aggressive, new drum edits
144-175  Third section or outro; subtract, drums last
```

**Producers perfect one 8-bar loop before writing anything else.** The genre is
made loop-first: the sound design is the composition, and the arrangement is
assembled afterwards from variations of a loop that already works.

Inside a drop, the structure is **call and response**: 2 bars of a bass gesture,
2 bars of its answer, escalating. A drop that repeats one 2-bar bass loop
sixteen times has no internal structure and is the most common beginner failure.

## Signature techniques

- **Modulation-rate automation inside one held note** — the defining gesture.
- **Independent modulators at unrelated rates** — filter, position, index,
  formants, notch, detune.
- **Resampling loops**, three to six passes.
- **Formant sweeps** between vowel pairs so the bass "talks".
- **Multiband discipline**: clean mono sub, everything else mangled.
- **Two-speed writing**: drums at 174, bass phrasing at 87.
- **Ghost-note editing** — the quiet hits are where the groove lives.
- **Switch-ups every 4 bars** inside a drop.
- **Sub-drop** (a sine falling 80 → 25 Hz) before the drop.
- **Silence or a single hit** on the last beat before the drop.
- **Sci-fi narrative** through dialogue samples and mechanical foley.

## Neighbouring styles

| Style | Difference |
|---|---|
| **Techstep** | The ancestor; rawer, more sampled, less designed |
| **Darkstep** | Faster, harsher, less funk |
| **Minimal / deep neuro** | The same sound design with far more space |
| **Halftime neuro** | Written at 170, snare on beat 3 only |
| **Jump-up** | Simpler, cartoonish basses, party-oriented — often confused with neuro by outsiders, and musically the opposite |
| **Crossbreed** | Neuro sound design over hardcore/gabber kicks |
| **Liquid** | The other pole of D&B: jazz chords, warmth, melody |

## Clichés (use knowingly)

The film-dialogue intro about machines or the future; the sub-drop into the
first drop; the halftime section two-thirds through; the "reload" build with a
rising siren; the bass that says a word; the second drop being a different patch
of the same idea.

## Hazards

- **Writing the bass as an arpeggio.** The single most common error. The genre's
  bass is one long note with internal movement; a run of short notes is a
  different genre.
- **Retriggering the note** mid-phrase, resetting every envelope.
- **Distorting the sub**, which destroys the low end instead of enlarging it.
- **Skipping resampling.** A single-pass synth patch does not sound like this,
  and no amount of preset-hunting substitutes.
- **Drums too quiet.** Neurofunk is a drum genre as much as a bass genre.
- **Adding melody to fill space** — the space is the aesthetic.
- **A 32-bar drop with no switch-ups.**
- **Modulators all synced to the same rate**, which sounds mechanical rather
  than alive.
- **Reverb tails longer than ~1.5 s** at 174, which wash the whole thing out.

## Further reading

- Ed Rush & Optical, *Wormhole* (1998) — the founding record
- Noisia, *Split the Atom* (2010); Phace, *Psycho* (2011); Mefjus, *Emulation* (2014)
- [What is Neurofunk — Bassgorilla](https://bassgorilla.com/what-is-neurofunk/)
- [Neurofunk bass in Serum — MusicRadar](https://www.musicradar.com/tuition/tech/how-to-create-a-neurofunk-bass-sound-in-xfer-records-serum-640465)

## Related

- The parent genre: `04-drum-and-bass.md`
- The gesture principle: `../30-patterns/11-signature-techniques.md`
- Bass construction: `../00-foundations/09-bass.md`, `../30-patterns/08-sound-design-recipes.md`
- The Access Virus: `../10-instruments/09-virtual-analog-and-90s.md`
- Wavetable and FM: `../10-instruments/05-fm-and-phase-distortion.md`, `../10-instruments/06-wavetable-vector-and-la.md`
