"""The funk layer: a slap bass, a clavinet, a horn section and a talkbox.

Sets the grid to 112 BPM and adds the band that plays 1983 - the point where
disco had become boogie, the drum machine had arrived, and the bass player
was still the loudest person in the room.

Three ideas run through everything here.

**The bass is one string.** A slapped bass is not a row of plucks: the string
never stops, and the thumb re-excites a note that is already sounding. So a
bar is rendered as ONE oscillator with a per-sample frequency track - which
gives hammer-ons and slides for free - and an amplitude that swells at every
attack instead of returning to zero. `slapbar` is the shape; `moogbar` is the
same engine with a synth on the end of it.

**The attack is a different instrument from the note.** The thumb hits the
string against the frets and the fret rattle is broadband noise at 2-5 kHz
with no pitch in it at all; the fundamental underneath is a sine. Mixed
together at the same level they read as one event, and separating them is
what makes a slap sound played rather than triggered. The same split runs
through the clav (hammer versus string), the horns (breath versus tone) and
the kit.

**The filter moves inside every note.** A slap, a clav, a wah'd guitar and a
horn all start bright and darken while they sound. A fixed filter with an
amplitude envelope only changes how loud something is; `morph_lp` driven by a
per-attack envelope changes what it is made of, which is the whole difference
between funk and a sequencer.

The kit is a 1982 drum machine, not a kit in a room: 8-bit samples at about
28 kHz, so every voice ends in `_lofi()` - quantisation grit and a lowpass
where the converter gave up. The snare gets its reverb gated, because in 1983
everybody's did.

Usage:
    from funklib import *
    s = Session(32, tail=2.0)
    for b in range(8):
        s.place(s.pos(b), slapbar(((0,30,'t'), (3,42,'p'), (6,30,'g'),
                                   (8,33,'t'), (11,45,'p'), (14,28,'t'))), 0.5, 'bass')
        s.pat(b, [(0, fkick()), (4, fsnare()), (8, fkick()), (12, fsnare())], bus='drums')
    s.render('funk_test_112.wav', drive=1.1)
"""
import numpy as np
import core
from core import *
from scipy.signal import fftconvolve
from scipy.ndimage import uniform_filter1d

BAR, STEP = core.set_grid(bpm=112)
BPM = core.BPM

# Every second 16th lands late by this fraction of a step. 0.12 is about 53%
# swing - under the threshold where you hear a shuffle and over the one where
# the machine sounds like a machine. The LinnDrum's own shuffle knob lived
# here, and so does every record made on one.
SWING = 0.12


def sw(st, amt=None):
    """Push an odd 16th late. Downbeats never move."""
    a = SWING if amt is None else amt
    return st + (a if int(st) % 2 else 0.0)


# ---- the string ----
# `ks` lives in core - see the note there.


# ---- the 1982 converter ----
def _lofi(x, bits=9, down=2, top=12000.0, mix=1.0):
    """8-bit samples at 28 kHz. The quantisation noise and the aliasing that
    a converter with no anti-alias filter folds back down are not damage -
    they are most of what people mean when they say a drum machine sounds
    like that record. `down=2` puts Nyquist at 11 kHz, which is where a
    LinnDrum's hats stop and its snare starts to sizzle."""
    if mix <= 0:
        return x
    y = lp(bitcrush(x, bits=bits, downsample=down), top, order=4)
    return (x * (1 - mix) + y * mix).astype(np.float32)


def chorus(seg, rate=0.55, depth_ms=5.5, base_ms=13.0, mix=0.55, voices=2):
    """Two modulated delays with their LFOs in opposite phase per channel.

    This is the effect that is ALWAYS ON in this decade - on the e-piano, on
    the clean guitar, on the syn-brass - and leaving it off is why a
    synthesised 80s track sounds thin. Opposite phase is the part that
    matters: the same delay in both channels is a flanger, and it is only
    when the two sides disagree about the pitch that it opens out."""
    n = len(seg)
    base = np.arange(n, dtype=np.float64)
    t = base / SR
    out = np.array(seg, dtype=np.float32, copy=True)
    for v in range(voices):
        lfo = np.sin(2 * np.pi * rate * (1 + 0.27 * v) * t + v * 2.3)
        for c in range(2):
            l = lfo if c == 0 else -lfo
            d = (base_ms * (1 + 0.3 * v) + depth_ms * 0.5 * (1 + l)) / 1000.0 * SR
            idx = np.clip(base - d, 0, n - 1)
            out[:, c] += (mix * 0.7 * np.interp(idx, base, seg[:, c])).astype(np.float32)
    return (out / (1 + mix)).astype(np.float32)


# ---- the bass ----
# A bass guitar is ONE string. Slapping it does not start a new note, it
# re-excites one that never stopped - which is why a bassline built out of
# eight separate plucks a bar comes out shattered: the fundamental dies in
# every gap and the overlaps cancel at unrelated phases. A whole bar is one
# oscillator whose pitch bends between notes and whose amplitude swells at
# every attack. The attacks are discrete; the low end never is.
def _bartrack(evs, n, glide):
    """(edges, frequency track, phase) for one bar of a bar-rendered bass."""
    edge = [min(int(st * STEP), n - 1) for st, _, _ in evs] + [n]
    f = np.empty(n)
    f[:edge[0]] = midi(evs[0][1])
    for i, (_, nt, _) in enumerate(evs):
        f[edge[i]:edge[i + 1]] = midi(nt)
    f = uniform_filter1d(f, max(int(glide * SR), 3))
    return edge, f, 2 * np.pi * np.cumsum(f) / SR


def _swell(edge, levels, n, tau, attack=0.0):
    """An envelope that rises at every attack and never returns to zero."""
    amp = np.zeros(n)
    for k, lv, ta in zip(edge, levels, tau):
        d = np.arange(n - k) / SR
        e = lv * np.exp(-d / ta)
        if attack:
            e = e * np.minimum(d / attack, 1.0)
        np.maximum(amp[k:], e, out=amp[k:])
    return uniform_filter1d(amp, max(int(0.004 * SR), 3))


@cached
def slapbar(notes, dur_steps=16, level=1.0, glide=0.009, decay=0.42,
            take=0, quack=1.0, attack=1.0, comp=1.35, mid=0.6):
    """One bar of slap bass. `notes` is a tuple of (step, midi, kind):

        't'  thumb - struck against the frets, the rattle is the sound
        'p'  pop   - pulled and released, brighter and an octave up
        'h'  hammer/slide - pitch changes with no new attack
        'g'  ghost - a dead string, all click and no note

    Ghosts are the reason funk is funk. They are inaudible as events and the
    bar collapses without them, because they are what fills the 16ths the
    thumb leaves open.

    The attack is normalised per event and mixed against the string by peak,
    not by taste: the fret rattle has to be LOUDER than the note it starts,
    and a fixed gain buried under a saturator is how a slap ends up sounding
    like a synth bass with a click on it."""
    n, t = steps(dur_steps)
    evs = sorted(notes)
    voiced = [e for e in evs if e[2] != 'g'] or [(0, evs[0][1], 't')]
    edge, f, ph = _bartrack(voiced, n, glide)

    lv = {'t': 1.0, 'p': 0.90, 'h': 0.58}
    amp = _swell(edge[:-1], [lv[k] for _, _, k in voiced], n,
                 [decay * (0.62 if k == 'p' else 1.0) for _, _, k in voiced])
    # The fingerboard: the note darkens over about 60 ms from every attack.
    br = _swell(edge[:-1], [1.0 if k != 'h' else 0.45 for _, _, k in voiced], n,
                [0.075 if k == 'p' else 0.055 for _, _, k in voiced])

    body = (np.sin(ph) + 0.42 * np.sin(2 * ph) + 0.18 * np.sin(3 * ph)
            + 0.07 * np.sin(4 * ph)) * amp
    string = saw_ph(ph, float(f.max()) * 1.02) * amp
    q = morph_lp(stereo(string), 240, 4300, br, bands=7, res=1.2)
    note = lp(stereo(body), 430, order=4) + q * 0.55 * quack
    # 700-1600 Hz is the band a phone speaker can actually move, and the one
    # a bass guitar's fingers live in. Without it the part is only felt.
    note = note + 0.40 * bandpass(note, 700, 1600)
    note = np.tanh(1.25 * note) * 0.78

    # the frets. Broadband, pitchless, and a different instrument from the
    # note underneath - which is the whole reason a slap reads as struck.
    KIND = {'t': (1000, 5400, 1.00, 0.0038, 4.1),
            'p': (2300, 9500, 1.20, 0.0024, 6.3),
            'g': (240, 1900, 0.62, 0.0110, 0.0),
            'h': (1200, 5000, 0.34, 0.0026, 0.0)}
    atk = np.zeros((n, 2), dtype=np.float32)
    rng = np.random.default_rng(600 + take)
    for st, nt, k in evs:
        lo, hi, lvl, tau, ring = KIND[k]
        j = min(int(st * STEP), n - 2)
        m = min(n - j, int(0.06 * SR))
        if m < 64:
            continue
        tt = np.arange(m) / SR
        b = rng.standard_normal(m) * np.exp(-tt / tau)
        if ring:
            b += np.sin(2 * np.pi * midi(nt) * ring * tt) * np.exp(-tt / (tau * 1.8)) * 0.5
        bb = bandpass(stereo(b), lo, hi, order=2)
        atk[j:j + m] += (bb / max(float(np.abs(bb).max()), 1e-9) * lvl).astype(np.float32)

    pk = max(float(np.abs(note).max()), 1e-9)
    out = note + np.tanh(1.3 * atk) * pk * attack * 0.62
    out = hp(out, 34, order=2)
    p2 = float(np.abs(out).max()) or 1.0          # squashed, as it always is
    out = softclip(out / p2 * comp, 1.0, knee=0.62) * p2 * 0.80
    if mid:
        out = out + mid * (1.5 * bandpass(out, 650, 2400) + 0.7 * bandpass(out, 2400, 5200))
        out = out / max(float(np.abs(out).max()), 1e-9) * p2 * 0.80
    return (out * adsr(n, a=0.0012, r=0.004)[:, None]).astype(np.float32) * level


@cached
def moogbar(notes, dur_steps=16, level=1.0, glide=0.013, decay=0.5, cutoff=1.0,
            res=1.6, take=0, drive=1.9, sub=0.5):
    """The other 80s bass: a mono synth, played legato, doubling the slap or
    replacing it. Same continuous bar, saws instead of a string, and a filter
    envelope that closes on every attack."""
    n, t = steps(dur_steps)
    evs = sorted(notes)
    voiced = [e for e in evs if e[2] != 'g'] or [(0, evs[0][1], 't')]
    edge, f, ph = _bartrack(voiced, n, glide)
    amp = _swell(edge[:-1], [1.0 if k != 'h' else 0.6 for _, _, k in voiced], n,
                 [decay] * len(voiced), attack=0.004)
    br = _swell(edge[:-1], [1.0 if k != 'h' else 0.5 for _, _, k in voiced], n,
                [0.10] * len(voiced))
    x = (saw_ph(ph, float(f.max()) * 1.02)
         + saw_ph(ph * 1.006, float(f.max()) * 1.02) * 0.7
         + sub * np.sin(ph * 0.5))
    out = morph_lp(stereo(x * amp / 2.2), 150, 3200 * cutoff, br, bands=7, res=res)
    out = np.tanh(drive * hp(out, 30, order=2))
    return (out * adsr(n, a=0.002, r=0.006)[:, None]).astype(np.float32) * level * 0.75


# ---- the clavinet ----
@cached
def clavi(notes, dur_steps=1.0, level=1.0, take=0, decay=0.16, damp=0.60,
          bright=1.0, mute=0.0):
    """Hohner D6: a rubber hammer throws a string at a fret and a magnetic
    pickup listens. Short, mid-forward, and percussive enough that sixteen of
    them a bar is a rhythm part rather than a chord.

    `mute` is the palm on the strings - the yank that turns a chank into a
    tick, and the difference between one bar and the next."""
    n, t = steps(dur_steps, floor=int(0.05 * SR))
    rng = np.random.default_rng(310 * take + sum(notes))
    x = np.zeros(n)
    for i, nt in enumerate(notes):
        d = int(0.0016 * i * SR)                       # the hammers are not level
        f = midi(nt) * (1 + 0.0018 * (rng.random() - 0.5))
        x[d:] += ks(f, n - d, decay=decay * (1 - 0.06 * i) * (1 - 0.7 * mute),
                    damp=damp + 0.2 * mute, pick=0.15, hardness=0.22,
                    seed=int(613 * take + 11 * nt)) * (1 - 0.08 * i)
    st = stereo(x / max(len(notes), 1))
    out = bandpass(st, 230, 5600 * bright, order=2)
    out = out + 0.95 * bandpass(out, 1100, 2700)       # the pickup's bark
    out = np.tanh(2.3 * out)
    env = np.exp(-t / (0.030 if mute else 0.13)) * adsr(n, a=0.0006, r=0.012)
    # No norm() here. Normalising every event to the same peak is what turns
    # a chank into a machine gun: the whole part is the difference between
    # the three chords that ring and the thirteen ticks that do not.
    return (out * env[:, None]).astype(np.float32) * level * (0.42 - 0.22 * mute)


@cached
def fgtr(notes, dur_steps=1.0, level=1.0, take=0, mute=0.0, bright=1.0):
    """The other 16th-note instrument: a clean Strat on the neck pickup
    through a chorus. Narrower and airier than the clav, so the two can play
    the same bar without becoming one blurred thing."""
    n, t = steps(dur_steps, floor=int(0.05 * SR))
    rng = np.random.default_rng(220 * take + sum(notes))
    x = np.zeros(n)
    for i, nt in enumerate(notes):
        d = int(0.0035 * i * SR)                       # a strum, not a chord
        x[d:] += ks(midi(nt) * (1 + 0.003 * (rng.random() - 0.5)), n - d,
                    decay=0.28 * (1 - 0.75 * mute), damp=0.34 + 0.25 * mute,
                    pick=0.30, hardness=0.5,
                    seed=int(457 * take + 19 * nt)) * (1 - 0.1 * i)
    st = stereo(x / max(len(notes), 1))
    out = bandpass(st, 320, 6200 * bright, order=2)
    out = out + 0.5 * bandpass(out, 1800, 3600)
    out = np.tanh(1.7 * out)
    env = np.exp(-t / (0.035 if mute else 0.20)) * adsr(n, a=0.0008, r=0.015)
    out = chorus(out * env[:, None], rate=0.6, depth_ms=4.0, mix=0.45)
    return out.astype(np.float32) * level * (0.80 - 0.42 * mute)


# ---- the electric piano ----
@cached
def ep(notes, dur_steps=8, level=1.0, vel=0.85, take=0, ring=1.4):
    """Two operators and a hammer. The tine is a modulator at fourteen times
    the carrier whose index dies in 60 ms - it is a bell that stops being a
    bell almost immediately, which is exactly what a struck tine does - over
    a body at 1:1 that lasts. Velocity moves the INDEX, not the volume: hit
    it harder and it gets brighter, which is the one thing a sampled piano
    from this decade could not do and an FM one could."""
    n, t = steps(dur_steps, floor=int(0.3 * SR))
    x = np.zeros(n)
    for nt in notes:
        ph = 2 * np.pi * midi(nt) * t
        tine = 2.6 * vel * np.exp(-t / 0.055) + 0.05
        bod = 1.15 * vel * np.exp(-t / 0.55) + 0.20
        x += np.sin(ph + bod * np.sin(ph)) * np.exp(-t / ring)
        x += 0.45 * np.sin(ph + tine * np.sin(14 * ph)) * np.exp(-t / 0.24)
    x = np.tanh(1.25 * x / max(len(notes), 1))
    out = lp(stereo(x), 6800)
    out = chorus(out, rate=0.45, depth_ms=6.5, mix=0.5)
    trem = 1 + 0.10 * np.sin(2 * np.pi * 4.6 * t)      # the suitcase's vibrato
    out[:, 0] *= trem
    out[:, 1] *= 2 - trem                              # which is really auto-pan
    return (out * adsr(n, a=0.003, r=0.06)[:, None]).astype(np.float32) * level * 0.55


# ---- the horns ----
@cached
def brass(notes, dur_steps=2, level=1.0, take=0, fall=0.0, scoop=1.0,
          blat=1.0, hold=0.5, breath=1.0):
    """A section, not a synth: every player arrives a few milliseconds apart,
    a few cents out, and none of them lands in tune - a horn scoops UP to the
    note over about 30 ms, and putting that back is most of what stops a saw
    stack sounding like a saw stack.

    `fall` is the drop at the end of a phrase, the thing a trumpet does
    instead of a full stop."""
    n, t = steps(dur_steps, floor=int(0.1 * SR))
    rng = np.random.default_rng(770 * take + sum(notes))
    st = np.zeros((n, 2), dtype=np.float32)
    for i, nt in enumerate(notes):
        det = 1 + 0.0045 * (rng.random() - 0.5) * 2
        up = 1 - 0.050 * scoop * np.exp(-t / 0.030)
        vib = 1 + 0.005 * np.sin(2 * np.pi * (5.0 + rng.random()) * t
                                 + rng.random() * 6) * np.minimum(t / 0.28, 1)
        fe = np.ones(n)
        if fall:
            k = int(n * 0.68)
            fe[k:] = 2 ** (-fall / 12 * np.linspace(0, 1, n - k) ** 1.6)
        ph = 2 * np.pi * np.cumsum(midi(nt) * det * up * vib * fe) / SR
        seg = 0.62 * saw_ph(ph, midi(nt) * 1.6) + 0.38 * np.sign(np.sin(ph))
        d = int((0.0035 * i + 0.002 * rng.random()) * SR)
        one = np.zeros(n)
        one[d:] = seg[:n - d] * (1 - 0.07 * i)
        # The section stands across a stage. Width made of four different
        # signals in four places survives a mono sum; width made of one
        # signal delayed does not.
        p = (i / max(len(notes) - 1, 1) - 0.5) * 0.9
        st += panned(stereo(one), p)
    st = (st / max(len(notes), 1)).astype(np.float32)
    out = bandpass(st, 280, 5200, order=2)
    out = out + blat * 0.85 * bandpass(out, 950, 2300)     # the blat
    out = out + 0.35 * bandpass(out, 2700, 4400)
    out = np.tanh(1.9 * out)
    out = out + hp(stereo(rng.standard_normal(n) * np.exp(-t / 0.022)),
                   2200) * 0.10 * breath
    dec = max(dur_steps * STEP / SR * hold, 0.05)
    env = np.minimum(t / 0.014, 1.0) * (0.35 + 0.65 * np.exp(-t / dec))
    env *= adsr(n, a=0.001, r=0.035)
    return norm(out * env[:, None], 0.9) * level * 0.55


@cached
def synbrass(notes, dur_steps=8, level=1.0, cutoff=2400, take=0, wide=1.0):
    """Jupiter-8 brass: saws with the pulse width moving, and a filter that
    opens over 90 ms instead of instantly. The other half of every horn line
    on a 1984 record, doubling the real section an octave up."""
    n, t = steps(dur_steps, floor=int(0.15 * SR))
    rng = np.random.default_rng(880 * take + sum(notes))
    x = np.zeros(n)
    for nt in notes:
        f = midi(nt)
        for d in (0.994, 1.0, 1.007):
            ph = 2 * np.pi * np.cumsum(np.full(n, f * d)) / SR + rng.random() * 6
            pw = 0.5 + 0.18 * np.sin(2 * np.pi * 0.35 * t + rng.random() * 6)
            x += (2 * ((ph / (2 * np.pi)) % 1.0) - 1) * 0.7
            x += np.where(((ph / (2 * np.pi)) % 1.0) < pw, 0.5, -0.5) * 0.5
    x /= max(len(notes) * 3, 1)
    op = np.minimum(t / 0.09, 1.0) * 0.75 + 0.25
    out = morph_lp(stereo(x), 420, cutoff, op, bands=6, res=0.5)
    out = np.tanh(1.6 * out)
    out = chorus(out, rate=0.4, depth_ms=7.0, mix=0.45 * wide)
    a = int(0.035 * SR)
    env = np.ones(n); env[:a] = np.linspace(0, 1, a)
    return (out * (env * adsr(n, a=0.001, r=0.09))[:, None]).astype(np.float32) * level


# ---- the talkbox ----
@cached
def talkbox(phrase, dur_steps=16, level=1.0, glide=0.026, take=0, sub=0.35,
            tube=1.0, drive=1.6):
    """Roger Troutman's instrument: a synth sent up a plastic tube into the
    mouth, shaped by the vocal tract and picked up by an ordinary microphone.

    So it is one continuous oscillator - the tube does not restart between
    words - with the FORMANTS moving over it. The formant pair does not track
    the pitch, which is why the note changes and the vowel does not, and why
    this reads as a voice instead of a filter sweep. The tube itself is the
    resonance at 2.6 kHz and the fact that nothing above 5 kHz survives a
    metre of plastic.

    `phrase` is a tuple of (step, midi, vowel) using core.FORMANTS' names."""
    n, t = steps(dur_steps)
    evs = sorted(phrase)
    edge = [min(int(st * STEP), n - 1) for st, _, _ in evs] + [n]
    f = np.empty(n)
    f[:edge[0]] = midi(evs[0][1])
    for i, (_, nt, _) in enumerate(evs):
        f[edge[i]:edge[i + 1]] = midi(nt)
    f = uniform_filter1d(f, max(int(glide * SR), 3))
    ph = 2 * np.pi * np.cumsum(f) / SR

    amp = _swell(edge[:-1], [1.0] * len(evs), n, [2.2] * len(evs), attack=0.018)
    x = (saw_ph(ph, float(f.max()) * 3) * 0.8
         + saw_ph(ph * 1.004, float(f.max()) * 3) * 0.6
         + np.sign(np.sin(ph * 0.5)) * 0.35)
    st = stereo(x * amp / 2.2)

    # The vowels crossfade over 45 ms - a mouth is not a switch, and the
    # transit between two vowels is where most of the word lives.
    vs = sorted({v for _, _, v in evs})
    W = {v: np.zeros(n) for v in vs}
    for i, (_, _, v) in enumerate(evs):
        W[v][edge[i]:edge[i + 1]] = 1.0
    k = max(int(0.045 * SR), 3)
    out = np.zeros((n, 2), dtype=np.float32)
    for v in vs:
        w = uniform_filter1d(W[v], k)
        if w.max() < 1e-4:
            continue
        vv = sum(bandpass(st, fc * 0.72, fc * 1.32, order=2) * g
                 for fc, g in zip(FORMANTS[v], (0.85, 1.05, 0.62)))
        out += (vv * w[:, None]).astype(np.float32)

    out = out + tube * 0.40 * bandpass(out, 2300, 3300)     # the tube
    out = out + 0.28 * bandpass(out, 160, 340)              # the mic, up close
    out = lp(out, 5400, order=3)
    out = np.tanh(drive * out)
    if sub:
        out = out + lp(stereo(np.sin(ph) * amp), 260) * sub
    return norm(out * adsr(n, a=0.004, r=0.03)[:, None], 0.92) * level * 0.75


# ---- the drum machine ----
@cached
def fkick(dur_steps=4, tune=58.0, gain=1.0, click=1.0, decay=0.150, seed=0,
          lofi=0.8):
    """A short, dry, sampled kick. Nothing about this decade's kick is long -
    the record needs the space between the beats for the bass to be in."""
    n, t = steps(dur_steps, floor=int(0.22 * SR))
    rng = np.random.default_rng(seed + 3)
    f = tune * (1 + 2.3 * np.exp(-t / 0.013))
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / decay)
    body += 0.45 * np.sin(2 * np.pi * tune * 2.0 * t) * np.exp(-t / 0.048)
    beat = rng.standard_normal(n) * np.exp(-t / 0.0024) * click
    beat += np.sin(2 * np.pi * 2300 * t) * np.exp(-t / 0.004) * 0.45 * click
    out = stereo(body) + hp(stereo(beat), 1400) * 0.85
    out = out + 0.40 * bandpass(out, 70, 140)
    out = np.tanh(1.75 * out)
    return norm(_lofi(hp(out, 30, order=2), mix=lofi)
                * adsr(n, a=0.0005, r=0.02)[:, None], 0.95) * gain


@cached
def fsnare(dur_steps=4, gain=1.0, tune=205.0, snap=1.0, decay=0.115, seed=0,
           gate=0.0, lofi=0.8, hold=0.20):
    """The backbeat, and in 1984 the loudest thing on the record after the
    voice. `gate` is the reverb that made it that way: a big bright room
    switched off after `hold` seconds, so the drum is enormous and the bar is
    still empty when the next one arrives."""
    n, t = steps(dur_steps, floor=int(0.5 * SR))
    rng = np.random.default_rng(seed + 5)
    pd = 1 + 0.20 * np.exp(-t / 0.008)
    shell = (np.sin(2 * np.pi * tune * pd * t) * np.exp(-t / 0.055)
             + 0.5 * np.sin(2 * np.pi * tune * 1.58 * pd * t) * np.exp(-t / 0.038)
             + 0.28 * np.sin(2 * np.pi * tune * 2.44 * t) * np.exp(-t / 0.024))
    nz = rng.standard_normal(n)
    wires = bandpass(stereo(nz), 1600, 8200) * np.exp(-t / decay)[:, None] * 1.25 * snap
    stick = bandpass(stereo(nz * np.exp(-t / 0.0016)), 2200, 7500) * 0.5
    dry = np.tanh(1.7 * (stereo(shell * 1.1) + wires + stick))
    dry = _lofi(dry, mix=lofi)
    if gate:
        ir = core._reverb_ir(1.5, 7000)
        wet = np.stack([fftconvolve(dry[:, c], ir[:, c])[:n] for c in range(2)], 1)
        h = min(int(hold * SR), n)
        g = np.zeros(n); g[:h] = 1.0
        r = max(int(0.012 * SR), 2)
        g[max(h - r, 0):h] = np.linspace(1, 0, min(r, h))
        wet = (wet * 0.45 + stereo(wet.mean(axis=1)) * 0.55).astype(np.float32)
        dry = dry + gate * 1.6 * (wet * g[:, None]).astype(np.float32)
    return norm(hp(dry, 110, order=2) * adsr(n, a=0.0006, r=0.02)[:, None], 0.93) * gain


@cached
def fclap(dur_steps=3, gain=1.0, seed=0, spread=1.0):
    """Four hands, not one: three bursts a few milliseconds apart and then
    the room they were in. If they land together it is a snare."""
    n, t = steps(dur_steps, floor=int(0.3 * SR))
    rng = np.random.default_rng(seed + 9)
    x = np.zeros(n)
    for d in (0.0, 0.0085, 0.0175, 0.0275):
        k = int(d * SR)
        x[k:] += rng.standard_normal(n - k) * np.exp(-np.arange(n - k) / SR / 0.0075)
    x += rng.standard_normal(n) * np.exp(-t / 0.075) * 0.5      # the tail
    out = bandpass(stereo(x), 850, 3900, order=2)
    out = out + 0.5 * bandpass(out, 1400, 2400)
    out = np.tanh(1.6 * out)
    out = widen(_lofi(out, mix=0.7), 1.1 * spread)
    return norm(out * adsr(n, a=0.0008, r=0.03)[:, None], 0.88) * gain * 0.7


@cached
def fhat(dur_steps=1, open_=False, gain=1.0, tone=1.0, seed=0, lofi=0.9):
    """Six inharmonic squares for the metal, noise for the air, and an 8-bit
    converter for the fizz on top of both."""
    n, t = steps(dur_steps, floor=int(0.03 * SR))
    rng = np.random.default_rng(seed + 11)
    ratios = (1.0, 1.35, 1.62, 2.0, 2.45, 2.80)
    x = sum(np.sign(np.sin(2 * np.pi * 880 * r * tone * t)) for r in ratios) / 6
    x = x * 1.05 + rng.standard_normal(n) * 0.8
    d = 0.30 if open_ else 0.028
    out = hp(stereo(x), 3600 if open_ else 4600)
    out = out + 0.45 * bandpass(out, 6000, 10000)
    out = out * (np.exp(-t / d) * adsr(n, a=0.0005, r=0.01))[:, None]
    return norm(_lofi(out, bits=8, top=16000, mix=lofi), 0.9) * gain * 0.5


@cached
def cabasa(dur_steps=1, gain=1.0, seed=0, tone=1.0):
    """The 16ths that are not the hats. Steel beads on a gourd: a scrape,
    not a tick, so it has a body after the attack and a hat does not."""
    n, t = steps(dur_steps, floor=int(0.04 * SR))
    rng = np.random.default_rng(seed + 13)
    x = rng.standard_normal(n)
    out = bandpass(stereo(x), 3800 * tone, 11000 * tone, order=2)
    env = np.exp(-t / 0.008) + 0.45 * np.exp(-t / 0.030)
    return norm(_lofi(out * env[:, None], bits=8, top=16000, mix=0.8), 0.85) * gain * 0.4


@cached
def ftom(dur_steps=2, tune=150.0, gain=1.0, seed=0):
    """Syn-tom: a shell with a pitch drop, and in this decade the drop is
    exaggerated far past anything a drum does, because that was the point."""
    n, t = steps(dur_steps, floor=int(0.2 * SR))
    rng = np.random.default_rng(seed + 41)
    f = tune * (1 + 0.75 * np.exp(-t / 0.055))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.24)
    x += 0.35 * np.sin(2 * np.pi * tune * 1.6 * t) * np.exp(-t / 0.09)
    head = bandpass(stereo(rng.standard_normal(n) * np.exp(-t / 0.008)), 800, 4500)
    out = np.tanh(1.5 * (stereo(x) + head * 0.45))
    return norm(_lofi(hp(out, 55, order=2), mix=0.7)
                * adsr(n, a=0.0007, r=0.02)[:, None], 0.92) * gain


@cached
def conga(dur_steps=2, tune=230.0, gain=1.0, slap=0.0, seed=0):
    """Hand drum. `slap` moves the hand from the middle of the head to its
    edge - higher modes, shorter, and the crack instead of the tone."""
    n, t = steps(dur_steps, floor=int(0.15 * SR))
    rng = np.random.default_rng(seed + 51)
    f = tune * (1 + 0.28 * np.exp(-t / 0.010))
    dec = 0.10 - 0.06 * slap
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / dec)
    x += (0.35 + 0.9 * slap) * np.sin(2 * np.pi * tune * 2.9 * t) * np.exp(-t / (0.03 - 0.015 * slap))
    hand = bandpass(stereo(rng.standard_normal(n) * np.exp(-t / (0.004 + 0.006 * slap))),
                    900, 6000) * (0.35 + 0.7 * slap)
    out = np.tanh(1.6 * (stereo(x) + hand))
    return norm(hp(out, 90, order=2) * adsr(n, a=0.0006, r=0.02)[:, None], 0.88) * gain * 0.7


@cached
def tamb(dur_steps=1, gain=1.0, seed=0, ring=0.0):
    """Jingles: a dozen little cymbals that are all slightly different, which
    is why one bandpassed noise burst never sounds like a tambourine."""
    n, t = steps(dur_steps, floor=int(0.06 * SR))
    rng = np.random.default_rng(seed + 61)
    x = rng.standard_normal(n) * 0.6
    for r in (1.0, 1.19, 1.37, 1.58, 1.83, 2.11):
        x += np.sin(2 * np.pi * 5400 * r * t + rng.random() * 6) * 0.25
    out = hp(stereo(x), 4800)
    env = np.exp(-t / (0.010 + 0.22 * ring)) * adsr(n, a=0.0005, r=0.02)
    return norm(_lofi(out * env[:, None], bits=8, top=16000, mix=0.7), 0.85) * gain * 0.35


@cached
def fcowbell(dur_steps=2, gain=1.0, tune=1.0, seed=0):
    """Two square waves a not-quite-fifth apart through a bandpass, which is
    all a cowbell has ever been."""
    n, t = steps(dur_steps, floor=int(0.1 * SR))
    x = (np.sign(np.sin(2 * np.pi * 540 * tune * t))
         + 0.8 * np.sign(np.sin(2 * np.pi * 800 * tune * t)))
    out = bandpass(stereo(x), 700, 6000, order=2)
    env = np.exp(-t / 0.10) * adsr(n, a=0.0008, r=0.02)
    return norm(_lofi(out * env[:, None], bits=8, mix=0.6), 0.8) * gain * 0.35


@cached
def fcrash(dur_steps=16, gain=1.0, seed=0):
    n, t = steps(dur_steps, floor=int(0.6 * SR))
    rng = np.random.default_rng(seed + 71)
    ratios = (1.0, 1.44, 1.87, 2.33, 2.81, 3.47, 4.2, 5.4, 6.9, 8.3)
    x = sum(np.sin(2 * np.pi * 720 * r * t + rng.random() * 6) for r in ratios) / 10
    x = x * 1.15 + rng.standard_normal(n) * 0.8
    out = hp(stereo(x), 1600)
    out = out + 0.4 * bandpass(out, 4000, 9000)
    out = out * (np.exp(-t / 1.1) * adsr(n, a=0.0008, r=0.25))[:, None]
    return norm(widen(_lofi(out, bits=9, top=16000, mix=0.6), 1.2), 0.85) * gain * 0.42


# ---- the room ----
def room(buf, decay=0.5, wet=0.18, tone=6000, block_bars=16):
    """The tail ONLY - add it to the bus, do not replace it. One space for
    the whole kit, convolved in blocks so a four-minute buffer does not need
    a four-minute FFT."""
    out = np.zeros_like(buf)
    ir = core._reverb_ir(decay, tone)
    pre = int(0.005 * SR)
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


def squash(buf, amount=2.8, out=0.55, knee=0.42):
    """Peak-normalise, drive into a soft knee, come back down. Not glue - a
    16th-note part has a crest factor of twenty and needs the quiet ticks
    pulled up to meet the accents, or only the accents are ever heard."""
    pk = float(np.abs(buf).max()) or 1.0
    return (softclip(buf / pk * amount, 1.0, knee=knee) * pk * out).astype(np.float32)


def autowah(seg, per_bar=1.0, lo=380.0, hi=3000.0, res=1.6, phase=0.0, bands=8):
    """A pedal nobody is standing on: a lowpass sweeping once every `per_bar`
    bars. On a 16th-note clav part this is the difference between a loop and
    a part, because the notes stop being identical without any of them
    changing."""
    n = len(seg)
    t = np.arange(n) / SR
    rate = BPM / 60.0 / (4.0 * per_bar)
    env = 0.5 - 0.5 * np.cos(2 * np.pi * rate * t + phase)
    return morph_lp(seg, lo, hi, env, bands=bands, res=res)


# =======================================================================
# The instruments that only exist in this genre
# =======================================================================

# ---- the Hammond ----
# Nine sine partials mixed by nine sliders. Additive synthesis, built in
# 1935, and the reason a drawbar organ sounds like nothing else: there is no
# filter anywhere in it, so the tone never changes while a note sounds. All
# the movement has to come from the speaker.
DRAWBARS = (0.5, 1.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0)   # 16' 5 1/3' 8' 4' ...
# The tonewheels are driven by gears, and no gear ratio is exactly the
# twelfth root of two - so every partial is a few cents out, differently.
# That fixed, tiny error is a large part of the instrument.
_WHEEL_ERR = (-0.0009, 0.0021, 0.0, 0.0011, -0.0016, 0.0007, 0.0026, -0.0013, 0.0018)


@cached
def organ(notes, dur_steps=8, bars='888000000', perc=0.0, click=1.0,
          drive=1.6, level=1.0, take=0):
    """A drawbar organ. `bars` is the nine sliders as digits 0-8:

        888000000  the first three out - fat, gospel, the funk default
        888800000  brighter rock
        800000888  the hollow whistle jazz setting
        868868868  a common blues registration

    `perc` is the percussion tab - a decaying 2 2/3' that sounds once at the
    start of a phrase and never again until you let go of every key. `click`
    is the key contacts making and breaking, which was a defect for thirty
    years and is now the sound."""
    n, t = steps(dur_steps, floor=int(0.15 * SR))
    lv = [int(c) / 8.0 for c in bars]
    rng = np.random.default_rng(500 + take)
    x = np.zeros(n)
    for nt in notes:
        f0 = midi(nt)
        for r, g, e in zip(DRAWBARS, lv, _WHEEL_ERR):
            if g <= 0:
                continue
            f = f0 * r * (1 + e)
            if f > 14000:
                continue
            x += g * np.sin(2 * np.pi * f * t + rng.random() * 6)
    x /= max(len(notes), 1)
    if perc:
        p = np.zeros(n)
        for nt in notes[:1]:                        # the tab is monophonic
            p += np.sin(2 * np.pi * midi(nt) * 3.0 * t)
        x += perc * p * np.exp(-t / 0.22)
    out = stereo(np.tanh(drive * x) / np.tanh(drive))
    if click:
        k = rng.standard_normal(n) * np.exp(-t / 0.0016)
        out = out + bandpass(stereo(k), 1200, 9000) * 0.22 * click
    a = int(0.004 * SR)
    env = np.ones(n); env[:a] = np.linspace(0, 1, a)
    return (out * (env * adsr(n, a=0.0008, r=0.010))[:, None]).astype(np.float32) * level * 0.5


def leslie(seg, rate=6.6, slow=None, ramp=1.8, depth=1.0, split_hz=800.0,
           dop=1.0):
    """A rotating horn over a rotating drum, in a wooden box, heard from
    outside. Three things happen at once and all three are the effect:
    Doppler pitch modulation from the source moving towards and away, an
    amplitude change as the mouth points at the mic or away from it, and the
    two rotors running at different speeds so they never line up.

    Pass `slow` and the speaker changes gear over `ramp` seconds - and the
    horn gets there before the drum does, because it weighs less. That
    acceleration is the most expressive thing an organist has."""
    n = len(seg)
    t = np.arange(n) / SR
    if np.ndim(rate):
        # A rate written per sample: the two rotors get there at different
        # speeds because the horn weighs a fraction of what the drum does,
        # so smoothing the same switch by two different amounts IS the
        # acceleration. Driving the whole bus at once also keeps the rotor
        # phase continuous across a four-minute record - restart it every
        # bar and the organ ticks.
        r = np.asarray(rate, dtype=np.float64)[:n]
        r_h = uniform_filter1d(r, max(int(1.1 * SR), 3))
        r_d = uniform_filter1d(r, max(int(2.4 * SR), 3)) * 0.86
    elif slow is not None:
        u = np.clip(t / max(ramp, 1e-3), 0, 1)
        r_h = slow + (rate - slow) * u ** 1.25
        r_d = slow * 0.88 + (rate * 0.86 - slow * 0.88) * u ** 2.1
    else:
        r_h = np.full(n, rate)
        r_d = np.full(n, rate * 0.86)
    lo, hi = split(seg, split_hz)
    out = np.zeros((n, 2), dtype=np.float32)
    base = np.arange(n, dtype=np.float64)
    for band, r, dmax, am in ((hi, r_h, 1.15 * dop, 0.38 * depth),
                              (lo, r_d, 0.42 * dop, 0.17 * depth)):
        ph = 2 * np.pi * np.cumsum(r) / SR
        for c in range(2):
            pc = ph + (0.0 if c == 0 else np.pi * 0.85)
            dl = dmax / 1000.0 * SR * (0.5 + 0.5 * np.sin(pc))
            idx = np.clip(base - dl, 0, n - 1)
            y = np.interp(idx, base, band[:, c])
            out[:, c] += (y * ((1 - am) + am * (0.5 + 0.5 * np.sin(pc)))).astype(np.float32)
    return (out + 0.12 * lp(out, 260)).astype(np.float32)    # the wooden box


# ---- the tenor ----
@cached
def saxline(phrase, dur_steps=16, level=1.0, glide=0.010, take=0, breath=1.0,
            bright=1.0, vib=5.4, drive=1.6):
    """A tenor saxophone. `phrase` is (step, midi, articulation):

        'n' plain    '>' accented    'g' growled
        '^' scooped into from below  'f' falls off the end

    A reed does not restart between slurred notes - the column of air keeps
    going and the fingers change its length - so the phrase is one
    oscillator, like the bass. What makes it a saxophone rather than a saw
    is the body: a fixed resonance around 800 Hz that does not move with the
    pitch, and a second one near 2 kHz that is where all the bite is.

    The growl is the player humming into the mouthpiece while blowing. It
    beats against the note at thirty-odd hertz, and it is the single most
    recognisable noise in this music."""
    n, t = steps(dur_steps)
    evs = sorted(phrase)
    edge = [min(int(st * STEP), n - 1) for st, _, _ in evs] + [n]
    rng = np.random.default_rng(430 + take)

    f = np.empty(n)
    f[:edge[0]] = midi(evs[0][1])
    since = np.zeros(n)                       # time since this note started
    for i, (_, nt, art) in enumerate(evs):
        a, b = edge[i], edge[i + 1]
        d = np.arange(b - a) / SR
        seg = np.full(b - a, midi(nt))
        if '^' in art:                        # the scoop, from a tone below
            seg = seg * (1 - 0.055 * np.exp(-d / 0.045))
        if 'f' in art:                        # and the fall at the end
            k = int((b - a) * 0.62)
            seg[k:] *= 2 ** (-np.linspace(0, 3.5, b - a - k) ** 1.4 / 12)
        f[a:b] = seg
        since[a:b] = d
    f = uniform_filter1d(f, max(int(glide * SR), 3))
    vibr = 1 + 0.009 * np.sin(2 * np.pi * vib * t) * np.minimum(since / 0.32, 1.0)
    ph = 2 * np.pi * np.cumsum(f * vibr) / SR

    amp = np.zeros(n)                         # wind sustains; it does not decay
    for i, (_, _, art) in enumerate(evs):
        a, b = edge[i], edge[i + 1]
        lv = 1.15 if '>' in art else 1.0
        seg = np.full(b - a, lv)
        r = min(int(0.045 * SR), (b - a) // 2)
        if r > 1:
            seg[-r:] *= np.linspace(1, 0.25, r)
        amp[a:b] = seg
    amp = uniform_filter1d(amp * np.minimum(since / 0.016, 1.0), max(int(0.007 * SR), 3))

    gr = np.zeros(n)
    for i, (_, _, art) in enumerate(evs):
        if 'g' in art:
            gr[edge[i]:edge[i + 1]] = 1.0
    gr = uniform_filter1d(gr, max(int(0.02 * SR), 3))

    # A reed is a pressure-controlled valve, so the waveform it makes is a
    # narrow PULSE, not a square - and a pulse of duty d has harmonic k at
    # |sin(pi*k*d)|/k, which is where the even harmonics of a conical horn
    # come from. Built as the difference of two band-limited saws, because a
    # naive pulse at 440 Hz aliases into everything above it.
    fm = float(f.max()) * 2.2
    duty = 0.20
    pulse = saw_ph(ph, fm) - saw_ph(ph - 2 * np.pi * duty, fm)
    x = 1.0 * saw_ph(ph, fm) + 0.40 * pulse
    # the hum against the note: a slow beat that is not a tremolo, because it
    # modulates the reed and therefore the harmonics, not the level
    x = x * (1 + gr * 0.55 * np.sin(2 * np.pi * 34.0 * t))
    x = x + gr * 0.30 * np.sin(ph * 0.5) * amp
    # A reed valve opens and closes against the mouthpiece, so it clips
    # ASYMMETRICALLY - which is what puts the even harmonics in. A plain
    # tanh is an odd function: drive a saw into one hard enough and it comes
    # out a square wave, with no even harmonics at all, and a saxophone
    # turns into a clarinet.
    y = drive * x * amp
    y = np.where(y >= 0, np.tanh(y), np.tanh(0.68 * y) * 0.82)
    x = (y - uniform_filter1d(y, max(int(0.05 * SR), 3))) / np.tanh(drive)

    st = stereo(x)
    # The body is EQ on the whole signal, never a sum of bands. Summing
    # disjoint bandpasses notches out every harmonic that falls in a gap
    # between them - which on a conical instrument silences the even ones and
    # turns a saxophone into a clarinet. Add resonances to the full band.
    out = lp(st, 7000, order=3)
    out = out + 1.15 * bandpass(out, 620, 1050)              # the tenor's formant
    out = out + 0.85 * bandpass(out, 1500, 2600) * bright    # the bite
    out = out + 0.30 * bandpass(out, 3000, 5200) * bright    # the reed's edge
    out = out - 0.35 * bandpass(out, 190, 430)               # and off the boom
    out = lp(out, 6800, order=3)
    air = hp(stereo(rng.standard_normal(n)), 3200) * (amp * 0.055 * breath)[:, None]
    for i in range(len(evs)):                      # the pads and the key noise
        a = edge[i]
        m = min(n - a, int(0.02 * SR))
        if m > 32:
            k = rng.standard_normal(m) * np.exp(-np.arange(m) / SR / 0.0035)
            air[a:a + m] += bandpass(stereo(k), 1800, 6500)[:m] * 0.10
    out = out + air
    return norm(out * adsr(n, a=0.004, r=0.02)[:, None], 0.92) * level * 0.6


# ---- the envelope filter ----
def envfilter(seg, lo=170.0, hi=2600.0, res=4.5, sens=1.0, attack=0.006,
              release=0.14, bands=8, floor=0.06):
    """A Mu-Tron III: a resonant filter whose cutoff is driven by how loud
    the player is playing, not by a pedal or an LFO.

    It is the difference between a bass part and Bootsy Collins. Every note
    opens the filter by itself and closes it again while it decays, so the
    harder a note is hit the further it opens - the instrument answers the
    hand instead of the clock, and a line of identical notes stops being
    identical."""
    m = np.abs(seg).max(axis=1).astype(np.float64)
    e = uniform_filter1d(m, max(int(attack * SR), 3))
    e = np.maximum(e, uniform_filter1d(
        np.maximum.accumulate(e * np.exp(-np.arange(len(e)) / SR / release))
        * np.exp(np.arange(len(e)) / SR / release), max(int(0.02 * SR), 3)))
    e = uniform_filter1d(e, max(int(release * 0.4 * SR), 3))
    e = np.clip(e / max(e.max(), 1e-9) * sens, 0, 1) * (1 - floor) + floor
    return morph_lp(seg, lo, hi, e, bands=bands, res=res)


def pedal(seg, per_bar=0.5, lo=380.0, hi=2400.0, res=5.5, phase=0.0, bands=9,
          mix=0.85):
    """A wah pedal being rocked. Not a lowpass sweep: the ear tracks the
    RESONANT PEAK travelling up and down, and a wah with the resonance turned
    off is just a tone control. `per_bar` is how many bars one rock takes -
    half a bar is a foot moving at a comfortable rate."""
    n = len(seg)
    t = np.arange(n) / SR
    rate = BPM / 60.0 / (4.0 * per_bar)
    env = 0.5 - 0.5 * np.cos(2 * np.pi * rate * t + phase)
    wet = morph_lp(seg, lo, hi, env, bands=bands, res=res)
    return (seg * (1 - mix) + wet * mix).astype(np.float32)


# ---- the suitcase ----
@cached
def suitcase(notes, dur_steps=8, level=1.0, vel=0.8, take=0, bark=1.0,
             ring=2.2):
    """A Rhodes. A hammer throws a tine at a tonebar and a pickup listens: an
    almost pure sine that lasts, with a bell on the front of it that does not.

    Velocity does not change the volume here so much as the TIMBRE - hit it
    softly and it is a sine, hit it hard and the tine bends towards the
    pickup and barks. That is why this instrument sounds played and a sampled
    one from the same decade does not."""
    n, t = steps(dur_steps, floor=int(0.3 * SR))
    rng = np.random.default_rng(340 + take)
    x = np.zeros(n)
    for nt in notes:
        f = midi(nt)
        ph = 2 * np.pi * f * t * (1 + 0.0007 * rng.random())
        x += np.sin(ph) * np.exp(-t / ring)
        x += 0.30 * np.sin(2 * ph) * np.exp(-t / (ring * 0.35))
        # the tine's own inharmonic partials - a struck bar, not a string
        x += 0.42 * vel * np.sin(ph * 4.22) * np.exp(-t / (0.09 + 0.05 * vel))
        x += 0.20 * vel * np.sin(ph * 9.6) * np.exp(-t / 0.035)
        x += bark * 0.28 * vel ** 2 * np.sin(3 * ph) * np.exp(-t / 0.13)
    x = np.tanh((1.0 + 0.9 * vel) * x / max(len(notes), 1))
    out = lp(stereo(x), 3200 + 3400 * vel)
    trem = 1 + 0.16 * np.sin(2 * np.pi * 5.4 * t + rng.random() * 6)
    out[:, 0] *= trem
    out[:, 1] *= 2 - trem                    # the suitcase pans, it does not tremolo
    return (out * adsr(n, a=0.003, r=0.05)[:, None]).astype(np.float32) * level * 0.5


# ---- the vocoder ----
# Sixteen bandpasses across the carrier, each one turned up or down by how
# much energy the voice has in that band. The formants come from the vowel
# table, so the "voice" is written rather than recorded - which is the only
# part of this that is not how a real one works.
_VOC_BANDS = np.geomspace(180.0, 7000.0, 16)


def _vowel_gains(vowel, unvoiced=0.0):
    fc = _VOC_BANDS
    g = np.full(16, 0.06)
    for f, a, w in zip(FORMANTS[vowel], (1.0, 0.85, 0.5), (0.30, 0.34, 0.40)):
        g += a * np.exp(-(np.log(fc / f) / w) ** 2)
    if unvoiced:                                    # s, sh, t - noise, up top
        g += unvoiced * np.exp(-(np.log(fc / 5200.0) / 0.55) ** 2)
    return g / g.max()


@cached
def vocoder(notes, phrase, dur_steps=16, level=1.0, take=0, buzz=0.35,
            bright=1.0):
    """A chord that talks. `notes` is the carrier chord, `phrase` is
    (step, vowel) - and because the carrier is a chord and not one note, the
    words come out harmonised, which no talkbox can do."""
    n, t = steps(dur_steps)
    rng = np.random.default_rng(260 + take)
    car = np.zeros(n)
    for nt in notes:
        f = midi(nt)
        for d in (0.995, 1.0, 1.006):
            car += 2 * (((f * d * t + rng.random()) % 1.0)) - 1
    car = car / max(len(notes) * 3, 1)
    car = car + buzz * rng.standard_normal(n) * 0.25         # the sibilance path
    st = stereo(car)

    evs = sorted(phrase)
    edge = [min(int(s_ * STEP), n - 1) for s_, _ in evs] + [n]
    G = np.zeros((n, 16))
    for i, (_, v) in enumerate(evs):
        G[edge[i]:edge[i + 1]] = _vowel_gains(v, unvoiced=0.5 if v == 'ss' else 0.0)
    k = max(int(0.040 * SR), 3)
    for j in range(16):
        G[:, j] = uniform_filter1d(G[:, j], k)

    out = np.zeros((n, 2), dtype=np.float32)
    for j, fc in enumerate(_VOC_BANDS):
        b = bandpass(st, fc * 0.80, fc * 1.25, order=2)
        out += (b * G[:, j:j + 1]).astype(np.float32) * (1.0 if fc < 4000 else bright)
    amp = np.zeros(n)
    for i in range(len(evs)):
        a, b = edge[i], edge[i + 1]
        seg = np.ones(b - a)
        r = min(int(0.03 * SR), (b - a) // 2)
        if r > 1:
            seg[-r:] *= np.linspace(1, 0.3, r)
        amp[a:b] = seg
    amp = uniform_filter1d(amp, max(int(0.012 * SR), 3))
    out = np.tanh(1.8 * out * amp[:, None])
    out = out + 0.30 * bandpass(out, 2300, 3600)
    return norm(out * adsr(n, a=0.004, r=0.03)[:, None], 0.9) * level * 0.55
