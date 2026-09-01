"""The drift layer: the cowbell that screams and the car that changes gear.

A sibling of `phonklib`, not a replacement. That module is the 160 BPM memphis
strain - a cowbell driven into tanh, a power chord, a single-ramp engine. This
one is the modern drift/rage strain at 156, and its kit is built for a montage
edit: a cowbell struck with a pitch ping and torn open by hard sync, a bass
split at 120 Hz into a clean mono sub and a folded upper half, a brass stab
that scoops into the note, a choir, and a car that goes up through the gears.

Everything general still lives in `core` - the filters, `split`, `sync_saw`,
`morph_lp`, `morph_formant`, the 808 kit, the Session. This file adds only the
voices the style is actually made of.

Usage:
    from driftlib import *
    s = Session(92, tail=3.0)
    s.hit(s.pos(0, 0))                                  # sidechain trigger
    s.place(s.pos(0, 0), stomp(), bus='drums')
    s.place(s.pos(0, 0), cowbell(67, 2.4, tear=0.35), bus='music')
    s.place(s.pos(0, 0), slug(31, 8), bus='bass')
    s.render('phonk_montage_156.wav', clip=1.25, limit=0.93)
"""
import numpy as np
import core
from core import *

BAR, STEP = core.set_grid(bpm=156)
BPM = core.BPM


def _sq_ph(ph, fmax):
    """band-limited square from a phase array - a saw against itself, half a
    cycle late, which cancels every even harmonic and leaves the odd ones"""
    return saw_ph(ph, fmax) - saw_ph(ph + np.pi, fmax)


# ---- the cowbell: the lead instrument ----
@cached
def cowbell(note, dur=2.0, gain=1.0, drive=7.0, decay=0.20, folded=0.35,
            bright=1.0, ping=4.0, tear=0.0, ring=0.0, vowel=None, clang=0.6):
    """The 808 cowbell as a lead: two squares at f and 1.4815f - the real
    ratio, deliberately inharmonic - then driven, folded and re-resonated.

    Four things separate this from a bandpassed square:

    `ping`   both oscillators start `ping` semitones sharp and fall to pitch
             in 8 ms. Every struck object does this; without it the note
             switches on instead of being hit.
    `tear`   a hard-synced saw whose ratio falls 3.4 -> 1.7 over the first
             50 ms. Sync tearing is metallic in a way no filter is, and it is
             what makes the note read as a scream rather than a clonk.
    `folded` the wavefolder AFTER the bandpass, so it folds the band that
             survived rather than the fizz above it - distortion with an EQ
             between the stages, which is the whole difference between power
             and hiss.
    `vowel`  a formant pair over the top ('ah','eh'...): the cowbell talks.

    Dead centre on purpose - a Haas delay here combs the clang away in mono.
    """
    n, t = steps(dur)
    f = midi(note)
    f2 = f * (1.4815 + ring)
    top = 2 ** (ping / 12)
    bend = 1 + (top - 1) * np.exp(-t / 0.008)
    x = (_sq_ph(2 * np.pi * np.cumsum(f * bend) / SR, f * top)
         + 0.85 * _sq_ph(2 * np.pi * np.cumsum(f2 * bend) / SR, f2 * top))
    if tear:
        ratio = 3.4 - 1.7 * (1 - np.exp(-t / 0.05))
        x = (1 - tear) * x + tear * 1.5 * sync_saw(t, f, ratio)
    x = x * 0.5 * np.exp(-t / decay)
    x += np.random.randn(n) * np.exp(-t / 0.0035) * 0.20          # the mallet
    out = bandpass(stereo(np.tanh(drive * x)),
                   max(f * 0.8, 140.0), min(f * 10.0 * bright, 16500.0))
    if folded:
        out = (1 - folded) * out + folded * fold(out, 1.35 + 0.07 * drive)
    out = out + clang * bandpass(out, f * 2.2, f * 3.3, order=2)
    if vowel:
        out = morph_formant(out, vowel[0], vowel[-1], wet=0.40, gain=1.5)
    return out * adsr(n, a=0.0012, r=0.02)[:, None] * gain * 0.5


# ---- the bass ----
def slug(note, dur, slide_from=None, glide=0.06, gain=1.0, grind=3.4,
         decay=0.9, mid=1.0, growl=0.0, click=1.0, cut=3600.0, suboct=0.0):
    """One oscillator, split at 120 Hz: a clean mono sine underneath, the same
    note folded and clipped above it.

    This is the two-layer rule from the bass chapter built into one voice, so
    the two halves can never drift out of tune or out of phase with each
    other. The sub is what a system moves air with; the folded half is what a
    phone speaker reproduces, and the ear rebuilds the missing fundamental
    from it. `growl` puts a tempo-free tremolo on the upper half only.
    """
    n, t = steps(dur)
    f0 = midi(note)
    f = np.full(n, f0) if slide_from is None else f0 + (midi(slide_from) - f0) * np.exp(-t / glide)
    ph = 2 * np.pi * np.cumsum(f) / SR
    env = np.exp(-t / decay) * adsr(n, a=0.002, r=0.05)

    low = (np.sin(ph) + 0.22 * np.sin(2 * ph)) * env             # felt
    if suboct:
        # An octave below the note, for roots written high enough that the
        # fundamental sits at 60-120 Hz and nothing reaches the bottom band.
        low = low + suboct * np.sin(0.5 * ph) * env
    up = np.sin(ph) + 0.60 * np.sin(2 * ph) + 0.40 * np.sin(3 * ph) + 0.22 * np.sin(5 * ph)
    if growl:
        up = up * (0.55 + 0.45 * (0.5 - 0.5 * np.cos(2 * np.pi * growl * t)))
    up = fold(np.tanh(grind * up), 1.25) * env                   # heard
    out = stereo(low * 0.95) + lp(hp(stereo(up), 120), cut) * (0.66 * mid)
    if click:
        out += stereo(np.sin(6 * ph) * np.exp(-t / 0.008)) * 0.30 * click
    return norm(mono_below(out, 130), 0.95) * gain


# ---- the kick ----
@cached
def stomp(dur=5, tune=49.0, gain=1.0, drive=3.0, knock=1.0, decay=0.30, top=330.0):
    """The phonk kick with a knock: an 808 dive plus a band at 260-1400 Hz.

    The dive is the weight and disappears on a laptop; the knock is the part
    that still says 'kick' through a phone, and it is a separate layer so it
    can be EQ'd and driven without touching the low end."""
    n, t = steps(dur)
    f = tune + (top - tune) * np.exp(-t / 0.022)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.tanh(drive * np.sin(ph)) * np.exp(-t / decay)
    kf = tune * 3.1 + 900.0 * np.exp(-t / 0.012)
    kn = bandpass(stereo(np.tanh(4.0 * np.sin(2 * np.pi * np.cumsum(kf) / SR))), 260, 1400)
    kn *= (np.exp(-t / 0.035) * 0.5 * knock)[:, None]
    click = hp(stereo(np.random.randn(n) * np.exp(-t / 0.0016)), 1500) * 0.45
    return norm((stereo(body) + kn + click) * adsr(n, a=0.0005, r=0.02)[:, None], 0.95) * gain


# ---- the gigachad brass ----
@cached
def chad(notes, dur, gain=1.0, drive=6.0, scoop=1.4, cut0=6200.0, cut1=850.0,
         wide=0.6, square=0.5):
    """Brass stab: a saw stack that scoops up into the note over 35 ms, under a
    filter that shuts from cut0 to cut1 in 90 ms.

    A real brass player arrives flat and bright and settles; both halves of
    that are here, and the moving filter (not an amplitude envelope) is what
    makes it a blat rather than a chord."""
    n, t = steps(dur)
    bend = 2 ** (-scoop / 12 * np.exp(-t / 0.035))
    x = np.zeros(n)
    for m in notes:
        f = midi(m)
        for d in (0.994, 1.0, 1.007):
            x += saw_ph(2 * np.pi * np.cumsum(f * d * bend) / SR, f * d)
        if square:
            x += square * _sq_ph(2 * np.pi * np.cumsum(f * bend) / SR, f)
    x /= len(notes) * 3.0
    st = morph_lp(stereo(np.tanh(drive * x)), cut1, cut0, np.exp(-t / 0.09),
                  bands=7, res=0.25)
    env = (0.35 + 0.65 * np.exp(-t / 0.45)) * adsr(n, a=0.004, r=0.05)
    return mono_below(widen(hp(st, 90), wide), 140) * env[:, None] * gain * 0.55


# ---- the choir ----
def chant(notes, dur, gain=1.0, vowel='oh', drive=2.2, wide=0.6, attack=0.12):
    """Low male choir through a fixed vowel: the epic layer, kept under 5 kHz
    so it never competes with the cowbell.

    The width comes from splitting the detuned voices between the channels,
    not from a Haas delay. A Haas on a signal that is otherwise identical in
    both ears is nearly all side content - it sounds enormous and then half
    of it disappears the moment anything sums to mono. Randomised phases per
    call, so do not cache it or every entry lands identically."""
    n, t = steps(dur)
    chans = [np.zeros(n), np.zeros(n)]
    for m in notes:
        f = midi(m)
        vib = 1 + 0.005 * np.sin(2 * np.pi * 4.2 * t + np.random.rand() * 6)
        for i, d in enumerate((0.993, 1.0, 1.006)):
            v = saw_ph(2 * np.pi * np.cumsum(f * d * vib) / SR, f * d)
            l = 0.5 + 0.5 * wide * (-1, 0, 1)[i]          # centre voice stays centred
            chans[0] += v * (1 - l); chans[1] += v * l
    st = np.tanh(drive * np.stack(chans, 1) / max(len(notes) * 1.5, 1.0)).astype(np.float32)
    out = sum(bandpass(st, fc * 0.72, fc * 1.32) * g
              for fc, g in zip(FORMANTS[vowel], (1.0, 0.70, 0.30)))
    out += hp(stereo(np.random.randn(n)), 5000) * 0.05
    a = min(int(attack * SR), n // 3); r = min(int(0.35 * SR), n // 3)
    env = np.ones(n); env[:a] = np.linspace(0, 1, a) ** 1.5; env[-r:] *= np.linspace(1, 0, r)
    return lp(out, 5000) * env[:, None] * gain * 1.5


# ---- the car ----
def revs(dur, gears=3, rpm0=38.0, rpm1=128.0, gain=1.0, grit=3.2, dip=0.62):
    """The engine through the gears: the firing rate climbs, drops back on
    every shift and climbs higher. A single ramp reads as a wind-up toy; the
    sawtooth of the gearbox is what reads as a car."""
    n, t = steps(dur)
    u = t / t[-1]
    seg = np.clip(u * gears, 0, gears - 1e-9)
    g_i = np.floor(seg); frac = seg - g_i
    lo = rpm0 + (rpm1 - rpm0) * (g_i / gears) * dip
    hi = rpm0 + (rpm1 - rpm0) * ((g_i + 1) / gears)
    ph = 2 * np.pi * np.cumsum(lo + (hi - lo) * frac ** 0.8) / SR
    x = sum(a * np.sin(k * ph + 0.5 * np.sin(0.5 * k * ph))
            for k, a in ((1, 1.0), (2, 0.75), (3, 0.5), (4, 0.35), (6, 0.22), (8, 0.14), (12, 0.08)))
    nz = stereo(np.random.randn(n))
    roar = (lp(nz, 400) * (1 - frac)[:, None] + lp(nz, 1800) * frac[:, None])[:, 0] * (0.25 + 0.45 * u)
    out = lp(stereo(np.tanh(grit * x / 3) + roar), 3400)
    return widen(out, 1.8) * adsr(n, a=0.04, r=0.10)[:, None] * gain * 0.5


def turbo(dur, gain=1.0, f0=800.0, f1=5600.0, blow=True):
    """Turbo: a whistle spooling up, then the blow-off valve letting go"""
    n, t = steps(dur)
    u = t / t[-1]
    f = f0 * (f1 / f0) ** (u ** 1.6)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = 0.6 * np.sin(ph) + 0.25 * np.sin(1.5 * ph) + 0.1 * np.sin(2.51 * ph)
    out = stereo(x) * (u ** 1.4)[:, None] + bandpass(stereo(np.random.randn(n)), 2000, 9000) * (0.5 * u ** 2)[:, None]
    if blow:
        k = int(n * 0.86)
        gate = 1 - np.clip((np.arange(n) - k) / max(n - k, 1), 0, 1)
        hiss = np.zeros(n); hiss[k:] = np.exp(-np.arange(n - k) / SR / 0.11)
        out = out * gate[:, None] + hp(stereo(np.random.randn(n)), 3500) * hiss[:, None] * 0.65
    return widen(out, 1.2) * gain * 0.4


def skid(dur, gain=1.0, f0=1200.0, chatter=28.0):
    """Tyres letting go: a resonant band with the rubber chattering under it.
    Stick-slip - the tyre gripping and releasing tens of times a second - is
    the amplitude modulation, and it is what a plain swept squeal misses."""
    n, t = steps(dur)
    u = t / t[-1]
    warble = 1 + 0.09 * np.sin(2 * np.pi * 6.5 * t) + 0.04 * np.sin(2 * np.pi * 19 * t)
    f = f0 * warble * (1 + 0.3 * np.sin(np.pi * u))
    ph = 2 * np.pi * np.cumsum(f) / SR
    tone = 0.55 * np.sin(ph) + 0.30 * np.sin(2 * ph) + 0.12 * np.sin(3.02 * ph)
    chat = 0.62 + 0.38 * np.sin(2 * np.pi * chatter * t * (1 + 0.4 * u))
    nz = bandpass(stereo(np.random.randn(n)), 900, 5000) * 0.75
    out = np.tanh(1.9 * (stereo(tone * chat) + nz * chat[:, None]))
    return widen(out, 1.5) * (np.sin(np.pi * u) ** 0.55)[:, None] * gain * 0.4


def grunt(note=45, dur=2.0, gain=1.0, vowel=('ah', 'oh'), drop=5.0):
    """The exhale: a low voice falling `drop` semitones, for the accents no
    instrument should take"""
    n, t = steps(dur)
    f = midi(note) * 2 ** (-drop / 12 * (1 - np.exp(-t / 0.18)))
    x = sum(saw_ph(2 * np.pi * np.cumsum(f * d) / SR, f[0] * d) for d in (0.995, 1.0, 1.006))
    st = stereo(np.tanh(2.0 * x / 3))
    out = morph_formant(st, vowel[0], vowel[-1], wet=1.0, gain=1.5)
    out += hp(stereo(np.random.randn(n)), 3000) * 0.09
    env = np.exp(-t / 0.42) * adsr(n, a=0.012, r=0.09)
    return widen(lp(out, 4200), 0.9) * env[:, None] * gain * 0.9
