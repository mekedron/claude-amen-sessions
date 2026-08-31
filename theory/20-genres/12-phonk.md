# Phonk

**Identity:** underground Memphis rap from the 1990s, recovered by the internet
and rebuilt as something faster, louder and more distorted. Chopped vocal
fragments, a Roland TR-808 pushed past its limits, and — in its dominant modern
form — a **cowbell playing the melody**.

It is one of the few genres whose defining sound is a *drum machine percussion
voice used as a lead instrument*, and one of the very few whose aesthetic
requires the mix to be damaged.

## Numbers

| Style | Tempo | Feel |
|---|---|---|
| OG / Memphis phonk | 130–145 BPM (felt at 65–72) | Halftime, murky, slow |
| **Drift phonk** | **140–170 BPM** (often 150–160) | Aggressive, cowbell-led |
| Brazilian phonk / funk automotivo | 130–160 BPM | Tamborzão groove, relentless |
| House phonk | 125–135 BPM | Four-on-the-floor |
| Rage / aggressive | 150–170 BPM | Distorted synths, hyperpop-adjacent |

| Parameter | Value |
|---|---|
| Meter | 4/4, felt halftime except in house phonk |
| Key | **Minor and Phrygian.** The b2 is the genre's characteristic colour |
| Track length | **1:30–2:30** — built for short-form video, not for albums |
| Loudness | −8 to −5 LUFS; clipping is part of the aesthetic |

## Where it came from

### The source: Memphis rap, 1991–1999
Slow (60–90 BPM), built on distorted TR-808s, dark samples lifted from horror
films, soul and funk records, and a rough cassette-tape recording aesthetic.
**Three 6 Mafia, DJ Zirk, Koopsta Knicca, Tommy Wright III, DJ Screw.** The
lo-fi quality was a consequence of four-track tape and dubbed cassettes — and it
is now the point.

### The revival: early 2010s
**SpaceGhostPurrp** coined and popularised the term. The **Raider Klan**
collective — Denzel Curry, Xavier Wulf, Amber London — plus **Lil Ugly Mane**
and **DJ Smokey** rebuilt the Memphis aesthetic for SoundCloud. `#phonk` was
among SoundCloud's most-trending tags every year from **2016 to 2018**.

### The mutation: drift phonk, late 2010s, Russia
The branch that became the genre for most listeners. **Kaito Shoma's "Scary
Garry" (2018)** is widely cited as the original drift phonk track: Three 6 Mafia
samples over remixed bass and a blown-out TR-808 cowbell melody.

It went viral on TikTok around **2020**, attached to car-drifting and
motovlogging footage. **Kordhell ("Murder in My Mind"), Interworld
("Metamorphosis") and DXRK ("RAVE")** are the tracks that carried it. Spotify
launched an official phonk playlist in **May 2021** — consisting almost
entirely of drift phonk, which tells you which branch won.

### The current wave: Brazil, mid-2020s
**Funk automotivo** — internationally mislabelled "Brazilian phonk" — fuses
drift phonk's distortion with the **tamborzão** groove and vocal chops of funk
carioca. **Slowboy's "Brazilian Phonk Mano"** popularised the label; **MC GW**,
**MC Binn** and the **"montagem"** style define the sound. A parallel Japanese
strand merges anime and J-pop material with baile funk rhythms.

## The cowbell — the genre's lead instrument

### Why it works
The TR-808 cowbell is **two square-wave oscillators at roughly 540 Hz and 800 Hz
through a band-pass filter** — a ratio of about 1.48, deliberately inharmonic
(`../10-instruments/08-drum-machines.md`). That inharmonicity means it has no
strong sense of pitch class, so it can carry a melody while still reading as
percussion. Push it into distortion and the sidebands multiply into a scream.

### Tuning it
Pitch the sample (or the oscillators) to the track's key and play an actual
riff. A common approach: tune down **10 semitones to the root**, then **9
semitones for the b2**, and **7 for the b3** — a Phrygian cell, which is why so
much drift phonk has that specific menacing colour.

### Building one
```
Two square waves, ~540 Hz and ~800 Hz (ratio ~1.48)
Band-pass 800 Hz - 6 kHz
Amp: instant attack, decay 100-400 ms, NO pitch envelope
Tune the pair to the key; transpose it to play the riff
Then: tanh drive, then a wavefolder, then clip - until it screams
Slight detune or chorus for width
Sidechain to the kick
Level: as loud as the drums. It is the lead, not an ornament
```

### Writing the riff
1–2 bars, syncopated, tresillo-derived, using root, b2, b3, 4, 5 and b7 of a
minor or Phrygian scale. Repetitive to the point of hypnosis — the pattern
should be simple enough to become an earworm on the third repetition.

```
step:    0 1 2 3 | 4 5 6 7 | 8 9 10 11 | 12 13 14 15
cowbell: x - - x | - - x - | x - -  x  | -  -  x  -
```

## Drums

```
step:  0 1 2 3 | 4 5 6 7 | 8 9 10 11 | 12 13 14 15
kick:  x - - - | - - x - | - - -  x  | -  -  -  -
snare: - - - - | - - - - | x - -  -  | -  -  -  -
hat:   x x x x | x x x x | x x x  x  | x  r  r  r
open:  - - - - | - - o - | -  - -  -  | -  -  -  -
808:   x - - - | - - x - | - - -  x  | -  -  x  -
```

- **Halftime snare on beat 3**, usually a distorted or clipped 808 snare/clap
  with a short tail.
- **TR-808 kit throughout**, saturated. Not a modern trap kit.
- **Hi-hat rolls** as in trap — 1/8 → 1/16 → 1/32 and triplets, changing
  every bar.
- Everything is clipped; the drum bus itself is driven.

### Brazilian phonk drums
Replace the trap skeleton with the **tamborzão**: syncopated Afro-Brazilian hand
drum patterns, polyrhythmic, with a hard punchy kick and a tight crisp snare
cutting through. Layered percussion is dense and continuous rather than sparse.

## Bass

The 808 is distorted, pitched down and pushed until it growls. **This is not
clean trap sub-bass** — it is deliberately mid-range heavy so it cuts through
laptop and phone speakers.

```
Sine 808, tuned to the key, glides between notes (40-150 ms)
Heavy saturation/overdrive - generating harmonics at 2f, 3f, 4f
Heavy compression
Often doubles the cowbell riff one or two octaves down
Keep ONE clean sub layer underneath if you want it to survive a club system
```

## Samples and texture

- **Memphis rap vocal fragments**, chopped, pitched down, drenched in reverb.
- **Chopped and screwed** treatment: pitch and tempo lowered 10–25%.
- Horror film dialogue, anime and movie quotes.
- **Vinyl noise, tape hiss, VHS artefacts** — the cassette lineage.
- In Brazilian phonk: vocal chops pitch-shifted and time-stretched until
  unrecognisable, where the words are secondary to the texture.

## Arrangement

```
0-7      Intro: a filtered vocal sample or dialogue, atmosphere
8-15     The cowbell riff enters
16-31    Full beat: drums, 808, cowbell
32-39    Breakdown: filtered, vocal sample, tension
40-63    Return, heavier: more distortion, extra layers, a second riff
64-71    Outro or a hard cut
```

**Keep it short.** 1:30–2:30. This is music made for a 15-second video and a
playlist, and a four-minute phonk track has usually stopped being one.

## Signature techniques

- **The cowbell is the lead.** Tune it, write a riff with it, and mix it as
  loud as the drums.
- **Distortion at every stage** — soft-clip the cowbell, saturate the 808, drive
  the drum bus, clip the master. The aesthetic is deliberate overload.
- **Chopped and screwed** the sampled material: pitch and tempo down 10–25%.
- **Lo-fi the whole bus**: bit reduction, tape emulation, a high-pass to imitate
  a cassette, hiss, wow and flutter.
- **Phrygian b2** in the riff for the characteristic menace.
- **Mono-heavy and narrow.** Phonk mixes are deliberately unpolished.
- **Tape stop** at the end of a section.
- **Repetition to hypnosis** — the riff should barely vary.

## Subgenres

| Style | Tempo | Feature |
|---|---|---|
| **OG / Memphis phonk** | 130–145 | Sampled Memphis tapes, murky, slow, lo-fi |
| **Drift phonk** | 140–170 | The distorted cowbell melody; car culture |
| **Rare phonk** | 130–150 | Cleaner, trap-influenced (DJ Yung Vamp, Soudiere, DJ Smokey) |
| **House phonk** | 125–135 | Four-on-the-floor with phonk timbres |
| **Brazilian phonk / funk automotivo** | 130–160 | Tamborzão, vocal chops, montagem |
| **Japanese funk / anime phonk** | 130–160 | J-pop and anime material over baile funk rhythms |
| **Rage phonk** | 150–170 | Maximum distortion, hyperpop crossover |
| **Ambient / atmospheric phonk** | 120–140 | Melodic, moody, less aggressive |
| **Sexy drill / phonk drill** | ~140 | Drill drums with phonk sound design |

## Clichés (use knowingly)

The chopped-and-screwed pitched-down vocal; the cowbell riff everyone knows; the
car engine sample; the anime or horror-film quote intro; the tape stop; the
"Murder in My Mind" descending cowbell shape; the drift footage the track was
made for.

## Hazards

- **A clean, well-mixed phonk track sounds wrong.** Some grit is required.
- **An untuned cowbell.** If it is not in the key, it is percussion, not the
  lead — and the track has no melody.
- **A clean trap 808.** Phonk's bass needs mid-range distortion or it vanishes
  on phone speakers, which is where this music is heard.
- **Too much melodic content.** Phonk is a riff genre; a chord progression
  usually dilutes it.
- **Excessive length.** Over three minutes and it stops working.
- **Modern polish** — wide stereo, clean top end, careful dynamics — removes the
  cassette lineage the genre is built on.
- **Confusing drift phonk with Brazilian phonk.** They share distortion and a
  tempo range and almost nothing else rhythmically.

## Further reading

- Three 6 Mafia, *Mystic Stylez* (1995); DJ Screw's mixtapes; Tommy Wright III
- Kaito Shoma, "Scary Garry" (2018); Kordhell, "Murder in My Mind" (2021)
- [Phonk — Wikipedia](https://en.wikipedia.org/wiki/Phonk)
- [What is Phonk Music? — Splice](https://splice.com/blog/what-is-phonk-music/)
- [Brazilian Phonk guide — Gunther Sound](https://gunthersound.com/blogs/the-sound-lab/blogs-what-is-brazilian-phonk-complete-guide-2026)

## Related

- The TR-808 cowbell circuit: `../10-instruments/08-drum-machines.md`
- The 808 bass: `../00-foundations/09-bass.md`
- Lo-fi processing: `../30-patterns/08-sound-design-recipes.md`
- Trap and drill: `10-hiphop-and-trap.md`, `11-drill.md`
- Brazilian rhythm: `24-latin-and-afro-cuban.md`
