# Progression Cookbook

Roman numerals plus, for the most useful ones, concrete MIDI note sets in
C (major key) or A (minor key). Transpose by adding a constant.

Reminder: uppercase = major, lowercase = minor, `°` = diminished, `b` before a
numeral lowers that degree.

## The universal four

| # | Progression | Also known as | Feel |
|---|---|---|---|
| 1 | `I – V – vi – IV` | The axis / four chords | Uplifting, universal |
| 2 | `vi – IV – I – V` | Axis rotation | Melancholic start, hopeful end |
| 3 | `I – vi – IV – V` | 50s / doo-wop | Nostalgic, innocent |
| 4 | `IV – I – V – vi` | Axis rotation | Soaring, anthemic |

In C major with simple triads:
```
I  = [60, 64, 67]   C
IV = [65, 69, 72]   F
V  = [67, 71, 74]   G
vi = [69, 72, 76]   Am
```
Voice-led (better): `C [60,64,67] → G/B [59,62,67] → Am [57,60,64] → F [53,57,60]`

## Major-key progressions

| Progression | Feel | Genre |
|---|---|---|
| `I – IV – V – I` | Plain, strong | Rock, blues, folk, country |
| `I – IV – I – V` | Traditional | Folk, country |
| `I – V – IV – V` | Static, driving | Rock, indie |
| `I – iii – IV – V` | Bright, open | 80s pop, anime |
| `I – vi – ii – V` | Rhythm changes A | Jazz, city pop |
| `ii – V – I` | The jazz cell | Jazz, bossa, liquid D&B |
| `iii – vi – ii – V – I` | Extended circle | Jazz standards |
| `I – IV – vi – V` | Warm, resolved | Pop |
| `I – V – vi – iii – IV – I – IV – V` | Pachelbel canon | Pop, classical, everywhere |
| `IV – V – iii – vi` | **Royal road** | J-pop, city pop, anime, future bass |
| `I – bVII – IV – I` | Mixolydian rock | Rock, Britpop, folk |
| `I – IV – iv – I` | The borrowed minor iv | Pop, soul, Beatles |
| `I – V/vi – vi – IV` | Secondary dominant lift | Pop, gospel |
| `I – I7 – IV – iv` | Blues-to-borrowed | Soul, jazz-pop |
| `I – bIII – IV – I` | Bright modal mixture | Rock, film |
| `I – bVI – bVII – I` | Epic mixture | Film, metal, EDM |
| `Imaj7 – #Idim7 – ii7 – V7` | Chromatic passing | Jazz, lo-fi |
| `I – vi – iii – IV` | Gentle descent | Ballads |
| `I – V – bVII – IV` | Modal rock | Classic rock |

## Minor-key progressions

| Progression | Feel | Genre |
|---|---|---|
| `i – bVI – bIII – bVII` | The minor anthem | Trance, EDM, metal, D&B |
| `i – bVII – bVI – V` | **Andalusian cadence** | Flamenco, metal, trap, hip-hop |
| `i – bVI – bVII – i` | Modal, driving | Rock, synthwave, D&B |
| `i – iv – bVII – bIII` | Circle motion | Liquid D&B, house |
| `i – bIII – bVII – iv` | Melancholic loop | Lo-fi, indie, D&B |
| `i – iv – v – i` | Plain, medieval | Folk, dark ambient |
| `i – iv – V7 – i` | Harmonic minor cadence | Neoclassical, psytrance, film |
| `iiø – V7 – i` | Minor jazz cell | Jazz, noir |
| `i – bVII – bIII – bVI` | Endless circle | House, trance, synthwave |
| `i – v – bVI – bVII` | Modern, cool | Pop, R&B |
| `i – bII – i` | Phrygian menace | Trap, hard techno, metal |
| `i – bVI – iv – V` | Dramatic | Cinematic, ballad |
| `i – IV` (Dorian) | Cool two-chord vamp | House, funk, D&B, jazz |
| `i – bVI – III – bVII` | Bright inside dark | Synthwave, pop |
| `i – bIII – iv – bVI` | Rising melancholy | Liquid, ambient |
| `i – V – i – bVII` | Old-world, folk | Balkan, klezmer, folk metal |
| `i – bVII – iv – i` | Dorian rock | Rock, funk |
| `i – iv – bVI – V` | Classical minor | Film, neoclassical |

In A minor:
```
i    = [57, 60, 64]  Am
bIII = [60, 64, 67]  C
iv   = [62, 65, 69]  Dm
v    = [64, 67, 71]  Em
V    = [64, 68, 71]  E   (harmonic minor)
bVI  = [65, 69, 72]  F
bVII = [67, 71, 74]  G
```

## Two-chord vamps (for loop-based music)

| Vamp | Mode | Genre |
|---|---|---|
| `im7 – IVmaj7` | Dorian | House, funk, liquid D&B |
| `im7 – bVIImaj7` | Aeolian | Lo-fi, downtempo |
| `Imaj7 – IVmaj7` | Ionian/Lydian | Lo-fi, city pop |
| `im7 – bVImaj7` | Aeolian | Synthwave, darkwave |
| `im – bIImaj` | Phrygian | Trap, techno, metal |
| `I – II` | Lydian | Dream pop, film |
| `I7 – IV7` | Mixolydian/blues | Funk, blues |
| `im9 – V7alt` | Minor ii–V | Jazz, neo-soul |
| `Imaj7 – iii7` | Ionian | Bossa, soft |
| `im11 – IVm11` | Modal | Ambient techno |

## Seventh-chord versions (add colour to any of the above)

| Triad | Upgrade to |
|---|---|
| `I` | `Imaj7`, `Imaj9`, `I6/9`, `Iadd9` |
| `ii` | `ii7`, `ii9`, `ii11` |
| `IV` | `IVmaj7`, `IVmaj9`, `IV6` |
| `V` | `V7`, `V9`, `V13`, `V7sus4`, `V7b9` |
| `vi` | `vi7`, `vi9`, `vi11` |
| `i` | `im7`, `im9`, `im11`, `im6`, `imMaj7` |
| `bVI` | `bVImaj7`, `bVImaj9` |
| `bVII` | `bVII`, `bVII7`, `bVIImaj7`? (usually plain or dominant) |

**Rule:** in groove genres (house, R&B, lo-fi, D&B, jazz) upgrade everything.
In anthemic genres (trance, big room, rock, hardstyle) leave the triads bare.

## Jazz standard progressions

| Progression | Source |
|---|---|
| `Imaj7 – vi7 – ii7 – V7` | Turnaround, everywhere |
| `iii7 – VI7 – ii7 – V7` | Turnaround variation |
| `Imaj7 – VI7 – ii7 – V7` | With a secondary dominant |
| `iiø7 – V7b9 – i` | Minor ii–V–i |
| `Imaj7 – I7 – IVmaj7 – iv – I` | Backdoor-ish |
| `Cmaj7 – Ebdim7 – Dm7 – G7` | Chromatic passing dim |
| **Rhythm changes A** `I – vi – ii – V | I – vi – ii – V | I – I7 – IV – #IVdim | I/V – vi – ii – V` | "I Got Rhythm" |
| **Rhythm changes B** `III7 – VI7 – II7 – V7` (2 bars each) | The bridge |
| **Autumn Leaves** `ii7 – V7 – Imaj7 – IVmaj7 – viiø – III7 – vi` | Circle of fifths |
| **Coltrane changes** `Imaj7 – bIII7 – bVImaj7 – VII7 – IIImaj7 – V7 – Imaj7` | Giant Steps; major thirds cycle |
| **Blues (jazz, F)** `F7 Bb7 F7 Cm7-F7 / Bb7 Bdim7 F7 D7 / Gm7 C7 F7-D7 Gm7-C7` | |
| **Modal (So What)** `Dm7 (16) – Ebm7 (8) – Dm7 (8)` | Modal jazz |

## Gospel and neo-soul moves

| Move | Description |
|---|---|
| `IV – iv – I` | The plagal-with-borrowed-minor |
| `bVII7 – I` | Backdoor cadence |
| `I – I/3 – IV – #IVdim – I/5` | Chromatic bass ascent |
| `ii7 – bII7 – Imaj9` | Tritone sub resolution |
| `IVmaj7/5 – V7sus – V7 – I` | The gospel cadence |
| `I – vi7 – ii7 – V7 – iii7 – VI7 – ii7 – V7` | Extended turnaround |
| Constant-structure parallel `m9` chords descending by whole step | Modern neo-soul |

## Cinematic and modal colour progressions

| Progression | Effect |
|---|---|
| `I – bVI` (chromatic mediant) | Wonder |
| `I – III` (chromatic mediant) | Awe, heroic |
| `i – bVI – bIII` | Epic minor |
| `I – II` (Lydian) | Magic, flight |
| `i – bII – bIII – bII` | Menace |
| `I – bIII – bVI – bVII` | Adventure |
| `i – i(add9) – bVI – bVII` | Modern trailer |
| Parallel triads sliding chromatically | Impressionist, dream |
| `Isus2 – IVsus2 – bVIIsus2` | Open, wide, no commitment |
| Quartal chords moving in parallel | Sci-fi, mystery |

## Chromatic bass lines (any of these harmonises a static melody)

**Descending from I:**
```
C – C/B – Am – Am/G – F – Fm/Ab – C/G – G7
bass: C  B    A     G     F    Ab     G     G
```

**Descending "lament" (i – i/7 – bVII... )**
```
Am – Am/G# – Am/G – Am/F# – F – E
bass: A  G#  G  F#  F  E
```

**Ascending:**
```
C – C/E – F – F#dim – C/G – A7 – Dm7 – G7
bass: C  E  F  F#  G  A  D  G
```

## Building your own: a decision procedure

1. Pick the mode and tonic.
2. Pick a length: 2, 4, or 8 bars.
3. Choose the **first** chord (usually i or I) and the **last** chord
   (tonic to close, V or bVII to force a loop).
4. Fill the middle with strong root motion — prefer down-a-5th, down-a-3rd, or
   up-a-step.
5. Add **one** non-diatonic chord if you want interest.
6. Voice-lead it: keep common tones, move other voices by 1–2 semitones.
7. Design the top note line deliberately.
8. Check it against the melody: melody notes on strong beats must be chord tones
   or legal tensions.

## Related

- Why these work: `../00-foundations/06-harmony-function.md`
- Voicing them: `../00-foundations/05-chords.md`, `../00-foundations/07-voice-leading.md`
