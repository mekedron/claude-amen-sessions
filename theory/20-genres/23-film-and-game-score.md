# Film, Trailer and Game Score

**Identity:** music with a job. Every choice serves a narrative, an image, or a
player's state. The craft is subordination — knowing when to disappear.

## Film scoring principles

1. **Serve the picture.** If the scene is already tense, the music can be calm.
   If the dialogue is dense, the music must thin out.
2. **Do not duplicate the visual.** Scoring exactly what is on screen ("mickey
   mousing") is a comedy technique.
3. **Enter and exit for a reason.** The moment music starts is itself a dramatic
   event, and so is silence.
4. **Register discipline**: dialogue lives at 300 Hz–4 kHz. Score that must play
   under dialogue lives below and above it — low strings and high shimmer, with
   the middle hollowed out.
5. **Tempo maps to the edit.** Hit points (cuts, actions, reactions) are aligned
   with musical accents; the tempo may change to make this work.

## The emotional vocabulary

| Emotion | Devices |
|---|---|
| **Wonder / awe** | Lydian mode (#4), chromatic mediants, wide open spacing, rising lines, shimmer, sustained strings |
| **Dread** | Low sustained clusters, minor 2nds, sub-bass drones, ticking ostinato, silence |
| **Heroism** | Major, brass, perfect 4ths and 5ths in the melody, dotted rhythms, `I–bVII–IV` |
| **Grief** | Descending stepwise lines, minor, solo instrument (cello, piano, voice), slow harmonic rhythm, suspensions |
| **Tension** | Ostinato, gradual crescendo, rising pitch, accelerating rhythm, unresolved dominant |
| **Romance** | Warm strings, maj7 and add9 chords, rubato, rising then falling melody |
| **Wonder + melancholy** | Major and minor alternating on the same root; the Picardy third and its reverse |
| **Alien / uncanny** | Whole tone, octatonic, microtonal, inharmonic timbres, extended technique |
| **Chase** | Fast ostinato, driving percussion, harmonic stasis with rising pitch, meter changes |
| **Triumph** | Full orchestra, timpani, cymbal roll, brass fanfare, plagal or authentic cadence |

**Chromatic mediants** deserve special mention: they are the single most
characteristic device of Hollywood scoring. `C → Ab`, `C → E`, `Cm → Ab`. One
common tone, no functional logic, immediate sense of scale and wonder.

## Techniques

| Technique | Description |
|---|---|
| **Leitmotif** | A theme attached to a character/idea, transformed as their story changes |
| **Thematic transformation** | The same melody in major/minor, fast/slow, brass/solo — carries meaning across a film |
| **Ostinato** | A repeating figure creating momentum without harmonic movement |
| **Pedal point** | A held bass note under changing harmony; tension and unity |
| **Cluster** | Dense adjacent notes; dread, chaos |
| **Aleatoric texture** | Instructions rather than notes ("play these pitches at random, accelerating") |
| **Drone + melody** | The most economical way to sound epic |
| **Ostinato + expanding orchestration** | The standard 90-second build |
| **Rhythmic unison hits** | Brass and percussion together; impact, danger |
| **Silence** | The most powerful cue in the toolkit |

## Trailer music

A separate craft with a rigid structure:

```
0:00-0:30  Atmosphere. A single sound, a piano figure, a distant voice.
0:30-1:00  Build 1: pulse enters, tension rises. First "braam" hit.
1:00-1:30  Rhythmic section: ostinato, percussion, rising.
1:30-2:00  Breakdown: sudden quiet, a vocal or solo instrument, a beat of silence.
2:00-2:30  Climax: full orchestra, choir, percussion, hits on the cuts.
2:30-2:40  Final hit, then decay or a button.
```

Trailer conventions: the "braam" (a massive detuned brass/synth impact), the
reverse riser into every cut, sub-bass drops, taiko/epic percussion, choir on
"ah", a slowed-down cover of a well-known pop song, and the "one last hit after
the silence".

## Game music — the difference

Games are non-linear. Music must accommodate an unknown duration and unknown
state changes.

| Technique | Description |
|---|---|
| **Looping** | Seamless loops with a separate intro. The loop point must be inaudible |
| **Vertical layering (re-orchestration)** | Stems that fade in/out with intensity: exploration = strings only; combat = add percussion and brass |
| **Horizontal re-sequencing** | Blocks of music that follow one another based on state, with transition segments |
| **Stingers** | Short cues on events (item found, enemy killed), harmonically compatible with the loop |
| **Transition bars** | Pre-composed 1–2 bar bridges between states, entered at a musical boundary |
| **Adaptive tempo/key** | Rare, but powerful |
| **Generative / procedural** | Rules generate the music in real time |
| **Silence budgets** | Music must stop sometimes, or a 40-hour game becomes unbearable |

**Key constraint:** everything must be written in the same key and tempo, or with
planned modulations, so any layer can combine with any other.

### Game genre conventions

| Genre | Musical language |
|---|---|
| RPG / fantasy | Orchestral, leitmotifs, folk instruments, town/battle/dungeon themes |
| Sci-fi | Synths, orchestral hybrid, drones, unusual timbres |
| Horror | Sparse, atonal, extended technique, sound-design-as-music, silence |
| Racing | Electronic, driving, high energy, loop-friendly |
| Puzzle | Minimal, gentle, unobtrusive, long loops |
| Platformer | Melodic, bright, memorable, chiptune heritage |
| Shooter | Percussive, hybrid orchestral/electronic, adaptive intensity |
| Strategy | Ambient with slow development, long loops |
| Roguelike/indie | Chiptune, lo-fi, distinctive small palette |

### Chiptune constraints (still an aesthetic)

| Platform | Channels |
|---|---|
| NES (2A03) | 2 pulse, 1 triangle, 1 noise, 1 DPCM |
| Game Boy | 2 pulse, 1 wave, 1 noise |
| C64 (SID) | 3 voices with filters and ring mod |
| Genesis (YM2612) | 6 FM channels + PSG |
| SNES (SPC700) | 8 sample channels with echo |

The constraint produces the style: arpeggios instead of chords (a single channel
cycling through chord tones fast enough to sound simultaneous), the triangle
channel doubling as bass and melody, noise channel as the entire drum kit.

## Production notes

- **Hybrid** is the modern default: real or sampled orchestra + synths +
  processed percussion + sound design.
- Orchestral samples need: velocity layers, round robins, note-length variation,
  legato transitions, and real dynamic (CC1/CC11) automation. Static velocity is
  the giveaway.
- Reverb: a shared scoring-stage convolution reverb on everything creates the
  "one room" impression. Different reverbs per section destroys it.
- Mix for the medium: cinema (huge dynamic range, real sub), streaming (−14
  LUFS, compressed), game (must survive being mixed with SFX and dialogue at
  runtime).
- Leave the 300 Hz–4 kHz band open when there is dialogue.

## Signature techniques

- **Score the subtext, not the picture.** If the scene is already tense, the
  music can be calm.
- **Hollow the middle.** Under dialogue, live below 300 Hz and above 4 kHz.
- **Ostinato plus expanding orchestration** is the standard 90-second build:
  the figure never changes, the number of players doubles.
- **Chromatic mediants for wonder** — one common tone, no functional logic.
- **Thematic transformation.** The same theme in major/minor, fast/slow, solo/
  tutti carries meaning across a whole film.
- **Hit points**: align accents to the cuts, changing tempo if necessary.
- **Silence as a cue.** Stopping is the strongest gesture available.
- **For games, write for recombination** — every layer in the same key and tempo
  so any stem can play against any other, with transitions entering only on a
  musical boundary.

## Hazards

- Music that competes with dialogue.
- A theme that never transforms.
- Trailer clichés without the drama to justify them.
- Game loops with an audible seam.
- Layered stems that were not written to combine (key or tempo clashes).
- Over-scoring: not every moment needs music.
