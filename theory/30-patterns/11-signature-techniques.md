# Signature Techniques — Gesture, Not Just Notes

A genre is identified far more by **how its sounds move over time** than by which
notes or instruments it uses. Two producers can use the same synth, the same
scale and the same drum pattern and land in different genres, because the
*gestures* differ.

This file is about that layer: the characteristic movements. The per-genre files
each carry a **Signature techniques** section applying it.

## The failure mode this exists to prevent

**Implementing a gesture as a note pattern.**

The most common form: a sound whose identity is *internal modulation* gets
written as a *sequence of separate notes*. The notes may be correct, the rhythm
may be correct, and the result is still wrong — because the genre's gesture was
never performed.

### Worked example: the neurofunk bass

**What it is not:** an arpeggiator. A run of short notes, one per 16th, stepping
through chord tones.

**What it is:** *one long sustained note* — often a single pitch held for one or
two bars — whose **modulation rate changes inside the note**.

```
bar 1  |  vzhuuuuuuu        LFO at 1/4   — slow, wide, the note breathes
bar 2  |  VZHU-ZHU-ZHU      LFO at 1/8   — the rate doubles, still one note
bar 3  |  zhuzhuzhuzhuzhu   LFO at 1/16  — now it reads as texture, not rhythm
bar 4  |  zhu-zhu-ZHUUU     rate drops back, and the note finally releases
```

Nothing about the pitch changed. Everything about the *timbre's rate of change*
did. That is the gesture, and it cannot be produced by triggering more notes —
retriggering resets the envelope and destroys the continuity the sound depends
on.

**How to implement it**

```
1. ONE note event, 1-2 bars long. Do not retrigger.
2. Inside it, automate:
     - filter cutoff LFO RATE: stepped or ramped, 1/4 -> 1/8 -> 1/16 -> 1/8T
     - LFO depth and shape (sine for smooth, saw-down for a rhythmic drop)
     - wavetable position, or FM index, on its own slower curve
     - two band-pass formant frequencies, swept between vowels
     - a notch/phaser sweeping independently of the filter
3. Keep a SEPARATE clean sine sub underneath, unmodulated and unretriggered.
4. Resample the result to audio, then process again - the second pass is where
   the "impossible" quality comes from.
5. Pitch moves rarely, and when it does it is a gesture: an octave drop, a
   slide into the next phrase, a bend at the end of 4 bars.
```

**The general test:** if you can write the part as a list of `(step, pitch)`
pairs and lose nothing, it was not this gesture.

## The gesture taxonomy

| Gesture | What moves | Where it defines a genre |
|---|---|---|
| **Modulation-rate change** | The speed of an LFO *inside* one sustained note | Neurofunk, dubstep, drum & bass |
| **Note-length manipulation** | Sustain vs. stab; ties across bar lines | Reggae, house, funk, minimal |
| **Pitch glide** | Continuous portamento between notes | Trap, drill, 808 music, dub |
| **Pitch sweep** | A pitch envelope inside a single note | Hoover, hardstyle kick, Simmons toms, 808 |
| **Filter envelope per note** | Brightness falls as each note decays | Acid, plucks, funk |
| **Filter automation per phrase** | Brightness moves across 8–32 bars | Techno, house, trance |
| **Timbre morph** | Wavetable position, formant, FM index | Modern bass music, future bass |
| **Density ratchet** | The same hit repeated at an accelerating rate | Trap hats, footwork, IDM, drill |
| **Accent and ghost** | Level and articulation, not placement | Funk, jungle, D&B, boom bap |
| **Anticipation / push** | Arriving one 16th early | Funk, salsa, house, samba |
| **Effect throw** | A send opened for one hit, then closed | Dub, techno, garage |
| **Stutter / beat repeat** | Re-reading recent audio | Trap, hyperpop, breakcore |
| **Detune beating** | Interference between near-unison voices | Reese, supersaw, drone |
| **Register displacement** | The same part jumping an octave | Disco bass, jungle, chiptune |

## Reading a genre for its gestures

When the per-genre file does not say, ask these five questions about a reference
track:

1. **What is moving that is not a note?** Filter, position, formant, rate, level,
   space — the answer is usually the genre's identity.
2. **How long is the longest single note?** If the defining sound sustains for a
   bar, the gesture is internal. If it is all short hits, the gesture is
   placement and articulation.
3. **What repeats, and what evolves?** Loop-based genres hold the notes constant
   and evolve the timbre; song-based genres do the opposite.
4. **Where does the sound change relative to the bar?** On the downbeat, at the
   half-bar, every 4 bars — the rate of change is as characteristic as the sound.
5. **What is the smallest expressive unit?** A ghost note, a 32nd ratchet, a
   filter step, a pitch bend of 20 cents.

## Two rules that follow

1. **Automate inside notes, not only between them.** A part whose parameters are
   fixed for its whole duration is a sample trigger, not a performance. Most
   genre identity lives in the automation.

2. **Do not substitute rhythm for timbre.** When a sound is supposed to move,
   adding more notes is the wrong fix — it produces something busier and less
   like the genre. Ask whether the reference has more *events* or more
   *movement*.

## Related

- Per-genre applications: the **Signature techniques** section in each `../20-genres/` file
- Sound construction: `08-sound-design-recipes.md`
- Modulation theory: `../00-foundations/12-timbre-and-synthesis.md`
