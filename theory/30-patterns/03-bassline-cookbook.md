# Bassline Cookbook

16-step grids. `x` = note, `-` = rest, `~` = note held/gliding, `.` = ghost.
Pitches given as scale degrees (1 = root, b3 = minor third, 5 = fifth, etc.)
unless stated.

## Four-on-the-floor family

### House — offbeat 8ths
```
step:  0 1 2 3 | 4 5 6 7 | 8 9 . . | . . . .
bass:  - - x - | - - x - | - - x - | - - x -
pitch: 1        1         1         1
```
Short notes (60–120 ms). Sidechained. The kick occupies the downbeats.

### House — rolling 16ths
```
bass:  - x x x | - x x x | - x x x | - x x x
pitch: 1 1 1   | 1 1 1   | 5 5 5   | 1 1 1
```

### Deep house — syncopated and sparse
```
bass:  x - - x | - - x - | - - - x | - x - -
pitch: 1       1         b7        5
```

### Techno — driving 16ths on one note
```
bass:  x x x x | x x x x | x x x x | x x x x
pitch: 1 (all, with filter and velocity variation)
```

### Trance — rolling offbeat
```
bass:  - x x x | - x x x | - x x x | - x x x
pitch: 1 all; root changes with the chord every 1-2 bars
```

### Disco — octave 8ths
```
bass:  x - x - | x - x - | x - x - | x - x -
pitch: 1   8   | 1   8   | 1   8   | 1   8
```

### Hi-NRG — octave 16ths
```
bass:  x x x x | x x x x | x x x x | x x x x
pitch: 1 8 1 8 | 1 8 1 8 | 1 8 1 8 | 1 8 1 8
```

### Hardstyle reverse bass
```
kick:  x - - - | x - - - | x - - - | x - - -
bass:  - - x - | - - x - | - - x - | - - x -
```
The bass sits in the kick's gaps with a reversed envelope.

## Breakbeat family

### Drum & bass — long sub + mid riff
```
sub:   x - - - - - - - | - - - - x - - -
pitch: 1                 b7
mid:   - - x - x - - x | - x - - x - x -
```

### Jungle — sparse ragga sub
```
bass:  x - - - - - - - | - - x - - - - -
pitch: 1                 5
```
Very long notes, huge, clean sine.

### Neurofunk — the modulated riff
```
bass:  x~~~~~x | ~~x - x | ~~~~x - | x - x~~~
```
One continuous sound whose *timbre* changes on each marked step.

### Dubstep — halftime wobble
```
bass:  x~~~~~~~ | ~~~~~~~~ | x~~~~~~~ | ~~~~~~~~
LFO:   1/4 rate   1/8 rate   1/16 rate  1/8T rate
```
The note is held; the LFO rate is the composition.

### UK garage — bouncy and syncopated
```
bass:  - - x - | - x - - | x - - x | - - x -
pitch: 1       b7        1     5     1
```

## Hip-hop family

### Boom bap — following the sample
```
bass:  x - - - | - - x - | - - x - | - - - -
pitch: 1         1         5
```

### Trap — tresillo 808
```
bass:  x - - x | - - x - | x - - - | - - x -
pitch: 1     1 | 1       | b6      | b7
```

### Drill — sliding 808
```
bass:  x~~~~~~~ | ~~~~~~x~ | x~~~~ - - | - - x~~~
pitch: 1 → b3    → 5         4 → 1        b7 → 1
```
Every note glides into the next.

### Phonk — cowbell-doubling 808
```
bass:  x - - x | - - x - | x - - x | - - x -
pitch: 1     b3| b3      | 1     5 | b7
```

## Funk family

### Funk — 16ths with ghosts
```
bass:  x - . x | - x - - | x . - x | - - x -
pitch: 1     1 | b7      | 1   5   | 4
```

### Slap funk
```
bass:  T - - P | - T - - | T - P - | - T - -
```
T = thumb slap (low), P = pop (high, an octave or a tenth up).

### Motown / soul — melodic and constant
```
bass:  x - x x | - x - x | x - x - | x x - x
```
Walking-ish, full of passing tones, rarely resting.

### Reggae — around the one
```
bass:  - - x - | - x - - | x - - - | - - x -
pitch: 1       5         1           b7
```
Beat 1 is often empty; the bass arrives late.

## Rock and metal

### Root 8ths
```
bass:  x x x x | x x x x | x x x x | x x x x
```
Following the guitar riff exactly.

### Metal — gallop
```
bass:  x . x x | . x x . | x x . x | x . x x
```
(16th–16th–8th gallop pattern doubling the guitar.)

### Punk — driving 8ths with root/fifth
```
bass:  x x x x | x x x x | x x x x | x x x x
pitch: 1 all, with a 5 on the last 8th of each bar
```

## Jazz and acoustic

### Walking bass (per bar of one chord)
```
beat:  1    2    3    4
notes: root chord-tone scale-tone approach-to-next-root
```
Example over Dm7 → G7 (in C): `D F A B | G B D Db`.
The last note is always a chromatic or a fifth approach into the next root.

### Bossa nova
```
bass:  x - - - | - - x - | x - - - | - - x -
pitch: 1         5         1         5
```
Root on 1, fifth on the "and" of 2. Repeat.

### Latin tumbao (anticipated)
```
bass:  - - - - | - - x - | - - - - | x - - -
pitch:           b7 or 5              1
```
**Beat 1 is empty.** The note before it (the "and" of 4 of the previous bar)
anticipates.

## Melodic and pop

### Pop root notes
```
bass:  x - - - | - - - - | x - - - | - - - -
```
One or two notes per bar, following the chords.

### Pop with an octave lift
```
bass:  x - - - | - - - x | x - - - | - - x -
pitch: 1               8 | 1           5
```

### Synthwave — driving 16ths with octaves
```
bass:  x x x x | x x x x | x x x x | x x x x
pitch: 1 1 1 1 | 1 1 1 8 | 1 1 1 1 | 1 1 8 8
```

### Arpeggiated bass
```
bass:  x - x - | x - x - | x - x - | x - x -
pitch: 1   5   | 8   5   | 1   5   | 8   5
```

## Techniques to apply to any of these

| Technique | Effect |
|---|---|
| **Approach note** on the last 8th or 16th of a bar (chromatic from below into the next root) | Turns a static line into a line that goes somewhere |
| **Octave displacement** of one note per bar | Movement without new material |
| **Ghost notes** at 20–35% velocity between the main notes | Groove |
| **Note-length variation**: alternate short and long | The most audible "human" cue |
| **Slide/portamento** into selected notes (40–120 ms) | Modern, expressive |
| **Rest on the downbeat** of one bar in four | Space and surprise |
| **Anticipation**: move a note one 16th earlier than expected | Push, funk |
| **Fifth instead of root** on a repeat | Harmonic variety at no cost |

## Layering rules

1. **Sub layer**: mono, sine, MIDI 28–40, no distortion, no reverb, monophonic.
2. **Mid layer**: the character, high-passed at 90–120 Hz, can be distorted,
   modulated and stereo.
3. **Top layer** (optional): a click or a pluck at 1–4 kHz for definition on
   small speakers.
4. All layers play the **same rhythm**. Different rhythms across layers turn a
   bass into a mess.

## Related

- Why: `../00-foundations/09-bass.md`
- Kick/bass interaction: `../00-foundations/14-dynamics-and-compression.md`
