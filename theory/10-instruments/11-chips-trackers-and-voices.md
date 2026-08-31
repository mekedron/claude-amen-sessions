# Sound Chips, Trackers and Voice Machines

Machines that were never meant to be musical instruments, and the devices that
turned the human voice into a synthesiser.

---

## Sound chips

Every one of these was a cost-constrained piece of consumer hardware. The
constraints define the aesthetic.

### MOS 6581/8580 SID — Commodore 64 (1982)
The most musical of the home-computer chips, designed by Bob Yannes (who later
co-founded Ensoniq).

| Feature | Detail |
|---|---|
| Voices | 3 |
| Waveforms | Triangle, sawtooth, pulse (variable width), noise — combinable |
| Filter | **One analog multimode filter** (LP/BP/HP) shared by all voices |
| Extras | Ring modulation, hard sync, per-voice ADSR |
| Quirk | The 6581's filter cutoff varies between individual chips; the 8580 is more consistent but "colder" |

Techniques the constraint forced:
- **Arpeggios instead of chords**: one voice cycling through chord tones at
  ~50 Hz (once per screen frame) reads as a chord. This is *the* chiptune sound.
- **Duty-cycle sweeps** on the pulse wave for movement.
- **Drums stolen from a melodic voice** — the composer drops a voice for one
  frame to place a noise hit.

Composers: Rob Hubbard, Martin Galway, Jeroen Tel, Chris Hülsbeck.

### Ricoh 2A03 — NES (1983)
| Channel | Use |
|---|---|
| 2 × pulse (duty 12.5 / 25 / 50 / 75%) | Melody and harmony |
| 1 × triangle (no volume control) | **Bass** — and, an octave up, a lead |
| 1 × noise | Drums |
| 1 × DPCM | Low-quality samples (often a kick or a voice) |

The triangle's lack of volume control is why NES bass lines are constant in
level and why the "drum" is usually the triangle pitched very low for a few
frames.

### Game Boy (LR35902, 1989)
2 pulse + 1 **wavetable** (32 4-bit samples, user-definable) + 1 noise. The
programmable wave channel is why Game Boy music has more timbral variety than
NES. LSDJ and Nanoloop turned it into a live instrument, and chiptune became a
performance genre.

### Yamaha YM2612 — Sega Mega Drive/Genesis (1988)
**6-channel 4-operator FM** plus a PSG. Real FM synthesis in a games console —
which is why Genesis music has basses and leads that sound like a synth rather
than a beeper. Its slightly broken DAC produces a characteristic crunch.

### Konami SCC, Namco WSG, Atari POKEY, AY-3-8910
Each with its own waveform set and limitations, each with a devoted following.

### Rebuild any of them
```
Pick a strict voice limit (3 or 4) and enforce it.
Waveforms: pulse at 12.5/25/50% duty, triangle, 4-bit wavetable, LFSR noise.
No filter (or one shared filter for everything).
Volume in 16 steps, not continuous.
Update all parameters at 50 or 60 Hz - nothing changes between frames.
Chords = fast arpeggios at 50-60 Hz on a single voice.
Vibrato and pitch slides applied per frame, in steps.
```
The per-frame quantisation of every parameter is what makes it sound authentic;
smooth automation immediately breaks the illusion.

---

## Trackers

### Ultimate Soundtracker / ProTracker — Commodore Amiga (1987–)

**Type:** pattern-based sequencer with **4 channels of 8-bit sampled audio**,
displayed as vertical columns of hexadecimal.

| Constraint | Consequence |
|---|---|
| 4 channels | Bass, drums, and two melodic parts — total. Everything else must be pre-mixed into a sample |
| 8-bit samples, ~28 kHz max | Crunchy, aliased, characterful |
| Pitch = varispeed | A break played faster is also higher — **the jungle sound** |
| Sample memory measured in kilobytes | Tiny loops, tightly chopped |
| Per-row effect commands | Arpeggio, portamento, vibrato, volume slide, sample offset, retrigger — all as hex codes |

**Effect commands worth knowing**, because they are still musical ideas:
| Command | Effect | Modern equivalent |
|---|---|---|
| `0xy` | Arpeggio — alternate between note, +x, +y semitones every frame | Fast arpeggiator |
| `9xx` | Sample offset — start playback partway in | Slice playback |
| `Exx` | Retrigger | Beat-repeat / ratchet |
| `1xx/2xx` | Portamento up/down | Pitch slide |
| `Cxx` | Volume | Per-step velocity |

### What trackers changed
The Amiga demoscene, then **jungle, hardcore, and early UK dance music**. Whole
genres were made by teenagers with a £400 computer. The tracker's per-row
parameter control is the direct ancestor of Elektron's parameter locks and of
modern step-sequencer automation.

Modern trackers: **Renoise**, **SunVox**, **Polyend Tracker**, **Dirtywave M8**.

---

## Voice machines

### The vocoder (1939 as a telephone codec; musical from the 1970s)

**How it works:** split the **modulator** (a voice) into 8–32 band-pass bands
and measure each band's amplitude. Apply those amplitudes to the same bands of a
**carrier** (a synth, usually a bright saw or pulse). The synth now "speaks".

| Control | Effect |
|---|---|
| Number of bands | 8 = robotic and crude; 20+ = intelligible |
| Carrier waveform | Must be harmonically rich — a saw or pulse. A sine will not work |
| Unvoiced/sibilance path | Consonants (s, t, k) are noise; a good vocoder passes high-frequency noise through separately, or speech is unintelligible |
| Band attack/release | Fast = clear consonants; slow = smeared and eerie |
| Formant shift | Moves the analysis bands relative to the synthesis bands |

Machines: EMS Vocoder 5000, Roland VP-330 (also a lovely string/choir machine),
Korg VC-10, Sennheiser VSM201.

Records: Kraftwerk (*Autobahn*, *Trans-Europe Express*), Herbie Hancock
"Rockit", ELO, Air, Daft Punk (extensively).

**Rebuild:** 16 band-pass filters logarithmically spaced from 100 Hz to 8 kHz on
both voice and carrier; envelope-follow each voice band (attack ~5 ms, release
~20 ms) and multiply the corresponding carrier band; sum. Add a high-passed
noise path keyed to the voice's high-frequency energy for consonants.

### The talkbox (1970s)

Not a vocoder. A **speaker driver sends the synth's sound up a plastic tube into
the performer's mouth**; the mouth shapes it acoustically and a normal
microphone picks up the result. The performer mouths the words silently.

The result has real vocal-tract resonance, so it sounds more organic and less
"digital" than a vocoder — but it cannot be applied to a recording.

Records: Peter Frampton, Roger Troutman/Zapp (and therefore all of G-funk),
Daft Punk, Stevie Wonder.

**Rebuild:** dynamic band-pass formant filtering — two or three band-pass
filters swept between vowel formant pairs (see
`../00-foundations/19-vocals-and-lyrics.md`), applied to a saw or square, with
the sweep drawn to follow the syllables.

### Auto-Tune (1997) and the artefact that became a genre

Antares Auto-Tune corrects pitch to the nearest note of a scale. Its **Retune
Speed** parameter controls how fast it moves.

| Retune speed | Result |
|---|---|
| 20–40 ms | Transparent correction |
| 10–20 ms | Audible but subtle |
| **0 ms** | **The effect**: pitch snaps instantly, producing the stepped, robotic glide between notes |

At zero retune speed the correction removes all the portamento and vibrato that
makes a voice sound human, replacing it with quantised jumps. Cher's "Believe"
(1998) was the first hit to use it deliberately; T-Pain built a career on it;
it is now the default vocal aesthetic of trap, hyperpop and much of pop.

**Requirements for it to work:** the scale must be set correctly (usually the
song's key, with unused notes removed), and the vocal must be sung slightly
*off* pitch for the snapping to be audible.

### Melodyne (2001) and DNA (2009)

Polyphonic pitch editing: it can separate individual notes inside a **chord** in
a recording and re-pitch them. That made it possible to re-harmonise a recorded
guitar chord or fix one note in a piano take — and, for producers, to turn any
sample into raw harmonic material.

---

## What to take from this file

Constraint-based instruments give you an identity for free. If a track sounds
generic, impose one of these:

- **4 voices maximum**, everything else pre-mixed.
- **All parameters update at 50 Hz**, in steps.
- **Pitch changes are varispeed** — length changes too.
- **8-bit samples at 28 kHz.**
- **Chords only as fast arpeggios.**
- **The voice is a carrier for a synth, not a melody.**

## Related

- Chiptune in context: `../20-genres/23-film-and-game-score.md`
- Jungle and the Amiga: `../20-genres/05-jungle-and-breakbeat.md`
- Vocal processing: `../00-foundations/19-vocals-and-lyrics.md`
