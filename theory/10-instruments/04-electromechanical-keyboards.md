# Electromechanical Keyboards

Not synthesisers: machines that make sound physically and amplify it
electrically. Their character comes from mechanical imperfection, and they
remain the warmest sounds available in electronic production.

---

## Hammond organ + Leslie speaker (1935 / 1940s)

**Type:** tonewheel organ — 91 spinning metal wheels next to pickups, mixed by
**drawbars**. This is **additive synthesis**, built in 1935.

### The drawbars
Nine drawbars per manual, each adding one harmonic at a level from 0 to 8:

| Drawbar | Footage | Harmonic | Interval above the key |
|---|---|---|---|
| 1 | 16' | sub-fundamental | octave below |
| 2 | 5⅓' | sub-third | fifth above (third harmonic, an octave down) |
| 3 | 8' | fundamental | unison |
| 4 | 4' | 2nd | octave |
| 5 | 2⅔' | 3rd | octave + fifth |
| 6 | 2' | 4th | 2 octaves |
| 7 | 1⅗' | 5th | 2 octaves + major third |
| 8 | 1⅓' | 6th | 2 octaves + fifth |
| 9 | 1' | 8th | 3 octaves |

Classic registrations (drawbar settings, 0–8 per bar):
```
888000000   full, fat, gospel/rock "first three"
888800000   brighter rock
800000888   the hollow "whistle" jazz sound
868868868   a common jazz/blues setting
88 8000 000 + percussion 3rd   the Jimmy Smith jazz organ
```

### The other controls
| Control | Effect |
|---|---|
| **Percussion (2nd/3rd, fast/slow, soft/normal)** | A decaying attack transient; only sounds on the *first* key of a legato phrase |
| **Vibrato/Chorus (V1–V3, C1–C3)** | A scanner-based delay line; C3 is the classic |
| **Key click** | The switch contacts making and breaking; originally a defect, now essential |
| **Overdrive** | The tube preamp pushed — the rock/gospel sound |
| **Leslie speed** | Chorale (slow, ~0.8 Hz) / Tremolo (fast, ~6.8 Hz); the *transition* between them is the expressive move |

### Why the Leslie matters
A Leslie is a rotating horn (highs) and a rotating drum baffle (lows), spinning
at different rates, in a wooden cabinet, miked from outside. It produces
simultaneous **Doppler pitch modulation**, **amplitude modulation**, and
**comb filtering from room reflections**, and the two rotors accelerate and
decelerate at different rates when you switch speed.

**Rebuild:** split the signal at ~800 Hz. Apply to each band: pitch modulation
(±10–25 cents), amplitude modulation (20–40% depth), and panning, all at the same
LFO rate but with the horn at ~7 Hz and the drum at ~6 Hz when fast, ~0.8/0.7 Hz
when slow. Ramp the rates over 1–3 seconds when switching. Add mild distortion
before it and a room reverb after.

---

## Fender Rhodes (1965–1984)

**Type:** electric piano. A hammer strikes a **tine** (a stiff steel rod) next to
a **tonebar**; an electromagnetic pickup senses the vibration.

### Character
- A **bell-like inharmonic attack** followed by a nearly sinusoidal sustain.
- **Velocity changes the timbre enormously**: soft = pure and dark, hard = a
  metallic "bark". This is not a volume change — the harmonic content shifts.
- Slight detuning and tine-to-tine inconsistency across the keyboard.
- The classic sound is a Rhodes into a **stereo tremolo** (the Suitcase model's
  built-in "vibrato", which is actually auto-panning) and often a **phaser** or
  **chorus**.

### What it changed
Jazz fusion, soul, funk, neo-soul, lo-fi hip-hop, liquid drum & bass, and
house. Herbie Hancock, Stevie Wonder, Bill Evans, D'Angelo, and every lo-fi
beat ever made.

### Rebuild
```
Sine fundamental + a bell-ish inharmonic layer (partials at ~1, 4.2, 9.6 x f)
Attack:   0 ms; the inharmonic layer decays in 80-250 ms, the sine in 1.5-4 s
Velocity: maps to the inharmonic layer's LEVEL and the low-pass cutoff
          (soft = 800 Hz, hard = 6 kHz), not just to output level
FX:       stereo tremolo/auto-pan at 4-6 Hz, phaser, light overdrive, spring or
          plate reverb
```

---

## Wurlitzer 200A (1968)

Similar concept, different physics: hammers strike **reeds**, not tines. The
result is more aggressive and reedier, with a distinctive growl when played hard
and a hollow, woody softness when played gently. Built-in tremolo (amplitude, not
panning) at around 5.5 Hz.

Heard on: Supertramp, Ray Charles, Queen ("You're My Best Friend"), Norah Jones,
and a lot of indie and modern soul.

**Rebuild:** as the Rhodes, but with more odd harmonics (a soft square component)
and a much more pronounced overdrive response to velocity. Mono tremolo, not
auto-pan.

---

## Hohner Clavinet D6 (1971)

**Type:** electrically amplified clavichord — a rubber-tipped hammer strikes a
string, magnetic pickups sense it. Short, percussive, and enormously funky.

Its rocker switches select pickup combinations (brilliant/treble/medium/soft)
and filters. Almost always played through a **wah pedal**, a **phaser**, or
both.

The definitive sound: Stevie Wonder's "Superstition".

**Rebuild:** a short, bright plucked tone (Karplus–Strong works well) with a
40–150 ms decay, band-passed at 800 Hz–3 kHz, into an auto-wah or an
envelope-following band-pass filter, with a phaser after it.

---

## Mellotron (1963)

**Type:** a keyboard where every key plays back its own **8-second tape strip**
of a recorded instrument. Release the key and the tape springs back to the start.

### The constraints that made the sound
- **8 seconds maximum per note.** You cannot hold a chord longer.
- Tape wow, flutter, azimuth error and inconsistent playback speed between keys —
  so the "choir" is slightly out of tune with itself and constantly wobbling.
- The heads and tapes degrade, so the timbre changes as the machine is used.

Famous tape banks: **3 Violins**, **MkII Flute** ("Strawberry Fields Forever"),
**8-Voice Choir**.

Heard on: The Beatles, King Crimson, Genesis, Radiohead, Tame Impala, and
almost all "hauntology" and library-music-influenced production.

**Rebuild:** sample a string or choir, apply per-note random pitch drift
(±10–20 cents, 0.5–2 Hz), per-note random start-time offset (0–40 ms), a
low-pass at 5 kHz, tape hiss, and — critically — a hard 8-second limit with a
sudden end.

---

## Combo organs: Vox Continental / Farfisa (1962/1964)

Transistor divide-down organs with a thin, buzzy, reedy tone. The Vox is
brighter and hollow ("House of the Rising Sun", The Doors); the Farfisa is
nasal and cheap-sounding in the best way (Pink Floyd, Sam the Sham, and most
60s garage).

**Rebuild:** a stack of square waves at octave and fifth relationships, with a
fixed band-pass and a fast vibrato. No filter envelope — the tone never changes.

---

## Why these still matter in electronic music

Every one of these instruments is a **velocity-sensitive, timbrally variable,
slightly imperfect** sound source — the opposite of a synthesiser preset. When a
programmed track sounds sterile, adding one of these (real, sampled, or
modelled with the recipes above) is the fastest fix, because it brings:

- Timbre that changes with how hard the note is played.
- Slight tuning inconsistency between notes.
- Mechanical noise (key click, hammer thud, pedal noise) that reads as "real".
- A decay that is not exponential.

## Related

- Velocity and humanisation: `../30-patterns/09-humanization-and-groove.md`
- Where they live in genres: `../20-genres/19-funk-soul-and-rnb.md`, `../20-genres/13-lofi-and-chillhop.md`
