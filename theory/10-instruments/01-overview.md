# Landmark Instruments — Overview

Electronic music's vocabulary was not invented in the abstract. It was invented
by specific machines, most of them with severe limitations, and the limitations
became the style. The 303 was a failed bass accompaniment box. The 808 sounded
nothing like real drums and was discontinued. The DX7 was too hard to programme,
so everyone used the presets — and those presets became the sound of a decade.

This section is a catalogue of the machines that mattered, written so their
sounds can be rebuilt with anything: another synth, a plugin, or code.

## How to read these files

Each instrument entry gives:

| Field | Meaning |
|---|---|
| **Year / type** | When it arrived and what kind of synthesis it uses |
| **Signal path** | The architecture, as a chain you can reproduce |
| **The controls that matter** | Which parameters actually change the character |
| **Why it sounds like that** | The specific engineering quirk responsible |
| **What it changed** | The genres and records that came out of it |
| **Rebuild** | Concrete settings to get the sound from a generic synth |

**The rebuild instructions are the point.** You almost never need the original
machine — you need to know that the TB-303's filter is 18 dB/octave rather than
24, that the DX7's electric piano is two operators at a 1:1 ratio with a fast
index decay, or that the JP-8000 supersaw is seven saws with a specific
non-linear detune curve. That is transferable knowledge.

## The section

| File | Covers |
|---|---|
| `02-analog-monosynths.md` | Minimoog, ARP 2600, Odyssey, MS-20, SH-101, TB-303, VCS3 |
| `03-analog-polysynths.md` | Prophet-5, Jupiter-8, Juno-106, OB-Xa, CS-80, Polysix |
| `04-electromechanical-keyboards.md` | Hammond/Leslie, Rhodes, Wurlitzer, Clavinet, Mellotron, string machines |
| `05-fm-and-phase-distortion.md` | DX7, TX81Z, Casio CZ, FM programming in general |
| `06-wavetable-vector-and-la.md` | PPG Wave, Prophet VS, Wavestation, D-50, Microwave |
| `07-samplers-and-workstations.md` | Fairlight, Synclavier, Emulator, SP-1200, MPC, S950, M1, JD-800 |
| `08-drum-machines.md` | TR-808, TR-909, LinnDrum, DMX, CR-78, 707, Simmons |
| `09-virtual-analog-and-90s.md` | JP-8000 (supersaw), Virus, Nord Lead, Supernova, grooveboxes |
| `10-modular-and-west-coast.md` | Moog modular, Buchla, Serge, Eurorack, Mutable |
| `11-chips-trackers-and-voices.md` | SID, NES, Game Boy, YM2612, Amiga/ProTracker, vocoder, talkbox |
| `12-software-instruments.md` | Reaktor, Massive, Sylenth1, Serum, Vital, Omnisphere, Diva, Harmor… |
| `13-effects-and-processors.md` | Space Echo, Lexicon, EMT, RMX16, H3000, Kaoss, OTT, Auto-Tune |
| `14-iconic-patch-recipes.md` | The hoover, the supersaw, the Reese, the 808 kick, the M1 piano… |
| `15-why-old-gear-sounds-like-that.md` | Aliasing, drift, bit depth, filter non-linearity, timing |

## The shortest possible history

| Era | Machines | What became possible |
|---|---|---|
| 1964–1970 | Moog modular, Buchla | Synthesis as a musical instrument at all |
| 1970–1977 | Minimoog, ARP 2600, VCS3 | Portable, playable, in bands |
| 1978–1983 | Prophet-5, Jupiter-8, OB-Xa, CS-80 | Programmable polyphony; patch memory |
| 1980–1985 | TR-808, TR-909, LinnDrum, TB-303, DMX | The rhythm machine as the composer |
| 1979–1988 | Fairlight, Synclavier, Emulator, SP-1200, S900 | Sampling: any sound becomes an instrument |
| 1983–1990 | DX7, D-50, M1, PPG, Wavestation | Digital timbres nobody had heard before |
| 1988–1996 | Amiga trackers, Akai S1000, Alpha Juno, Roland W-30 | Bedroom production; rave; the hoover; jungle |
| 1995–2003 | JP-8000, Nord Lead, Virus, ReBirth, Reason, FL Studio | Virtual analog; the supersaw; the DAW |
| 2004–2014 | Massive, Sylenth1, Nexus, Kontakt, Ableton | The plugin economy; dubstep and EDM |
| 2014– | Serum, Vital, Phase Plant, Omnisphere, Eurorack revival | Wavetable everywhere; visual sound design |

## The one lesson to carry out of this section

**Constraints produce style.** Every sound here that people love came from a
machine that could not do something:

- The SP-1200 could only sample 10 seconds at 12 bits — so producers chopped
  tightly, and the aliasing became the texture of golden-age hip-hop.
- The DX7 had no filter — so its brightness had to come from FM index
  envelopes, which is why its bells and electric pianos evolve as they decay.
- The 303 had a strange 3-pole filter and an accent circuit that could not be
  turned off — so acid house sounds like that and nothing else does.
- The Juno-106 had one oscillator — so its chorus had to do the thickening,
  and that noisy chorus is now the definition of "warm 80s pad".
- The Amiga had four 8-bit channels — so jungle producers layered breaks
  destructively and learned to make one channel do three jobs.

When you build a sound, **decide what your instrument cannot do**. An
unconstrained synthesiser produces unconstrained, characterless results.

## Related

- The synthesis theory behind all of it: `../00-foundations/12-timbre-and-synthesis.md`
- Where these sounds belong: `../20-genres/`
- Generic patch recipes: `../30-patterns/08-sound-design-recipes.md`
