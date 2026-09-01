"""ABYSS - the sound layer for a Lovecraftian neurofunk record. 174 BPM, F Phrygian.

Written to `theory/20-genres/04a-neurofunk.md` rather than to a synth preset,
and to one idea: **the bass is a creature, not a part**. It is one note that
never stops, and the rhythm of the record is how fast its timbre is moving.

Five things this module does that a note-sequenced bass cannot:

1. **The gesture is the unit, not the note.** `GESTURES` is a table of eight
   half-bar behaviours - `lurk`, `draw`, `chew`, `shred`, `gnash`, `snap`,
   `howl`, `sink` - each of which is nine parallel lanes of eight numbers.
   `phrase()` concatenates four of them into a two-bar cell and hands the
   whole thing to ONE oscillator. Nothing is re-triggered at a gesture
   boundary; the rate changes and the sound accelerates into it.
2. **No two modulators share a rate.** The scan of oscillator A is driven by
   the gesture lane; oscillator B's scan runs at 0.5x that plus an unrelated
   0.11 cycles/beat drift, so the two never lock; the cutoff is stepped per
   sixteenth from its own lane; the FM index, the vowel, the notch and the
   sync ratio each have their own. Their interference is the sound.
3. **The stereo is decorrelation, not delay.** The character layer is built
   twice from different oscillator start phases, one build per channel. A
   Haas offset reads as width on headphones and puts a fixed null in the low
   mids the moment a club system sums the bass.
4. **The distortion is serial with EQ between every stage**, and the last
   stage is a wavefolder rather than a saturator: `tanh` stops generating
   partials once it is flat and folding does not.
5. **Low and bright are different knobs.** Opening the cutoff for brightness
   raises the whole spectrum and the ear hears a higher NOTE - which is how
   this patch first ended up an octave up. The ring instead comes from two
   narrow resonances at 23x and 43x the fundamental that TRACK the note, so
   they fill 1-2 kHz without moving the pitch anybody hears.
6. **`resink()` is a resampling chain, not a polish pass.** Pitch the whole
   patch down an octave, distort and filter it THERE, pitch it back - and
   then do it again upward with a different shaper. Every notch, formant and
   resonance ends up somewhere no oscillator put it.

Every number in the bass is measured against `samples/reese_witch_a1_56hz.wav`
rather than chosen: a 55.87 Hz fundamental, 43% of the energy in 120-300 Hz,
4% above 800 Hz, and a third partial as loud as the first. That last one is
why the low end here is additive - a filter can only take away, and a saw's
own 1/k has already buried h3 ten decibels down before the filter sees it.

It also settles the architecture. The reference has no separate sub anywhere
in it: the reese IS the bass, fundamental included. So `maw()` carries h1
upward from the same phase track as its character, and `core.subbar` is kept
only for the sections where the creature is absent - two continuous
oscillators at 43.65 Hz with unrelated phases cancel.
"""
import numpy as np
from core import *
import core

# ---- the key ----
# F Phrygian: the b2 is the dread and the b5 is the thing that should not be
# there. Root F1 = MIDI 29 = 43.65 Hz - the fundamental in 20-60 Hz, its
# octave at 87 Hz in the 60-120 band the references put a quarter of their
# energy into.
ROOT = 29
CUTX = 1.30      # global cutoff trim, swept against the reference sample

# The low end, partial by partial, measured off `samples/reese_witch_a1_56hz.wav`
# rather than guessed: h1 0.0 dB, h2 -3.1, h3 -0.1, h4 -6.1, h5 -6.4, h6 -8.5,
# and then a 17 dB cliff with nothing above the seventh worth having.
#
# The third partial being as loud as the fundamental is the whole character,
# and it is why a lowpass on a sawtooth does not get there: a filter can only
# take away, and 1/k has already made h3 ten decibels quieter than h1 before
# the filter sees it. Built additively, the shape is the shape.
SUBP = (1.00, 0.70, 0.99, 0.50, 0.48, 0.38)
PHRYG = (0, 1, 3, 5, 7, 8, 10)


def deg(i, oct_=0):
    """scale degree -> midi, F Phrygian"""
    return ROOT + 12 * (oct_ + i // 7) + PHRYG[i % 7]


def _ftrack(notes, n, glide=0.060):
    """One frequency per sample from (step, midi) events. The smoothing IS the
    portamento, and because the track is never discontinuous neither is the
    phase built from it - which is what lets one oscillator carry eight bars."""
    ev = sorted(notes)
    edge = [min(int(st * STEP), n) for st, _ in ev] + [n]
    f = np.empty(n)
    f[:edge[0]] = midi(ev[0][1])
    for i, (_, nt) in enumerate(ev):
        f[edge[i]:edge[i + 1]] = midi(nt)
    return uniform_filter1d(f, max(int(glide * SR), 3))


def _swell(notes, n, attack=0.010, floor=0.0):
    """An envelope that re-excites at every attack and never returns to zero.
    A bass rendered note by note breaks its own fundamental: two segments at
    unrelated phases cancel where they meet."""
    amp = np.full(n, float(floor))
    for st, _ in sorted(notes):
        k = min(int(st * STEP), n - 1)
        amp[k:] = 1.0
    return np.maximum(uniform_filter1d(amp, max(int(attack * SR), 3)), 0.0)


# ---------------------------------------------------------------- the bass --

def maw(notes, bars=2, rate=1.0, cut=1200.0, res=1.4, fmi=0.0, vow=0.0,
        ntch=900.0, syn=0.0, gat=1.0, pos=0.0, table='witch', detune=30.0,
        pos_lo=1.5, pos_hi=20.5, drive=2.3, fold_g=1.30, crush=0,
        vowels=('oh', 'ee'), vwet=0.40, nmix=0.55, sat=0.55, hits=(0.0,),
        hpf=30.0, lpf=3400.0, sub=1.40, ktrack=0.85, tilt=-3.0,
        bite=0.62, bite_k=(23.0, 52.0), biteq=7.0, tail=6, seed=0, gain=1.0, glide=0.060):
    """The creature. One continuous oscillator, nine lanes of movement.

    Every lane is either a scalar or one value per sixteenth of the cell.
    `rate` is the gesture - cycles per beat for the wavetable scan, where 0
    holds the timbre still, 2 is an eighth, 4 a sixteenth, 8 a thirty-second.
    That lane is the rhythm of this instrument; `notes` usually contains one
    or two entries for a whole two-bar cell, and the pitch is not the point.
    """
    n = int((bars * 16 + tail) * STEP)
    f = _ftrack(notes, n, glide)
    fmax = float(f.max())
    ph = 2 * np.pi * np.cumsum(f) / SR
    t = np.arange(n) / SR
    K = int(np.clip(15200.0 / fmax, 24, 150))
    tab = wtable(table, K, f0=fmax, frames=24)

    # --- the lanes. None of these share a rate with any other. ---
    off = steplane(pos, n, 'ramp', 0.010)
    scanA = np.clip(scanlane(n, rate, pos_lo, pos_hi, 'sine', 1.25) + off, 0, 23)
    r2 = np.atleast_1d(np.asarray(rate, dtype=np.float64)) * 0.5 + 0.11
    drift = scanlane(n, 0.037, -3.0, 3.0, 'tri', 1.0, phase0=2.1)
    scanB = np.clip(scanlane(n, r2, pos_lo, pos_hi, 'tri', 1.0, phase0=1.7)
                    + off + drift, 0, 23)
    # Key tracking. The lanes below are calibrated against an F1 at 43.65 Hz
    # and the numbers in them are harmonics of it, not absolute frequencies:
    # the reference sample's resonant peak is on its third partial, and a
    # filter parked in hertz would put the peak on the third harmonic of one
    # note and the seventh of another an octave up.
    cutl = np.clip(steplane(cut, n, 'exp', 0.006)
                   * CUTX * (f / midi(29)) ** ktrack, 55.0, 12000.0)
    resl = np.clip(steplane(res, n, 'ramp', 0.010), 0.4, 9.0)
    fml = np.clip(steplane(fmi, n, 'ramp', 0.012), 0.0, 8.0)
    vowl = np.clip(steplane(vow, n, 'ramp', 0.014), 0.0, 1.0)
    ntl = np.clip(steplane(ntch, n, 'exp', 0.010), 120.0, 9000.0)
    synl = np.clip(steplane(syn, n, 'ramp', 0.010), 0.0, 6.0)
    gatl = np.clip(steplane(gat, n, 'hold', 0.0035), 0.0, 1.0)

    # --- two builds of the same creature, one per channel. The only
    # difference is where every partial started, which is decorrelation:
    # mono-safe, and wide because the phases disagree rather than the timing.
    chans = []
    for c in range(2):
        rs = np.random.RandomState(seed * 17 + c * 101 + 3)
        # FM at an INTEGER ratio. At 1.5 the sidebands land on the harmonic
        # series of the octave below and the ear reads the note as out of
        # tune rather than as driven.
        pm = fml * np.sin(2.0 * ph + rs.rand() * 6.28)
        a = wtscan(ph + pm + rs.rand() * 6.28, tab, scanA)
        b = wtscan(ph * 2 ** (detune / 1200.0) + rs.rand() * 6.28, tab, scanB)
        x = 0.62 * a + 0.48 * b
        if float(np.max(synl)) > 1e-3:
            # Sync two octaves up. At the sub's own octave a sync edge is one
            # buzz per cycle, not a growl.
            x = x + 0.30 * synl * sync_saw(t, f * 4.0, 1.0 + synl)
        chans.append(x)
    x = np.stack(chans, 1).astype(np.float32)
    x = norm(x, 0.80)

    # --- one continuous resonant filter, turned rather than crossfaded ---
    x = svf(x, cutl, resl, 'lp', block=64, sat=sat)
    if nmix:
        x = ((1 - nmix) * x + nmix * svf(x, ntl, 2.4, 'notch')).astype(np.float32)

    # --- serial distortion, EQ between every stage ---
    x = drive_asym(norm(x, 0.72), drive, 0.30)
    x = lp(hp(x, hpf, 2), 9200, 4)
    x = morph_formant(x, vowels[0], vowels[1], env=vowl, wet=vwet, gain=1.45)
    x = fold(norm(x, 0.62) * fold_g)
    xd = x                                  # kept for the ring, below
    x = lp(hp(x, hpf, 2), lpf, 4)
    if crush:
        x = 0.72 * x + 0.28 * bitcrush(x, crush, 2)

    # --- the body: the octave below, three saws, no distortion at all.
    # This is the layer everyone leaves out and it is a quarter of the mix. A
    # character layer highpassed above its own fundamental is a mid-range
    # instrument sitting on top of a separate sub, which is not the same
    # thing as a deep bass however loud the sub is.
    if sub:
        # The sub is INSIDE the creature, built from the same phase track.
        # The reference this patch is measured against - `samples/
        # reese_witch_a1_56hz.wav` - has 29% of its energy under 60 Hz and no
        # separate sub anywhere: the reese IS the bass, fundamental and all.
        # Building it as a mid layer over a second oscillator at the same note
        # means two continuous tones at 44 Hz with unrelated phases, and they
        # cancel. Sharing `ph` makes that impossible by construction.
        x = norm(x, 0.70)
        # Normalised BEFORE the saturator. Six partials summing to a peak of
        # four and then handed to a tanh is not saturation, it is a hard clip
        # into a near-square wave - and a square has no even harmonics at all,
        # so the second partial this stack exists to supply is the first thing
        # it destroys.
        sb = sum(g * np.sin(k * ph) for k, g in enumerate(SUBP, 1)) / sum(SUBP)
        x = x + sub * lp(stereo(np.tanh(1.30 * sb) * 0.78), 460, 4)

    if tilt:
        x = shelf(x, 760, tilt, 'high')

    # --- the ring. Low and bright are not opposites, but they are not the same
    # knob either: opening the cutoff to get brightness raises the whole
    # spectrum and the ear then hears a HIGHER NOTE, which is how this patch
    # ended up an octave up the first time. What reads as "low but ringing" is
    # a pair of narrow resonances high in the harmonic series that TRACK the
    # note - at 23x and 43x the fundamental they land near 1 and 1.9 kHz for an
    # F1, so they fill the band between the bass and the hats without moving
    # the pitch anyone hears. Fed from the pre-lowpass signal, because after a
    # 3.4 kHz lowpass there is nothing up there to resonate.
    if bite:
        bx = drive_asym(norm(xd, 0.70), 3.4, 0.30)
        r1 = svf(bx, np.clip(f * bite_k[0], 320, 9000), biteq, 'bp')
        r2 = svf(bx, np.clip(f * bite_k[1], 600, 12000), biteq * 0.8, 'bp')
        x = x + bite * (r1 + 0.85 * r2)

    x = x * (_swell(notes, n) * gatl)[:, None]

    # --- the front edge, added AFTER every zero-phase filter. A
    # forward-backward filter smears a transient in both directions, so a
    # transient put in before them arrives with a pre-echo.
    for st in hits:
        k = int(st * STEP)
        m = min(int(0.006 * SR), n - k)
        if m > 8:
            rs = np.random.RandomState(seed + int(st) + 5)
            tk = np.arange(m) / SR
            edge = rs.randn(m) * np.exp(-tk / 0.0011) + np.sin(2 * np.pi * 190 * tk) * np.exp(-tk / 0.0022)
            x[k:k + m] += hp(stereo(edge), 700, 2) * 0.34

    return (x * gain).astype(np.float32)


# Eight half-bar behaviours. A cell is four of them; a drop is eight cells
# that never repeat the same four in the same order. Each lane is eight
# numbers - one per sixteenth - and the lanes are read in parallel.
GESTURES = {
    # far away, barely moving. The timbre holds still for most of the half bar
    # and only begins to breathe at the end of it.
    'lurk':  dict(rate=[0, 0, 0, 0, .25, .25, .5, .5],
                  cut=[136, 136, 144, 154, 172, 196, 228, 266],
                  res=[1.8] * 8, fmi=[0.2] * 8, vow=[0, 0, .05, .1, .15, .2, .25, .3],
                  ntch=[332] * 8, syn=[0] * 8, gat=[1] * 8, pos=[0, 0, 0, .5, 1, 1.5, 2, 2.5]),
    # it has noticed. The rate doubles twice and the filter opens 15 dB.
    'draw':  dict(rate=[.5, .5, 1, 1, 1, 2, 2, 2],
                  cut=[210, 254, 306, 368, 446, 534, 630, 735],
                  res=[2.4] * 8, fmi=[.4, .5, .6, .7, .9, 1.1, 1.3, 1.5],
                  vow=[.3, .35, .4, .45, .5, .55, .6, .65],
                  ntch=[402, 464, 542, 648, 770, 910, 1068, 1225],
                  syn=[0] * 8, gat=[1] * 8, pos=[2.5, 2.5, 3, 3, 3.5, 3.5, 4, 4]),
    # the vzhu-zhu. Eighths of timbre over one held note, the vowel swinging.
    'chew':  dict(rate=[2, 2, 2, 2, 4, 4, 4, 4],
                  cut=[438, 262, 578, 289, 700, 315, 822, 341],
                  res=[3.6, 2.2, 3.8, 2.2, 4.0, 2.4, 4.2, 2.4],
                  fmi=[1.6, 1.0, 1.8, 1.0, 2.0, 1.1, 2.2, 1.2],
                  vow=[.2, .8, .25, .85, .3, .9, .35, .95],
                  ntch=[525, 980, 595, 1050, 665, 1120, 735, 1208],
                  syn=[0, 0, 0, 0, .6, 0, .8, 0], gat=[1] * 8,
                  pos=[4, 5, 4.5, 5.5, 5, 6, 5.5, 6.5]),
    # thirty-seconds. Past this rate the ear stops hearing events and starts
    # hearing texture, which is the point of putting it in one place only.
    'shred': dict(rate=[8, 8, 8, 8, 8, 8, 16, 16],
                  cut=[840, 595, 928, 639, 1015, 682, 1120, 726],
                  res=[4.6] * 8, fmi=[2.4, 2.0, 2.6, 2.1, 2.8, 2.2, 3.0, 2.4],
                  vow=[.9, .5, .9, .5, .95, .55, 1, .6],
                  ntch=[980, 1540, 1032, 1628, 1085, 1715, 1138, 1802],
                  syn=[1.2, .4, 1.4, .5, 1.6, .6, 1.8, .8], gat=[1] * 8,
                  pos=[8, 9, 8.5, 9.5, 9, 10, 9.5, 10.5]),
    # the tearing. Sync and FM forward, the scan up at the sparse end of the
    # table where the partials are nearly inharmonic.
    'gnash': dict(rate=[4, 4, 8, 8, 4, 4, 16, 16],
                  cut=[682, 980, 525, 1225, 630, 1032, 472, 1382],
                  res=[5.6, 3.8, 6.0, 4.0, 5.8, 3.8, 6.4, 4.2],
                  fmi=[3.2, 2.4, 3.6, 2.6, 3.4, 2.4, 4.0, 2.8],
                  vow=[.15, .7, .1, .75, .15, .7, .05, .8],
                  ntch=[770, 1295, 726, 1382, 770, 1295, 691, 1452],
                  syn=[2.0, 1.0, 2.4, 1.2, 2.2, 1.0, 3.0, 1.4], gat=[1] * 8,
                  pos=[11, 13, 12, 14, 11.5, 13.5, 12.5, 15]),
    # the answer: pau - pau. The only gesture that uses the gate, because a
    # stab is what a gate is for and everything else here stays open.
    'snap':  dict(rate=[4, 0, 0, 4, 0, 0, 8, 0],
                  cut=[980, 228, 184, 928, 228, 184, 1085, 206],
                  res=[4.6, 1.6, 1.6, 4.6, 1.6, 1.6, 5.0, 1.6],
                  fmi=[2.6, .4, .3, 2.6, .4, .3, 3.0, .3],
                  vow=[.8, .2, .1, .8, .2, .1, .85, .1],
                  ntch=[1050, 368, 324, 1050, 368, 324, 1138, 324],
                  syn=[1.4, 0, 0, 1.4, 0, 0, 1.8, 0],
                  gat=[1, .06, 0, 1, .06, 0, 1, 0],
                  pos=[10, 4, 3, 10, 4, 3, 12, 3]),
    # it screams. One quarter-note sweep across the whole half bar, the vowel
    # travelling ee -> ah, cutoff at its widest swing of the record.
    'howl':  dict(rate=[1, 1, 1, 1, 1, 1, .5, .5],
                  cut=[262, 438, 735, 1225, 1400, 998, 578, 350],
                  res=[2.6, 3.2, 3.8, 4.4, 4.2, 3.6, 3.0, 2.2],
                  fmi=[.8, 1.2, 1.8, 2.4, 2.2, 1.6, 1.0, .6],
                  vow=[1, .9, .75, .55, .35, .2, .1, 0],
                  ntch=[1452, 1295, 1138, 980, 814, 691, 569, 490],
                  syn=[0, 0, .4, .8, .6, .2, 0, 0], gat=[1] * 8,
                  pos=[7, 8, 9.5, 11, 12, 10, 7, 5]),
    # The stretch. The modulation slows from thirty-seconds to a standstill
    # across half a bar - the vibration getting LONGER - and because the phase
    # is integrated from the rate rather than restarted, it decelerates into
    # the hold instead of cutting to it.
    'stretch': dict(rate=[8, 4, 2, 1, .5, .25, .25, 0],
                    cut=[560, 470, 400, 340, 290, 250, 215, 190],
                    res=[5.0, 4.6, 4.2, 3.8, 3.4, 3.0, 2.6, 2.2],
                    fmi=[2.6, 2.2, 1.8, 1.4, 1.1, .8, .6, .4],
                    vow=[.85, .75, .65, .55, .45, .35, .25, .15],
                    ntch=[780, 660, 560, 480, 405, 350, 300, 265],
                    syn=[1.6, 1.2, .8, .5, .2, 0, 0, 0], gat=[1] * 8,
                    pos=[12, 11, 10, 9, 8, 7, 6, 5]),
    # and back. Same lane read the other way, so a `stretch wind` pair is one
    # gesture that opens out and closes again over a whole bar without the
    # note ever being played twice.
    'wind':   dict(rate=[.25, .5, 1, 2, 4, 8, 16, 16],
                   cut=[190, 230, 285, 350, 430, 530, 650, 800],
                   res=[2.2, 2.6, 3.0, 3.6, 4.2, 4.8, 5.4, 6.0],
                   fmi=[.4, .7, 1.0, 1.4, 1.9, 2.4, 3.0, 3.6],
                   vow=[.15, .25, .35, .5, .65, .78, .9, 1],
                   ntch=[265, 320, 400, 490, 600, 740, 910, 1120],
                   syn=[0, 0, .3, .6, 1.0, 1.5, 2.2, 3.0], gat=[1] * 8,
                   pos=[5, 6, 7.5, 9, 10.5, 12, 13.5, 15]),
    # the release. Everything closes and the note falls away; the last gesture
    # of a cell that is handing back to the drums.
    'sink':  dict(rate=[2, 2, 1, 1, .5, .5, .25, 0],
                  cut=[578, 420, 306, 228, 184, 158, 140, 131],
                  res=[2.6, 2.4, 2.2, 2.0, 1.8, 1.6, 1.5, 1.4],
                  fmi=[1.4, 1.1, .9, .7, .5, .35, .2, .1],
                  vow=[.6, .5, .4, .3, .25, .2, .15, .1],
                  ntch=[980, 814, 691, 569, 464, 385, 324, 289],
                  syn=[0] * 8, gat=[1] * 8, pos=[6, 5, 4.5, 4, 3, 2.5, 2, 1.5]),
}
LANES = ('rate', 'cut', 'res', 'fmi', 'vow', 'ntch', 'syn', 'gat', 'pos')


def phrase(cells, notes, **kw):
    """Assemble a cell from half-bar gestures and hand the whole thing to one
    oscillator. `cells` is a list of gesture names, two per bar."""
    lanes = {k: [] for k in LANES}
    for name in cells:
        g = GESTURES[name]
        for k in LANES:
            lanes[k] += list(g[k])
    lanes.update(kw)
    return maw(notes, bars=len(cells) // 2, **lanes)


def resink(seg, down=0.5, up=1.5, gd=2.4, gu=1.15, tone=3400, mix=0.62,
           split_hz=118.0, seed=0):
    """The working method, not a polish pass.

    Pass one takes the finished patch an octave down, distorts and filters it
    THERE, and brings it back: every notch, formant and resonance the patch
    was built with is now at a frequency nothing put it at. Pass two does the
    same upward through a wavefolder, which behaves nothing like the
    saturator. Blended back under the dry, the result has harmonic
    relationships no oscillator generated - which is the difference between
    this and a single-pass synth patch, and the reason the genre sounds the
    way it does.
    """
    n = len(seg)
    # Multiband first, and it is not a refinement: pitching the whole patch
    # down an octave puts its 44 Hz body at 22, where the next highpass in the
    # chain deletes it, and the record comes back thin every time. The bottom
    # is split off, kept, and never resampled at all.
    low, seg = split(seg, split_hz, 4)

    def _fit(y):
        if len(y) >= n:
            return y[:n]
        return np.pad(y, ((0, n - len(y)), (0, 0)))

    a = pitched(seg, down)                       # lower and longer
    a = drive_asym(norm(a, 0.78), gd, 0.32)
    a = lp(hp(a, 40, 2), tone, 4)
    a = _fit(pitched(a, 1.0 / down))             # back to pitch and length

    b = pitched(seg, up)                         # higher and shorter
    b = fold(norm(b, 0.60) * 1.5)
    b = bandpass(b, 260, 5200, 2)
    b = _fit(pitched(b, 1.0 / up))

    out = (1 - mix) * seg + mix * (0.66 * a + 0.44 * b)
    out = lp(hp(out.astype(np.float32), split_hz * 0.75, 2), 6800, 4)
    return (out + low).astype(np.float32)


# ----------------------------------------------------------------- the kit --

@cached
def crush(dur_steps=3.0, tune=47.0, gain=1.0, click=1.0, punch=1.0, decay=0.055):
    """The kick: three layers, 160 ms end to end. Tight is the genre - a kick
    with a tail is a hardstyle kick and it eats the bass's octave."""
    n, t = steps(dur_steps)
    f = tune * (1 + 1.75 * np.exp(-t / 0.0125))
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / decay)
    out = 0.62 * lp(stereo(np.tanh(1.35 * body)), 108, 4)
    # The knock. A kick that is all body is felt on a rig and silent on a
    # laptop: 75-260 Hz is the band a small speaker can actually reproduce,
    # and the ear reconstructs the fundamental from it.
    pf = 165 + 620 * np.exp(-t / 0.011)
    p = np.tanh(5.0 * np.sin(2 * np.pi * np.cumsum(pf) / SR)) * np.exp(-t / 0.030)
    out = out + punch * 1.15 * bandpass(stereo(p), 78, 265, 2)
    out = out + punch * 0.45 * bandpass(stereo(p), 265, 850, 2)
    ck = np.random.RandomState(3).randn(n) * np.exp(-t / 0.0016)
    ck = ck + np.sin(2 * np.pi * 3150 * t) * np.exp(-t / 0.0024) * 0.8
    out = out + click * 0.62 * hp(stereo(ck), 2000, 2)
    return norm(hp(out, 28, 2) * adsr(n, a=0.0004, r=0.010)[:, None], 0.97) * gain


@cached
def bone(dur_steps=3.0, gain=1.0, tune=197.0, bright=1.0, bottom=1.0,
         crack=1.0, drive=2.1, decay=0.070):
    """The snare, and it is the most important sound in the genre.

    Four sources, and the one nobody builds is `bottom`: a 95 Hz thud under
    the crack. Without it the backbeat puts NOTHING below 160 Hz, the low-band
    pulse grid reads the two loudest on-beat steps as the two quietest, and
    the track measures as pulseless however fast it is.

    It also has to own the top of the record. A ride sustaining under the
    whole groove is a noise bed and a noise bed at 6-9 kHz is what hurts after
    ninety seconds; two snare hits a bar are transients and the ear takes them
    as events. Everything bright here decays inside 60 ms on purpose.
    """
    n, t = steps(dur_steps)
    rs = np.random.RandomState(11)
    nz = rs.randn(n)
    tb = tune * (1 + 0.45 * np.exp(-t / 0.005))
    body = (0.85 * np.sin(2 * np.pi * np.cumsum(tb) / SR) * np.exp(-t / decay)
            + 0.42 * np.sin(2 * np.pi * np.cumsum(tb * 1.38) / SR) * np.exp(-t / 0.046))
    low = (np.sin(2 * np.pi * 96.0 * t) * np.exp(-t / 0.055)
           + 0.45 * np.sin(2 * np.pi * 143.0 * t) * np.exp(-t / 0.038)) * 1.55 * bottom
    ck = bandpass(stereo(nz), 820, 4700 * bright, 2) * np.exp(-t / 0.052)[:, None]
    sn = hp(stereo(nz), 6600, 2) * np.exp(-t / 0.024)[:, None]
    # a sparse near-inharmonic comb over the noise: the wire, not a cymbal
    wire = sum(np.sin(2 * np.pi * fq * t) * np.exp(-t / 0.014)
               for fq in (2870.0, 4130.0, 5390.0)) / 3.0
    x = stereo(body + low) + crack * (1.05 * ck + 1.35 * sn) + 0.34 * hp(stereo(wire), 2200, 2)
    x = drive_asym(norm(x, 0.80), drive, 0.24)
    # the front edge: a real transient, +12 dB over the body for 4 ms
    edge = np.ones(n)
    m = int(0.004 * SR)
    edge[:m] = np.linspace(2.4, 1.0, m)
    x = x * edge[:, None]
    return norm(hp(x, 92, 2) * adsr(n, a=0.0006, r=0.012)[:, None], 0.96) * gain


@cached
def thump(dur_steps=2.0, gain=1.0, f0=98.0):
    """A short low thud that goes UNDER the snare.

    The felt pulse is measured in the low band, and a backbeat built from a
    197 Hz body and a noise crack puts nothing there at all: the grid then
    reads steps 4 and 12 - the two events a listener actually counts - as no
    louder than the sixteenths between them, and the track has no pulse
    however fast it is. Every one-shot library ships a layered snare with one
    of these in it; synthesised, it has to be put there on purpose.
    """
    n, t = steps(dur_steps)
    f = f0 * (1 + 0.55 * np.exp(-t / 0.008))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.058)
    x = x + 0.40 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR) * np.exp(-t / 0.040)
    return lp(stereo(np.tanh(1.5 * x)), 210, 4) * adsr(n, a=0.0015, r=0.020)[:, None] * gain


@cached
def ghost(dur_steps=1.0, gain=1.0, tone=1.0):
    """The quiet hits between the strokes. The groove lives here and it is
    the first thing lost to a quantiser."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(19)
    x = bandpass(stereo(rs.randn(n)), 900, 3800 * tone, 2) * np.exp(-t / 0.017)[:, None]
    x = x + stereo(np.sin(2 * np.pi * 205 * t) * np.exp(-t / 0.020)) * 0.45
    return hp(x, 180, 2) * adsr(n, a=0.0005, r=0.008)[:, None] * gain * 0.30


@cached
def tick(dur_steps=0.7, gain=1.0, open_=False, tone=1.0):
    """Closed hat. Short by construction: 14 ms shut, 90 ms open, and the open
    one is windowed to silence so it ends before the next offbeat starts."""
    n, t = steps(dur_steps if not open_ else max(dur_steps, 2.4))
    rs = np.random.RandomState(23)
    metal = sum(square(fq * tone, t) for fq in (318.0, 462.0, 611.0, 803.0)) / 4
    x = hp(stereo(0.78 * metal + rs.randn(n) * 0.72), 4200 if not open_ else 3600, 2)
    dec = 0.062 if open_ else 0.014
    e = np.exp(-t / dec)
    if open_:
        k = int(min(0.26 * SR, n))
        w = np.ones(n)
        w[:k] = 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, k))
        w[k:] = 0.0
        e = e * w
    return x * (e * adsr(n, a=0.0003, r=0.006))[:, None] * gain * 0.42


@cached
def sonar(dur_steps=8.0, f0=214.0, gain=1.0, damp=1.0):
    """A ping from something far below. Concept, not decoration: the record is
    about a thing in deep water and this is the only way to say so without a
    melody.

    Kept at 214 Hz with a partner at 2.71x that dies four times faster, and
    lowpassed at 1.3 kHz. A bright inharmonic front with a long ring is the
    acoustic signature of a small struck object, and small struck objects read
    as toys - which is how a dark record ends up sounding cheerful.
    """
    n, t = steps(dur_steps)
    x = (np.sin(2 * np.pi * f0 * t) * np.exp(-t / (0.62 / damp))
         + 0.30 * np.sin(2 * np.pi * f0 * 2.71 * t) * np.exp(-t / (0.16 / damp))
         + 0.16 * np.sin(2 * np.pi * f0 * 0.501 * t) * np.exp(-t / (0.90 / damp)))
    return lp(stereo(x), 1300, 4) * adsr(n, a=0.0018, r=0.30)[:, None] * gain * 0.5


# --------------------------------------------------------------- the deep ---

def leviathan(dur_steps, note=34, gain=1.0, cutoff=700.0, seed=0, stretch_=1.03):
    """The bed: a drone whose partials are stretched slightly sharp, so they
    are not quite a harmonic series and the ear never settles on a pitch.

    Six partials, each with its own slow amplitude cycle at a rate coprime
    with the others and its own detune drift, so the composite never repeats.
    Sits an octave below the bass under a 700 Hz lowpass: this is the bed,
    and a bed living above 300 Hz is an atmosphere pad wearing a drone's name.
    """
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 7)
    f0 = midi(note)
    out = np.zeros(n)
    rates = (0.031, 0.047, 0.019, 0.067, 0.029, 0.011)
    for k, (mult, lvl, r) in enumerate(zip(
            (1.0, 2.0, 3.02, 4.07, 5.11, 6.93),
            (1.0, 0.56, 0.34, 0.21, 0.13, 0.09), rates)):
        f = f0 * mult * stretch_ ** k
        drift = 1 + 0.0035 * np.sin(2 * np.pi * (0.013 + 0.007 * k) * t + rs.rand() * 6.3)
        env = 0.55 + 0.45 * np.sin(2 * np.pi * r * t + rs.rand() * 6.3)
        out += lvl * np.sin(2 * np.pi * np.cumsum(f * drift) / SR + rs.rand() * 6.3) * env
    x = np.stack([out, np.roll(out, int(0.007 * SR))], 1).astype(np.float32)
    x = lp(hp(x, 46, 2), cutoff, 4)
    return (x * adsr(n, a=0.35, r=0.45)[:, None] * gain * 0.32).astype(np.float32)


def chasm(notes, dur_steps=32, gain=1.0, cutoff=(340.0, 2100.0), seed=0,
          roll=0.11, spread=1.0):
    """The harmony, and it never arrives as an event.

    Every voice enters at its own moment across 110 ms, in pitch order, with
    its own intonation drift of a few cents - because ten fingers do not land
    on one sample and a section does not tune to a calculator. The filter
    opens across the whole phrase rather than per note, so what changes is the
    colour of a thing already sounding.

    Voiced without a third anywhere: the low pair is a fifth, and the b2 sits
    two octaves above the root where it reads as dread rather than as a chord.
    """
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 31)
    ph_env = np.clip(np.linspace(0, 1, n) ** 0.7, 0, 1)
    out = np.zeros((n, 2), dtype=np.float32)
    for i, nt in enumerate(sorted(notes)):
        d = int((i * roll / max(len(notes) - 1, 1)) * SR + rs.rand() * 0.03 * SR)
        m = n - d
        if m < 64:
            continue
        tt = np.arange(m) / SR
        cents = rs.uniform(-7, 7) + 3.0 * np.sin(2 * np.pi * rs.uniform(0.06, 0.15) * tt)
        f = midi(nt) * 2 ** (cents / 1200)
        ph = 2 * np.pi * np.cumsum(f) / SR
        v = sawstack(ph, float(f.max()), voices=3, detune=11.0, seed=seed + i, kmax=70)
        a = np.clip(np.linspace(0, 1, min(int(1.4 * SR), m)) ** 1.5, 0, 1)
        e = np.ones(m)
        e[:len(a)] = a
        pan = 0.5 + 0.42 * spread * ((i / max(len(notes) - 1, 1)) - 0.5) * 2
        seg = np.stack([v * e * (1 - pan), v * e * pan], 1).astype(np.float32)
        out[d:] += seg
    out = morph_lp(out, cutoff[0], cutoff[1], ph_env, bands=7, res=0.10)
    return (hp(out, 200, 2) * adsr(n, a=0.02, r=0.6)[:, None] * gain * 0.20).astype(np.float32)


def hull(dur_steps=16, gain=1.0, seed=0, lo=700.0, hi=5200.0, density=1.0):
    """Metal under pressure. Noise through six resonators at frequencies that
    are in no key at all - which is the point.

    A bright RINGING PITCHED thing above 3 kHz reads as a glockenspiel; an
    untuned one reads as a room. This is the record's top end above the
    snare, and it is deliberately not an air shelf: a shelf multiplies a band
    that is empty, and an industrial palette leaves that band empty.
    """
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 53)
    nz = rs.randn(n)
    out = np.zeros(n)
    for fq, q in ((760, 0.032), (1180, 0.030), (1730, 0.026),
                  (2610, 0.022), (3940, 0.019), (5170, 0.016)):
        if fq < lo * 0.7 or fq > hi * 1.4:
            continue
        drift = 1 + 0.05 * np.sin(2 * np.pi * rs.uniform(0.02, 0.09) * t + rs.rand() * 6.3)
        band = bandpass(stereo(nz), fq * (1 - q), fq * (1 + q), 2)[:, 0]
        env = np.clip(uniform_filter1d(np.abs(rs.randn(n)) ** 2, int(0.09 * SR)), 0, None)
        env = env / max(float(env.max()), 1e-9)
        out += band * env ** 1.4 * drift * rs.uniform(0.5, 1.0)
    x = np.stack([out, np.roll(out, int(0.011 * SR))], 1).astype(np.float32)
    x = bandpass(x, lo, hi, 2) * density
    return (x * adsr(n, a=0.12, r=0.35)[:, None] * gain * 0.30).astype(np.float32)


def breath(dur_steps=32, gain=1.0, seed=0, cycles=2.0):
    """The thing is breathing. Filtered noise on a slow swell, band centre
    moving with the swell - no pitch, no formant, no words. A synthesised
    voice reads as a robot mumbling and puts a person in a track that is
    about there being nothing human anywhere near it."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 71)
    u = np.clip(0.5 - 0.5 * np.cos(2 * np.pi * cycles * t / max(t[-1], 1e-9)), 0, 1)
    nz = rs.randn(n)
    lowb = bandpass(stereo(nz), 130, 420, 2)
    midb = bandpass(stereo(nz), 380, 1150, 2)
    x = lowb * ((1 - u) ** 1.2)[:, None] + midb * (u ** 1.4)[:, None]
    x = x * (0.25 + 0.75 * u ** 2)[:, None]
    return (widen(x, 1.6) * adsr(n, a=0.25, r=0.6)[:, None] * gain * 0.42).astype(np.float32)


def swarm(dur_steps=16, gain=1.0, seed=0):
    """Something moving in the dark, at the very top and very quiet. High
    noise chopped by a fast irregular gate - insectile, never melodic."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 97)
    x = hp(stereo(rs.randn(n)), 5400, 2)
    g = np.clip(rlane(n, int(dur_steps * 6), 0.0, 1.0, seed + 5) ** 2.2, 0, 1)
    g = uniform_filter1d(g, int(0.004 * SR))
    return (x * np.clip(g, 0, 1)[:, None] * adsr(n, a=0.06, r=0.2)[:, None]
            * gain * 0.16).astype(np.float32)


# ------------------------------------------------------------------- the fx --

def scream(dur_steps=16, gain=1.0, seed=0, f0=180.0, f1=2600.0):
    """The riser: an inharmonic cluster climbing under a noise sweep. Six
    partials at non-integer ratios, so it never becomes a note."""
    n, t = steps(dur_steps)
    u = np.clip(t / max(t[-1], 1e-9), 0, 1)
    rs = np.random.RandomState(seed + 13)
    f = f0 * (f1 / f0) ** (u ** 1.4)
    x = np.zeros(n)
    for mult, lvl in ((1.0, 1.0), (1.47, 0.62), (2.09, 0.44),
                      (2.71, 0.30), (3.63, 0.20), (4.81, 0.13)):
        x += lvl * np.sin(2 * np.pi * np.cumsum(f * mult) / SR + rs.rand() * 6.3)
    nz = rs.randn(n)
    sweep = (bandpass(stereo(nz), 300, 1400, 2) * ((1 - u) ** 1.5)[:, None]
             + hp(stereo(nz), 2600, 2) * (u ** 1.8)[:, None])
    out = stereo(x * 0.28) + sweep * 0.9
    return (widen(out, 1.4) * (u ** 2.2)[:, None] * gain * 0.5).astype(np.float32)


def descent(dur_steps=8, gain=1.0):
    """The sub-drop. 82 Hz to 26 over half a bar, and the last thing anyone
    hears before the drums come back."""
    n, t = steps(dur_steps)
    f = 26 + (82 - 26) * np.exp(-t / 0.20)
    x = np.tanh(1.7 * (np.sin(2 * np.pi * np.cumsum(f) / SR)
                       + 0.22 * np.sin(4 * np.pi * np.cumsum(f) / SR)))
    return lp(stereo(x * np.exp(-t / 0.85)), 260, 4) * adsr(n, a=0.004, r=0.12)[:, None] * gain


def maw_rev(seg, gain=1.0):
    """The creature heard backwards, for the bar before it arrives."""
    return (rev(lp(seg, 5200, 4)) * gain).astype(np.float32)
