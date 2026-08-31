# Bass

In modern music the bass is not "the low part of the harmony". It is a rhythm
instrument that happens to carry pitch, and in most electronic genres it is the
lead instrument.

## What the bass does

1. **Defines the harmony's root** — the same chord over a different bass note is
   a different chord.
2. **Locks to the kick** — bass and kick share 40–120 Hz and must be arranged in
   time so they do not fight.
3. **Carries the groove** — the interaction of bass rhythm and drum rhythm *is*
   the groove in funk, house, D&B, garage and hip-hop.
4. **Supplies physical energy** — everything below ~80 Hz is felt in the chest,
   not heard. That is the payload of club music.

## The two bass layers

Almost every modern electronic track has **two** distinct bass elements, and
confusing them is the most common production error.

| Layer | Range | Content | Rules |
|---|---|---|---|
| **Sub** | 30–90 Hz (MIDI 24–45) | Near-sine, no character | **Mono. Monophonic. No reverb. Minimal distortion.** Just pitch and envelope. |
| **Mid/top bass** | 90–800 Hz+ | The character: reese, growl, saw, pluck, 808 harmonics | Can be stereo above ~150 Hz, distorted, filtered, modulated |

Design them as one instrument in two bands. A common approach: one oscillator
low-passed at 90 Hz for the sub, a separate distorted/modulated layer high-passed
at 90–120 Hz for the character. Keep both playing the same notes, or put the
character layer an octave up.

**HAZARD:** distorting a sub bass generates harmonics *and* intermodulation
products, which eat headroom and make the low end sound smaller, not bigger.
Distort the mid layer, keep the sub clean.

## Register: where the root note should live

| MIDI | Note | Hz | Verdict |
|---|---|---|---|
| 21–27 | A0–Eb1 | 27–39 | Below most speakers; energy is wasted, felt only on big systems |
| 28–33 | E1–A1 | 41–55 | **The club sweet spot.** Deep and reproducible |
| 34–40 | Bb1–E2 | 58–82 | **The universal safe zone.** Works on phones and clubs |
| 41–47 | F2–B2 | 87–123 | Punchy, warm, "bass guitar" |
| 48+ | C3+ | 131+ | Mid bass; needs a sub layer beneath it to feel low |

**Practical:** put your tonic root between MIDI 29 and 40. This is why F minor
(F1 = 29, 43.7 Hz), G minor (G1 = 31, 49 Hz) and A minor (A1 = 33, 55 Hz) are
the default club keys.

**HAZARD:** a bassline that leaps around across two octaves loses power on every
note that goes high. Keep the low anchor and move the *character* layer instead.
If the line must ascend, consider dropping the top notes an octave (the "octave
fold") so the whole line stays in 29–45.

## Bass and kick: the collision

Both occupy 40–120 Hz. Four solutions, usable in combination:

| Technique | How | Genres |
|---|---|---|
| **Rhythmic separation** | Bass notes never start exactly with the kick; bass fills the gaps | Funk, D&B, jungle, garage |
| **Sidechain ducking** | Bass volume drops for 40–150 ms on every kick | House, techno, trance, EDM — the "pumping" sound |
| **Frequency split** | Kick owns 50–70 Hz, bass owns 80–120 Hz (or vice versa) | Techno, dubstep |
| **Tuning** | Tune the kick to the key's root or fifth so its pitch reinforces the bass | Hardstyle, techno, trap |
| **Same element** | The 808 *is* the kick and the bass | Trap, drill, phonk |

**Sidechain settings that work**: attack as fast as possible, hold 20–50 ms,
release matched to the tempo — usually a 1/16 or 1/8 note (at 128 BPM: 117 or
234 ms), depth 3–10 dB for subtlety, 10–20 dB for the audible pump.

## Note length is a parameter

| Length | Effect |
|---|---|
| Very short (30–80 ms) | Punchy, percussive, leaves space; trap 808 staccato, techno stabs |
| 1/16–1/8 | Rolling, driving; D&B, house |
| Sustained through the bar | Weight, drone; dubstep, dark techno, ambient |
| Overlapping / legato | Gliding, liquid; reese basses with portamento |

**HAZARD:** overlapping sub notes cause phase cancellation and level jumps —
one note's tail against another's attack can cancel almost entirely. Enforce
strict monophony in the sub layer with a short (5–15 ms) release, or use
portamento/glide so the oscillator never restarts.

## Bass line construction

### From simplest to most complex

1. **Root on every downbeat.** Always correct, never interesting alone.
2. **Root + octave.** Add the octave above on offbeats. Disco, house, techno.
3. **Root + fifth.** The oldest bass line in the world.
4. **Root + fifth + octave + b7.** Rock, boogie.
5. **Arpeggiated chord tones.** Trance, synthwave, funk.
6. **Scale-based line with passing tones.** Funk, R&B, jazz.
7. **Walking bass.** One note per beat, mostly stepwise, root on the downbeat of
   each chord, chromatic approach into the next root. Jazz.
8. **Riff bass.** The bass line *is* the hook: a fixed melodic-rhythmic figure.
   D&B, dubstep, drill, funk, metal.
9. **Modulated single note.** One pitch, everything happening in the timbre —
   wobbles, growls, formant sweeps. Dubstep, neuro.

### Approach notes — how to make any bass line sound intentional

Before landing on a new chord root, approach it:

| Approach | From | Feel |
|---|---|---|
| Chromatic from below | root − 1 | Jazz, funk; strongest pull |
| Chromatic from above | root + 1 | Smooth, descending |
| Dominant (a fifth above) | root + 7 | Functional, strong |
| Scale step | root ± 2 | Neutral, melodic |
| Octave leap | root ± 12 | Emphatic |

Put the approach note on the last 8th or 16th of the bar. This single habit
turns a static root-note bass into a line.

## Genre bass grammar (summary)

| Genre | Rhythm | Character | Range |
|---|---|---|---|
| **House** | Offbeat 8ths, or rolling 16ths | Round, filtered saw or sine; short | MIDI 33–45 |
| **Deep house** | Sparse, syncopated, dubby | Warm sine + slight sat | 29–40 |
| **Techno** | 16ths or offbeats, hypnotic | Sub + distorted mid, or one drone | 28–40 |
| **Trance** | Offbeat 8ths ("rolling bass"), 3 hits per beat gap | Short, plucky, filtered | 33–45 |
| **Drum'n'bass** | Long sub notes + separate mid riff | Reese, wobble, sub | 28–38 |
| **Jungle** | Ragga sub, sparse, huge | Pure sine, long | 26–36 |
| **Dubstep** | Halftime, modulated | Growl, wobble, formant, LFO | 28–45 |
| **Trap** | 808 slides, tresillo | Distorted 808 sine with pitch glides | 24–40 |
| **Drill** | Sliding 808s, syncopated | Same, with heavy glide | 24–38 |
| **UK garage** | Syncopated, "bouncy", off-grid | Filtered saw, organ bass, sub | 31–43 |
| **Funk** | 16ths with ghost notes, slap | Fingered/slapped electric bass | 28–52 |
| **Disco** | Octave 8ths, walking-ish | Round electric bass | 33–52 |
| **Reggae/dub** | Sparse, plays around the one | Deep, round, muted | 26–40 |
| **Rock/metal** | Follows guitar riff or root 8ths | Picked, distorted | 28–48 |
| **Synthwave** | Driving 8ths or 16ths | Saw or square with sidechain | 33–45 |
| **Ambient** | Long drones or nothing | Sine, filtered noise | 24–40 |

## The 808 in detail

A tuned sine with a long exponential decay, usually distorted. It is a kick and a
bass simultaneously.

- Pitch: the fundamental is the note; the click at the start is a separate
  transient layer.
- **Glide/portamento** between notes is the defining gesture of trap and drill —
  slide times of 40–150 ms.
- **Distortion** is what makes it audible on phones: saturating the 808 creates
  harmonics at 2×, 3× the fundamental (e.g. an 808 at 50 Hz gets content at 100,
  150, 200 Hz) which small speakers can reproduce, and the ear reconstructs the
  missing fundamental.
- Decay length is a rhythmic parameter: a long 808 fills the bar, a short one
  leaves the beat open.

## Reese bass

Two (or more) detuned sawtooth oscillators, low-passed, with the detune creating
a beating/phasing movement. Named after Kevin Saunderson's "Just Want Another
Chance".

- Detune 8–30 cents for a slow throb; more for a growl.
- Add a third oscillator an octave down, or a clean sine sub, to restore the low
  end that phase cancellation eats.
- Movement comes from: filter LFO, phaser, notch filter sweeps, chorus.
- **HAZARD:** a detuned pair periodically cancels in mono. Always keep a mono
  sine sub underneath and check mono compatibility.

## Wobbles and growls

- **Wobble** = LFO on a low-pass filter cutoff, synced to note values
  (1/4, 1/8, 1/8T, 1/16, 1/32). Changing the LFO rate per bar *is* the
  arrangement in dubstep.
- **Growl** = the same idea with a much faster LFO (20–100 Hz) or FM, so the
  modulation itself becomes audible as timbre rather than rhythm.
- **Talking bass / formant** = band-pass filters at vowel frequencies.
  Rough vowel formant pairs (F1/F2): "ee" 270/2300, "eh" 530/1840,
  "ah" 730/1090, "oh" 570/840, "oo" 300/870 Hz. Sweeping between two vowels is
  the classic neurofunk/dubstep move.

## HAZARDS checklist

- Two sub notes sounding at once → mud and level jumps.
- Sub bass in stereo → collapses in mono, energy lost on club systems.
- Reverb on the sub → smears the low end into a wash.
- Bass and kick starting on the same sample → phase interaction, unpredictable
  level. Offset by a few ms or sidechain.
- Bass line too high → no weight; too low → inaudible on phones. Layer.
- Fully quantised bass with no note-length variation → lifeless.
- Bass playing a chord's 3rd or 7th on a downbeat without intent → the harmony
  reads as an inversion you did not want.

## Related

- Kick/bass frequency split: `13-frequency-and-eq.md`
- Sidechain: `14-dynamics-and-compression.md`
- Bassline patterns per genre: `../30-patterns/03-bassline-cookbook.md`
