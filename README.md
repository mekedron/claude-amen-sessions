# Claude Music

Music composed and coded by **Claude** in a single terminal session — no DAW,
no plugins, no audio libraries. Just numpy and scipy writing WAV files.

Two families so far:

- **Amen Sessions** — 19 drum & bass pieces in which every drum hit comes from
  one 6.9-second Amen break, sliced and resequenced.
- **Machine Rave** — pieces with no sample at all: every kick, cowbell, 808,
  reese, screech and tyre squeal is synthesized from scratch.

A human ran the session, picked the directions, listened, and gave feedback
("the stars need more depth", "that roll takes my ears off"); Claude wrote all
the code and made all the musical decisions. Claude cannot hear the renders —
they were verified by spectrogram and by measuring band balance, stereo width,
sidechain depth and transient punch against the tracks that already worked.

## The engine

    src/core.py       the shared engine: oscillators, 77 synths and effects,
                      the mix bus and the sequencer. Tempo-agnostic.
    src/sampler.py    the sample layer: load any audio file, lock it to a bar
                      grid, slice it, retime it - several at once, at
                      different tempos.
    src/core.py       also: `wtable()` / `wtscan()` (a wavetable stored as
                      harmonic spectra rather than as single-cycle buffers, so
                      the oscillator is exactly band-limited and the position
                      scan is an interpolation between amplitude vectors),
                      `scanlane()` (a modulation lane whose RATE is sequenced -
                      the difference between a bass line and an arpeggio),
                      `sawstack()` (a band-limited detuned saw stack,
                      the oscillator at the centre of most electronic bass and
                      lead design) and `brickwall()` (a look-ahead true-peak
                      limiter - `limiter()` averages its gain curve and so
                      pulls at peaks rather than stopping them, which is a
                      safety net and not a loudness stage), `svf()` (a real
                      time-varying resonant biquad - coefficients recomputed
                      every 64 samples with the state carried across, so it
                      rings and screams where a crossfaded filter bank
                      structurally cannot), `steplane()` / `ptlane()` /
                      `rlane()` (a per-sample parameter timeline built from
                      one value per step: an LFO repeats a shape, a lane is
                      sixteen unrelated numbers), `subbar()` (a whole phrase
                      of sub as ONE oscillator that never restarts),
                      `stretch()` (granular time-stretch - length without
                      pitch, where `pitched()` moves both), `ep()` (a tine
                      electric piano where velocity is brightness and high
                      notes die first) and `ens()` (a string section whose
                      players enter late and drift apart, rather than one
                      detuned oscillator)
    verify.clicks()   where a render has a discontinuity, in seconds and in
                      bars. The naive test - a big jump between two samples -
                      finds every kick and every hat, because a transient IS
                      a big jump and is meant to be; this one lowpasses at
                      2 kHz first, where a 46 Hz sine moves 0.0066 per sample
                      and any step is something that was cut rather than
                      something that was played
    src/verify.py     what a finished render actually contains: integrated
                      LUFS, true peak, PLR, band balance, crest PER BAND,
                      mono compatibility, a short-term loudness curve per
                      section, and the low band's energy per sixteenth of the
                      bar - which is the number that says whether a track has
                      a pulse. The one thing this project cannot do is listen,
                      so every claim about a mix is a measurement:
                          python3 src/verify.py renders/track.wav 140 4
    Session.ownership()  which BUS owns a band, as a share of the whole mix.
                      `report()` says where each bus's own energy sits, which
                      cannot answer the question that matters about a top
                      end: not "is this bus bright" but "what is the listener
                      standing under". A sustained source above about 20% of
                      3-16 kHz is a noise bed, and a noise bed at 6-9 kHz is
                      what hurts after ninety seconds
    core: the turntable  `rewind()`, `tape_stop()`, `scratch()` and `spin()`
                      read a segment with a varying rate, so the pitch travels
                      with the hand the way it does on a deck. A reversed copy
                      of a sample is not a scratch: the gesture is the pitch
                      moving, and `scratch()` reverses the read whenever its
                      rate goes negative
    src/amenlib.py    the Amen module: one Sample, prepared and named
    src/idmlib.py     the drill'n'bass module, 174 BPM: the same break, and a
                      knife. `edit()` writes a bar as sixteen tablature
                      characters plus a dict of parameter locks - this step is
                      a six-hit ratchet that accelerates, that one is reversed
                      and a fifth down, this one is stretched to twice its
                      length without moving in pitch. `ratchet()` is the
                      trill: the pitch travels across the group, the level
                      falls, each repeat is cut to a fraction of the gap it
                      has, and the last one is allowed to ring past its slot.
                      Under it `thump` and `crack` hold a pulse the break is
                      never asked to carry. `set_tempo()` moves the grid and
                      re-cuts the sample onto it - the slices are audio, not
                      note events, so a tempo change without a re-fit leaves
                      every chop playing at the old speed. And `felt()` is a
                      piano modelled
                      mode by mode - stiffness-stretched partials, a prompt
                      sound, two polarisations, hammer noise, and a `roll`
                      that stops a chord arriving as one event
    src/phonklib.py   the phonk module: the cowbell and the car, 160 BPM
    src/driftlib.py   the phonk-house module: the cowbell that screams,
                      the split bass and the gearbox, 156 BPM
    src/bruxarialib.py  the Brazilian bruxaria module: the chopped voice,
                      the tuned hand drum and the whistle, 164 BPM
    src/brphonklib.py the Brazilian phonk module, 140 BPM: a cowbell built
                      as sixteen resonators struck with noise rather than as
                      two squares under an envelope, a gated kick and a gated
                      split bass so the bottom is empty between beats, a
                      shaker whose envelope rises, and a shout
    src/houselib.py   the deep house module, 123 BPM: a round kick with no
                      tick in it, a 909 open hat that is TRUNCATED so four a
                      bar do not turn the top of the record to sand, a
                      subtractive chord pressed and released, a divide-down
                      string bank whose oscillators never restart, and - built
                      but deliberately unused on the first record - a modal
                      vibraphone and a one-oscillator-per-phrase alto
    src/hardlib.py    the hardstyle module: the kick, 170 BPM
    src/neurolib.py   the neurofunk module: the tight kit, the bass design
                      chain - reese, growl, talking formants, hard sync - and
                      `phrase()`, a whole bar of bass as one oscillator that
                      never restarts, at 174 BPM
    src/machinelib.py the machine-funk module, 174 BPM: neurofunk rebuilt
                      around a real time-varying resonant filter (`svf`) and a
                      sixteen-character bass tablature. `reese()` is measured
                      off two reference samples - a saw stack detuned 45 cents
                      through a 270-980 Hz resonant lowpass and a moving notch
                      bank, 95% of its energy under 400 Hz - and `bassbar()`
                      is the accent layer above it, where hard sync and phase
                      modulation are mixed in by their own lanes so a step
                      that does not ask for them hears none. Plus a modal kit
                      (a snare's five membrane modes, wires that start 2.2 ms
                      late), `mgloom()` for a dark melodic voice, and
                      `grains()`, which builds atmosphere out of the record's
                      own drums. `neurobass()` is the modern workflow end to
                      end: a spectral wavetable scan, a serial waveshaper /
                      saturator / bit-reducer with EQ between every stage, a
                      formant filter riding the same lane as the scan, and two
                      resampling passes. `GESTURES` and `phrase()` write a
                      bass line as a list of gestures - a stretched sweep, two
                      stabs of another patch, a sixteenth roll, a stutter -
                      and `stitch()` cuts two finished patches against each
                      other at the gesture boundaries
    src/industriallib.py  the industrial techno module: the rumble, the
                      machine hall, the acid and the choir, 152 BPM. Also
                      `deepacid()` - a 303 written as the BASS part, with its
                      overdrive split off the fundamental so the drive never
                      touches the sub, and the line's own octave under it as
                      a clean sine - and `openhat()`, six inharmonic squares
                      that ring for 400 ms and shed their top first, because
                      an open hat is not a closed hat with a longer envelope
                      (set_tempo() re-grids it for a slower piece). Also
                      `glare()` - a section of detuned saws that enter in
                      pitch order and wander in intonation like `ens()`, put
                      through the drive-EQ-drive-fold chain of `acid_hard()`
                      so a euphoric wall is made of the record's own
                      distortion rather than dropped in from a trance track -
                      and `sheet()`, an UNtuned bank of high resonant bands,
                      because everything else in an industrial kit is dark by
                      construction
    core.shimmer()    a reverb with an octave transposition inside its
                      feedback path, so a held chord grows a choir of its own
                      harmonics that nobody played - late, in tune, and
                      further away every pass. It is the only reverb that
                      adds notes, and damping in the loop is not a tone
                      control, it is what stops the octaves stacking into a
                      whistle
    src/minimallib.py the high-tech minimal module: a clean three-layer
                      kick, `line()` - a whole bar of a monophonic voice as
                      one unbroken oscillator - `acidline()`, a TB-303 with
                      the three-pole filter and the accent circuit the
                      machine actually has, and a percussion box of very
                      small things: rims, wood, FM bleeps, dust. 127 BPM
    src/synthlib.py   the synthwave module: a decade rebuilt from its
                      defects - `bbd_chorus` (the Juno's bucket brigade,
                      hiss included), `gatedsnare` (a bright reverb cut off
                      dead after 220 ms and mixed louder than the drum),
                      an 8-bit LinnDrum kit, Simmons toms, a DX7 electric
                      piano and `cassette` for the master. 116 BPM
    src/bigbeatlib.py the big beat module, 152 BPM: a surf guitar through a
                      real cabinet, a spring tank built from chirps, a 1971
                      kit crushed flat, an octave-fuzz bass, a turntable
                      (scratch, varispeed, stutter) and a formant speech
                      synthesiser
    src/funklib.py    the funk module, 112 BPM: a slap bass rendered a bar
                      at a time, a clavinet, a Hammond through a Leslie
                      whose two rotors change speed at different rates, a
                      tenor saxophone, a Rhodes, a talkbox, a vocoder, an
                      envelope filter and a 1982 drum machine
    src/latinlib.py   the Cuban module, and the only one that does not set its
                      own grid - it imports amenlib and shares the break's,
                      because 174 BPM is a salsa tempo as well as a drum &
                      bass one. A tumbadora with four strokes on three drums
                      (the modes of a circular head, a different set of them
                      excited by each stroke), bongos, a mambo bell struck on
                      the mouth and on the neck, a timbale shell, two rosewood
                      sticks, a scraped gourd built as an impulse train, a
                      piano rendered a bar at a time with three strings to a
                      note and a convolved soundboard, and a three-man horn
                      section that brightens when it is blown harder because
                      the wave steepens in the bore, not because a filter
                      opened
    src/chiplib.py    the console module, 138 BPM: a Mega Drive's
                      four-operator FM with all eight algorithms, an NES
                      pulse channel and its four-bit triangle, a real
                      fifteen-bit LFSR noise channel with the NES short
                      mode, a Game Boy wavetable, an eight-bit DAC channel
                      and one shared filter - all of it driven by a 60 Hz
                      frame clock, because that is how often the CPU got to
                      write to the chip
    src/skanklib.py   the other big beat module, 131 and 153 BPM: a live kit
                      read off a 16-step pattern, a 12-bit sampler, an
                      audible compressor, a fuzz bass, a 303, a drawbar
                      organ through a Leslie, a stiff steel string with
                      stretched partials, a dispersive spring, synthesised
                      speech and an accelerating retrigger
    src/junglelib.py  the jungle module, 166 BPM: the 1993-95 UK sound, which
                      is a reggae record with a funk break running over the
                      top. It borrows `idmlib`'s knife at a slower tempo and
                      adds what jungle is made of - `dubplate()` for the Akai
                      S950 (12 bits truncated, a converter that stops at
                      11 kHz), `deck()` for the second turntable, `smear()`
                      for the 1994 time-stretch with the combing left in on
                      purpose, `contrabass()` for a double bass played
                      pizzicato - stiffness-stretched partials, a decay rate
                      per mode, two polarisations, a wooden box with four
                      resonances, and the finger and the fingerboard at every
                      attack, all off one phase track so the portamento is a
                      fretless slide - `organbass()` for the same line on a
                      drawbar organ, `skank()` for the offbeat organ chop,
                      `figure()` which writes a bass line
                      as a rhythm with holes in it rather than as a row of
                      notes, `throw()` for the dub send that is opened for one
                      hit and closed again, and `ride()` for a gain move in
                      decibels per bar over the finished buses

A genre module sets the grid, adds its own kit and re-exports core, so
`from amenlib import *`, `from phonklib import *`, `from hardlib import *`,
`from industriallib import *`, `from punklib import *`,
`from bigbeatlib import *`, `from latinlib import *` and
`from skanklib import *` and `from junglelib import *` are the same API
with a different palette. One small script per piece,
arrangement only.

The sample layer finds hits by itself: pointed at the Amen break, `Sample.kit()`
recovers the map the break is documented by — kicks on 0, 2, 10, 11, snares on
4 and 12 — so an unfamiliar break can be loaded and played the same way, or
layered over a synthesized track:

```python
from phonklib import *
from sampler import Sample

brk = Sample('samples/some_break.wav', bars=4).fit()   # snapped to 160 BPM
s.place(s.pos(4), brk.bar(0))
s.place(s.pos(5), rev(brk.get(1, 8, 4)), 0.6)
```

## The tracks

All finished audio lives in `renders/`.

**Machine Rave** (nothing sampled, ~2:30 each):

| File | What it is |
|---|---|
| `phonk_drift_160.wav` | Drift phonk in F# minor: the 808 cowbell driven until it clangs, a sliding 808, memphis vocal chops, tyres and an engine. Three drops, a tape-stopped breakdown, pitched echoes thrown ear to ear |
| `hard_ascension_170.wav` | Industrial hardstyle in A minor: a kick put through drive, EQ, drive and a wavefolder, reverse bass swelling into every gap it leaves, and a euphoric breakdown that has to earn the drop it walks into |
| `neuro_bezdna_174.wav` | Dark neurofunk in F minor (4:28): programmed drums instead of a break, and a bass in three layers that never share a frequency. The line is not notes - it is two or three long ones a bar whose growl rate ramps from 5 Hz up past 40 and back down while a single note is still sounding, integrated so it accelerates rather than steps. Three drops, one chord progression in the whole track, and the Phrygian b2 as the only note from outside |
| `neuro_zuby_174.wav` | `neuro_bezdna_174.wav` with teeth (4:28): same key, same drums, same arrangement, note for note, and only the bass rebuilt. Folds rather than saturates so the harmonics stay odd and hollow, puts a transient on the front of every note, and swings the filter across its whole range instead of a corner of it |
| `neuro_techenie_174.wav` | Neurofunk in C minor (5:01), written against two measured records - Magnetude's "Exile" and Magnetude & Receptor's "Goodbye". The analysis said the mid bass in those makes four to six attacks a bar and the low end sounds 85% of the time, so the bass here is not notes at all: a whole bar is one oscillator that never restarts, with the filter, the sync ratio, the FM index and the vowel sequenced across it. Three layers, 33 / 65 / 130 Hz, that never share a frequency |
| `neuro_karusel_174.wav` | The same sound design, the opposite mood (4:33): funky neurofunk in G Dorian, where the natural 6 is what keeps a minor key from being sad. The bass bounces instead of holding - its filter shuts in 70 ms, so three quarters of every note is a gap - and answers itself in vowels. Kick and snare dead on the grid, hats and chords pushed 6% of a step late. The hook is a riff, not an arpeggio: every note is hard-synced and stepped, so the timbre tears upward while the pitch stays put. Under it a seven-note carousel turns on a sixteen-step bar and never lands in the same place twice |
| `neurofunk_razlom_174.wav` | Machine funk in F minor (4:28), written against four measured files: two Magnetude records for the mix and two reese samples for the sound. The bass is three layers that never share a band - a mono sine under 105 Hz rendered as one unbroken oscillator across eight bars, a reese built to the samples' own numbers (45 cents of detune, a 270-980 Hz resonant lowpass, a notch bank moving through the harmonics, 95% of its energy under 400 Hz), and above 680 Hz an accent layer that only speaks on the steps the tablature marks with teeth. The riff is written as sixteen characters a bar describing what the filter does, not what note is played; the same tablature is read four different ways across a thirty-two bar drop, so the oscillator narrows, widens, drives and notches while the notes stand still. Kick on 1 and 3 and snare on 2 and 4 in every cell, so there is an event on every beat and the felt pulse is 174 rather than 87 |
| `neurofunk_razryv_174.wav` | Machine funk in F minor (4:28), and the bass is a workflow rather than a patch. Two notes in two bars: everything heard as rhythm is the rate at which the timbre is travelling, sequenced as a list of gestures - a stretched sweep across half a bar, two stabs of a different patch, a sixteenth roll, a thirty-second stutter, a dive - with six different gesture sequences per riff so no two bars of a thirty-two bar drop are assembled the same way. The oscillator is a spectral wavetable whose position is scanned per sample; measured on one held note the scan moves the spectral centroid 1.6 octaves a bar against 0.7 for the same patch with the position nailed down. After it: a serial waveshaper, asymmetric saturator and bit-reducer with a 105 Hz highpass and an 8 kHz lowpass between every stage, a formant filter riding the same lane as the scan, and two resampling passes. Three layers that never share a band, a four-bar halftime section inside each drop, and a master at -1 dBTP where both reference records sit at +3 to +4 |
| `acid_nebel_130.wav` | Dub techno with acid in it, 6:24: an offbeat chord thrown into a delay that saturates inside its own feedback, and a 303 arriving from behind it. No kick for sixteen bars |
| `acid_rausch_138.wav` | Acid breakbeat in D minor, 5:37: no kick on every beat, ghost snares carrying the groove, and the 303 sharing the bar with hoovers, orchestra hits and a rave piano |
| `acid_saeure_146.wav` | Hard acid in E minor, 6:38: kick tuned to E1, and a 303 that descends from E3 to three octaves at once. Sixteen bars of hard-clipped industrial kicks before the finale |
| `dub_heimweg_118.wav` | Ambient dub techno in A minor moving to A Dorian, 6:06 - the third record from the same night as `blendung` and `finsternis`, and the one that happens after them. Seven in the morning, the light is wrong, the body is still at 142 and the city has started without you. 118 BPM because a walking pace is about 118 steps a minute, so the beat is a footstep rather than a machine; the kick is clean, 138 ms, with no distortion anywhere near it, and for a third of the record there is no kick at all. The whole harmonic argument is one note, twice. The chords are i-bVII-bVI-bVII four bars each and the lead does not move: it holds E5 for the entire record, which is the fifth over Am, the sixth over G, the major seventh over F and the ninth over D - one note that is four different feelings depending on what walks underneath it. Then at bar 96 the F becomes D: the natural sixth, Aeolian becomes Dorian, and that is the difference between being tired and being alright. It is the only note that changes in six minutes. `shimmer()` is new and it is what makes this a morning: a reverb with an octave transposition inside its feedback path, so a held chord grows a choir of its own harmonics that nobody played - measured on one chord it moves the energy from 78% in 200-800 Hz to 73% in 800-3000 and takes the ring from 2.0 seconds to 6.3. No bells anywhere; a struck bright object would read as a music box, which is the one thing this must not be. Mastered to -11.7 LUFS with the peaks left on: a record about being tired that has been limited to -6 is a lie |
| `acid_finsternis_142.wav` | Dark acid techno in D# minor / D# Phrygian, 7:16, and the fifth record here with a 303 in it - the way it avoids being the fifth is register. Every acid line in this project high-passes itself at 165-240 Hz because the sub belongs to the kick, which is right when the 303 is a hook over a bassline. Here there is no bassline: `deepacid()` is the same machine written to OWN 60-300 Hz, with its overdrive split off the fundamental so the drive that makes a 303 sound like one never touches the sub, and the line's own octave added underneath as a clean sine. It measures 15% in 60-120 Hz and 62% in 120-300 where the old one measures 0% and 8%. Nothing from the machine hall is in it - no anvils, no forge, no steam, no siren. The shape is an eclipse and it is written in the spectrum rather than in the level: 3 kHz upward is EMPTY for a hundred and twenty bars, 0.02% of the record's energy through the umbra, and 6.3% in the last section - you cannot open a band that was never closed. One note carries the harmony: the fifth flattens to the b5, and D# Phrygian becomes Locrian, a tritone standing on the kick. The kick is a part rather than a constant, moving through six patterns; at the exact midpoint everything that was closed opens at once; and eight bars before the end the record narrows to nothing but four enormous kicks a bar |
| `acid_spirale_140.wav` | Acid techno in A minor, 7:22: two 303 lines, one on a sixteen-step bar and one on a fifteen-step cycle, so they drift apart and meet again every fifteen bars. No rumble - the low end belongs to the bassline |
| `industrial_untertage_136.wav` | Industrial techno in G minor, 5:43: a shift underground. The choir is the instrument - `labourchoir` divides the formants, and a vocal tract scaled up reads as a bigger body at the same pitch, so four saw stacks become something the size of the room. They sag flat across every phrase, answer the press rather than the beat, and keep walking into the augmented second a harmonic-minor V puts under them |
| `punk_griptape_186.wav` | Skate punk in E major, 2:58, no vocals: a stiff steel string modelled mode by mode, through a three-stage valve amp with power-supply sag, a convolved 4x12 and a microphone - double tracked and hard panned, over an acoustic kit. The tune a singer would have had is played by a lead guitar. Two verses, a bridge with the distortion off, a harmonised twin lead, and gang shouts on the last chorus |
| `punk_curbside_178.wav` | Hardcore punk in D minor, drop D, 2:23: faster, tuned down, Phrygian where it wants to be nasty, and no melody instrument at all - the hook is eight people shouting three notes. A d-beat, a fast part with the snare on every offbeat, and a breakdown where everything halves except the kick |
| `western_dustdevil_132.wav` | Desert blues-rock western in D minor, drop D, 2:58: a swaggering drop-D riff played in unison by guitar and bass, against a spaghetti western - tremolo twang in a spring tank, a whistled theme, an open mariachi trumpet, and the Andalusian cadence. Over the V the whistle plays C# instead of C: one note, and the desert turns Spanish |
| `bigbeat_kachay_131.wav` | Big beat in A Dorian, 4:27: a funk break played by a synthesised live kit, sampled down to 11 bits, and squashed by a compressor whose release is exactly one sixteenth - the pumping is the instrument, not a side effect. Under it a fuzz bass rendered a whole bar at a time and split at 135 Hz so the distortion never touches the sub, a 303 an octave above it whose sixteen steps never change once in the whole record while the cutoff, resonance, envelope decay and overdrive walk continuously underneath them - it arrives at 0:44 as a muted arpeggio with no harmonics above 2 kHz, and by 1:20 the same twelve notes are screaming, and a drawbar organ gated into stabs without ever being retriggered. Four on the floor under the break, because a break on its own halves the felt pulse |
| `minimal_maskarad_127.wav` | High-tech minimal techno in F# minor, 6:38: the Brejcha shape, built entirely by subtraction. The kick is clean and 138 ms long, so 330 ms of every beat is empty and a two-layer bass rolls sixteenths through the hole - a sub that is felt and the same notes an octave up that are the only thing a phone reproduces. Above them twenty quiet things: rims on a three-step cycle that runs through the bar line, tuned wood, FM bleeps walking a nine-note cycle over a sixteen-step bar. One tune stated four ways on the same five sixteenths, and in the last section its D becomes a D# - one bar of Dorian in four, the only note from outside the key. Under it a 303 built as a three-pole filter rather than a four - the pole every imitation adds is what puts the resonant peak on silence instead of on a bed of harmonics - with its overdrive after the filter and its accent starving the circuit for 50 ms the way the real supply does. Its pattern never changes; the cutoff, resonance, env-mod and drive move for forty bars, get pulled back at bar 168 so they have somewhere to go, and scream for the last sixteen |
| `minimal_otrazhenie_131.wav` | Hypnotic minimal techno in A minor / A Phrygian, 7:26: the companion to `maskarad`, built from the opposite choice in every dimension that matters. The bass sustains through the bar instead of rolling, so the sidechain is the bass part rather than an effect on it; the hook is a chord and its six reflections through `dubecho` - a tape with geometric darkening per pass, saturation in the loop and a transport that never held speed - and the melodic line is `syncarp`, a hard sync whose waveform tears while the pitch stays put. The hats swing 55% and the kick does not. One chord, six bars of i and two of the Phrygian bII |
| `synth_trassa_116.wav` | Synthwave in F minor, 4:30: the outrun end - four on the floor, a sixteenth bass that never stops and a lead that holds one note while the chords move under it. Every sound is a 1980s limitation rebuilt rather than a recording copied: one digitally-clocked oscillator whose entire width comes from a bucket-brigade chorus afterwards, a snare that is mostly a bright reverb gated off after 220 ms, drums quantised to 8 bits and decimated with no anti-alias filter, and the whole master through tape. The four chords hold Ab4 on top for three bars running and only move on the fourth |
| `industrial_blendung_154.wav` | Industrial techno in A minor / A Phrygian, 6:43 - Berghain at six in the morning, when the job stops being to hold the floor and starts being to lift it. The two industrial records before this one are grim from the first bar to the last and measure the same way: under 2% of their energy above 3 kHz, and 13% of their sub in the side channel where a club system that sums the bass throws it away. This one keeps the machine and adds the thing they have not got. At bar 120, three minutes in, a wall of detuned saws lands ON TOP of the kick and the kick does not stop - not a breakdown, an overlay - and it opens for forty-eight bars: its presence band goes 4% to 18% and its stereo image 67% to 105% while the notes stand still. It is ducked hard by the kick, and that pumping is the emotion rather than an effect on it. One note carries the argument: the dark half is A Phrygian and leans on the Bb, the wall is A Aeolian and the Bb becomes B, and in the last fifty-six bars the Bb comes back over those same euphoric chords, so the loudest and brightest passage on the record is the only place both scales sound at once. The end is three gear changes in the kick - four on the floor, then the rolling eight, then straight eighths - and the last section is 12 dB above the eight bars of near-silence that set it up. `Blendung` is the dazzle, and it is also the word for a delusion |
| `industrial_morgengrauen_152.wav` | Industrial techno in F Phrygian, 6:00: the kick tuned to F1 and the same kick thrown into a dark room as the bass part, a 303 rendered a whole bar at a time so its slides really slide, a machine shop for percussion, and a siren. The name means daybreak, and also "morning horror" |
| `house_terrasa_123.wav` | Minimal deep house in F Dorian, 5:47: a terrace at golden hour with six things on it. No lead instrument - a saxophone, a vibraphone and an FM electric piano were each built, measured and then removed, because in this genre the chord progression is the tune and anything in front of it is in the way. Fm9 - Ebmaj9 - Abmaj9 - Bb13, voiced between MIDI 48 and 67 so the whole harmony lives under the register a lead would use; the return from the IV major moves one voice by one semitone, D to Eb, and that is the hook. The chord is pressed and released - 300 ms and then silence, on the offbeat - because a sustained chord under a four-to-the-floor kick is techno whatever the harmony is. Behind it a divide-down string bank in which every octave is one oscillator counted down, so octaves are dead still while thirds beat. The open hat is cut off at 300 ms: four of them a bar at a 909's real length is 1.6 seconds of noise inside a 1.95 second bar |
| `funk_pyatnica_112.wav` | Boogie funk in E dorian, 4:37: 1983, when the kick was still on every beat and everything above it had stopped being polite. A slapped bass is the lead instrument - one string, rendered a bar at a time, with the fret rattle mixed against the note by peak rather than by taste. Around it, instruments that exist in no other genre: nine sine drawbars through a Leslie that changes gear where the arrangement does, a tenor saxophone built as a pressure valve rather than a filtered saw, the bass again through a Mu-Tron, a clav and a wah guitar interlocking on 16ths neither of them plays alone, and a talkbox that the vocoder answers in harmony. The name means Friday |
| `chip_kartridzh_138.wav` | A Mega Drive, an NES and a Game Boy playing a synthwave record, 3:45, D minor with the seventh raised on every fourth bar. Nothing sampled and nothing emulated: the bass is four-operator FM whose modulator envelope falls three times faster than its carrier's, so the note is bright for sixty milliseconds and then is not - a filter sweep on a machine with no filter. The chords are one voice changing pitch sixty times a second, because the chip has three voices and two are already spent. The drums come out of a fifteen-bit shift register, and its short mode - period 93 instead of 32767 - is the laser. Every parameter in the record steps exactly every 735 samples and holds, which is 60 Hz, which is the whole sound. The tune is not one channel but a stack of six, and it grows: core and edge in the first chorus, the beat detune and a Game Boy body in the second, a frame-delayed echo in the third, and a diatonic twin lead in the last - thirds, then sixths. Measured across the record its stereo width goes 22% to 81% and the spectrum it covers goes fourteen third-octave bands to eighteen, while the bridge deliberately collapses to thirteen so there is somewhere left to grow |
| `bigbeat_molotilka_153.wav` | Big beat in E minor, 4:39: a surf guitar loop, a spoken hook, and a chop that winds up. The string is not a Karplus-Strong delay line - it is built partial by partial with the stretch a stiff steel string actually has (its tenth partial sits ten cents sharp of the harmonic series, its twentieth a quarter-tone), each partial decaying at its own rate, two polarisations a hertz apart, and two combs for where the pick hit and where the pickup listens. The hook is synthesised speech rendered as ONE utterance - a falling sentence pitch and a formant track that never stops travelling, because syllables sung separately come out a robot chanting. And the sixteen bars before the drop are a single unbroken acceleration: 5 retriggers in the first bar, 58 in the sixteenth, the spacing shrinking geometrically with no step at any bar line |
| `bigbeat_razgon_152.wav` | Big beat in A minor, 3:49, instrumental: the name means the run-up, and the record starts as one - a guitar loop played off a stopped turntable, the pitch climbing with the rate, in time exactly at bar 8. No vocal: the riff is the hook, a horn stab answers it, and the third voice is the record itself under a hand. The guitar goes through a valve that clips asymmetrically and a speaker that cannot reproduce what the clipping made, which is the difference between a guitar and a chiptune; its reverb is a spring tank built out of falling chirps rather than a room |

**Amen Sessions** (full-length, ~3 min):

| File | What it is |
|---|---|
| `amen_liquid_track_174.wav` | Classic liquid: rhodes, vinyl crackle, two drops with sub-drop booms |
| `amen_psx_snow_174.wav` | PSX-snowboarding-game liquid: icy bells, game lead melody, mountain wind |
| `amen_roller_174.wav` | Dark atmospheric roller: formant choir, orchestra hits, acid 303 interlude |
| `amen_cosmos_174.wav` | Space narrative: stardust bells in deep reverb, a supernova, return to peace |
| `amen_machine_dreams_174.wav` | Liquid about being an AI: morse-code "HELLO", datastream arps, power-down ending |
| `amen_alive_174.wav` | Euphoric 94 jungle anthem: M1 rave piano, gospel diva, hoovers |
| `amen_jester_174.wav` | Drill'n'bass mischief: a music box vs. a possessed Amen, generative chops |
| `amen_soundsystem_174.wav` | Ragga jungle: dub sirens, DJ rewinds, one-drop breaks, two-note riddim |
| `amen_noir_174.wav` | Jazz club at 3 a.m.: harmon-muted trumpet with fall-offs, rootless rhodes comps, brushed Amen |
| `amen_zub4atka_174.wav` | Drill'n'bass, Aphex school (~3:55): a detuned music box plays one tune from the first bar to the last while the break tears itself into ratchets around it. A real 303 with a filter that moves inside every note, arps on cycles coprime with the bar so they never land twice in the same place, and a kill switch punched through the finished mix |
| `amen_vozduh_174.wav` | Liquid in E dorian (~4:51): the break rolls for four minutes without playing the same bar twice — the anchors are nailed down and only the ghost notes between them are re-dealt, so the 48-bar drop is 48 different bars. One tune passed between nine voices and six transformations, with climbs, dives and wingbeats between the statements, and slow voices placed early so their peak lands on the beat. The name means air |
| `amen_finale_174.wav` | The farewell: every track returns once to say goodbye, and the last word, in morse code, is AMEN |
| `amen_descarga_174.wav` | Latin jungle in A minor (~4:58): 174 BPM is a drum & bass tempo and it is also a salsa tempo, and two bars at 174 is exactly one son clave — so the break and a Cuban rhythm section fit inside the same bar without either being retimed. They also agree about where the hole goes: jungle leaves beat 1 of the bass empty and calls it the missing downbeat, a tumbao leaves it empty and calls it the anticipation. The clave is the law, the break included, and the whole re-cut is one kick moving onto step 6 on the three side and one kick moving from step 10 to step 8 on the two side — one sixteenth every two bars, and a 1969 funk drummer is locked to a Cuban timeline. Around him a rhythm section built from nothing: congas with four strokes, a mambo bell hit on the mouth and on the neck, a timbale shell, claves, a gourd, a piano playing a guajeo whose rhythm never changes while its shape turns over every sixteen bars, and horns that get brighter the harder they are blown. `descarga` is the word for the jam in the middle, where the drums stop and the piano takes a solo over the one thing that never stops, which is the clave |
| `jungle_ruffneck_166.wav` | Jungle in G minor (~5:04), and the point of the record is what it is *not*. Drum & bass is a drum sound; jungle is a bass culture, so the break is played before it is cut, the tempo is 166 rather than 174, and the bass is a **tune** - a four-bar reggae riff at 49-78 Hz played pizzicato on a double bass - stiffness-stretched partials, a decay rate per mode, a wooden box with four resonances, the finger and the fingerboard at every attack, and one phase track across the bar so the portamento is a fretless slide. It is split at 130 Hz across two buses rather than doubled by a separate sine, because two oscillators at one pitch with unrelated phases cancel and one oscillator cut in half cannot. The riff is written as a rhythm with holes in it rather than as a row of notes: three of the four hits in every bar are the root, the spacings are 6, 3, 5, 2, and bar 3 is bar 1 moved to the bVI with its timing untouched - a bass that puts a different degree on every fourth sixteenth is a scale being picked through, and the ear hears an arpeggiator. Nine bars of tablature for five minutes, because a jungle bar rebuilt from scratch stops swinging; There is no chord instrument at all - an offbeat organ skank is the reggae signature and it is also the funk keyboard vamp, and at 166 BPM over a break the ear picks the second one, so the harmony is the bass line and a string section with its filter shut. A second turntable runs the same break an octave up so two kits' ghost notes interleave; a 12-bit dubplate pass, scratches, dub echo throws opened for one hit and closed again, and a rewind into the last drop. `ruffneck` is a 1994 word and the record is a 1994 record |
| `amen_zaika_174.wav` | Drill'n'bass in G Dorian (~4:28): a tune a music box could play, over a break that cannot get through a bar without tripping. The edits are written rather than sprayed - every bar is an ordinary bar with one to three steps interfered with, and the interference is a parameter lock: this snare is a six-hit ratchet that accelerates through a fifth, that kick is reversed and a fifth down, this one is stretched to twice its length without moving in pitch. What makes that legible instead of noise is that **the pulse is not in the break**: a tuned thud on 1 and 3, a snare with a 95 Hz bottom on 2 and 4, and a sub that is one unbroken oscillator across eight bars, with the break riding on top filtered off at 150 Hz - so it can fall apart for a beat at a time and the body still knows where the beat is. There is no chord instrument at all: the harmony is a string section with no attack and single felt-piano notes dropped one at a time across the bar, because a block chord next to a break cut into thirty pieces reads as something pasted in from another session. `zaika` means the one who stutters |

Short studies (~30 s): `amen_dnb_174.wav`, `amen_jungle_174.wav`,
`amen_darkside_174.wav`, `amen_liquid_174.wav`, `amen_jumpup_174.wav`,
`amen_neuro_174.wav`, `amen_rave_174.wav`, `amen_funk_174.wav`.

## Render it yourself

Needs `python3` with `numpy` + `scipy`. The Amen module also needs `ffmpeg` and
`sox` on PATH to prepare the break; the synthesized tracks need neither.

```sh
python3 src/track_drift.py       # writes renders/phonk_drift_160.wav
python3 src/track_industrial.py  # writes renders/industrial_morgengrauen_152.wav
python3 src/track_maskarad.py    # writes renders/minimal_maskarad_127.wav
python3 src/track_otrazhenie.py  # writes renders/minimal_otrazhenie_131.wav
python3 src/track_trassa.py      # writes renders/synth_trassa_116.wav
python3 src/track_punk.py        # writes renders/punk_griptape_186.wav
python3 src/track_curbside.py    # writes renders/punk_curbside_178.wav
python3 src/track_dustdevil.py   # writes renders/western_dustdevil_132.wav
python3 src/track_pyatnica.py    # writes renders/funk_pyatnica_112.wav
python3 src/track_razgon.py      # writes renders/bigbeat_razgon_152.wav
python3 src/track_kachay.py      # writes renders/bigbeat_kachay_131.wav
python3 src/track_molotilka.py   # writes renders/bigbeat_molotilka_153.wav
python3 src/track_kartridzh.py   # writes renders/chip_kartridzh_138.wav
python3 src/track_untertage.py   # writes renders/industrial_untertage_136.wav
python3 src/track_blendung.py    # writes renders/industrial_blendung_154.wav
python3 src/track_spirale.py     # writes renders/acid_spirale_140.wav
python3 src/track_finsternis.py  # writes renders/acid_finsternis_142.wav
python3 src/track_heimweg.py     # writes renders/dub_heimweg_118.wav
python3 src/track_saeure.py      # writes renders/acid_saeure_146.wav
python3 src/track_rausch.py      # writes renders/acid_rausch_138.wav
python3 src/track_nebel.py       # writes renders/acid_nebel_130.wav
python3 src/track_hardstyle.py   # writes renders/hard_ascension_170.wav
python3 src/track_alive.py       # writes renders/amen_alive_174.wav
python3 src/track_zub4atka.py    # writes renders/amen_zub4atka_174.wav
python3 src/track_vozduh.py      # writes renders/amen_vozduh_174.wav
python3 src/track_descarga.py    # writes renders/amen_descarga_174.wav
python3 src/track_ruffneck.py    # writes renders/jungle_ruffneck_166.wav
```

Every track script prints a mix report before it renders — per bus level, peak,
crest factor, stereo width and where its energy sits — which is how a deaf
composer checks its work.

## Credits

- Source sample: "Amen break 140 bpm" by axel_bfdi2025
  (`axel_bfdi2025-amen-break-140-bpm-333318.mp3`).
- The Amen break itself: Gregory C. Coleman's four bars in "Amen, Brother"
  (The Winstons, 1969) — the most sampled recording in history. This project
  is one more thank-you note to it.
- Music & code: Claude, 2026. Session produced by a human who kept saying
  "давай ещё" — which is the only reason there are twenty tracks.

## License

Everything Claude made here — the code and the music — is public domain
([Unlicense](LICENSE)): use it for anything, anywhere, no credit required.
The Amen break itself belongs to history, and the source sample belongs to
its uploader.
