# Sampling, Chopping and Breaks

Sampling is composition with recorded sound. Whole genres exist because of it.

## Types of sampling

| Type | Description | Genres |
|---|---|---|
| **Loop** | Take 1–4 bars and repeat it | Hip-hop, house, jungle |
| **Chop** | Slice into pieces and re-sequence | Boom bap, jungle, footwork |
| **One-shot** | A single hit used as an instrument | Drums, orchestra hits, stabs |
| **Multi-sample** | A note mapped across a keyboard | Playing the sample melodically |
| **Micro / granular** | Grains smaller than a note | Ambient, IDM |
| **Field recording** | Non-musical sound as material | Ambient, experimental |
| **Interpolation / replay** | Re-record the part yourself | Legally safer than sampling |

## Chopping method

1. **Find the tempo.** Detect it, or measure a bar's length in samples and derive
   BPM = `60 * SR * beats / bar_samples`.
2. **Find the downbeat.** Trim so the sample starts exactly on beat 1.
3. **Slice.** By transient (onset detection) or by even division (16ths).
4. **Re-sequence.** Play the slices in a new order.
5. **Fade edges** (2–5 ms) on every slice to remove clicks.
6. **Process** each slice individually — pitch, reverse, filter, gate.

**Slice ordering strategies:**

| Strategy | Result |
|---|---|
| Original order | The loop |
| Swap two slices | Subtle variation |
| Repeat one slice 2–4× | Stutter |
| Reverse one slice | Lead-in |
| Play beats 1,2,4,3 | Displaced feel |
| Random order within the beat | Chaotic, IDM/breakcore |
| Keep kick/snare slices in place, shuffle the ghost slices | **The best default** — preserves groove, adds novelty |

## Time and pitch

Two operations, and they are different:

| Operation | Effect on pitch | Effect on length | Artefacts |
|---|---|---|---|
| **Vari-speed / resampling** | Changes | Changes inversely | None (this is "correct" analogue behaviour) |
| **Time-stretch** | Unchanged | Changes | Smearing, phasing, "warble" |
| **Pitch-shift** | Changes | Unchanged | Formant shift ("chipmunk"), smearing |
| **Formant shift** | Unchanged | Unchanged | Changes perceived size of the source |

Vari-speed maths:
```
rate = target_bpm / source_bpm
semitone_shift = 12 * log2(rate)
```
Speeding a 140 BPM break to 174: `rate = 1.243`, `shift = +3.76 semitones`.

**This is a genre-defining fact.** Jungle producers sped 1970s funk breaks from
~100–140 BPM up to 160–175, and the resulting bright, thin, pitched-up drums are
the sound of the genre. Time-stretching instead would have produced a different
music.

**Time-stretch artefacts as an aesthetic:** crude stretching produces granular
smearing and metallic phasing. That artefact is used deliberately in jungle,
garage and IDM.

## The classic breaks

| Break | Source | BPM | Character |
|---|---|---|---|
| **Amen** | The Winstons, "Amen, Brother" (1969) | ~136 | 4 bars; ghost notes; a shifted final bar with a crash |
| **Think** | Lyn Collins, "Think (About It)" (1972) | ~120 | Bright, snappy, the "woo!"/"yeah!" |
| **Funky Drummer** | James Brown (1970) | ~100 | Ghost-note masterclass, laid-back |
| **Apache** | Incredible Bongo Band (1973) | ~116 | Bongos, open, spacious |
| **Hot Pants** | Bobby Byrd (1971) | ~104 | Punchy |
| **Soul Pride** | James Brown (1969) | ~130 | Loose |
| **Impeach the President** | The Honey Drippers (1973) | ~92 | Dry, hip-hop staple |
| **Assembly Line** | Commodores (1974) | ~100 | Clean, open |
| **Substitution** | Incredible Bongo Band (1973) | ~108 | Percussion-rich |
| **Scorpio** | Dennis Coffey (1971) | ~102 | Breakdance staple |

**HAZARD (legal):** every one of these is a copyrighted recording. Commercial
release requires clearance from the recording owner *and* the composition owner.
The history of jungle and hip-hop is largely uncleared; that is a historical
fact, not a legal strategy. For released work: use royalty-free breaks, licensed
sample packs, or program/record your own.

## Working with a break

### Preparation
1. Trim to an exact number of bars (find the first transient).
2. Adjust speed to your tempo.
3. High-pass at 80–150 Hz — the break supplies texture, not low end.
4. Optionally split into frequency bands and process each separately.

### Layering
- Put a **clean modern kick** under the break's kicks (transient-aligned).
- Put a **clean snare** under its snares.
- The break supplies ghost notes, room, and character; the one-shots supply
  weight and punch.
- Parallel-compress the break so the ghost notes come up.

### Processing
| Move | Effect |
|---|---|
| Parallel compression | Brings up ghosts and room |
| Transient shaping | More or less attack |
| Saturation | Glue and grit |
| Bit reduction | Period-correct lo-fi |
| Band-splitting | Process lows and highs independently |
| Gating | Tighten a roomy break |
| Reverse individual hits | Fills and lead-ins |
| Pitch individual slices | Melodic drum patterns |

## Flipping a melodic sample

| Technique | Description |
|---|---|
| **Filter and loop** | Low-pass so only the bass and body remain; loop 2 bars |
| **Chipmunk** | Pitch a vocal up 3–7 semitones |
| **Slow / screw** | Pitch down 10–25%; the "chopped and screwed" sound |
| **Chop into stabs** | Isolate one chord and play it as an instrument |
| **Re-harmonise** | Pitch different slices to different notes to create a new progression |
| **Isolate a fragment** | Band-pass one instrument out of a full mix |
| **Reverse** | An entire phrase, played backwards, becomes new material |
| **Stretch to a pad** | Extreme time-stretch turns a chord into an ambient bed |
| **Beat-repeat a syllable** | The core hook of a lot of modern club music |

## Detecting things programmatically

**Onset detection**: compute the spectral flux (the positive change in magnitude
spectrum between consecutive frames), smooth it, and pick peaks above an
adaptive threshold. The peaks are hits.

**Which hit is which**: classify slices by their spectral centroid and energy
distribution —
- Kick: energy concentrated below 150 Hz, low centroid.
- Snare: broadband, energy at 150–250 Hz *and* 1–8 kHz, mid centroid.
- Hat: energy above 5 kHz, high centroid, short.
- Crash: broadband, high centroid, long decay.

**Tempo**: autocorrelation of the onset envelope, or check candidate BPMs by
seeing which gives the best alignment of onsets to a grid.

**Key**: compute a chroma vector (energy per pitch class) and correlate against
major/minor key profiles.

## Legal and ethical summary

- Sampling a recording without permission is copyright infringement in most
  jurisdictions, regardless of length. There is no reliable "x seconds is fine"
  rule.
- Two rights are involved: the **master** (the recording) and the **composition**
  (the song). Both need clearing.
- Safer paths: royalty-free packs, public domain recordings, Creative Commons
  material (check the licence terms), interpolation (re-recording the part), or
  synthesising something similar.
- Field recordings you made yourself are yours.
- Crediting the source is good practice regardless of the legal position.

## Related

- Jungle technique: `../20-genres/05-jungle-and-breakbeat.md`
- Drum layering: `../00-foundations/10-drums-and-groove.md`
