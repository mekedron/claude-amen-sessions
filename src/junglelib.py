"""Jungle: a reggae record at 166 with a funk break running over the top.

The distinction this module exists to hold is the one the genre is named
for. Drum & bass is a drum sound; **jungle is a bass culture**. Both use the
Amen, both sit near 170, and everything else about them is different:

|                | jungle 1993-95            | drum & bass 1996-     |
|----------------|---------------------------|-----------------------|
| tempo          | 160-170                   | 172-176               |
| the break      | *played*, then cut        | programmed two-step   |
| the bass       | a reggae **tune**         | one note, modulated   |
| harmony        | minor stabs, dark strings | usually none          |
| where it's from| Kingston via Hackney      | a studio              |

So the writing rule here is inverted from `machinelib` and `neurolib`: the
bass is not a gesture, it is a **line**, with rests in it, sliding into its
notes and leaving beat one alone the way a reggae bassline does. What moves
is the break; what carries the record is a melody at 45-90 Hz.

Everything that cuts the break comes from `idmlib` - the tablature, the
parameter locks, the ratchets, `thump` and `crack`. That module is the same
knife pointed at a different genre, and re-pointing it costs one call:
`idmlib.set_tempo(166)` re-fits the sample so its pitch travels with the
speed, which is the whole reason a 1969 funk record sounds like this here.

What lives in this file is only what jungle is made of and the engine had
not got:

    dubplate()   the Akai S950 - 12 bits, a low converter, a band limit
    deck()       a second turntable: the same break at another speed
    smear()      the 1994 time-stretch, artefacts left in on purpose
    contrabass() a double bass, pizzicato: stiff string, wooden box, finger
    organbass()  the same line on a drawbar organ, for a phone
    skank()      the offbeat organ chop
    stab()       the minor chord hit, dry and short

`core.subbar` is still the right sub for a synth bass line, and `core.ens` is
the strings unchanged - a darkside string patch is a section with its filter
shut, and `ens` is the one voice in the engine whose players disagree with
each other. But a bass line that is meant to be *played* is `contrabass`, and
it carries its own bottom: it is split at 130 Hz and sent to two buses rather
than doubled by a separate sine, because two oscillators at one pitch with
unrelated phases cancel and one oscillator cut in half cannot.

    from junglelib import *
    s = Session(64, tail=3.0)
    edit(s, 0, "K.gS.h.G k.KhS.hH", hpf=170)
    s.place(s.pos(0), thump(tune=49.0), 1.0, 'drums')
    lo, hi = split(contrabass(((0, G1), (10, Bb1)), 16, sub=0.22), 130.0)
    s.place(s.pos(0), lo, 0.9, 'sub'); s.place(s.pos(0), hi, 0.5, 'bass')
"""
import numpy as np
from scipy.ndimage import uniform_filter1d

import core
import idmlib

BPM = 166.0
idmlib.set_tempo(BPM)                 # re-cuts the break onto the new bar

from core import *                                            # noqa: E402
from core import _ftrack, _amp                                # noqa: E402
from idmlib import *                                          # noqa: E402
from idmlib import (sl, shape, edit, ratchet, stut, glitch, roll, poly,
                    thump, crack, tick, hush, amen, CHARS)     # noqa: E402

BAR, STEP = core.BAR, core.STEP

# The sub is the record. It ducks all the way against the kick under the
# break, because that is the only thing on the mix that has to get through
# it; the break itself never ducks, and the skank barely does.
Session.DUCKED = {'sub': 1.0, 'bass': 0.70, 'music': 0.30, 'pad': 0.25}


# ================================================================ the sampler
def dubplate(seg, bits=12, down=1, lo=75.0, hi=11500.0, drive=1.15,
             wow_=0.0, gain=1.0):
    """The Akai S950, which is most of why these records sound like this.

    Every jungle break went through a 12-bit sampler with a variable rate and
    a converter that stopped around 11 kHz, and it was truncated, not
    dithered. That is three separate things and they do not sound the same:
    the bit reduction adds a quantisation floor that moves with the signal
    (audible on the *decay* of a cymbal, not on the hit), the rate reduction
    folds everything above half of it back down as aliasing, and the band
    limit takes the air off the top so what is left reads as a record rather
    than as a file.

    `down` is the honest one. Leave it at 1 and this is a clean 12-bit pass;
    at 2 the converter is running near 22 kHz, which is the setting a 1994
    engineer used to fit four bars in memory and the reason the top of an old
    break is gritty in a way an EQ cannot imitate.
    """
    y = bitcrush(np.asarray(seg, dtype=np.float32), bits, down)
    y = hp(lp(y, hi, 4), lo, 2)
    if wow_:
        y = wow(y, depth_ms=wow_, rate=0.55)
    if drive and drive != 1.0:
        y = np.tanh(drive * y) / np.tanh(drive)
    return y.astype(np.float32) * gain


def deck(seg, semis=12.0, lo=800.0, hi=9500.0, steps_=None, gain=1.0,
         fade=2.0):
    """A second turntable.

    Jungle is never one break. It is the Amen for the body and something
    brighter over the top - Think, Hot Pants, Tighten Up - so the ghost notes
    of two different kits interleave and the bar fills up without anything
    being programmed. This record has one recording, so the second deck plays
    the same one faster and band-passed, which is what a second deck in 1994
    was doing anyway.

    `semis=12` is the useful default: at double speed one bar is exactly two
    copies, so the layer stays on the grid instead of tumbling over itself.
    Odd intervals are for one-shot chops, where alignment is not the point.
    """
    y = pitched(np.asarray(seg, dtype=np.float32), 2.0 ** (semis / 12.0))
    y = bandpass(y, lo, hi, 2)
    if steps_:
        n = int(steps_ * STEP)
        if len(y) < n:
            y = np.concatenate([y] * int(np.ceil(n / max(len(y), 1))))
        y = y[:n]
    return fade_edges(y, fade) * gain


def smear(seg, factor=2.0, grain=0.115, jitter=0.05, tone=6500.0, gain=1.0,
          seed=0):
    """The 1994 time-stretch, with the artefacts left in.

    `core.stretch` randomises its read position precisely so the overlapping
    grains do not comb against each other into an audible ring. An S950 did
    not have that luxury: its grains were a fixed distance apart, and the
    metallic smear that came out is not a defect of the era, it is one of the
    era's instruments - the sound of a vocal or a snare held past the length
    it was recorded at. So this asks for a long grain and almost no jitter,
    and then rolls the top off, because the ring lives above 7 kHz and one
    pass of it is a texture while four is an ice pick.
    """
    y = stretch(np.asarray(seg, dtype=np.float32), factor, grain=grain,
                jitter=jitter, seed=seed)
    return lp(y, tone, 2) * gain


# =================================================================== the bass
def figure(events, n=16, swing=0.0, swing_steps=()):
    """(step, midi, length) -> (notes, gate): a bass line written as a RHYTHM.

    The difference this exists to make is the one between a riff and an
    arpeggio. `subbar` takes note events and holds each pitch until the next,
    so a bar of four evenly spaced notes on four different degrees comes out
    as something being picked through - technically a bassline, musically a
    scale exercise. What a jungle bass actually is is one rhythmic cell,
    mostly on the root, with **holes in it**, repeated until it is a hook and
    then moved to another degree with its rhythm intact.

    The holes are the whole point, and they are not a note-off: they are a
    gate. A note this does not switch off is a drone with a pitch change in
    the middle of it.

    `swing` nudges the listed steps late by a fraction of a sixteenth. Ten
    milliseconds is not audible as timing, it is audible as feel.
    """
    ev = [(st + (swing if int(st) in swing_steps else 0.0), nt, ln)
          for st, nt, ln in events]
    notes = tuple((st, nt) for st, nt, _ in ev)
    g = [0] * n
    for st, _, ln in events:
        for k in range(int(st), min(int(st + ln), n)):
            g[k] = 1
    return notes, tuple(g)


@cached
def organbass(notes, dur_steps=16, gain=1.0, glide=0.030, decay=0.0,
              cut=2400.0, click=0.6, drive=1.7, floor=0.0, gatep=None,
              bars=(1.0, 0.28, 0.42, 0.26, 0.18, 0.11, 0.06), hpf=82.0):
    """The bassline an octave above the sub - what a small speaker hears.

    Reggae bass is deliberately dark: rolled off hard above 800 Hz, with no
    definition boost, because on a soundsystem the definition is in the air
    moving. Through a laptop that is silence, and jungle lives on laptops
    now. So the tune is played twice - `subbar` carries it at 45-90 Hz where
    the body feels it, and this carries the same notes an octave up, where a
    phone can still reproduce them and the ear puts the missing fundamental
    back underneath by itself.

    An octave up is exactly the right distance. Both layers keep their own
    fundamental, which is the thing that gets lost when a mid bass is
    high-passed above the note it is playing, and neither is in the other's
    band.

    Drawbars rather than a filtered saw: the sound being copied is a tonewheel
    organ through a bass amp, so a few sine harmonics at fixed ratios - and
    the 1.5 is the one that matters, the fifth above, which is what stops a
    harmonic stack sounding like a synth. One continuous oscillator across the
    bar, so the phase never breaks between notes, and a contact click at each
    attack for the key.
    """
    n = int(dur_steps * STEP)
    f = _ftrack(notes, n, glide)
    ph = 2 * np.pi * np.cumsum(f) / SR
    # Out to the 8th, deliberately. The point of this layer is to be audible
    # on a speaker that stops at 200 Hz, and a G2 at 98 Hz with four harmonics
    # is still entirely below 400 - which is to say still inaudible. The 6th
    # and 8th put it at 590 and 785 Hz, where a laptop lives.
    ratios = (1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0)
    x = sum(a * np.sin(r * ph) for r, a in zip(ratios, bars))
    amp = np.maximum(_amp(notes, n, decay, 0.005, floor), 0.0)
    if gatep is not None:
        amp = amp * np.clip(steplane(gatep, n, 'hold', 0.006), 0, 1)
    y = np.tanh(drive * x * amp) / np.tanh(drive)
    out = lp(stereo(y), cut, 4)
    if click:
        rs = np.random.RandomState(11)
        ck = np.zeros(n)
        for st, _ in sorted(notes):
            k = min(int(st * STEP), n - 1)
            L = min(int(0.014 * SR), n - k)
            if L > 8:
                ck[k:k + L] += rs.randn(L) * np.exp(-np.arange(L) / SR / 0.0024)
        out = out + hp(stereo(ck), 950, 2) * 0.20 * click
    out = hp(out, hpf, 2)
    return (out * adsr(n, a=0.004, r=0.010)[:, None]).astype(np.float32) * gain


@cached
def contrabass(notes, dur_steps=16, gain=1.0, glide=0.030, decay=2.4,
               damp=0.085, B=5.0e-5, pluck=0.16, kmax=36, gatep=None,
               body=1.0, finger=1.0, tilt=0.25, polar=0.68, sub=0.0,
               cut=2600.0, drive=1.25, seed=0):
    """A double bass, pizzicato: a stiff string in a wooden box.

    `organbass` puts the tune an octave up on a drawbar stack, and it is
    audible on a phone and it is unmistakably a keyboard - it has one decay
    rate, exact integer harmonics and no attack that is not a click. Three
    things separate that from a plucked string, and none of them is EQ:

    * **Stiffness.** A wound bass string resists bending, so mode k sits at
      `k*f0*sqrt(1 + B*k^2)` rather than at `k*f0`. Exact harmonicity is what
      an organ has, which is precisely the problem being fixed.
    * **One decay per mode, and two polarisations.** The string swings across
      the fingerboard and into it, at slightly different frequencies and very
      different decay rates - so a plucked note drops several dB at once and
      then rings for two seconds. A single exponential is what a synthesiser
      has.
    * **The finger and the fingerboard.** Most of what identifies a double
      bass is not the string at all: it is the pad of a finger dragging off a
      wound string, and the string slapping back onto the board. Both are
      noise, both are gone in 20 ms, and without them a modal string is a
      very good synth pad with a fast attack.

    Everything is built on ONE phase track through the whole bar, so the
    portamento between notes is a fretless slide rather than a crossfade, an
    attack re-excites a string that never stopped, and `sub` - harmonic one,
    read off the same phase - cannot fall out of phase with the instrument it
    belongs to. A separate sine sub at the same pitch can, and does.

    The body is three resonances and not a shelf: the air inside the box
    around 60 Hz, the top plate near 105, and the broad cluster the bridge
    drives from 200 to 420. A wooden box is why a note played at 49 Hz is
    heard at all through a speaker that stops at 80.
    """
    n = int(dur_steps * STEP)
    rng = np.random.default_rng(seed)
    tt = np.arange(n) / SR
    onsets = sorted({min(int(st * STEP), n - 1) for st, _ in notes})

    f = _ftrack(notes, n, glide)
    # The pluck stretches the string, so the pitch is a few cents sharp for
    # the first 40 ms and settles. Small, and the difference between a note
    # being played and a note being switched on.
    settle = np.zeros(n)
    for o in onsets:
        L = min(int(0.050 * SR), n - o)
        np.maximum(settle[o:o + L], np.exp(-np.arange(L) / SR / 0.015),
                   out=settle[o:o + L])
    ph = 2 * np.pi * np.cumsum(f * (1 + 0.0055 * settle)) / SR

    k = np.arange(1, kmax + 1, dtype=np.float64)
    fk = k * np.sqrt(1 + B * k * k)                   # stiffness-stretched
    a = np.sin(k * np.pi * pluck) / k ** 2            # where it was plucked
    a = a * k ** (1.0 + tilt)                         # a finger, not a plectrum
    tau = decay / (1 + damp * k ** 1.25)              # the top dies first
    ph0 = rng.random(kmax) * 6.283
    det = 0.0016 * (0.6 + 0.8 * rng.random(kmax))     # the second polarisation

    env = np.zeros((kmax, n))
    for i in range(kmax):
        for o in onsets:
            e = np.exp(-tt[:n - o] / tau[i])
            np.maximum(env[i, o:], e, out=env[i, o:])
    x = np.zeros(n)
    for i in range(kmax):
        x += a[i] * env[i] * np.sin(fk[i] * ph + ph0[i])
        if polar:
            x += polar * 0.6 * a[i] * env[i] ** 1.9 *                 np.sin(fk[i] * (1 + det[i]) * ph + ph0[i] + 1.3)
    x /= max(np.abs(x).max(), 1e-9)
    if sub:
        x = x + sub * env[0] * np.sin(ph)

    y = stereo(x)
    if body:
        y = y * 0.78 + body * (0.55 * bandpass(y, 52, 80, 2)
                               + 0.95 * bandpass(y, 92, 130, 2)
                               + 0.85 * bandpass(y, 200, 450, 2)
                               + 0.35 * bandpass(y, 520, 950, 2)) * 0.52
    if finger:
        nz, th = np.zeros(n), np.zeros(n)
        for o in onsets:
            L = min(int(0.032 * SR), n - o)
            nz[o:o + L] += rng.standard_normal(L) * np.exp(-np.arange(L) / SR / 0.0055)
            M = min(int(0.022 * SR), n - o)
            th[o:o + M] += rng.standard_normal(M) * np.exp(-np.arange(M) / SR / 0.0034)
        y = y + bandpass(stereo(nz), 260, 2400, 2) * 0.13 * finger
        y = y + lp(stereo(th), 240, 4) * 0.22 * finger

    if gatep is not None:
        # A bassist damps with the heel of the hand, which is not a note-off:
        # 25 ms of it, and the string is quieter rather than absent.
        g = np.clip(steplane(gatep, n, 'hold', 0.025), 0, 1)
        y = y * (0.10 + 0.90 * g)[:, None]
    y = lp(y, cut, 4)
    y = np.tanh(drive * y) / np.tanh(drive)
    return (y * adsr(n, a=0.003, r=0.012)[:, None]).astype(np.float32) * gain * 0.85


# ================================================================== the skank
@cached
def skank(notes, dur_steps=2.0, gain=1.0, decay=0.070, lo=265.0, hi=4200.0,
          click=1.0, roll=0.013, detune=3.0, drive=1.5, seed=0,
          bars=(1.0, 0.34, 0.58, 0.26, 0.13)):
    """The offbeat chop: a whole reggae rhythm section in one 70 ms event.

    Three things make it a skank rather than a chord. It is **short** - the
    hand comes off the keys immediately, so the sound is an articulation and
    not a harmony. It is **dry** - reverb on the skank is what turns a
    rhythm part into a pad. And its notes do not arrive together: thirteen
    milliseconds apart, lowest first, which is a hand, and simultaneous,
    which is a keypress.

    Same drawbar stack as `organbass` and deliberately so: on the records
    being copied they were the same instrument, one hand each.

    **The tuning does not move with the seed.** `detune` spreads the chord's
    notes across a few cents deterministically, so the instrument has a fixed
    intonation and every chop is the same pitch. Drawing that offset from the
    seed instead - which is the obvious way to make repeated hits sound
    played - gives each chop its own tuning, and four of those a bar for four
    minutes is a keyboard player who has been drinking. The seed varies the
    contact click and the millisecond of roll, and nothing else.
    """
    n, t = steps(dur_steps, floor=int(0.06 * SR))
    rs = np.random.RandomState(seed)
    out = np.zeros((n, 2), dtype=np.float64)
    ratios = (1.0, 1.5, 2.0, 3.0, 4.0)
    ph0 = np.random.RandomState(3).rand(len(notes), len(ratios)) * 6.28
    ns = sorted(notes)
    for i, nt in enumerate(ns):
        lag = int((i * roll + rs.uniform(0.0, 0.004)) * SR)
        m = n - lag
        if m < 64:
            continue
        tt = np.arange(m) / SR
        cents = detune * (2.0 * i / max(len(ns) - 1, 1) - 1.0)
        f = midi(nt) * 2.0 ** (cents / 1200.0)
        x = sum(a * np.sin(2 * np.pi * f * r * tt + ph0[i, j])
                for j, (r, a) in enumerate(zip(ratios, bars)))
        y = x * np.exp(-tt / decay)
        p = np.clip((i / max(len(notes) - 1, 1) - 0.5) * 0.9, -1, 1)
        ang = (p + 1) * np.pi / 4
        out[lag:, 0] += y * np.cos(ang)
        out[lag:, 1] += y * np.sin(ang)
    out = np.tanh(drive * out.astype(np.float32) / max(len(notes), 1))
    out = bandpass(out, lo, hi, 2)
    if click:
        L = min(int(0.010 * SR), n)
        ck = rs.randn(L) * np.exp(-np.arange(L) / SR / 0.0018)
        out[:L] += bandpass(stereo(ck), 1400, 6000, 2) * 0.22 * click
    return (fade_edges(out, 1.5)).astype(np.float32) * gain


@cached
def stab(notes, dur_steps=3.0, gain=1.0, decay=0.22, cut=3800.0, drive=2.2,
         roll=0.010, seed=0):
    """The minor chord hit: sawtooths, not sines, and gone in a quarter of a
    second. Where `skank` is the rhythm guitar's job, this is the horn
    section's - it lands on a downbeat, it says which chord the tune is on,
    and then it gets out of the way before the next kick."""
    n, t = steps(dur_steps, floor=int(0.08 * SR))
    rs = np.random.RandomState(seed)
    out = np.zeros((n, 2), dtype=np.float64)
    for i, nt in enumerate(sorted(notes)):
        lag = int((i * roll + rs.uniform(0.0, 0.003)) * SR)
        m = n - lag
        if m < 64:
            continue
        tt = np.arange(m) / SR
        f = midi(nt)
        # +-4 cents, not +-10. Three saws a tenth of a semitone apart beat
        # at a couple of hertz, which over a quarter-second chord is not
        # width, it is a chord going out of tune while you listen to it.
        x = np.zeros(m)
        for d in (0.99769, 1.0, 1.00231):
            x += 2 * ((f * d * tt + rs.rand()) % 1.0) - 1
        y = x / 3 * np.exp(-tt / decay)
        p = np.clip((i / max(len(notes) - 1, 1) - 0.5) * 1.1, -1, 1)
        ang = (p + 1) * np.pi / 4
        out[lag:, 0] += y * np.cos(ang)
        out[lag:, 1] += y * np.sin(ang)
    y = np.tanh(drive * out.astype(np.float32) / max(len(notes), 1) ** 0.7)
    y = hp(lp(y, cut, 4), 190, 2)
    return fade_edges(y, 1.5).astype(np.float32) * gain


# ====================================================================== dub
def throw(s, t, seg, gain=1.0, bus='fx', times=4, delay_steps=3.0, fb=0.52,
          damp=2600.0, pan=0.55):
    """Send one hit to the echo and close the send again.

    The single most useful thing dub gave this music. It is not a delay on a
    channel - it is a fader being opened for one event, so the repeats belong
    to that moment rather than to the arrangement. Each pass is darker than
    the last, which is what a tape machine does and what a digital delay
    left flat does not.
    """
    d = int(delay_steps * STEP)
    for i in range(times + 1):
        y = seg if i == 0 else lp(seg, max(damp - 380 * i, 620), 2)
        if i:
            y = panned(y, pan * (1 if i % 2 else -1))
        s.place(t + i * d, y, gain * fb ** i, bus)


def rewind_into(s, b, seg, gain=1.0, bus='fx', accel=3.4):
    """The rewind: spin the record backwards into the downbeat of bar `b`.

    A performance convention, not a mistake - the DJ pulls the tune back and
    drops it again, and by 1994 producers were printing it onto the record
    because the crowd expected it. Placed so the spin *ends* on the downbeat,
    which is the only placement that works: the silence it leaves behind is
    the gap the drop lands in.
    """
    y = rewind(np.asarray(seg, dtype=np.float32), accel)
    s.place(s.pos(b) - len(y), y, gain, bus)
    return len(y)


def ride(buf, arc, smooth=0.030):
    """A gain ride over a finished bus, in decibels per bar.

    Per-part gains do not sum to a section: a section is two hundred `place`
    calls across nine buses, and turning each of them down by the amount that
    feels right leaves the total where it was. Contrast is a level, so it is
    written as one - a master fader move, interpolated per sample and
    smoothed so it does not zipper.
    """
    n = len(buf)
    t = np.arange(n) / BAR
    db = np.interp(t, [p[0] for p in arc], [p[1] for p in arc])
    g = uniform_filter1d(10.0 ** (db / 20.0), max(int(smooth * SR), 3))
    return (buf * np.maximum(g, 0.0)[:, None]).astype(np.float32)
