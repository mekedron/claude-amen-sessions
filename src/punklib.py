"""The skate punk layer: an electric guitar, an amp, a cab and a real kit.

Sets the grid to 186 BPM and adds the amp: what a guitar is plugged into,
and the kit behind it.

The string itself and the speaker cabinet are `core.string` and `core.cab` -
a stiff steel string and a convolved 4x12, both of which any genre can use.
What belongs here is the AMP, and the amp is the sound: a highpass BEFORE
the gain (an amp that is not tight in the low end turns a low E into mud),
three clipping stages with an EQ between each, power-supply sag so a loud
chord runs on a lower voltage than the one after it, and the cabinet at the
end. The cabinet is not an afterthought - a distorted guitar with no cab is
a buzzsaw, because the fizz above 5 kHz that a 4x12 cannot reproduce is most
of what the clipping made.

Rhythm guitars are DOUBLE TRACKED: two separate takes, different seeds,
different detune, a few milliseconds apart, hard left and hard right. No
plugin widens a guitar the way two performances do.

Two ways to render them. `gtr()`/`mute()` are chord-at-a-time - fine for a
wall that changes once a bar. `riff()` renders a whole PHRASE as one take
through one amp pass: strings ring into the next chord, restrikes re-excite
strings that never stopped, chokes and pick scrapes land between events, and
the amp hisses in the rests - which is what separates a performance from a
patch being triggered. `jangle()` is the second guitar: single coils, edge
of break-up, a chorus pedal - a different instrument, not a copy, and the
two together are why a record sounds like a band. `GUITARS` holds the
pickup voicings.

The kit is acoustic, not a drum machine: shell modes with a pitch drop,
wires, a beater click, and one shared room on the whole bus so the kit
sounds like it was played in a place.

Usage:
    from punklib import *
    s = Session(64, tail=2.0)
    for b in range(8):
        chug(s, b, 40, [(0,2),(2,2),(4,2),(6,2),(8,2),(10,2),(12,2),(14,2)])
        s.pat(b, [(0, pkick()), (4, psnare()), (8, pkick()), (12, psnare())],
              bus='drums')
    s.render('punk_test_186.wav', drive=1.1)
"""
import numpy as np
import core
from core import *

BAR, STEP = core.set_grid(bpm=186)
BPM = core.BPM

# Standard tuning, as MIDI. A power chord is a root and its fifth, so it is
# neither major nor minor - which is why punk can put one over any degree of
# the scale and let the bass and the melody decide what the chord means.
STRINGS = (40, 45, 50, 55, 59, 64)          # E2 A2 D3 G3 B3 E4
DROP_D = (38, 45, 50, 55, 59, 64)          # low string down a tone: D2


def set_tempo(bpm, beats=4):
    """Move the grid. Clears the segment cache, because every cached voice
    was rendered against the old bar and would come back the wrong length."""
    global BAR, STEP, BPM
    BAR, STEP = core.set_grid(bpm=bpm, beats=beats)
    BPM = core.BPM
    core._SEG_CACHE.clear()
    return BAR, STEP


def _heavy_cab(heavy):
    """Detuned guitars need the amp's highpass moved down with them. The
    default chain is built around a low E at 82 Hz; a drop-D chord's root is
    73 Hz and would be sitting on the wrong side of the filter, which is how
    a downtuned guitar ends up sounding thinner than a standard-tuned one."""
    if not heavy:
        return None, 98.0
    return (dict(low=62.0, high=4600.0, cone=1.0 + 0.35 * heavy,
                 presence=1.0 - 0.15 * heavy),
            98.0 - 24.0 * heavy)


# ---- the amp ----
def _tube(x, g, asym=0.22):
    """One valve stage. Asymmetric, so it makes even harmonics as well as
    odd - which is the whole difference between 'warm' and 'buzzing'. The
    asymmetry puts DC on the signal, so it comes straight back off."""
    y = np.where(x >= 0, np.tanh(g * x), np.tanh(g * (1 - asym) * x) * (1 - asym * 0.6))
    return (y - y.mean(axis=0)).astype(np.float32)


def amp(x, gain=14.0, tight=98.0, push=0.5, presence=1.0, master=1.0,
        cab_kw=None):
    """Highpass, screamer, three stages with EQ between them, cabinet.

    The highpass comes FIRST and it is not optional: distortion is a
    multiplication, so any two frequencies going in come out with their sum
    and difference as well. Send 82 Hz and 110 Hz into a lot of gain and you
    get 28 Hz of mud that no EQ afterwards can unpick. Cut it before."""
    st = x if x.ndim == 2 else stereo(x)
    y = hp(st, tight, order=2)
    y = y + push * bandpass(y, 480, 1150)             # the overdrive pedal
    y = _tube(y, gain)
    y = lp(y, 6500, order=2)
    # Power supply sag. A valve amp's rails droop when the output stage pulls
    # current, so a loud chord is running on a lower voltage than the note
    # that follows it - the gain breathes with the playing. A memoryless
    # tanh cannot do that, and a distortion that sounds identical on every
    # note is most of what "synthetic" means.
    lvl = uniform_filter1d(np.abs(y).max(axis=1), int(0.018 * SR))
    lvl = lvl / max(float(lvl.max()), 1e-9)
    sag = (1.0 - 0.30 * lvl).astype(np.float32)[:, None]
    y = _tube(y * sag, gain * 0.55) / np.maximum(sag * 0.6 + 0.4, 0.4)
    y = y + presence * 0.30 * bandpass(y, 2000, 3600)
    y = _tube(y, 1.9)
    return cab(y, **(cab_kw or {})) * master


# ---- the guitar ----
def _chord_notes(root, shape='power'):
    if shape == 'power':   return [root, root + 7, root + 12]
    if shape == 'octave':  return [root, root + 12]
    if shape == 'five':    return [root, root + 7]
    if shape == 'maj':     return [root, root + 7, root + 12, root + 16]
    if shape == 'min':     return [root, root + 7, root + 12, root + 15]
    if shape == 'sus4':    return [root, root + 5, root + 12, root + 17]
    return [root]


@cached
def gtr(root, dur_steps=4, take=0, shape='power', gain=14.0, spread=0.006,
        decay=0.85, damp=0.026, level=1.0, ring=True, heavy=0.0):
    """An open power chord, strummed. Each string gets its own seed, its own
    few cents of error and its own few milliseconds of strum delay, because a
    chord where every string starts at the same instant and in tune is an
    organ, not a guitar."""
    n, _ = steps(dur_steps if ring else dur_steps, floor=int(0.12 * SR))
    notes = _chord_notes(root, shape)
    x = np.zeros(n)
    rng = np.random.default_rng(1000 * take + root)
    for i, nt in enumerate(notes):
        cents = spread * (rng.random() - 0.5) * 2
        f = midi(nt) * (1 + cents)
        d = int((0.0055 * i + 0.0015 * rng.random()) * SR)          # strum
        s_ = string(f, n - d, decay=decay * (1 - 0.08 * i), damp=damp,
                    pick=0.22 + 0.1 * rng.random(), B=1.3e-4 * (82.0 / f) ** 0.4,
                    seed=int(7919 * take + 13 * nt))
        x[d:] += s_ * (1.0 - 0.10 * i)
    ck, tight = _heavy_cab(heavy)
    ck = dict(ck or {}, seed=take // 10)               # two speakers, two mics
    out = amp(x / len(notes), gain=gain, tight=tight, cab_kw=ck)
    env = adsr(n, a=0.0004, r=0.010)
    return norm(out * env[:, None], 0.9) * level


@cached
def mute(root, dur_steps=2, take=0, gain=13.0, level=1.0, thud=0.9, heavy=0.0):
    """Palm mute. The side of the picking hand rests on the strings at the
    bridge, so the note dies in a tenth of a second and loses its top before
    it even reaches the amp. What survives is the attack and a thump, and
    eight of those a bar is the engine of the entire genre."""
    n, _ = steps(dur_steps, floor=int(0.05 * SR))
    notes = _chord_notes(root, 'five')
    rng = np.random.default_rng(500 * take + root)
    x = np.zeros(n)
    for i, nt in enumerate(notes):
        f = midi(nt) * (1 + 0.004 * (rng.random() - 0.5))
        d = int(0.0025 * i * SR)
        x[d:] += string(f, n - d, decay=0.075 + 0.02 * rng.random(), damp=0.070,
                        pick=0.11 + 0.05 * rng.random(), B=1.6e-4,
                        top=5600.0, polar=0.5,
                        seed=int(2711 * take + 17 * nt)) * (1 - 0.15 * i)
    y = amp(x / 2, gain=gain, tight=82.0 - 16.0 * heavy, push=0.35, presence=0.35,
            cab_kw=dict(seed=take // 10, low=72.0 - 10.0 * heavy, high=4600.0,
                        cone=1.15 + 0.35 * heavy, presence=1.15))
    f0 = midi(root)                                                 # the thump
    _, t = steps(dur_steps, floor=int(0.05 * SR))
    t = t[:n]
    y = y * 0.55 + thud * stereo(
        (np.sin(2 * np.pi * f0 * t) + 0.5 * np.sin(2 * np.pi * f0 * 2 * t))
        * np.exp(-t / 0.045))
    env = np.exp(-t / 0.075) * adsr(n, a=0.0004, r=0.008)
    return norm(y * env[:, None], 0.9) * level


@cached
def solo(note, dur_steps=4, gain=22.0, level=1.0, vib=5.4, vib_depth=0.010,
         decay=2.4, take=0, bend=0.0):
    """Lead voice: one string, more gain, a long decay and vibrato that fades
    in the way a finger's does. `bend` is semitones pulled up over the note."""
    n, t = steps(dur_steps, floor=int(0.08 * SR))
    x = string(midi(note), n, decay=decay, damp=0.030, pick=0.34, B=6e-5,
               top=6000.0, seed=int(4211 * take + 31 * note))
    y = amp(x, gain=gain, tight=150.0, push=1.0, presence=2.2,
            cab_kw=dict(seed=take // 10 + 2, low=95.0, high=5200.0, cone=0.5,
                        presence=2.4))
    y = np.tanh(2.2 * y) / np.tanh(2.2)                             # sustain
    y = y + 0.7 * bandpass(y, 900, 2200)                            # and cut
    if vib_depth or bend:
        ramp = np.minimum(t / 0.16, 1.0)
        cents = vib_depth * np.sin(2 * np.pi * vib * t) * ramp
        if bend:
            cents = cents + (2 ** (bend / 12) - 1) * np.minimum(t / 0.09, 1.0)
        idx = np.clip(np.cumsum(1 + cents), 0, n - 1)
        y = np.stack([np.interp(idx, np.arange(n), y[:, c]) for c in range(2)], 1)
    env = adsr(n, a=0.0018, r=0.055)
    return norm(y.astype(np.float32) * env[:, None], 0.88) * level


@cached
def clean(root, dur_steps=8, shape='min', level=1.0, take=0, bright=1.0):
    """The same string with the amp turned down: a clean arpeggiated chord
    for the bridge, where the wall has to disappear for a moment so that its
    return means something."""
    n, t = steps(dur_steps, floor=int(0.1 * SR))
    notes = _chord_notes(root, shape)
    x = np.zeros(n)
    for i, nt in enumerate(notes):
        d = int(0.030 * i * SR)                                     # slow strum
        x[d:] += string(midi(nt), n - d, decay=1.8, damp=0.038, pick=0.30,
                        B=1.0e-4, top=6500.0,
                        seed=int(911 * take + 23 * nt)) * (1 - 0.1 * i)
    y = stereo(np.tanh(1.6 * x / len(notes)))
    y = cab(y, seed=take // 10 + 1, low=100.0, high=6200.0, cone=0.4,
            presence=1.2 * bright)
    y = y + 0.30 * hp(y, 3000) * bright
    return norm(y * adsr(n, a=0.003, r=0.06)[:, None], 0.8) * level


# ---- guitars, plural ----
# What makes one guitar not another one is not the string - it is where the
# coil sits under it, where that coil resonates against the cable, and where
# the pick lands. A humbucker at the bridge is fat and speaks at 2.7 kHz; a
# single coil further up the body is thin, bright and peaks over 4 kHz. Give
# a record two of these at once, through two different amps, and it stops
# being "a guitar sound" and becomes a band.
GUITARS = dict(
    hb=dict(pickup=0.13, res_hz=2700.0, res_q=2.0, pick=0.20),   # the wall
    sc=dict(pickup=0.21, res_hz=4300.0, res_q=3.1, pick=0.13),   # the shimmer
)


@cached
def riff(events, bars=1, take=0, gain=18.0, heavy=0.0, guitar='hb', level=1.0,
         tail=6, hiss=1.0, tight=None, thud=0.5, push=0.5, presence=1.0):
    """One continuous rhythm-guitar take: the whole phrase into one amp.

    `gtr()` renders every chord as its own segment through its own pass of
    the amp, normalised to the same peak. That is a sampler playing a patch,
    and it is audible as one: each chord starts from digital silence at a
    loudness identical to the last. A recorded rhythm track is one
    performance - the strings ring INTO the next chord until the fretting
    hand chokes them, a restrike re-excites strings that never stopped, the
    pick scrapes at every change, and the amp hisses in the rests. So the
    whole phrase is built dry, as a performance, and the amp sees it once.

    events: ((step, root, length_steps, kind), ...) with steps counted
    across the whole phrase (0..16*bars). kind:
      'chord'  open power chord; rings its written length, then is choked -
               unless the next event restrikes the same root with no gap, in
               which case the old strings keep ringing under the new strum
      'oct'    root + octave, the two-string post-punk voicing
      'note'   one string
      'mute'   palm mute: dies by itself, with the palm's low thud
    A chord whose written length runs past the end of the phrase is left to
    ring into the tail (`bar-rendered-parts-must-overhang`)."""
    body = int(bars * 16 * STEP)
    n = body + max(int(tail * STEP), int(0.15 * SR))
    rng = np.random.default_rng(6007 * take + 131 * len(events))
    g = GUITARS[guitar]
    dry = np.zeros(n)
    thuds = np.zeros(n)
    evs = sorted(events)
    for i, (st, root, ln, kind) in enumerate(evs):
        a = int(st * STEP) + (int(rng.integers(-88, 89)) if st else 0)
        a = max(a, 0)
        rel = min(int((st + ln) * STEP), n)
        accent = st % 4 == 0
        vel = 1.0 if accent else 0.82 + 0.10 * rng.random()
        tilt = 0.0 if accent else -0.10                 # soft strokes are darker
        if kind == 'mute':
            m = min(n - a, max(int(0.30 * SR), rel - a))
            tm = np.arange(m) / SR
            x = np.zeros(m)
            for j, nt in enumerate((root, root + 7)):
                f = midi(nt) * (1 + 0.004 * (rng.random() - 0.5))
                d = int(0.0022 * j * SR)
                x[d:] += string(f, m - d, decay=0.070 + 0.02 * rng.random(),
                                damp=0.070, pick=0.10 + 0.04 * rng.random(),
                                B=1.6e-4, top=5200.0, polar=0.5, tilt=tilt,
                                seed=int(311 * take + 17 * nt + 7 * i)) * (1 - 0.15 * j)
            f0 = midi(root)                            # the palm on the string:
            x += 0.8 * (np.sin(2 * np.pi * f0 * tm)    # this goes THROUGH the
                        + 0.5 * np.sin(4 * np.pi * f0 * tm)   # amp - a driven
                        ) * np.exp(-tm / 0.045)               # thud IS the chug
            dry[a:a + m] += x * vel
            thuds[a:a + m] += np.sin(2 * np.pi * f0 * tm) * np.exp(-tm / 0.050) * vel
            continue
        notes = ([root, root + 7, root + 12] if kind == 'chord' else
                 [root, root + 12] if kind == 'oct' else [root])
        ring = min(n - a, rel - a + int(0.45 * SR))    # ring past the note-off
        x = np.zeros(ring)
        for j, nt in enumerate(notes):
            f = midi(nt) * (1 + 0.006 * (rng.random() - 0.5) * 2)
            d = int((0.0048 * j + 0.0016 * rng.random()) * SR)
            if ring - d < 64:
                continue
            x[d:] += string(f, ring - d, decay=0.9 * (1 - 0.08 * j), damp=0.026,
                            pick=g['pick'] + 0.06 * rng.random(),
                            pickup=g['pickup'], res_hz=g['res_hz'],
                            res_q=g['res_q'], B=1.3e-4 * (82.0 / f) ** 0.4,
                            tilt=tilt,
                            seed=int(7919 * take + 13 * nt + 5 * i)) * (1 - 0.10 * j)
        if rel - a < ring and st + ln < bars * 16 - 0.01:
            # A restrike of the same chord with no gap only dips the old
            # strings - the pick passes through them; a change or a rest is
            # the fretting hand landing, and that is a choke.
            nxt = evs[i + 1] if i + 1 < len(evs) else None
            restrike = (nxt is not None and nxt[3] == kind and nxt[1] == root
                        and nxt[0] - (st + ln) < 0.01)
            floor_ = 0.34 if restrike else 0.06
            c0 = max(rel - a - int(0.006 * SR), 0)
            tt = np.arange(ring - c0) / SR
            env = np.ones(ring)
            env[c0:] = floor_ + (1 - floor_) * np.exp(-tt / 0.011)
            x *= env
        dry[a:a + ring] += x * vel
        if i and kind in ('chord', 'oct'):             # the scrape at a change
            m = min(int(0.007 * SR), n - a)
            sc = rng.standard_normal(m) * np.exp(-np.arange(m) / SR / 0.0022)
            b0 = max(a - int(0.003 * SR), 0)
            dry[b0:b0 + m] += bandpass(sc[:, None], 1200, 5600)[:, 0] * 0.16
    th = np.arange(n) / SR                             # the amp itself: hiss
    bed = 0.0011 * rng.standard_normal(n)              # and mains hum, so the
    bed += 0.0008 * np.sin(2 * np.pi * 50 * th)        # rests are a room, not
    bed += 0.0005 * np.sin(2 * np.pi * 150 * th + 1.1) # a digital zero
    dry = dry + hiss * bed
    ck, tdef = _heavy_cab(heavy)
    ck = dict(ck or {}, seed=take // 10)
    if guitar == 'sc':
        ck = dict(ck, high=ck.get('high', 4800.0) + 700.0,
                  presence=ck.get('presence', 1.0) * 1.25)
    y = amp(dry / 2.6, gain=gain, tight=tight if tight else tdef, push=push,
            presence=presence, cab_kw=ck)
    y = y / max(float(np.abs(y).max()), 1e-9) * 0.9
    if thud:
        y = y + stereo(thuds) * 0.5 * thud
    k = int(0.05 * SR)
    y[-k:] *= np.linspace(1, 0, k)[:, None]
    return y.astype(np.float32) * level


@cached
def jangle(events, bars=1, take=0, level=1.0, bright=1.0, tail=10, drive=2.2,
           chor=0.55):
    """The other guitar. Single coils into an amp just past clean, then a
    chorus pedal - the cold shimmer that answers the wall on every post-punk
    record. Arpeggios and octaves, everything left ringing into everything
    else: where the wall is a wall, this is the rain running down it.

    Same event format as `riff()`; one continuous take, no chokes - a
    picked arpeggio lives on its overlaps."""
    n = int(bars * 16 * STEP) + max(int(tail * STEP), int(0.3 * SR))
    rng = np.random.default_rng(3391 * take + 101 * len(events))
    g = GUITARS['sc']
    dry = np.zeros(n)
    for i, (st, note, ln, kind) in enumerate(sorted(events)):
        a = int(st * STEP) + (int(rng.integers(-66, 67)) if st else 0)
        a = max(a, 0)
        notes = ([note, note + 12] if kind == 'oct' else
                 [note, note + 7, note + 12] if kind == 'chord' else [note])
        ring = min(n - a, int(ln * STEP) + int(1.3 * SR))
        vel = 1.0 if st % 4 == 0 else 0.84 + 0.10 * rng.random()
        for j, nt in enumerate(notes):
            f = midi(nt) * (1 + 0.005 * (rng.random() - 0.5))
            d = int(0.006 * j * SR)
            if ring - d < 64:
                continue
            dry[a + d:a + ring] += string(f, ring - d, decay=1.6, damp=0.030,
                                          pick=g['pick'] + 0.05 * rng.random(),
                                          pickup=g['pickup'], res_hz=g['res_hz'],
                                          res_q=g['res_q'], B=9e-5, top=7000.0,
                                          seed=int(1117 * take + 29 * nt + 3 * i)
                                          ) * vel * (1 - 0.12 * j)
    y = np.tanh(drive * stereo(dry / 1.8))
    y = cab(y, seed=take // 10 + 3, low=105.0, high=5800.0, cone=0.4,
            presence=1.5)
    y = y + bright * 0.22 * hp(y, 3200)
    y = chorus(y, voices=2, depth_ms=4.2, rate=0.45, base_ms=16.0, mix=chor)
    k = int(0.08 * SR)
    y[-k:] *= np.linspace(1, 0, k)[:, None]
    return norm(y, 0.85) * level


# ---- the bass ----
# A bass guitar is ONE string that keeps vibrating. Picking it again does not
# start a new note, it re-excites a note that never stopped - which is why a
# bassline rendered as eight separate plucks per bar comes out shattered: the
# fundamental dies in every gap, and where two plucks do overlap they are at
# unrelated phases and cancel. So a whole bar is rendered as one continuous
# oscillator whose pitch bends between notes and whose amplitude swells at
# each pick. The attacks are discrete; the low end never is.
@cached
def bassbar(notes, dur_steps=16, level=1.0, drive=2.0, glide=0.016,
            decay=0.34, take=0, bright=1.0):
    """One bar of picked bass. `notes` is a tuple of (step, midi)."""
    n, t = steps(dur_steps)
    evs = sorted(notes)
    edge = [min(int(st * STEP), n) for st, _ in evs] + [n]

    f = np.empty(n)                                   # one frequency track...
    f[:edge[0]] = midi(evs[0][1])
    for i, (_, nt) in enumerate(evs):
        f[edge[i]:edge[i + 1]] = midi(nt)
    f = uniform_filter1d(f, max(int(glide * SR), 3))  # ...smoothed = portamento
    ph = 2 * np.pi * np.cumsum(f) / SR                # one unbroken phase

    amp = np.zeros(n)                                 # swells at every pick,
    for k in edge[:-1]:                               # never returns to zero
        d = np.exp(-np.arange(n - k) / SR / decay)
        np.maximum(amp[k:], d, out=amp[k:])
    amp = uniform_filter1d(amp, max(int(0.005 * SR), 3))

    low = (np.sin(ph) + 0.30 * np.sin(2 * ph) + 0.12 * np.sin(3 * ph)) * amp

    pick = np.zeros(n)                                # the attacks, discrete
    rng = np.random.default_rng(900 + take)
    for i, (st, nt) in enumerate(evs):
        k = edge[i]
        m = min(n - k, int(0.24 * SR))
        if m < 32:
            continue
        pick[k:k + m] += string(midi(nt), m, decay=0.22, damp=0.048, pick=0.10,
                                B=4.2e-4, top=4800.0, bright=1.15,
                                seed=int(3301 * take + 41 * nt + 7 * i))
        c = min(n - k, int(0.006 * SR))
        pick[k:k + c] += rng.standard_normal(c) * np.exp(
            -np.arange(c) / SR / 0.0022) * 0.30 * bright

    st_ = stereo(pick)
    grind = np.tanh(drive * 3.0 * bandpass(st_, 300, 2600)) * 0.30
    out = (lp(stereo(low), 330, order=4) * 0.55
           + hp(st_, 200, order=2) * 1.05
           + grind * 2.3
           + hp(st_, 2000, order=2) * 0.30 * bright)
    out = out + 0.45 * bandpass(out, 280, 620)        # the fingers on the string
    out = np.tanh(1.35 * hp(out, 34, order=2))
    return (out * adsr(n, a=0.0012, r=0.0030)[:, None]).astype(np.float32) * level * 0.82


@cached
def pbass(note, dur_steps=2, level=1.0, drive=2.0, pick=1.0, decay=0.55, take=0):
    """A single picked note, for the places a bar of them is not what is
    wanted - the last chord of the track, a stab, a pickup."""
    return bassbar(((0, note),), dur_steps=dur_steps, level=level, drive=drive,
                   decay=decay, take=take, bright=pick)


# ---- the kit ----
@cached
def pkick(dur_steps=4, tune=61.0, gain=1.0, click=1.0, decay=0.175, seed=0):
    """A 22-inch kick with a wooden beater and no front head. Punk kicks are
    clicky because the mic is inside the drum, close to the beater."""
    n, t = steps(dur_steps, floor=int(0.2 * SR))
    rng = np.random.default_rng(seed)
    f = tune * (1 + 2.6 * np.exp(-t / 0.010))
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / decay)
    punch = np.sin(2 * np.pi * tune * 2.05 * t) * np.exp(-t / 0.045) * 0.55
    shell = np.sin(2 * np.pi * tune * 3.4 * t) * np.exp(-t / 0.022) * 0.30
    beater = rng.standard_normal(n) * np.exp(-t / 0.0030)
    beater += np.sin(2 * np.pi * 2900 * t) * np.exp(-t / 0.0055) * 0.6
    out = stereo(body + punch + shell) + hp(stereo(beater), 1400) * 1.5 * click
    out = np.tanh(1.6 * out)
    out = out + 0.60 * bandpass(out, 65, 140) + 0.9 * bandpass(out, 2400, 5200)
    out = out + 0.25 * bandpass(out, 300, 700)                      # the shell
    return norm(hp(out, 42, order=2) * adsr(n, a=0.0004, r=0.02)[:, None], 0.95) * gain


@cached
def psnare(dur_steps=4, gain=1.0, tune=196.0, snap=1.0, decay=0.115, seed=0,
           rim=0.0):
    """The crack. A tuned shell with three modes, a stick transient, and the
    wires - a longer, brighter noise underneath that is what actually says
    'snare drum'. In this genre it is the second loudest thing on the record."""
    n, t = steps(dur_steps, floor=int(0.18 * SR))
    rng = np.random.default_rng(seed + 5)
    pd = 1 + 0.22 * np.exp(-t / 0.008)                              # head tension
    shell = (np.sin(2 * np.pi * tune * pd * t) * np.exp(-t / 0.062)
             + 0.55 * np.sin(2 * np.pi * tune * 1.59 * pd * t) * np.exp(-t / 0.042)
             + 0.30 * np.sin(2 * np.pi * tune * 2.47 * t) * np.exp(-t / 0.026))
    nz = rng.standard_normal(n)
    wires = bandpass(stereo(nz), 1500, 8000) * np.exp(-t / decay)[:, None] * 1.30 * snap
    stick = bandpass(stereo(nz * np.exp(-t / 0.0018)), 2000, 7000) * 0.55
    out = stereo(shell * 1.05 * (1.0 + rim)) + wires + stick
    out = np.tanh(1.8 * out)
    out = out + 0.26 * bandpass(out, 2200, 4800)                    # the crack
    out = out + 0.18 * bandpass(out, 170, 320)                      # the shell
    return norm(hp(out, 110) * adsr(n, a=0.0004, r=0.02)[:, None], 0.95) * gain


@cached
def phat(dur_steps=1, open_=False, gain=1.0, tone=1.0, seed=0):
    """Hi-hat: six inharmonic squares for the metal, noise for the air."""
    n, t = steps(dur_steps, floor=int(0.03 * SR))
    rng = np.random.default_rng(seed + 11)
    ratios = (1.0, 1.34, 1.61, 1.99, 2.44, 2.79)
    x = sum(np.sign(np.sin(2 * np.pi * 860 * r * tone * t)) for r in ratios) / 6
    x = x * 1.1 + rng.standard_normal(n) * 0.7
    d = 0.32 if open_ else 0.030
    out = hp(stereo(x), 4200 if not open_ else 3400)
    out = out + 0.5 * bandpass(out, 5000, 9000)
    out = lp(out, 13500, order=2)
    out = out * (np.exp(-t / d) * adsr(n, a=0.0006, r=0.01))[:, None]
    return norm(out, 0.9) * gain * 0.58


@cached
def pcrash(dur_steps=16, gain=1.0, seed=0, size=1.0):
    """18-inch crash: a dense inharmonic wash with a stick attack on top."""
    n, t = steps(dur_steps, floor=int(0.6 * SR))
    rng = np.random.default_rng(seed + 21)
    ratios = (1.0, 1.41, 1.83, 2.31, 2.77, 3.42, 4.11, 5.3, 6.7, 8.1)
    x = sum(np.sin(2 * np.pi * 760 * r * t + rng.random() * 6) for r in ratios) / 10
    x = x * 1.2 + rng.standard_normal(n) * 0.75
    out = hp(stereo(x), 1700)
    out = out + 0.45 * bandpass(out, 4000, 9000)
    out = out * (np.exp(-t / (1.15 * size)) * adsr(n, a=0.0008, r=0.25))[:, None]
    out = out + hp(stereo(rng.standard_normal(n) * np.exp(-t / 0.004)), 5000) * 0.5
    return norm(widen(out, 1.1), 0.85) * gain * 0.46


@cached
def pride(dur_steps=2, gain=1.0, bell=0.0, seed=0):
    """Ride: mostly ping, a little wash. The bell is the same cymbal hit
    where it is stiffest, so its partials are higher and it rings longer."""
    n, t = steps(dur_steps, floor=int(0.1 * SR))
    rng = np.random.default_rng(seed + 31)
    ratios = (1.0, 1.47, 2.09, 2.71, 3.4) if not bell else (1.0, 2.0, 2.97, 4.1)
    base = 940 if not bell else 1180
    x = sum(np.sin(2 * np.pi * base * r * t + rng.random() * 6) for r in ratios) / 5
    x = x * (1.0 if bell else 0.7) + rng.standard_normal(n) * (0.2 if bell else 0.45)
    out = hp(stereo(x), 1500)
    out = out * (np.exp(-t / (0.5 + 0.7 * bell)) * adsr(n, a=0.0006, r=0.06))[:, None]
    return norm(out, 0.85) * gain * 0.38


@cached
def ptom(dur_steps=2, tune=140.0, gain=1.0, seed=0):
    """Rack/floor tom: a shell mode with a pitch drop, plus head noise."""
    n, t = steps(dur_steps, floor=int(0.15 * SR))
    rng = np.random.default_rng(seed + 41)
    f = tune * (1 + 0.35 * np.exp(-t / 0.020))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.20)
    x += 0.4 * np.sin(2 * np.pi * tune * 1.5 * t) * np.exp(-t / 0.10)
    head = bandpass(stereo(rng.standard_normal(n) * np.exp(-t / 0.010)), 900, 5000)
    out = np.tanh(1.5 * (stereo(x) + head * 0.5))
    return norm(hp(out, 60) * adsr(n, a=0.0006, r=0.02)[:, None], 0.92) * gain


def room(buf, decay=0.55, wet=0.22, tone=5200, block_bars=16):
    """The tail ONLY - add it to the bus, do not replace it.

    One room for the whole kit. A drum kit is not five instruments in five
    different spaces; the same pair of overheads hears all of it, and that
    shared early reflection pattern is most of what 'a band' sounds like.
    Convolved in blocks so a three-minute buffer does not need a
    three-minute FFT."""
    out = np.zeros_like(buf)
    ir = core._reverb_ir(decay, tone)
    pre = int(0.006 * SR)
    blk = int(block_bars * BAR)
    for a in range(0, len(buf), blk):
        seg = buf[a:a + blk]
        if np.abs(seg).max() < 1e-6:
            continue
        for c in range(2):
            w = wet * fftconvolve(seg[:, c], ir[:, c])
            b = a + pre
            e = min(b + len(w), len(out))
            if b < len(out):
                out[b:e, c] += w[:e - b].astype(np.float32)
    return out


# ---- gang vocals ----
@cached
def gang(note, dur_steps=8, gain=1.0, vowel='ah', voices=8, seed=0, rasp=0.0,
         drop=0.0):
    """Eight people in a room shouting one vowel, none of them in tune with
    each other. The spread is the point: a single voice is a synth, and it is
    only when the detuning is wide enough to beat that it becomes a crowd."""
    n, t = steps(dur_steps, floor=int(0.1 * SR))
    rng = np.random.default_rng(seed + 77)
    f = midi(note)
    x = np.zeros(n)
    for i in range(voices):
        det = 1 + 0.016 * (rng.random() - 0.5) * 2
        drift = 1 + 0.004 * np.sin(2 * np.pi * (3.5 + rng.random()) * t + rng.random() * 6)
        if drop:                                       # every shout starts above
            drift = drift * (1 + drop * np.exp(-t / 0.055))
        ph = np.cumsum(f * det * drift) / SR
        x += (2 * ((ph + rng.random()) % 1.0) - 1) * (0.7 + 0.3 * rng.random())
    st = stereo(x / voices)
    out = sum(bandpass(st, fc * 0.72, fc * 1.35) * g
              for fc, g in zip(FORMANTS[vowel], (1.0, 0.8, 0.5)))
    out += 0.45 * bandpass(st, 2400, 3400)          # the singer's formant: how a
    out += 0.25 * bandpass(st, 4000, 6000)          # shout carries over a band
    out += hp(stereo(rng.standard_normal(n)), 3000) * 0.045 * np.minimum(t / 0.05, 1)[:, None]
    if rasp:                                           # the torn edge of a shout
        out = out + rasp * 0.5 * bandpass(np.tanh(6.0 * st), 900, 5200)
    out = np.tanh((2.4 + 3.0 * rasp) * out)
    env = np.minimum(t / 0.045, 1.0) * np.exp(-t / (dur_steps * STEP / SR * 1.6))
    return norm(widen(out, 1.4) * (env * adsr(n, a=0.004, r=0.06))[:, None], 0.85) * gain
