"""Drill'n'bass: the edit is the instrument.

Every other module in this repo builds a sound and then plays it. This one
does the opposite. The sound already exists - six seconds of Gregory Coleman
playing a drum kit in 1969 - and the composition is what you do to it with a
knife. That is not a metaphor for the genre, it is literally how the records
were made: a tracker, a four-bar sample, and a per-row parameter column.

So the unit here is not a note. It is an EDIT, and it has four dimensions:

    which slice      the break's own kick, snare, ghost or hat
    what happens     pitch, reverse, stretch, crush, filter, gate
    how many         one hit, or the same hit fired 3, 5, 7 times inside it
    at what rate     even, accelerating, decelerating, or unevenly

`edit()` takes those as a sixteen-character tablature plus a dict of
parameter locks, in the Elektron sense: the pattern says WHAT plays and the
locks say what is different about this particular step. A drill'n'bass bar is
mostly an ordinary bar with three steps that have been interfered with, and
writing it that way keeps the groove legible - which is the whole difficulty
of the style. Chop everything and the result is noise with a tempo.

The one rule the chaos is built on: **the low end never joins in.** The
sub is one continuous oscillator, `thump` lands on beats 1 and 3 and `crack`
on 2 and 4 in almost every bar, and the sliced break rides on top of that
with its bottom filtered off at 150 Hz. The break can fall apart completely
for two beats and the body still knows where the pulse is, because the pulse
was never in the break. Take that scaffolding away and the edits stop being
syncopation and become an error.

    from idmlib import *
    s = Session(32, tail=3.0)
    edit(s, 0, "K.gS.h.G k.KhS.hH")                    # a plain bar
    edit(s, 1, "K.gS.h.G k.KhS.hH",
         locks={12: dict(rat=6, curve='accel', p1=1.6),   # a ratchet
                14: dict(rev_=True, pitch=0.5)})         # and a reversal
    s.place(s.pos(0), subbar(((0, 31), (10, 34)), 16), 0.9, 'sub')
"""
import os
import numpy as np
import core
from core import *
from core import _ftrack, _amp
from sampler import Sample, prepare
from scipy.ndimage import uniform_filter1d

BAR, STEP = core.set_grid(bpm=174.0)
BPM = core.BPM

# The break is the loudest thing on the record and it is allowed to duck as
# hard as everything else; what does not duck is `drums`, because the whole
# point is that the kit stays where it is while the harmony breathes.
Session.DUCKED = {'sub': 1.0, 'bass': 0.85, 'music': 0.55, 'keys': 0.5,
                  'pad': 0.6, 'atmos': 0.35, 'lead': 0.4}

SRC_MP3 = os.path.join(SAMPLES, 'axel_bfdi2025-amen-break-140-bpm-333318.mp3')
BREAK_WAV = os.path.join(SAMPLES, 'amen_174.wav')
prepare(SRC_MP3, BREAK_WAV, trim=0.03118, length=6.85714, speed=174 / 140)

amen = Sample(BREAK_WAV, bars=4, name='amen').fit()


# ================================================================ the slices
# Measured, not guessed - `Sample.analyze()` labels every sixteenth of the
# four bars by energy, spectral centroid and low-band share:
#
#   bars 0,1   K . K h S h h h  h h K K S . h h
#   bar  2     K . K h S h h h  h h K K K . S h
#   bar  3     h h K . S h h h  h h C S h h S h        (C = the loud one)
#
# The names below are those positions. Everything a bar is built from comes
# from here, so a "kick" in this module is a kick recorded in a room with a
# ride cymbal ringing over it - which is exactly why chopped breaks sound
# like a performance and layered one-shots sound like a drum machine.
def sl(bar, step, n=1.0, fade=2.0):
    return amen.get(bar, step, n, fade)


K   = sl(0, 0, 2)          # the downbeat kick, with the ride over it
K2  = sl(0, 2, 2)          # the second kick - lower, rounder
KL  = sl(0, 10, 1)         # the late kick pair, tight
KL2 = sl(0, 11, 1)
S   = sl(0, 4, 2)          # the backbeat snare, with its tail
S1  = sl(0, 4, 1)          # the same snare cut short - for rolls
S2  = sl(0, 12, 2)         # the second snare, slightly darker
S3  = sl(3, 11, 1)         # the dry snare from the shifted bar
S4  = sl(3, 14, 2)
G   = sl(0, 1, 1)          # ghost
G2  = sl(3, 3, 1)
H   = sl(0, 5, 1)          # hats - the quiet half of the break
H2  = sl(0, 7, 1)
H3  = sl(0, 9, 1)
H4  = sl(3, 0, 1)
C   = sl(3, 10, 2)         # the crash accent
BAR3 = amen.bar(3)         # the shifted bar, whole

# tablature character -> slice
CHARS = {'K': K, 'k': K2, 'q': KL, 'Q': KL2,
         'S': S, 's': S1, 'D': S2, 'd': S3, 'X': S4,
         'G': G, 'g': G2, 'h': H, 'i': H2, 'j': H3, 'H': H4,
         'C': C}

# The same map as data, so the break can be cut again at another tempo:
# character -> (bar, step, length) and character -> the global it is bound to.
CUTS = {'K': (0, 0, 2), 'k': (0, 2, 2), 'q': (0, 10, 1), 'Q': (0, 11, 1),
        'S': (0, 4, 2), 's': (0, 4, 1), 'D': (0, 12, 2), 'd': (3, 11, 1),
        'X': (3, 14, 2), 'G': (0, 1, 1), 'g': (3, 3, 1), 'h': (0, 5, 1),
        'i': (0, 7, 1), 'j': (0, 9, 1), 'H': (3, 0, 1), 'C': (3, 10, 2)}
NAMED = {'K': 'K', 'k': 'K2', 'q': 'KL', 'Q': 'KL2', 'S': 'S', 's': 'S1',
         'D': 'S2', 'd': 'S3', 'X': 'S4', 'G': 'G', 'g': 'G2', 'h': 'H',
         'i': 'H2', 'j': 'H3', 'H': 'H4', 'C': 'C'}


def set_tempo(bpm, beats=4):
    """Move the grid and re-cut the break onto it.

    The slices are audio, not note events. They were resampled onto the bar
    this module set when it was imported, so moving the tempo afterwards
    without re-cutting leaves every chop playing at the old speed against a
    grid that has changed underneath it.

    Re-fitting is also the correct move musically. `Sample.fit()` is a deck,
    not a time-stretcher: pitch travels with the speed, which is the whole
    reason a 1969 funk record played at 166 sounds like jungle and the same
    record time-stretched to 166 does not. 174 is drill'n'bass; 160-170 is
    where the break came from.
    """
    global BAR, STEP, BPM, amen, BAR3
    BAR, STEP = core.set_grid(bpm=bpm, beats=beats)
    BPM = core.BPM
    core._SEG_CACHE.clear()          # every cached voice was the old bar long
    amen = Sample(BREAK_WAV, bars=4, name='amen').fit()
    for ch, cut in CUTS.items():
        seg = sl(*cut)
        CHARS[ch] = seg
        globals()[NAMED[ch]] = seg
    BAR3 = amen.bar(3)
    return BAR, STEP


# ============================================================ the knife
def shape(seg, pitch=1.0, str_=1.0, rev_=False, crush=0, down=4, cut=None,
          kind='lp', q=1.0, drive=0.0, hold=1.0, pan=0.0, hpf=0.0, gain=1.0,
          fade=1.6):
    """One slice, interfered with. The order is deliberate: retime first, so
    a filter set in Hz still means the same thing afterwards; gate last, so
    the shortening cuts the finished sound rather than something the drive
    then rings back out of."""
    y = np.asarray(seg, dtype=np.float32)
    if str_ != 1.0:
        y = stretch(y, str_, grain=0.055, jitter=0.4)
    if pitch != 1.0:
        y = pitched(y, 1.0 / pitch) if pitch < 0 else pitched(y, pitch)
    if rev_:
        y = y[::-1]
    if crush:
        y = bitcrush(y, crush, down)
    if hpf:
        y = hp(y, hpf, 2)
    if cut is not None:
        y = svf(y, cut, q, kind, block=64)
    if drive:
        y = np.tanh(drive * y) / np.tanh(drive)
    if hold < 1.0:
        n = max(int(len(y) * hold), 96)
        y = y[:n]
    if pan:
        y = panned(y, pan)
    return fade_edges(y, fade) * gain


def _times(n, total, curve='even', drift=0.0, seed=0):
    """Where the repeats of a ratchet land inside `total` samples.

    A ratchet at an even rate is a drum roll and the ear files it as one
    event. The interest is in the rate CHANGING inside the group: six hits
    that accelerate read as a stumble, six that decelerate read as a machine
    losing power, and the same six unevenly spaced read as a person."""
    u = np.arange(n, dtype=np.float64) / n
    if curve == 'accel':
        pos = u ** 1.85
    elif curve == 'decel':
        pos = 1 - (1 - u) ** 1.85
    elif curve == 'swing':
        pos = u + 0.5 / n * (np.arange(n) % 2)
    elif curve == 'gallop':                      # long-short-short
        pos = np.cumsum(np.array([1.6 if i % 3 == 0 else 0.7 for i in range(n)]))
        pos = np.concatenate([[0.0], pos[:-1]]) / pos[-1]
    else:
        pos = u
    if drift:
        rs = np.random.RandomState(seed)
        pos = np.clip(pos + rs.uniform(-drift, drift, n) / n, 0, 0.98)
        pos = np.sort(pos)
    return (pos * total).astype(int)


def ratchet(seg, n=4, dur=2.0, curve='even', p0=1.0, p1=1.0, semis=None,
            g0=1.0, g1=0.8, hold=0.9, rev_last=False, drift=0.0, tail=1.0,
            fly=0.55, seed=0, **kw):
    """The same hit fired `n` times inside `dur` steps: the trill, the
    stutter, the "treschalka".

    Three things stop it from being a machine gun, and all three are on by
    default. The pitch moves across the group (`p0` -> `p1`, or a list of
    semitones), the level falls, and each repeat is cut to `hold` of the gap
    it has - so the hits get shorter as they get closer and the group has a
    shape rather than a length. The last one is allowed to ring: `tail`
    scales how far past its slot it plays, which is what makes a ratchet land
    on the next downbeat instead of stopping before it.

    `fly` walks the repeats across the stereo field. The break is a mono
    recording, so every bit of width on it has to be put there deliberately -
    and a trill that travels is the difference between a stutter and a machine
    fault. The first and last hits stay near the centre so the group still
    starts and ends where the beat is.
    """
    total = int(dur * STEP)
    ts = _times(n, total, curve, drift, seed)
    out = np.zeros((total + int(2.5 * STEP), 2), dtype=np.float32)
    rs = np.random.RandomState(seed + 7)
    for i in range(n):
        f = i / max(n - 1, 1)
        p = (p0 * (p1 / p0) ** f) if semis is None else 2 ** (semis[i % len(semis)] / 12.0)
        g = g0 + (g1 - g0) * f
        room = (ts[i + 1] - ts[i]) if i < n - 1 else total - ts[i]
        room = max(room, 64)
        last = (i == n - 1)
        kk = dict(kw)
        if fly and 'pan' not in kk:
            kk['pan'] = fly * np.sin(np.pi * f) * (1 if i % 2 else -1)
        y = shape(seg, pitch=p, rev_=(rev_last and last), gain=g, **kk)
        keep = int(room * hold) if not last else int(room * tail * 2.2)
        y = fade_edges(y[:max(keep, 96)], 1.2)
        a = ts[i]
        e = min(a + len(y), len(out))
        out[a:e] += y[:e - a] * (0.94 + 0.12 * rs.rand())
    return out


def stut(seg, n=4, dur=2.0, **kw):
    """A ratchet on a piece of a bar rather than on one hit - the buffer
    repeat. `seg` is whatever was playing; this jams on the first slice of
    it and lets it get shorter."""
    return ratchet(seg, n, dur, **kw)


def glitch(seg, n=6, dur=1.0, seed=0, crush=5, down=6):
    """A digital error rather than a musical repeat: the same fragment
    restarted at a length that is not a division of anything, crushed, with
    the pitch stepping in whole tones. Two of these per record."""
    rs = np.random.RandomState(seed)
    total = int(dur * STEP)
    out = np.zeros((total + int(STEP), 2), dtype=np.float32)
    pos = 0
    for i in range(n):
        L = int(total / n * rs.uniform(0.5, 1.5))
        y = shape(seg, pitch=2 ** (rs.choice([-12, -5, 0, 0, 2, 7, 12]) / 12.0),
                  crush=crush, down=down, gain=0.9 - 0.05 * i)
        y = fade_edges(y[:max(L, 128)], 0.8)
        e = min(pos + len(y), len(out))
        out[pos:e] += y[:e - pos]
        pos += L
        if pos >= total:
            break
    return out


def roll(s, b, st, count, spacing=0.5, seg=None, bus='drums', gain=0.8,
         accel=False, p0=1.0, p1=1.0, seed=0):
    """A snare roll placed straight into the session - the build's engine.
    `accel` halves the spacing across the roll instead of keeping it."""
    seg = S1 if seg is None else seg
    pos = 0.0
    for i in range(count):
        f = i / max(count - 1, 1)
        sp = spacing * (1 - 0.55 * f) if accel else spacing
        s.place(s.pos(b, st + pos),
                shape(seg, pitch=p0 * (p1 / p0) ** f, hpf=140,
                      pan=0.25 * np.sin(i * 1.7)),
                gain * (0.55 + 0.45 * f), bus)
        pos += sp


# ============================================================ the tablature
def edit(s, b, tab, locks=None, gain=1.0, bus='drums', hpf=150.0, swing=0.0,
         seed=0, humanise=0.0035, ghost=1.0, width=1.0):
    """One bar of chopped break.

    `tab` is sixteen characters, one per sixteenth, from CHARS - plus '.' for
    a rest and '-' to let whatever is ringing carry on. Spaces are ignored,
    so a bar can be written in beats.

    `locks` is {step: {...}}: anything `shape()` takes, plus `rat` (fire this
    step as a ratchet of that many hits), `dur` (how long the ratchet has,
    in steps - default is the gap to the next event), `curve`, `semis`, and
    `gain`. A step with no lock is played straight.

    The break arrives high-passed at 150 Hz. Its own kick has plenty of low
    end and none of it is in tune with anything; the weight on this record
    comes from `thump` and the sub, and letting both play in that band is how
    a chopped break turns to mud.
    """
    locks = locks or {}
    rs = np.random.RandomState(seed * 131 + b)
    events = [(i, c) for i, c in enumerate(tab.replace(' ', '')) if c in CHARS]
    for k, (i, c) in enumerate(events):
        nxt = events[k + 1][0] if k + 1 < len(events) else 16
        L = locks.get(i, {})
        kw = {x: v for x, v in L.items()
              if x not in ('rat', 'dur', 'curve', 'semis', 'g1', 'gain', 'p0',
                           'p1', 'hold', 'tail', 'drift', 'rev_last', 'fly')}
        kw.setdefault('hpf', hpf)
        # The sample is mono, so width is a decision rather than a property.
        # Kicks and the backbeat stay centred - they are the pulse, and the
        # pulse belongs in the middle on any system. Ghosts, hats and the late
        # kick pair are spread, alternating side by side, which is where the
        # 110-140% of side energy above 3 kHz on a modern break comes from.
        if 'pan' not in kw and c not in 'KkSD':
            kw['pan'] = width * (0.62 if c in 'ghijH' else 0.34) * \
                (1 if i % 2 else -1) * (1 - 0.45 * (i % 4 == 0))
        g = gain * L.get('gain', 1.0) * (ghost if c in 'gGhijH' else 1.0)
        off = swing * (i % 2) + rs.uniform(-humanise, humanise) * 16
        t = s.pos(b, i + off)
        if 'rat' in L:
            seg = ratchet(CHARS[c], L['rat'], L.get('dur', max(nxt - i, 1)),
                          curve=L.get('curve', 'even'), p0=L.get('p0', 1.0),
                          p1=L.get('p1', 1.0), semis=L.get('semis'),
                          g0=1.0, g1=L.get('g1', 0.8), hold=L.get('hold', 0.9),
                          rev_last=L.get('rev_last', False),
                          drift=L.get('drift', 0.0), tail=L.get('tail', 1.0),
                          fly=L.get('fly', 0.55 * width),
                          seed=seed + i, **{x: v for x, v in kw.items()
                                            if x != 'pan'})
            s.place(t, seg, g, bus)
        else:
            s.place(t, shape(CHARS[c], **kw), g, bus)


def poly(period, n=16, offset=0):
    """Steps of a cycle that does not divide the bar. A seven-step figure
    over sixteen lands somewhere new every bar and comes home after seven -
    the cheapest way to make a fixed loop stop repeating."""
    return [(offset + i * period) % n for i in range(int(np.ceil(n / period)))]


# ============================================================ the scaffolding
def thump(dur_steps=3.0, tune=48.0, gain=1.0, click=0.5, decay=0.145, drive=1.6):
    """The kick UNDER the break. Not a drum machine kick - a body.

    Everything above 200 Hz is already in the sample, in a room, with a
    cymbal ringing over it. What the break has not got is a fundamental that
    stays in one place: its own kick wanders between 55 and 80 Hz and is
    tuned to nothing. So this is almost all sine, a fast dive, one click for
    the transient to line up against, and a low-pass that keeps it out of the
    break's way entirely."""
    n, t = steps(dur_steps)
    f = tune * (1 + 2.6 * np.exp(-t / 0.016))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / decay)
    x = np.tanh(drive * x) / np.tanh(drive)
    out = lp(stereo(x), 190, 4)
    if click:
        ck = np.random.RandomState(int(tune * 7)).randn(n) * np.exp(-t / 0.0016)
        out = out + hp(stereo(ck), 1200) * 0.30 * click
    return (out * adsr(n, a=0.0008, r=0.02)[:, None]).astype(np.float32) * gain


def crack(dur_steps=3.0, gain=1.0, tune=196.0, bright=1.0, body=1.0, room=0.35,
          bottom=0.55, seed=0):
    """The snare layer. The break's snare has the character; this has the
    crack, in the 1.5-4 kHz band a laptop can reproduce, plus a short room so
    the two read as one instrument recorded in one place.

    `bottom` is the part that is not about the snare at all. The felt pulse of
    a track is where its LOW end lands: measure the energy under 160 Hz per
    sixteenth and a record whose bass only moves on beats 1 and 3 reads as
    half its tempo, however busy the top is. A short 95 Hz thud under the
    backbeat puts weight on 2 and 4 without putting a second kick there.
    """
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed)
    tone = (np.sin(2 * np.pi * tune * t) + 0.6 * np.sin(2 * np.pi * tune * 1.58 * t))
    tone *= np.exp(-t / 0.055) * body
    if bottom:
        low = np.sin(2 * np.pi * 95.0 * t * (1 + 0.5 * np.exp(-t / 0.010)))
        tone = tone + bottom * low * np.exp(-t / 0.052)
    nz = np.stack([rs.randn(n), rs.randn(n)], 1)
    hi = bandpass(nz, 1500, 8200, 2) * np.exp(-t / 0.085)[:, None] * bright
    mid = bandpass(nz, 320, 1400, 2) * np.exp(-t / 0.045)[:, None] * 0.5
    y = stereo(tone) * 0.55 + hi * 0.55 + mid * 0.35
    y = np.tanh(1.8 * y)
    if room:
        y = y + reverb(y, decay=0.42, wet=room, tone=5200, predelay=0.004)[:n] * 0.55
    return (hp(y, 62, 2) * adsr(n, a=0.0006, r=0.03)[:, None]).astype(np.float32) * gain


def tick(dur_steps=0.7, gain=1.0, f=2100.0, seed=0):
    """A single dry click, for the sixteenths the break does not cover."""
    n, t = steps(dur_steps, floor=256)
    rs = np.random.RandomState(seed)
    y = bandpass(np.stack([rs.randn(n), rs.randn(n)], 1), f, f * 3.4, 2)
    return (y * np.exp(-t / 0.006)[:, None]).astype(np.float32) * gain * 0.9


# ============================================================ the liquid half
def wood(notes, dur_steps=16, gain=1.0, cut=(320.0, 1500.0), q=2.2, glide=0.020,
         decay=0.30, drive=1.5, sub=0.55, tone=0.6, seed=0):
    """The mid bass, warm rather than mechanical - and rendered as ONE
    oscillator per phrase.

    A liquid bass is a plucked wooden thing: a triangle-ish core with just
    enough saw in it to be heard on a laptop, a filter that closes fast on
    each attack, and no motion of its own. `machinelib.bassbar` is the other
    end of the same idea and is far too aggressive here - the whole contrast
    of this record is a violent kit over a bass that refuses to be violent.

    `notes` are (step, midi) events; the frequency track is continuous across
    them, so a note change is a glide in one running oscillator rather than a
    new segment butted against the old one's tail.
    """
    n = int(dur_steps * STEP)
    f = _ftrack(notes, n, glide)
    ph = 2 * np.pi * np.cumsum(f) / SR
    amp = _amp(notes, n, decay=decay, attack=0.004)
    core_ = (np.sin(ph) * (1 - tone)
             + tone * (0.6 * saw_ph(ph, 5200.0, kmax=40) + 0.4 * np.sin(2 * ph)))
    x = core_ * amp
    lane = cut[0] + (cut[1] - cut[0]) * amp ** 1.7           # filter follows the hit
    y = svf(stereo(x.astype(np.float32)), lane, q, 'lp', block=64)
    y = np.tanh(drive * y) / np.tanh(drive)
    y = hp(y, 60, 2)
    if sub:
        low = np.sin(ph) * amp
        y = y + lp(stereo(low.astype(np.float32)), 130, 4) * sub
    return (y * adsr(n, a=0.004, r=0.008)[:, None]).astype(np.float32) * gain * 0.8


def glass(freq, dur_steps=4, gain=1.0, ratio=3.46, idx=2.2, decay=0.55,
          damp=2600.0, seed=0, spread=0.0):
    """A struck glass object: FM at a deliberately non-integer ratio, with the
    index decaying five times faster than the amplitude. The strike is
    inharmonic and the ring is nearly a sine, which is what a struck object
    does and what a fixed-spectrum bell cannot.

    `damp` is not a tone control, it is what keeps this out of music-box
    territory. Bright inharmonic partials plus an instant attack plus a long
    ring is the acoustic signature of a small hard toy, and a dark record with
    one of those in it sounds cheerful whatever notes it is playing. Above
    about 2.8 kHz the ear stops hearing a struck thing and starts hearing a
    glockenspiel, so the default cuts there and the register belongs an octave
    lower than instinct puts it.

    The width is two slightly different modulator ratios, not a delay: a
    Haas-shifted copy measures wider and disappears the moment anything sums
    to mono.
    """
    n, t = steps(dur_steps)
    w = 2 * np.pi * freq * t
    ie = idx * np.exp(-t / (decay * 0.18))
    chans = []
    for r in (ratio, ratio * 1.004):
        x = np.sin(w + ie * np.sin(r * w)) * np.exp(-t / decay)
        x += 0.35 * np.sin(2 * w + 0.5 * ie * np.sin(r * 1.7 * w)) * np.exp(-t / (decay * 0.45))
        chans.append(np.tanh(1.1 * x))
    out = np.stack(chans, 1).astype(np.float32)
    if damp:
        out = lp(out, damp, 2)
    if spread:
        out = panned(out, spread)
    return (out * adsr(n, a=0.002, r=0.04)[:, None]) * gain


def felt(notes, dur_steps=8, gain=1.0, vel=0.6, roll=0.045, damp=1.0,
         hammer=0.55, B=0.0006, pick=0.13, K=32, spread=0.5, seed=0,
         detune=2.5, room=0.30):
    """A felt piano: hammers hitting strings through a strip of cloth.

    Written because a chord played by an FM electric piano - or by any voice
    that renders every note of it at the same instant with the same spectrum -
    reads as somebody pressing a key on a synthesiser rather than as an
    instrument in a room. Four things fix that, and none of them is EQ:

    **The chord is not simultaneous.** `roll` scatters the notes over 20-90 ms
    in pitch order, the way a hand does. That single change is most of the
    difference between "a chord" and "a chord being played".

    **The partials are not harmonic.** A real string is stiff, so mode k sits
    at `k*f0*sqrt(1 + B*k^2)` - by the twentieth partial that is tens of cents
    sharp, and it is what stops an additive stack from sounding like an organ.
    The excitation follows `sin(k*pi*pick)/k^2`: hitting a string an eighth of
    the way along is why a piano has no strong eighth harmonic.

    **The top dies first.** Each mode has its own decay, `tau/(1 + damp*k^1.6)`,
    and a second polarisation at 0.6 cents and 55% of the decay beats against
    the first. A tone whose spectrum is fixed while it fades is a sample being
    faded out.

    **The mechanism is audible.** Felt makes the attack soft and the hammer
    thud loud: a filtered noise burst around 300-1400 Hz that has nothing to
    do with the pitch. Take it away and the instrument stops being a physical
    object.
    """
    n, t = steps(dur_steps, floor=int(0.25 * SR))
    rs = np.random.RandomState(seed)
    out = np.zeros((n, 2), dtype=np.float64)
    v = float(np.clip(vel, 0.05, 1.3))
    order = sorted(notes)
    for i, f in enumerate(order):
        note = 69 + 12 * np.log2(max(f, 1e-6) / 440.0)
        lag = int((i * roll + rs.uniform(0, roll * 0.5)) * SR)
        m = n - lag
        if m < 256:
            continue
        tt = t[:m]
        # longer strings are less stiff and ring longer; both scale with pitch
        stiff = B * 2 ** ((note - 60) / 18.0)
        tau0 = 1.7 * 2 ** (-(note - 60) / 20.0)
        y = np.zeros(m)
        for k in range(1, K + 1):
            fk = k * f * np.sqrt(1 + stiff * k * k)
            if fk > 15000:
                break
            # velocity opens the spectrum: a soft hammer through felt excites
            # almost nothing above the sixth mode, a hard one reaches the
            # twentieth. This is the whole of what a velocity layer is.
            amp = abs(np.sin(k * np.pi * pick)) / k ** 1.05
            amp *= np.exp(-(k - 1) * (0.40 - 0.30 * v) / 2.2)
            tk = tau0 / (1 + damp * k ** 1.35)
            ph = rs.rand() * 6.28
            y += amp * np.sin(2 * np.pi * fk * tt + ph) * np.exp(-tt / tk)
            # the second polarisation: same mode, a hair flat, dying faster
            y += 0.5 * amp * np.sin(2 * np.pi * fk * (1 - detune / 1200.0) * tt
                                    + ph + 1.1) * np.exp(-tt / (tk * 0.55))
            # the prompt sound: the first tenth of a second of a struck string
            # is several dB louder than the tail, and a single exponential
            # cannot make a hit - it makes a fade-in that starts loud.
            y += 0.55 * amp * np.sin(2 * np.pi * fk * tt + ph + 2.2) * \
                np.exp(-tt / (tk * 0.14))
        if hammer:
            # the thud of the mechanism: felt on wire, plus the key bed
            nz = rs.randn(m) * np.exp(-tt / 0.011)
            y = y + hammer * 0.34 * bandpass(stereo(nz), 300, 2600, 2)[:, 0] * (0.4 + v)
            kb = rs.randn(m) * np.exp(-tt / 0.030)
            y = y + hammer * 0.10 * bandpass(stereo(kb), 90, 400, 2)[:, 0] * v
        # felt: the attack is soft, so no edge for the ear to call a click
        y *= np.minimum(1.0, tt / 0.009)
        p = np.clip((note - 62) / 26.0, -1, 1) * spread
        ang = (p + 1) * np.pi / 4
        out[lag:, 0] += y * np.cos(ang) * 1.41
        out[lag:, 1] += y * np.sin(ang) * 1.41
    out = np.tanh(1.25 * out / max(len(order), 1) ** 0.55)
    y = lp(out.astype(np.float32), 4600 + 4200 * v, 2)
    if room:
        # The box the strings are in. A piano is never dry, and a dry one is
        # the second half of what "synthetic" means.
        y = y + reverb(y, decay=0.9, wet=room, tone=3600, predelay=0.008)[:n] * 0.6
    return (hp(y, 80, 2) * adsr(n, a=0.001, r=0.06)[:, None]) * gain * 0.5


def scatter(notes, dur_steps=8, spread_steps=3.0, gain=1.0, vel=0.55, seed=0,
            order='up', **kw):
    """The same chord, played as separate events across `spread_steps` instead
    of as one. Returns [(step_offset, segment)] - a chord that arrives over
    half a beat is a part; a chord that arrives all at once is a keypress."""
    rs = np.random.RandomState(seed)
    ns = list(notes)
    if order == 'down':
        ns = ns[::-1]
    elif order == 'random':
        rs.shuffle(ns)
    out = []
    for i, f in enumerate(ns):
        st = i * spread_steps / max(len(ns), 1) + rs.uniform(-0.05, 0.05)
        d = dur_steps - st
        out.append((max(st, 0.0), felt([f], d, gain=gain,
                                       vel=vel * (0.8 + 0.4 * rs.rand()),
                                       seed=seed + i, roll=0.0, **kw)))
    return out


def hush(dur_steps=16, gain=1.0, seed=0, lo=600.0, hi=5200.0):
    """Room tone and tape. Between the edits this record has real holes in
    it, and a hole with nothing in it sounds like the file stopped."""
    n, t = steps(dur_steps, floor=1024)
    rs = np.random.RandomState(seed)
    y = bandpass(np.stack([rs.randn(n), rs.randn(n)], 1), lo, hi, 2)
    env = 1 + 0.5 * np.sin(2 * np.pi * 0.08 * t + rs.rand() * 6.28)
    return (y * env[:, None] * gain * 0.055).astype(np.float32)
