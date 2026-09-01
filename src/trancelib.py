"""The trance layer: the main-stage kit, the rolling bass and the hypersaw.

Uplifting trance at 138 BPM. What separates this from every other
four-on-the-floor module here is not the tempo - it is that trance spends its
entire vocabulary on ONE gesture: accumulate, withhold, release. Everything in
this file exists to serve that.

Four things are built rather than borrowed, and each of them is a gap the
engine genuinely had:

`tkick` sits between `hkick` and `hardkick` and is neither. The house kick
deliberately has no click - "a kick with a bright tick in it turns a warm
record into a techno one" - and the hardstyle kick is a distortion chain with
a tuned tail that IS the bassline. A trance kick is a third thing: bright,
short (185 ms at 138 is under half a beat), undistorted, and with a real
transient at 2-7 kHz, because the offbeat bass needs the second half of every
beat and the open hat needs to be answered.

`rollbass` is the genre's engine. Three sixteenths after every kick, plucky,
short, with a filter envelope on each one - and rendered as ONE phase track
per phrase with the sub taken as `sin(ph/2)` off that same track. That is one
oscillator cut in half rather than two oscillators, so the octave can never
drift out of phase with its own fundamental.

`hypersaw` is the JP-8000 waveform written properly. The obvious way to build
a seven-saw stack is to spread the voices LINEARLY, and that gives a chorus;
the thing that makes the real one sound like a wall is that the spread
ACCELERATES - the outer pair sits nearly four times as far out as the inner
pair. The other half is the high-pass: an unfiltered seven-saw stack still
carries its full 1/n spectrum under 250 Hz and eats the bassline whole.

`uplift` is the riser. `core.riser` crossfades three static filters over a
quadratic swell, which is a whoosh; a festival riser is a RESONANT band-pass
whose centre climbs exponentially, with a tone rising underneath it, and the
resonance is most of why it feels like pressure rather than noise.

Everything else - the arp voice, the impact, the crash, the sub-drop, the
crowd - is already in core and fits.

Usage:
    from trancelib import *
    s = Session(64, tail=4.0)
    for st in (0, 4, 8, 12):
        t = s.pos(0, st); s.hit(t)
        s.place(t, tkick(seed=st), bus='drums')
    s.place(s.pos(0), rollbass([(0, 42)], 1), bus='bass')
    s.render('trance.wav', drive=1.0, limit=0.93)
"""
import numpy as np
import core
from core import *
from scipy.ndimage import uniform_filter1d
from core import _ftrack, _amp, _SEG_CACHE

BAR, STEP = core.set_grid(bpm=138)
BPM = core.BPM

def set_tempo(bpm, beats=4):
    """Re-grid the module. Every cached segment was rendered against the old
    grid, so the cache goes with it."""
    global BAR, STEP, BPM
    BAR, STEP = core.set_grid(bpm=bpm, beats=beats)
    BPM = core.BPM
    core._SEG_CACHE.clear()
    return BAR, STEP


# Trance pumps, and it pumps on purpose - the duck is an audible part of the
# record, not a fix for a collision. The bass gets out of the way completely;
# the pad and the lead breathe by 4-6 dB, which is the "wave" under a
# sustained supersaw chord; the arp dips less because its own notes are short
# and a deep duck would swallow them.
Session.DUCKED = {'bass': 1.00, 'sub': 1.00, 'pad': 0.58, 'lead': 0.42,
                  'arp': 0.30, 'music': 0.50, 'air': 0.34}

# Three sixteenths after every kick. This is the whole rhythmic identity of
# the genre and it is worth a name: the kick owns steps 0, 4, 8, 12 and the
# bass owns everything else, so the low band is continuous while the pulse
# stays unambiguous.
ROLL = (1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15)
ROLL8 = (2, 3, 6, 7, 10, 11, 14, 15)          # thinner: two per beat
OFFBEAT = (2, 6, 10, 14)


# ================================================================= the kit ===
@cached
def tkick(dur_steps=4.0, tune=46.25, top=215.0, tau=0.016, decay=0.170,
          body=1.0, click=1.0, beater=1.0, drive=2.5, gain=1.0, sub=1.0,
          tone=1.0, seed=0):
    """Short, bright, and not distorted.

    The dive is fast - 215 Hz down to the root in 16 ms - so what is heard at
    the front is a snap rather than the thump a house kick makes out of a slow
    24 ms slide. The body is gone in 185 ms, which at 138 BPM is 43% of a beat
    and leaves the rest of it to the offbeat bass and the open hat.

    The click is band-limited noise at 2.2-7 kHz and it is the sound that says
    festival: it survives a PA at fifty metres where 50 Hz has already turned
    into a wash. `seed` re-rolls it on every hit, because a bright transient
    that is bit-identical four thousand times stops being a drum and becomes a
    tick."""
    n, t = steps(max(dur_steps, 2.2), floor=int(0.30 * SR))
    rs = np.random.RandomState(1300 + seed * 13)
    f = tune * (top / tune) ** np.exp(-t / tau)
    ph = 2 * np.pi * np.cumsum(f) / SR
    env = np.minimum(t / 0.0011, 1.0) * np.exp(-t / decay)
    x = np.sin(ph) * env * sub
    x += body * 0.74 * np.sin(2 * np.pi * 97.0 * t) * np.exp(-t / 0.058)
    x += body * 0.32 * np.sin(2 * np.pi * 163.0 * t) * np.exp(-t / 0.021)
    st = stereo(x / 2.06)
    if beater:
        b = rs.standard_normal(n) * np.exp(-t / 0.0085)
        st = st + bandpass(stereo(b), 600, 2500, order=2) * 0.40 * beater
    if click:
        c = rs.standard_normal(n) * np.exp(-t / 0.0042)
        st = st + bandpass(stereo(c), 2200 * tone, 7000 * tone, order=2) * 0.62 * click
    # Asymmetric: a symmetric tanh on a sine is a square, and a square at
    # 46 Hz is a buzz rather than weight.
    st = drive_asym(st, drive, asym=0.26)
    st = hp(st, 28, order=2)
    return (st * adsr(n, a=0.0004, r=0.018)[:, None]).astype(np.float32) * gain * 0.82


@cached
def tclap(dur_steps=4.0, gain=1.0, spread=1.0, room=1.0, tone=1.0, seed=0):
    """The other half of the backbeat, and the loudest reverb on the record.

    Four bursts about 9 ms apart, each in a different place across the image,
    then a body burst underneath - the same construction every clap uses. What
    makes it a TRANCE clap is what happens after: a bright plate with a 900 ms
    tail mixed in at 45%, which is far more reverb than any other genre here
    puts on a percussion hit and is exactly why the backbeat of a main-stage
    record sounds like it is happening in a stadium."""
    n, t = steps(max(dur_steps, 3.6), floor=int(0.55 * SR))
    rs = np.random.RandomState(2400 + seed * 29)
    st = np.zeros((n, 2), dtype=np.float32)
    for off, lvl, p in ((0.000, 1.00, -0.22), (0.0088, 0.88, 0.26),
                        (0.0172, 0.76, -0.34), (0.0256, 0.60, 0.38)):
        d = int((off + 0.0018 * rs.rand()) * SR)
        m = n - d
        tm = np.arange(m) / SR
        b = rs.standard_normal(m) * np.exp(-tm / 0.0040)
        one = np.zeros((n, 2), dtype=np.float32)
        one[d:] = panned(bandpass(stereo(b), 950, 4600 * tone, order=2), p * spread) * lvl
        st += one
    tail = rs.standard_normal(n) * np.exp(-t / 0.075)
    st = st * 0.55 + bandpass(stereo(tail), 800, 2800, order=2) * 0.45
    st = hp(st, 340, order=2)
    if room:
        wet = reverb(st, decay=0.95, wet=1.0, tone=6800, predelay=0.012)[:n]
        st = st + room * 0.45 * hp(wet, 500, order=2)
    return (st * adsr(n, a=0.0004, r=0.040)[:, None]).astype(np.float32) * gain * 0.68


@cached
def tsnare(dur_steps=2.5, gain=1.0, tune=196.0, bright=1.0, body=1.0,
           room=0.0, seed=0):
    """The snare that hides under the clap and does the rolls on its own.

    Two tuned sines with a fast drop for the body, a band of noise for the
    crack and a high-passed layer for the snap. It carries a real 190 Hz
    fundamental because the backbeat has to be felt in the low band and a
    clap has nothing down there - `the-felt-pulse-is-in-the-low-band`."""
    n, t = steps(max(dur_steps, 2.0), floor=int(0.26 * SR))
    rs = np.random.RandomState(3100 + seed * 37)
    drop = 2 ** (-1.1 * np.minimum(t / 0.016, 1.0))
    x = (np.sin(2 * np.pi * tune * drop * t) * 0.95
         + np.sin(2 * np.pi * tune * 1.48 * drop * t) * 0.45) * np.exp(-t / 0.052) * body
    nz = rs.standard_normal(n)
    crack = bandpass(stereo(nz), 300, 7200 * bright, order=2) * np.exp(-t / 0.075)[:, None]
    snap = hp(stereo(nz), 6200 * bright, order=2) * np.exp(-t / 0.030)[:, None]
    st = stereo(x) * 0.50 + crack * 0.42 + snap * 0.30
    st = hp(st, 150, order=2)
    st = np.tanh(1.6 * st) / np.tanh(1.6)
    if room:
        st = st + room * 0.35 * hp(reverb(st, decay=0.7, wet=1.0, tone=6200)[:n], 600)
    return (st * adsr(n, a=0.0004, r=0.022)[:, None]).astype(np.float32) * gain * 0.48


# Six squares at ratios that are deliberately not a harmonic series, so the
# stack has a metal colour and no pitch. Same principle as the 808/909 hat.
_HR = (1.0, 1.348, 1.618, 2.005, 2.451, 2.799)

@cached
def thhat(dur_steps=1.0, open_=False, gain=1.0, tone=1.0, base=336.0,
          decay=None, seed=0):
    """Brighter and sizzlier than a house hat, and the open one is TRUNCATED.

    At 138 BPM the offbeats are 435 ms apart. An open hat with a merely long
    exponential is still sounding when the next one starts, and four of those
    a bar turns the top of the record into sand
    (`an-open-hat-must-end-before-the-next-one`). This one rings for 160 ms
    and is windowed to silence by 340, which leaves ninety milliseconds of air
    before the next offbeat - and that gap is what makes each one read as an
    event."""
    dec = decay if decay is not None else (0.160 if open_ else 0.021)
    n, t = steps(max(dur_steps, 0.5), floor=int(0.42 * SR))
    rs = np.random.RandomState(4400 + seed * 19)
    x = np.zeros(n)
    for r in _HR:
        x += np.sign(np.sin(2 * np.pi * base * r * t + rs.rand() * 6.283))
    x = x / len(_HR) + 0.62 * rs.standard_normal(n)
    st = hp(stereo(x), (6200 if open_ else 8000) * tone, order=4)
    st = st - 0.24 * bandpass(st, 9200, 11800, order=2)
    env = np.exp(-t / dec)
    if open_:
        k0, k1 = int(0.170 * SR), min(int(0.340 * SR), n)
        if k1 > k0:
            env[k0:k1] *= 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, k1 - k0))
        env[k1:] = 0.0
    st = st * env[:, None]
    st[:, 1] = np.roll(st[:, 1], int(SR * 0.0004))
    return (st * adsr(n, a=0.0002, r=0.006)[:, None]).astype(np.float32) * gain * 0.50


@cached
def tride(dur_steps=8.0, gain=1.0, tone=1.0, seed=0):
    """A ping with a wash behind it. Sixteenths of this under a drop are what
    keeps the top end moving without another open hat in the way."""
    n, t = steps(max(dur_steps, 3.0), floor=int(0.40 * SR))
    rs = np.random.RandomState(5200 + seed * 23)
    x = sum(np.sin(2 * np.pi * 520 * r * tone * t + rs.rand() * 6.283) for r in _HR) / 6
    ping = bandpass(stereo(x), 2400, 6800, order=2) * np.exp(-t / 0.042)[:, None]
    wash = hp(stereo(rs.standard_normal(n)), 7200 * tone, order=2) * np.exp(-t / 0.115)[:, None]
    st = ping * 0.55 + wash * 0.45
    return (st * adsr(n, a=0.0004, r=0.02)[:, None]).astype(np.float32) * gain * 0.22


def roll(s, b0, bars, bus='drums', gain=1.0, rates=(2.0, 2.0, 1.0, 0.5),
         v0=0.30, v1=1.05, tune=196.0, bright=1.0, seed=0, curve=1.6):
    """The accelerating snare roll - the single most reliable build in music.

    `rates` is one step-value per bar: 2.0 is eighths, 1.0 sixteenths, 0.5
    thirty-seconds. The velocity ramps across the WHOLE run rather than per
    bar, so the last bar of a four-bar roll is not merely faster, it is also
    the loudest thing in the section."""
    ev = []
    for i in range(bars):
        r = rates[min(i, len(rates) - 1)]
        st = 0.0
        while st < 16.0 - 1e-6:
            ev.append((b0 + i, st))
            st += r
    for k, (b, st) in enumerate(ev):
        u = (k / max(len(ev) - 1, 1)) ** curve
        v = v0 + (v1 - v0) * u
        s.place(s.pos(b, st),
                tsnare(2.0, tune=tune, bright=bright, body=0.85,
                       seed=(k * 7 + seed) % 61),
                gain * v, bus)


# ================================================================ the bass ===
@cached
def rollbass(notes, dur_bars=1, gate=ROLL, gain=1.0, cutoff=560.0, f_hi=3200.0,
             res=1.6, decay=0.052, hold=0.060, voices=3, detune=17.0,
             sub=0.50, drive=1.9, hpf=70.0, glide=0.014, tail=5.0, seed=0,
             bands=7, kmax=48):
    """The rolling offbeat bass, one phrase at a time.

    Cached, so `notes` and `gate` must be tuples.

    `notes` is [(step, midi), ...] across the whole phrase; the pitch changes
    where the chord changes and nowhere else. `gate` is which steps of each
    bar sound - ROLL is the three sixteenths after every kick, which is the
    genre.

    Two decisions carry it. The first is that the phrase is ONE phase track:
    the oscillator never restarts, so a chord change glides instead of
    clicking and the gate cuts a continuous sound into notes rather than
    triggering separate ones. The second is where the octave comes from - the
    sub is `sin(ph/2)` taken off that same track, so it is the character layer
    cut in half rather than a second oscillator underneath it, and the two can
    never drift out of phase (`one-oscillator-cut-in-half-not-two-oscillators`).

    The saw stack keeps its own fundamental: written at MIDI 38-45 it sits at
    73-110 Hz and the high-pass is at 70, under the lowest note it plays
    (`bass-must-keep-its-own-fundamental`). Each gated note gets its own
    filter envelope falling from `f_hi` to `cutoff`, which is what makes a
    rolling bass pluck rather than pulse."""
    n = int((dur_bars * 16 + tail) * STEP)
    f = _ftrack(notes, n, glide)
    ph = 2 * np.pi * np.cumsum(f) / SR
    fmax = max(midi(m) for _, m in notes)

    # the gate, as an amplitude envelope and a filter envelope at once
    amp = np.zeros(n)
    cut = np.zeros(n)
    for b in range(dur_bars):
        for st in gate:
            k = int((b * 16 + st) * STEP)
            if k >= n:
                continue
            m = min(int(2.4 * STEP), n - k)
            tt = np.arange(m) / SR
            e = np.minimum(tt / 0.0022, 1.0) * np.exp(-tt / decay)
            e *= np.exp(-np.maximum(tt - hold, 0.0) / 0.020)   # a real release
            np.maximum(amp[k:k + m], e, out=amp[k:k + m])
            np.maximum(cut[k:k + m], np.exp(-tt / (decay * 0.62)), out=cut[k:k + m])
    amp = np.maximum(uniform_filter1d(amp, max(int(0.0015 * SR), 3)), 0.0)
    cut = np.maximum(uniform_filter1d(cut, max(int(0.0025 * SR), 3)), 0.0)

    x = sawstack(ph, fmax, voices=voices, detune=detune, seed=seed, kmax=kmax)
    y = morph_lp(stereo(x), cutoff, f_hi, cut, bands=bands, res=res)
    y = np.tanh(drive * y) / np.tanh(drive)
    y = hp(y, hpf, order=2) * amp[:, None]

    if sub:
        sb = np.sin(ph * 0.5) + 0.22 * np.sin(ph)       # h1 and its own octave
        sb = np.tanh(1.25 * sb / 1.22) / np.tanh(1.25)
        low = lp(stereo(sb), 150, 4) * amp[:, None] * sub
        y = y + low.astype(np.float32)
    return (y * gain * 0.62).astype(np.float32)


@cached
def subline(notes, dur_bars=1, gain=1.0, gate=None, glide=0.020, drive=1.2,
            h2=0.55, tail=4.0, floor_=0.0, attack=0.006):
    """A held sub under a breakdown or a drop - one sine, one phase, mono.
    `gate` is a per-step 0/1 lane if the sub should breathe with the kick."""
    n = int((dur_bars * 16 + tail) * STEP)
    f = _ftrack(notes, n, glide)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) + h2 * np.sin(2 * ph)
    if gate is not None:
        g = np.clip(steplane(list(gate) * dur_bars, n, 'hold', 0.006), 0, 1)
        x = x * (floor_ + (1 - floor_) * g)
    x = np.tanh(drive * x / (1 + h2)) / np.tanh(drive)
    env = np.ones(n)
    a = min(int(attack * SR), n // 4)
    r = min(int(0.05 * SR), n // 4)
    env[:a] = np.linspace(0, 1, a) ** 1.5
    env[-r:] *= np.linspace(1, 0, r)
    return (lp(stereo(x), 150, 4) * env[:, None]).astype(np.float32) * gain * 0.85


# ================================================================ the lead ===
# The JP-8000 curve. Seven voices, and the spread ACCELERATES: the outer pair
# sits nearly four times as far out as the inner pair. A linear spread is a
# chorus; this is a wall. Values are fractions of the `spread` parameter,
# which is the outer pair's detune in cents.
_SS_OFFS = (0.0, -0.263, 0.263, -0.579, 0.579, -1.0, 1.0)
_SS_PAN = (0.0, -0.30, 0.30, -0.62, 0.62, -0.94, 0.94)

def _noteenv(notes, n, attack=0.012, release=0.10, decay=0.0, sustain=1.0):
    """One envelope over a continuous oscillator: every note swells, and a
    note that ends fades rather than stopping (`note-envelopes-need-a-release`).
    Overlapping notes max-accumulate, so a legato line never dips to zero."""
    env = np.zeros(n)
    for ev in notes:
        st, dur = ev[0], ev[2]
        vel = ev[3] if len(ev) > 3 else 1.0
        a = int(st * STEP)
        hold = dur * STEP / SR
        m = min(int((dur + 2.0) * STEP) + int(release * SR), n - a)
        if a >= n or m <= 0:
            continue
        tt = np.arange(m) / SR
        e = np.minimum(tt / max(attack, 1e-4), 1.0) ** 1.4
        if decay:
            e = e * (sustain + (1 - sustain) * np.exp(-tt / decay))
        e = e * np.exp(-np.maximum(tt - hold, 0.0) / max(release, 1e-4))
        np.maximum(env[a:a + m], e * vel, out=env[a:a + m])
    return np.maximum(uniform_filter1d(env, max(int(0.0012 * SR), 3)), 0.0)


@cached
def hypersaw(notes, dur_steps=16, gain=1.0, spread=34.0, mix=0.68, hpf=270.0,
             lpf=12000.0, attack=0.014, release=0.11, decay=0.0, sustain=1.0,
             sub=0.30, sub_wave='square', vib=9.0, vib_hz=5.4, vib_delay=0.32,
             glide=0.010, width=1.0, drive=1.1, seed=0, kmax=100):
    """Seven saws on the JP-8000 curve, played as a monophonic lead line.

    Cached, so `notes` is a tuple of tuples.

    `notes` is [(step, midi, dur[, vel]), ...]. The whole line is one phase
    track, so a legato pair glides and a repeated note re-excites an
    oscillator that never stopped.

    The high-pass at 270 Hz is not optional. Seven saws carry their full
    1/n spectrum down to the fundamental, and a lead voiced at MIDI 78 still
    puts enough at 90-250 Hz to swallow the bassline whole - which is why
    every trance lead in the world is high-passed and why the sub layer here
    is added AFTER the filter rather than before it.

    The vibrato fades in over `vib_delay` seconds. Applied from the attack it
    reads as a synth preset; applied late it reads as a hand on a mod wheel."""
    n = int(max(dur_steps, 1) * STEP) + int(release * SR) + int(0.05 * SR)
    rs = np.random.RandomState(6100 + seed * 31)
    ft = _ftrack([(ev[0], ev[1]) for ev in notes], n, glide)
    if vib:
        t = np.arange(n) / SR
        depth = np.minimum(t / max(vib_delay, 1e-3), 1.0) ** 2
        ft = ft * 2.0 ** (vib * depth * np.sin(2 * np.pi * vib_hz * t) / 1200.0)
    ph = 2 * np.pi * np.cumsum(ft) / SR
    fmax = float(ft.max())

    l = np.zeros(n); r = np.zeros(n)
    for i, (o, p) in enumerate(zip(_SS_OFFS, _SS_PAN)):
        ratio = 2.0 ** (spread * o / 1200.0)
        v = saw_ph(ph * ratio + rs.rand() * 6.283, fmax * ratio, kmax=kmax)
        lvl = 1.0 if i == 0 else mix
        ang = (np.clip(p * width, -1, 1) + 1) * np.pi / 4
        l += v * lvl * np.cos(ang)
        r += v * lvl * np.sin(ang)
    y = np.stack([l, r], 1) / (1.0 + 6 * mix)          # normalise BEFORE the drive
    y = lp(y.astype(np.float32), lpf, 4)
    y = hp(y, hpf, order=2)
    if drive and drive != 1.0:
        y = np.tanh(drive * y) / np.tanh(drive)
    if sub:
        s_ = (np.sign(np.sin(ph * 0.5)) if sub_wave == 'square'
              else np.sin(ph * 0.5))
        y = y + lp(stereo(s_ * 0.5), 900, 4) * sub
    env = _noteenv(notes, n, attack, release, decay, sustain)
    return (y * env[:, None]).astype(np.float32) * gain * 0.50


def stack3(s, t, notes, bus='lead', gain=1.0, low=0.42, top=0.30, **kw):
    """The lead in three registers at once - the move that separates a trance
    lead from a synth playing a tune. The same notes an octave down for weight
    and an octave up for air, all three sharing one reverb, so the ear hears
    one instrument three octaves tall rather than three parts."""
    s.place(t, hypersaw(notes, gain=gain, **kw), 1.0, bus)
    if low:
        lo = tuple((e[0], e[1] - 12) + tuple(e[2:]) for e in notes)
        s.place(t, hypersaw(lo, gain=gain * low, hpf=kw.get('hpf', 270) * 0.55,
                            sub=0.0, spread=kw.get('spread', 34.0) * 0.7,
                            **{k: v for k, v in kw.items()
                               if k not in ('hpf', 'sub', 'spread')}), 1.0, bus)
    if top:
        hi = tuple((e[0], e[1] + 12) + tuple(e[2:]) for e in notes)
        s.place(t, hypersaw(hi, gain=gain * top, sub=0.0,
                            **{k: v for k, v in kw.items() if k != 'sub'}), 1.0, bus)


# ================================================================= the pad ===
@cached
def tpad(chords, dur_steps=16, gain=1.0, voices=3, detune=15.0, cutoff=2600.0,
         hpf=230.0, attack=0.55, release=1.2, wide=1.0, sub=0.0, seed=0,
         sweep=0.0, kmax=70):
    """A detuned saw stack chord with a slow swell.

    Cached, so `chords` is a tuple of MIDI notes. Band-limited by construction - `pad()`
    in core builds its saws with a naive modulo, which aliases badly on a
    chord voiced above MIDI 60. High-passed at 230 so it lives above the bass;
    `sweep` opens the filter across the segment, which in a breakdown does the
    work an arrangement would otherwise need four more parts for."""
    n, t = steps(max(dur_steps, 4), floor=int(0.5 * SR))
    rs = np.random.RandomState(7300 + seed * 41)
    out = np.zeros((n, 2), dtype=np.float64)
    for note in chords:
        f = midi(note)
        ph = 2 * np.pi * f * t
        for v in range(voices):
            o = (v / max(voices - 1, 1) - 0.5) * 2 if voices > 1 else 0.0
            ratio = 2.0 ** (detune * o / 1200.0)
            y = saw_ph(ph * ratio + rs.rand() * 6.283, f * ratio, kmax=kmax)
            ang = (np.clip(o * 0.85 * wide, -1, 1) + 1) * np.pi / 4
            out[:, 0] += y * np.cos(ang)
            out[:, 1] += y * np.sin(ang)
    out /= max(len(chords) * voices, 1) ** 0.8
    y = out.astype(np.float32)
    if sweep:
        env = np.linspace(0.0, 1.0, n) ** 0.7
        y = morph_lp(y, cutoff * 0.20, cutoff * (1 + sweep), env, bands=7, res=0.6)
    else:
        y = lp(y, cutoff, 4)
    y = hp(y, hpf, order=2)
    if sub:
        y = y + lp(stereo(np.sin(2 * np.pi * midi(min(chords) - 12) * t)), 200) * sub
    a = min(int(attack * SR), n // 2)
    r = min(int(release * SR), n // 2)
    env = np.ones(n, dtype=np.float32)
    env[:a] = np.linspace(0, 1, a) ** 1.6
    env[-r:] *= np.linspace(1, 0, r) ** 1.2
    return (y * env[:, None]).astype(np.float32) * gain * 0.42


def tgate(seg, rate_steps=1.0, duty=0.52, depth=1.0, soft=0.005, shift=0.0):
    """The trance gate: chop a held sound into the grid. A sustained pad
    through this is a rhythm part with no new instrument in the arrangement,
    which is the cheapest density there is."""
    n = len(seg)
    period = max(int(rate_steps * STEP), 8)
    on = int(period * duty)
    env = np.zeros(n)
    k = max(int(soft * SR), 2)
    for a in range(int(shift * STEP), n, period):
        a = max(a, 0)
        b = min(a + on, n)
        if b <= a:
            continue
        env[a:b] = 1.0
        if b - a > 2 * k:
            env[a:a + k] = np.linspace(0, 1, k)
            env[b - k:b] = np.linspace(1, 0, k)
    return (seg * (1 - depth * (1 - env))[:, None]).astype(np.float32)


# ================================================================== the fx ===
def uplift(dur_steps=16, gain=1.0, f0=240.0, f1=9000.0, q=6.0, tone=520.0,
           tone1=2600.0, curve=2.0, noise=1.0, seed=0, swell=2.2, width=1.0):
    """The riser. A resonant band whose centre climbs exponentially, plus a
    tone rising underneath it.

    `core.riser` crossfades three fixed filters, which gives a whoosh - the
    energy never sits anywhere in particular. Here `q` is the whole point:
    the band is narrow enough to be heard as a pitch, so the sweep reads as
    something being wound up rather than as noise getting brighter, and the
    ear tracks it all the way to the drop."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(8200 + seed * 43)
    u = (t / t[-1]) ** curve
    nz = np.stack([rs.randn(n), rs.randn(n)], 1).astype(np.float32)
    # svf takes a per-sample cutoff, so the sweep is continuous rather than a
    # crossfade between static bands.
    band = svf(nz, f0 * (f1 / f0) ** u, q=q, kind='bp') * noise
    ph = 2 * np.pi * np.cumsum(tone * (tone1 / tone) ** u) / SR
    tn = stereo(np.sin(ph) + 0.35 * np.sin(2 * ph)) * 0.30
    y = band * 1.3 + tn * (u[:, None] ** 0.6)
    y = widen(y, 0.9 * width) if width else y
    return (y * (u ** swell)[:, None]).astype(np.float32) * gain * 0.50


def downlift(dur_steps=8, gain=1.0, f0=9000.0, f1=180.0, q=4.0, seed=0):
    """The release: the riser run backwards, spent across the first bar of the
    new section."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(8900 + seed * 17)
    u = (t / t[-1]) ** 0.55
    nz = np.stack([rs.randn(n), rs.randn(n)], 1).astype(np.float32)
    band = svf(nz, f0 * (f1 / f0) ** u, q=q, kind='bp')
    return (widen(band, 1.2) * np.exp(-t / 0.85)[:, None]).astype(np.float32) * gain * 0.55


def boom(dur_steps=16, gain=1.0, f0=105.0, f1=32.0, tau=0.28, decay=1.9,
         noise=0.55, seed=0):
    """The impact on the downbeat of a drop: a sine falling into the sub with
    a broadband blast over it. The blast darkens as it decays, which is what
    makes it read as a room being hit rather than as a noise burst."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(9400 + seed * 11)
    f = f1 + (f0 - f1) * np.exp(-t / tau)
    low = np.tanh(1.7 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t / decay)
    nz = np.stack([rs.randn(n), rs.randn(n)], 1).astype(np.float32)
    m = np.exp(-t / 0.35)[:, None]
    blast = (hp(nz, 1800) * m + lp(nz, 800) * (1 - m)) * np.exp(-t / 0.9)[:, None]
    return ((stereo(low) + noise * blast) * adsr(n, a=0.0015, r=0.3)[:, None]
            ).astype(np.float32) * gain * 0.85


def subdive(dur_steps=8, gain=1.0, f0=88.0, f1=26.0, decay=0.9, drive=1.6, seed=0):
    """The sub-drop that marks the half-bar before a drop. Mono, and nothing
    above 160 Hz, so it is felt and not heard."""
    n, t = steps(dur_steps)
    u = (t / t[-1]) ** 0.85
    f = f0 * (f1 / f0) ** u
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / decay)
    return lp(stereo(np.tanh(drive * x) / np.tanh(drive)), 160, 4
              ).astype(np.float32) * gain * 0.8


def tcrash(dur_steps=16, gain=1.0, tone=1.0, decay=1.25, seed=0):
    """A bright wash for the top of a drop, off the same metal the hats are."""
    n, t = steps(max(dur_steps, 6), floor=int(0.9 * SR))
    rs = np.random.RandomState(9900 + seed * 7)
    x = sum(np.sign(np.sin(2 * np.pi * 620 * r * tone * t + rs.rand() * 6.283))
            for r in _HR) / 6
    x = x + 1.5 * rs.standard_normal(n)
    st = hp(stereo(np.tanh(1.15 * x / 2.5)), 3600 * tone, order=4)
    env = np.exp(-t / decay) * adsr(n, a=0.0012, r=0.18)
    return (widen(st, 1.3) * env[:, None]).astype(np.float32) * gain * 0.46
