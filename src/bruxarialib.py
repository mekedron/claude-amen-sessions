"""The Brazilian layer: a chopped voice, a hand drum, and a whistle.

Bruxaria - the aggressive strain of Brazilian funk/montagem - at 164 BPM.
Its low end is the whole record: measured against five reference tracks, the
style puts 55-80% of its energy under 120 Hz and almost none above 6 kHz, and
its sub always has gaps - a note on the beat, its tail through the next 16th,
then silence.

What it reuses, deliberately: `slug` and `stomp` from `driftlib`. `slug` is a
single oscillator split at 120 Hz into a clean mono sub and a folded upper
half, which is exactly this low end; `stomp` is an 808 dive with a separate
260-1400 Hz knock, and the difference this track wants from it (tuned to C,
harder, shorter) is entirely in its parameters. `grunt` is a low voice falling
a fixed interval - an accent, not an instrument, and it does the same job
here. Importing driftlib sets the
grid to 156; the `set_grid` below overrides it, and both voices read the grid
through `core.steps()` at call time, so they follow this module's tempo.

What it adds, because nothing in the engine does it:

    chopvoice   a slice of a voice pitched by varispeed, formants moving with
                the pitch. Every vocal voice in the engine keeps its formants
                fixed on purpose - that is what makes a voice sound like one
                person singing higher. A montagem chop is the opposite.
    atabaque    a struck membrane: inharmonic partials at the ratios of a
                circular drumhead, a pitch that falls, a slap of noise
    tuim       the whistle over a baile funk beat - a falling noise band

Usage:
    from bruxarialib import *
    s = Session(72, tail=2.2)
    s.place(s.pos(0, 0), stomp(4, tune=65.4), bus='drums')
    s.place(s.pos(0, 0), slug(36, 3.2, decay=0.22), bus='roll')
    s.place(s.pos(0, 0), chopvoice(79, 2.0, vowel='ah'), bus='music')
"""
import numpy as np
import core
from core import *
from driftlib import slug, stomp, grunt

BAR, STEP = core.set_grid(bpm=164)
BPM = core.BPM


# ---- the lead: a slice of a voice ----
@cached
def chopvoice(note, dur=2.0, gain=1.0, vowel='ah', base=69, grit=0.35,
              bright=1.0, air=0.25, drive=2.0, wob=0.0):
    """A chopped, pitched vocal hit.

    Pitched the way a sampler pitches: by playback rate, so the formants move
    with the note. `ratio` is how far the tape was sped up, and every formant
    centre is multiplied by it - which is why a chop a fifth up sounds like a
    smaller person and not like the same one singing higher. `morph_formant`
    and the phonk module's `chop` both hold their formants still on purpose;
    here the shift is the point.

    Instant attack and a 4 ms gate at the end, because a slice is cut out of
    a recording, not played. `grit` is the bit reduction of having been
    resampled twice on the way to the beat.
    """
    n, t = steps(dur)
    f = midi(note)
    ratio = f / midi(base)
    vib = 1 + 0.008 * ratio * np.sin(2 * np.pi * 5.4 * ratio * t)
    x = sum(g * saw_ph(2 * np.pi * np.cumsum(f * d * vib) / SR, f * d)
            for d, g in ((0.996, 0.5), (1.0, 1.0), (1.005, 0.5))) / 2.0
    if wob:
        x = x * (1 - wob + wob * (0.5 - 0.5 * np.cos(2 * np.pi * 11.0 * t)))
    st = stereo(x)
    out = sum(bandpass(st, fc * ratio * 0.74, fc * ratio * 1.30) * g
              for fc, g in zip(FORMANTS[vowel], (1.0, 0.72, 0.34)))
    out += hp(stereo(np.random.randn(n)), min(3500 * ratio, 15000)) * air * 0.11
    out = np.tanh(drive * out)
    if grit:
        out = (1 - grit) * out + grit * bitcrush(out, 7, 3)
    a = max(int(0.0015 * SR), 2); r = max(int(0.004 * SR), 2)
    env = np.ones(n); env[:a] = np.linspace(0, 1, a); env[-r:] = np.linspace(1, 0, r)
    return lp(out, min(9000 * bright, 16000)) * env[:, None] * gain * 1.15


# ---- the percussion melody: a struck skin ----
@cached
def atabaque(note=45, dur=2.0, gain=1.0, decay=0.16, slap=1.0, drop=7.0,
             wood=1.0, tight=1.0):
    """A hand drum, tuned.

    A membrane is not a bell and not a rim. Its overtones are inharmonic but
    close in - 1, 1.59, 2.14, 2.30 times the fundamental for a circular
    head - and the pitch falls a few semitones in the first 25 ms as the skin
    tension releases. That fall is what says struck skin rather than struck
    metal, and it is the whole difference from the cowbell."""
    n, t = steps(dur)
    f = midi(note)
    ph = 2 * np.pi * np.cumsum(f * 2 ** (drop / 12 * np.exp(-t / 0.025))) / SR
    x = (np.sin(ph) + 0.50 * np.sin(1.593 * ph) + 0.28 * np.sin(2.135 * ph)
         + 0.16 * np.sin(2.295 * ph)) * np.exp(-t / (decay / tight))
    x += np.random.randn(n) * np.exp(-t / 0.0045) * 0.5 * slap
    out = bandpass(stereo(np.tanh(2.2 * x)), 70, min(3200 * wood, 15000))
    out += hp(stereo(np.random.randn(n) * np.exp(-t / 0.011)), 4000) * 0.16 * slap
    return out * adsr(n, a=0.0008, r=0.015)[:, None] * gain * 0.55


# ---- the whistle ----
def tuim(dur=2.0, gain=1.0, f0=3400.0, f1=1500.0, breath=0.45, fall=0.55):
    """The whistle over a baile funk beat: a narrow band and a tone falling
    together. `dubsiren` is a clean LFO'd sine and `turbo` climbs; this drops,
    fast, and is mostly air."""
    n, t = steps(dur)
    u = (t / t[-1]) ** 0.7
    f = f0 * (f1 / f0) ** u
    ph = 2 * np.pi * np.cumsum(f * (1 + 0.02 * np.sin(2 * np.pi * 9 * t))) / SR
    tone = np.sin(ph) + 0.18 * np.sin(2 * ph)
    band = np.zeros((n, 2), np.float32)
    for k, w in ((1.0, 1.0), (1.35, 0.4)):
        band += bandpass(stereo(np.random.randn(n)), f0 * k * 0.75, f0 * k * 1.25) * w
    out = stereo(tone) * (1 - breath) + band * breath * 0.5
    env = np.exp(-t / (dur * STEP / SR * fall)) * adsr(n, a=0.004, r=0.02)
    return widen(out, 0.8) * env[:, None] * gain * 0.45


# ---- the dry accent: 'beat seco' ----
@cached
def seco(dur=1.5, gain=1.0, tune=190.0, decay=0.055, snap=1.0):
    """The dry hit that punctuates a montagem bar: a short pitched knock with
    no tail at all. `rim` is a ring with no body; this has a body and no ring."""
    n, t = steps(dur)
    f = tune * 2 ** (5.0 / 12 * np.exp(-t / 0.012))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / decay)
    x += np.random.randn(n) * np.exp(-t / 0.0028) * 0.7 * snap
    out = bandpass(stereo(np.tanh(3.0 * x)), 140, 6000)
    return out * adsr(n, a=0.0005, r=0.008)[:, None] * gain * 0.6
