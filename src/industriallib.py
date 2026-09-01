"""The industrial techno layer: the rumble, the machine hall and the acid.

Sets the grid to 152 BPM - the tempo the hard end of the floor runs at - and
adds what this genre is actually made of, none of which lives in core.

The kick is only half the kick. The other half is `rumble()`: the same hit
thrown into a short dark room, band-limited to the growl and driven, then
ducked by the kick that made it. That tail is what fills the gap between two
kicks at 152 BPM, and it is the reason a modern hard techno record sounds
like one continuous machine rather than four hits per bar.

The melody is not played by an instrument. `grind()` tunes resonant bands to
the root and lets broadband noise through them, and `acidline()` renders a
whole bar of 303 as one monophonic voice so slides really slide - the
oscillator never restarts - through one moving resonant lowpass. Between them
sit the things a factory makes: struck plates, a drop forge, escaping steam,
a stepper motor and an air-raid siren.

Usage:
    from industriallib import *
    s = Session(64, tail=3.0)
    t = s.pos(0, 0); s.hit(t)
    s.place(t, techkick(), bus='drums')
    s.place(t, rumble(), bus='rumble')
    s.place(s.pos(0), acidline(ACID_A), bus='acid')
    s.render('industrial_something_152.wav', drive=1.3, limit=0.9)
"""
import numpy as np
import core
from core import *
from scipy.signal import fftconvolve, butter, sosfiltfilt, resample_poly

BAR, STEP = core.set_grid(bpm=152)
BPM = core.BPM

def set_tempo(bpm, beats=4):
    """Re-grid the module. 152 is this genre's tempo and the import sets it,
    but the palette is not tied to it - a slower, heavier piece wants the same
    machine shop. A bare core.set_grid() is not enough: this module keeps its
    own BAR/STEP, and every cached segment was rendered against the old grid,
    so both have to move together."""
    global BAR, STEP, BPM
    BAR, STEP = core.set_grid(bpm=bpm, beats=beats)
    BPM = core.BPM
    core._SEG_CACHE.clear()
    return BAR, STEP

# The rumble is a bass instrument: it has to move out of the way of the hit
# that made it, or the two sum into one long smear.
Session.DUCKED = {'bass': 1.0, 'rumble': 0.9, 'acid': 0.35, 'music': 0.55,
                  'air': 0.45, 'pad': 0.8}

# ---- utilities ----
def bus_reverb(buf, decay=2.0, wet=0.25, tone=4000, block_bars=24):
    """Reverb across a whole bus, one block at a time (overlap-add), so a
    six-minute buffer never asks for a six-minute FFT."""
    n = len(buf)
    out = np.array(buf, dtype=np.float32, copy=True)
    ir = core._reverb_ir(decay, tone)
    step_n = max(int(block_bars * BAR), 1)
    for a in range(0, n, step_n):
        seg = buf[a:a + step_n]
        if np.abs(seg).max() < 1e-5:
            continue
        for c in range(2):
            y = fftconvolve(seg[:, c], ir[:, c])
            e = min(a + len(y), n)
            out[a:e, c] += (wet * y[:e - a]).astype(np.float32)
    return out

# ---- the kick ----
@cached
def techkick(dur_steps=2.2, tune=43.65, rise=3.2, tau=0.019, drive=6.5, decay=0.19,
             body=1.1, mid=1.6, click=1.0, grit=0.35, tone=7000, gain=1.0,
             ctone=2100.0, ctrack=0.0, cdecay=0.0028, cseed=7):
    """The floor. A sine dives onto `tune` and is driven, EQ'd and driven
    again - every stage after an EQ makes new harmonics, and that is where a
    techno kick gets its bite without getting longer. Shorter and less shrill
    than a hardstyle kick: this one has to leave room for the rumble."""
    n, t = steps(dur_steps)
    f = tune * (1 + rise * np.exp(-t / tau))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.tanh(drive * np.sin(ph))                              # stage 1
    x = lp(stereo(x), tone)
    x = x + body * bandpass(x, tune * 0.75, tune * 2.2)          # the chest
    x = x + mid * bandpass(x, 220, 1500)                         # the part you hear
    x = np.tanh(2.0 * x / (1 + mid * 0.4))                       # stage 2
    if grit:
        # This layer is two waveshapers in series - a hard tanh on a swept
        # saw, then a wavefolder - and a waveshaper makes harmonics without
        # asking whether they fit under Nyquist. `ph` here is the KICK's
        # phase, which starts (1+rise) times higher than `tune`, so the saw
        # is momentarily at 163 Hz and its partials reach 68 kHz. Measured
        # against an 8x reference, computing this at 1x has -21 dB of
        # aliasing error: 9% of the layer arriving as inharmonic fizz on the
        # attack of every kick, and identical on every one of them, which is
        # what a metronome is. At 4x the error is -34 dB.
        OS = 4
        sr = SR * OS
        t4 = np.arange(n * OS) / sr
        f4 = tune * (1 + rise * np.exp(-t4 / tau))
        ph4 = 2 * np.pi * np.cumsum(f4) / sr
        g = np.tanh(6 * saw_ph(ph4, tune * 11 * (1 + rise), nyq=sr * 0.45, kmax=60))
        g = np.stack([g, g], 1).astype(np.float32)
        g = sosfiltfilt(butter(2, [350, 5200], 'band', fs=sr, output='sos'),
                        g, axis=0).astype(np.float32)
        g = fold(g * np.exp(-t4 / 0.035)[:, None], 1.0)
        g = np.stack([resample_poly(g[:, c], 1, OS) for c in range(2)],
                     1)[:n].astype(np.float32)
        x = x + grit * g
    x = x * np.exp(-t / decay)[:, None]
    if click:
        # The beater. Half of it is a noise burst and half is tonal, and the
        # tonal half is where a kick turns into a metronome: a sine at a
        # FIXED frequency, the same pitch and the same length on every beat,
        # a thousand times in a record, is exactly what a metronome is - and
        # `cseed` fixed at 7 meant every kick got the same noise as well, so
        # there was not even variation to hide it behind.
        #
        # `ctrack` ties that tone to the kick's own phase instead. At 1.0 it
        # starts at (1+rise) x ctone and falls with the drum, which is what a
        # beater exciting the head actually does, and it stops being a pitch
        # the ear can lock onto. `cseed` varies the noise per hit.
        c = np.random.RandomState(cseed).randn(n) * np.exp(-t / 0.0016) * 0.9
        cph = (1 - ctrack) * (2 * np.pi * ctone * t) + ctrack * (ph * (ctone / tune))
        c += np.sin(cph) * np.exp(-t / cdecay) * 0.45
        x = x + hp(stereo(c), 2500) * 0.5 * click
    return norm(hp(x, 30) * adsr(n, a=0.0004, r=0.012)[:, None], 0.97) * gain

@cached
def rumble(dur_steps=8, tune=43.65, decay=1.1, tone=210, drive=2.6, tilt=48,
           gain=1.0, seed=0):
    """The other half of the kick: the room it is standing in. The hit goes
    into a short dark reverb, everything above the growl is thrown away and
    what is left is driven until it is a continuous tone. Put it on the
    'rumble' bus so the next kick ducks it - that pumping IS the groove."""
    k = techkick.uncached(dur_steps=2.0, tune=tune, decay=0.16, grit=0.0, click=0.0)
    r = reverb(lp(k, tone * 3.0), decay=decay, wet=1.0, tone=tone, predelay=0.004)
    n, _ = steps(dur_steps)
    r = r[:n] if len(r) >= n else np.pad(r, ((0, n - len(r)), (0, 0)))
    r = bandpass(r, tilt, tone * 2.0)
    # Normalise BEFORE the drive. The convolution leaves peaks around 6.0, so
    # a bare tanh() here is not saturation - it is hard-clipping a reverb
    # tail, and a reverb tail is noise. Clipped noise crackles like a fire,
    # which is exactly what it sounded like.
    r = r / max(float(np.abs(r).max()), 1e-9) * 0.85
    r = np.tanh(drive * r) / np.tanh(drive)
    # And a rumble is a rumble: whatever the drive put up top is not part of
    # it. Everything above the growl goes.
    r = lp(r, tone * 1.5, order=4)
    t = np.arange(n) / SR
    return (r * np.exp(-t / (decay * 0.85))[:, None] * adsr(n, a=0.004, r=0.05)[:, None]
            * gain * 0.55).astype(np.float32)

def kickroll(s, b, steps_, bus='drums', gain=1.0, tune=43.65, climb=0.0, **kw):
    """A run of kicks across the bar, optionally climbing in pitch."""
    for i, st in enumerate(steps_):
        u = i / max(len(steps_) - 1, 1)
        t = s.pos(b, st)
        s.hit(t)
        s.place(t, techkick(tune=tune * (1 + climb * u), **kw), gain, bus)

# ---- the kit ----
@cached
def metalhat(dur_steps=0.7, open_=False, gain=1.0, tone=1.0, grit=0.5):
    """Not an 808 hat: six inharmonic squares tuned to nothing in particular,
    driven, then highpassed. Industrial hats are metal, not sizzle."""
    n, t = steps(dur_steps if not open_ else max(dur_steps, 3.2))
    parts = (317.0, 431.0, 587.0, 743.0, 941.0, 1231.0)
    x = sum(square(f * tone, t) for f in parts) / 6
    x = x + np.random.RandomState(3).randn(n) * 0.45
    x = np.tanh((1.5 + grit * 4) * x)
    out = hp(stereo(x), 6200 if open_ else 8200)
    dec = 0.26 if open_ else 0.021
    return out * (np.exp(-t / dec) * adsr(n, a=0.0004, r=0.008))[:, None] * gain * 0.5

@cached
def distclap(dur_steps=3.0, gain=1.0, spread=1.0, drive=3.0, room=0.5):
    """Four noise bursts into a gated room, then driven flat. The backbeat
    of a genre that does not believe in snares."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(11)
    burst = np.zeros(n)
    for d in (0.0, 0.010, 0.020, 0.031):
        k = int(d * SR)
        burst[k:] += rs.randn(n - k) * np.exp(-np.arange(n - k) / SR / 0.012)
    body = bandpass(stereo(burst), 900, 6500)
    tail = bandpass(stereo(rs.randn(n)), 1300, 5200) * np.exp(-t / 0.075)[:, None] * room
    out = np.tanh(drive * (body + tail)) / np.tanh(drive)
    return widen(out, 0.5 * spread) * adsr(n, a=0.0008, r=0.02)[:, None] * gain * 0.5

@cached
def anvil(note=60, dur_steps=3.0, gain=1.0, ring=0.6, decay=0.16, bright=1.0, seed=0):
    """Struck metal. Six partials at irrational ratios - a plate, not a bell -
    ring-modulated against each other and hit with a noise transient. The
    sound of a pipe in a machine hall, and the only pitched percussion here."""
    n, t = steps(dur_steps)
    f = midi(note)
    parts = ((1.0, 1.0), (1.732, 0.7), (2.414, 0.55), (3.163, 0.4),
             (4.271, 0.3), (5.836, 0.22), (7.414, 0.14))
    x = np.zeros(n)
    for i, (p, a) in enumerate(parts):
        x += a * np.sin(2 * np.pi * f * p * t) * np.exp(-t / (decay / (1 + i * 0.55)))
    if ring:
        x = x * (1 - ring) + ring * x * np.sin(2 * np.pi * f * 1.37 * t)
    x += np.random.RandomState(seed + 17).randn(n) * np.exp(-t / 0.0022) * 1.2
    out = bandpass(stereo(np.tanh(1.8 * x)), max(f * 0.7, 160), min(f * 14 * bright, 15000))
    out += 0.4 * hp(out, f * 3.2)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0006))
    return out * adsr(n, a=0.0008, r=0.02)[:, None] * gain * 0.45

@cached
def hammer(dur_steps=8, tune=44.0, gain=1.0, metal=1.0, steamy=0.6, seed=0):
    """The drop forge: a low thud, a sheet of metal answering it a few
    milliseconds later, and the press letting go. One per phrase, no more."""
    n, t = steps(dur_steps)
    f = tune * (1 + 5.0 * np.exp(-t / 0.014))
    thud = np.tanh(3.0 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t / 0.28)
    out = stereo(thud)
    if metal:
        k = int(0.012 * SR)
        m = np.zeros(n)
        for p, a in ((1.0, 1.0), (2.756, 0.6), (4.13, 0.4), (6.31, 0.25), (9.7, 0.15)):
            m[k:] += a * np.sin(2 * np.pi * 186 * p * t[:n - k]) * np.exp(-t[:n - k] / (0.6 / p))
        out += metal * bandpass(stereo(np.tanh(1.4 * m)), 300, 9000) * 0.5
    if steamy:
        rs = np.random.RandomState(seed + 41)
        u = np.clip((t - 0.10) / 0.5, 0, 1)
        hiss = hp(stereo(rs.randn(n)), 3000) * (np.exp(-np.maximum(t - 0.10, 0) / 0.34) * (u > 0))[:, None]
        out += steamy * hiss * 0.35
    return widen(out * adsr(n, a=0.0006, r=0.05)[:, None], 0.7) * gain * 0.7

@cached
def steam(dur_steps=6, gain=1.0, f0=700.0, f1=7000.0, seed=0):
    """A pressure release: noise through a filter that opens fast and slams
    shut. Fills a bar-end without pretending to be a drum fill."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 61)
    nz = stereo(rs.randn(n))
    u = np.clip(t / (0.22 * t[-1]), 0, 1) ** 0.6
    u = u * np.exp(-np.maximum(t - 0.22 * t[-1], 0) / (0.3 * t[-1]))
    x = morph_lp(hp(nz, 400), f0, f1, u, bands=6)
    return widen(x, 1.1) * (u ** 0.8)[:, None] * gain * 0.5

@cached
def servo(dur_steps=4, rate=26.0, accel=2.4, note=72, gain=1.0, rmax=340.0, seed=0):
    """A stepper motor. Very short metallic clicks whose repetition rate
    accelerates - machine percussion, and the cheapest way to raise rhythmic
    density without adding a drum.

    `rmax` is the motor's top speed, and it is not cosmetic. The gap between
    two clicks is 1/r and r grows geometrically, so the gaps are a geometric
    series: for a slow start and a hard acceleration that series CONVERGES,
    and if it converges to less than the segment's length the loop placing the
    clicks never reaches the end and never terminates. rate=11, accel=3.2 over
    2.1 s converges at 1.9 s and hangs. A real stepper reaches its top speed
    and stays there, which is both the physical behaviour and the bound."""
    n, t = steps(dur_steps)
    dur_s = n / SR
    ts, cur, r = [], 0.0, rate
    while cur < dur_s:
        ts.append(cur)
        cur += 1.0 / r
        r = min(r * accel ** (1.0 / max(rate * dur_s, 1)), rmax)
    x = np.zeros(n)
    f = midi(note)
    rs = np.random.RandomState(seed + 5)
    for i, c in enumerate(ts):
        k = int(c * SR)
        m = min(int(0.010 * SR), n - k)
        if m <= 4:
            break
        tt = np.arange(m) / SR
        x[k:k + m] += (np.sin(2 * np.pi * f * (1 + 0.02 * i) * tt) + rs.randn(m) * 0.7) \
            * np.exp(-tt / 0.0018)
    out = bandpass(stereo(np.tanh(2.2 * x)), 1800, 11000)
    return out * adsr(n, a=0.002, r=0.02)[:, None] * gain * 0.5

# ---- the machine hall ----
@cached
def grind(dur_steps=16, note=41, gain=1.0, res=1.0, lfo=0.14, crush=0, seed=0,
          partials=(1.0, 2.0, 3.0, 4.03, 6.05, 8.1)):
    """The room tone of a factory. Broadband noise squeezed through resonant
    bands tuned to the root, each breathing on its own slow LFO. It is
    pitched, and nothing played it - which is the whole trick in a genre with
    no chords."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 101)
    nz = stereo(rs.randn(n) * 0.9)
    f = midi(note)
    out = np.zeros((n, 2), dtype=np.float32)
    for i, p in enumerate(partials):
        fc = f * p
        if fc > SR * 0.42:
            break
        b = bandpass(nz, fc * 0.94, fc * 1.06, order=2)
        breath = 0.35 + 0.65 * (0.5 - 0.5 * np.cos(
            2 * np.pi * (lfo * (0.7 + 0.3 * i)) * t + rs.rand() * 6))
        out += b * (breath / (1 + i * 0.55))[:, None]
    out = np.tanh(2.4 * res * out)
    if crush:
        out = bitcrush(out, bits=crush, downsample=3)
    out = hp(out, 60)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0021))
    env = np.ones(n)
    a = min(int(0.4 * SR), n // 2); r = min(int(0.5 * SR), n // 2)
    env[:a] = np.linspace(0, 1, a); env[-r:] *= np.linspace(1, 0, r)
    return out * env[:, None] * gain * 0.4

@cached
def tunnel(dur_steps=32, note=29, gain=1.0, motor=0.25, seed=0):
    """Deep drone with a motor in it: sine layers plus a slow amplitude pulse,
    so the low end is never actually still."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 13)
    f = midi(note)
    x = np.zeros(n)
    for mult, amp, rate in ((1.0, 1.0, 0.037), (1.5, 0.35, 0.053), (2.0, 0.28, 0.041),
                            (3.01, 0.14, 0.067), (4.02, 0.08, 0.083)):
        breath = 0.6 + 0.4 * np.sin(2 * np.pi * rate * t + rs.rand() * 6)
        x += amp * np.sin(2 * np.pi * f * mult * t + rs.rand() * 6) * breath
    if motor:
        x *= 1 - motor * (0.5 - 0.5 * np.cos(2 * np.pi * (BPM / 60) * t))
    x += 0.18 * lp(stereo(rs.randn(n)), 220)[:, 0]
    out = stereo(np.tanh(x / 1.7))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0024))
    env = np.ones(n)
    a = min(int(1.6 * SR), n // 2); r = min(int(2.0 * SR), n // 2)
    env[:a] = np.linspace(0, 1, a); env[-r:] *= np.linspace(1, 0, r)
    return out * env[:, None] * gain * 0.5

# ---- the acid ----
def _line_envelopes(pattern, n, decay, cut_decay, acc_amt):
    """amplitude, cutoff and instantaneous-frequency arrays for a whole bar"""
    fs = np.zeros(n); amp = np.zeros(n); cut = np.zeros(n)
    prev_f = None
    for (st, note, dur, acc, slide) in pattern:
        a = int(st * STEP); b = min(int((st + dur) * STEP), n)
        if a >= n:
            continue
        m = b - a
        tt = np.arange(m) / SR
        f = midi(note)
        if slide and prev_f is not None:
            fs[a:b] = f + (prev_f - f) * np.exp(-tt / 0.045)
        else:
            fs[a:b] = f
        lvl = 1.0 if not acc else 1.0 + acc_amt
        amp[a:b] = np.maximum(amp[a:b], lvl * np.exp(-tt / (decay * (0.75 if acc else 1.0)))
                              * np.minimum(tt / 0.003, 1))
        c = (0.62 + (0.38 if acc else 0.0)) * np.exp(-tt / (cut_decay * (1.5 if acc else 1.0)))
        cut[a:b] = np.maximum(cut[a:b], c)
        prev_f = f
    fs[fs == 0] = midi(pattern[0][1]) if pattern else 100.0
    return fs, amp, cut

def acidline(pattern, dur_bars=1, f_lo=170, f_hi=3800, res=3.2, decay=0.18,
             cut_decay=0.11, drive=3.4, gain=1.0, wave='saw', acc_amt=0.55,
             bands=9, sub=0.0, base=0.06, low=170, knob=None):
    """A whole bar of 303 as one continuous monophonic voice. The oscillator
    never restarts, so a slide really slides; accents open the filter further
    and hit harder; the bar goes through one moving resonant lowpass.

    pattern: list of (step, note, dur_steps, accent, slide)
    knob:    the cutoff control, swept across the whole call. Any number of
             points, interpolated - (0.3, 1.0) opens, (0.3, 1.0, 0.4) opens
             and closes again. This is the knob a player has their hand on.

    Render a PHRASE per call, not a bar. The oscillator phase is continuous
    inside one call and restarts between calls, so a line cut into bars and
    re-rendered every 16 steps has a waveform discontinuity on every bar line
    - a click, sitting at the top of the spectrum where it is most audible.
    Eight or sixteen bars at a time, with `knob` doing the movement.
    """
    n = int(round(dur_bars * BAR))
    fs, amp, cut = _line_envelopes(pattern, n, decay, cut_decay, acc_amt)
    ph = 2 * np.pi * np.cumsum(fs) / SR
    top = float(fs.max())
    x = saw_ph(ph, top, kmax=48) if wave == 'saw' else \
        (2 / np.pi) * sum(np.sin(k * ph) / k for k in range(1, 40, 2)) * 2
    if sub:
        x = x + sub * np.sin(0.5 * ph)
    # Smooth the cutoff envelope before it drives the filter bank. morph_lp
    # crossfades static filters by this value, so a step in it swaps the
    # filter mid-waveform - a discontinuity, and at the top of the spectrum
    # where it is most audible. 4 ms is far shorter than any 303 envelope and
    # removes the artefact completely.
    cut = uniform_filter1d(cut, max(int(0.004 * SR), 3))
    if knob is not None:
        k = np.atleast_1d(np.asarray(knob, dtype=np.float64))
        if len(k) == 1:
            cut = cut * k[0]
        else:
            cut = cut * np.interp(np.linspace(0, 1, n), np.linspace(0, 1, len(k)), k)
    st = stereo(x * amp)
    out = morph_lp(st, f_lo, f_hi, base + (1 - base) * cut, bands=bands, res=res)
    out = np.tanh(drive * out / (1 + res * 0.45))
    out = hp(out, low, order=4)                     # the sub belongs to the kick
    # Dead centre, deliberately. A 0.7 ms Haas delay here reads as width on
    # headphones and combs -14 dB out of 600-850 Hz the moment a club system
    # sums the low end - and this line is the hook. Width comes from the
    # reverb send instead, which is decorrelated rather than delayed.
    return fade_edges(out.astype(np.float32), 2.0) * gain * 0.75

@cached
def _acid_cached(key, dur_bars, **kw):
    return acidline(list(key), dur_bars, **kw)

def acid(pattern, dur_bars=1, **kw):
    """cached acidline - the same bar is played dozens of times"""
    return _acid_cached(tuple(tuple(p) for p in pattern), dur_bars, **kw)

# ---- stabs, bass, voices ----
@cached
def stab(notes, dur_steps=1.6, gain=1.0, drive=7.0, lo=280, hi=5200, metal=0.35,
         decay=0.075, seed=0):
    """A chord treated as percussion: saws hard-clipped, band-limited so it
    sits above the kick, with a metallic transient welded onto the front."""
    n, t = steps(dur_steps)
    x = np.zeros(n)
    for f in notes:
        for d in (0.994, 1.0, 1.006):
            x += saw(f * d, t, phase=np.random.RandomState(seed + int(f)).rand() * 6)
    x = np.tanh(drive * x / (len(notes) * 2))
    out = bandpass(stereo(x), lo, hi)
    if metal:
        rs = np.random.RandomState(seed + 23)
        tr = bandpass(stereo(rs.randn(n)), 1800, 9000) * np.exp(-t / 0.006)[:, None]
        out = out + metal * tr * 1.4
    # same reasoning as the acid: the stab is a hook, so it stays centred
    env = (0.35 + 0.65 * np.exp(-t / decay)) * np.exp(-t / (decay * 3.2)) * adsr(n, a=0.0015, r=0.02)
    return out * env[:, None] * gain * 0.55

@cached
def distbass(note=29, dur_steps=2.0, gain=1.0, cutoff=430, drive=4.5, swell=0.8,
             tail=0.014):
    """The offbeat: a driven saw+sine that swells into the gap the kick left
    and is cut off by the next one."""
    n, t = steps(dur_steps)
    f = midi(note)
    x = saw(f, t) * 0.65 + np.sin(2 * np.pi * f * t) + 0.35 * saw(f * 2.004, t)
    out = lp(stereo(np.tanh(drive * x / 2.0)), cutoff)
    env = np.linspace(0, 1, n) ** swell
    k = min(int(tail * SR), n // 2)
    env[-k:] *= np.linspace(1, 0, k)
    return out * env[:, None] * gain * 0.6

@cached
def alarm(dur_steps=32, f0=185.0, f1=520.0, cycles=2.0, gain=1.0, drive=2.6,
          tone=3200, seed=0):
    """Air-raid siren: a motor winding a horn up and back down. Harmonically
    rich enough to read over a full drop, slow enough to be dread."""
    n, t = steps(dur_steps)
    u = 0.5 - 0.5 * np.cos(2 * np.pi * cycles * t / max(t[-1], 1e-9))
    f = f0 * (f1 / f0) ** u
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = sum(np.sin(k * ph) / k for k in (1, 2, 3, 4, 5, 7))
    x = np.tanh(drive * x)
    out = lp(stereo(x), tone)
    out += 0.25 * bandpass(stereo(np.random.RandomState(seed + 71).randn(n)), 900, 4000) \
        * (0.3 + 0.7 * u)[:, None]
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0018))
    env = adsr(n, a=0.18, r=0.35) * (0.45 + 0.55 * u)
    return widen(out, 1.2) * env[:, None] * gain * 0.4

@cached
def screamer(dur_steps=6, note=57, gain=1.0, vowel='eh', drive=5.0, crush=0,
             fall=0.0, seed=0):
    """A voice put through the machine: formants over a pitch drop, clipped
    and optionally bit-reduced until you can hear that it was human and not
    what it said."""
    n, t = steps(dur_steps)
    f0 = midi(note)
    f = f0 * (1 + 0.30 * np.exp(-t / 0.06))
    if fall:
        k = int(n * 0.6)
        f[k:] *= 2 ** (-fall / 12 * np.linspace(0, 1, n - k))
    ph = 2 * np.pi * np.cumsum(f * (1 + 0.02 * np.sin(2 * np.pi * 5.4 * t))) / SR
    rs = np.random.RandomState(seed + 91)
    x = saw_ph(ph, f0 * 2.2) + rs.randn(n) * 0.22
    st = stereo(x)
    out = sum(bandpass(st, fc * 0.70, fc * 1.38) * g
              for fc, g in zip(FORMANTS[vowel], (1.0, 0.85, 0.5)))
    out = np.tanh(drive * out)
    if crush:
        out = bitcrush(out, bits=crush, downsample=2)
    env = np.exp(-t / (0.22 * max(dur_steps / 6, 0.5))) * adsr(n, a=0.008, r=0.06)
    return widen(out, 0.9) * env[:, None] * gain * 0.55

@cached
def blip(note=84, dur_steps=0.6, gain=1.0, ring=1.62):
    """Modular bleep: a sine ping with an inharmonic ring on it. The machine
    talking to itself in the gaps."""
    n, t = steps(dur_steps)
    f = midi(note)
    x = np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * ring * t)
    x = x * np.exp(-t / 0.055)
    out = hp(stereo(np.tanh(1.6 * x)), 500)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0011))
    return out * adsr(n, a=0.0008, r=0.02)[:, None] * gain * 0.5

# ---- fx ----
def gate(seg, rate_steps=1.0, duty=0.5, depth=1.0, soft=0.004):
    """Trance gate: chop a held sound onto the grid."""
    n = len(seg)
    period = max(int(rate_steps * STEP), 8)
    on = int(period * duty)
    env = np.zeros(n)
    k = max(int(soft * SR), 2)
    for a in range(0, n, period):
        b = min(a + on, n)
        env[a:b] = 1.0
        if b - a > 2 * k:
            env[a:a + k] = np.linspace(0, 1, k)
            env[b - k:b] = np.linspace(1, 0, k)
    return (seg * (1 - depth * (1 - env))[:, None]).astype(np.float32)

def stutter(seg, slice_steps=1.0, repeats=4, decay=1.0, accel=1.0):
    """Beat repeat: take the head of a segment and fire it again, faster and
    quieter each time. The last two beats before a drop."""
    k = max(int(slice_steps * STEP), 64)
    head = fade_edges(seg[:k], 1.5)
    out = []
    step_k = k
    for i in range(repeats):
        step_k = max(int(k / (accel ** i)), 128)
        piece = head[:step_k] if step_k <= len(head) else np.pad(head, ((0, step_k - len(head)), (0, 0)))
        out.append(piece * (decay ** i))
    return np.concatenate(out).astype(np.float32)


# ---- the voices in the shaft ----
@cached
def labourchoir(notes, dur_steps=16, gain=1.0, vowel='oh', size=1.25, voices=4,
                spread=20.0, rasp=0.16, sag=35.0, breath=0.14, attack=0.5, seed=0):
    """A choir of men nine hours into a shift.

    `size` divides the formants. A vocal tract scaled up does not read as a
    lower voice, it reads as a BIGGER one - same pitch, larger body - which is
    how a handful of saw stacks becomes something that belongs in a room the
    size of a shaft. That single number is most of the grotesque.

    `spread` is how far apart the voices are tuned, in cents, because a crowd
    does not agree; `sag` is how many cents the whole choir drifts flat across
    the phrase, because nobody is holding it up any more; `rasp` is the edge on
    a voice that has spent the day shouting over machinery."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 301)
    u = t / max(t[-1], 1e-9)
    drift = 2 ** (-(sag / 1200) * u ** 1.4)                  # the shift wearing them down
    # Width comes from spreading the singers across the field, never from a
    # Haas delay: this choir lives at 200-800 Hz and a 1.6 ms delay puts its
    # first comb notch at 312 Hz, straight through the middle of it. Detuned
    # voices at different pan positions are wide and survive a mono sum.
    l = np.zeros(n); r = np.zeros(n)
    total = max(voices * len(notes), 1)
    idx = 0
    for f in notes:
        for v in range(voices):
            cents = spread * (v - (voices - 1) / 2) / max((voices - 1) / 2, 1)
            cents += rs.uniform(-spread * 0.35, spread * 0.35)
            vib = 1 + rs.uniform(0.004, 0.011) * np.sin(
                2 * np.pi * rs.uniform(4.1, 5.9) * t + rs.rand() * 6) * np.minimum(t / 0.6, 1)
            ph = 2 * np.pi * np.cumsum(f * 2 ** (cents / 1200) * drift * vib) / SR
            sig = saw_ph(ph, f * 1.6, kmax=30)
            ang = ((idx / max(total - 1, 1)) * 1.7 - 0.85 + 1) * np.pi / 4
            l += sig * np.cos(ang); r += sig * np.sin(ang)
            idx += 1
    st = (np.stack([l, r], 1) / total).astype(np.float32)
    out = sum(bandpass(st, fc / size * 0.68, fc / size * 1.42) * g
              for fc, g in zip(FORMANTS[vowel], (1.0, 0.75, 0.4)))
    if breath:
        out = out + breath * bandpass(stereo(rs.randn(n)), 600, 4200) * \
            (0.35 + 0.65 * (0.5 - 0.5 * np.cos(2 * np.pi * 0.35 * t)))[:, None] * 0.35
    if rasp:
        out = (1 - rasp) * out + rasp * np.tanh(3.5 * out)
    a = min(int(attack * SR), n // 2); r = min(int(0.6 * SR), n // 2)
    env = np.ones(n); env[:a] = np.linspace(0, 1, a) ** 1.6; env[-r:] *= np.linspace(1, 0, r) ** 0.8
    return out * env[:, None] * gain * 1.5

@cached
def groan(note=48, dur_steps=12, gain=1.0, fall=2.5, vowel='uh', size=1.35,
          rasp=0.28, seed=0):
    """One voice giving up. The pitch sags a couple of semitones across the
    note and the vibrato widens as it goes - a groan IS a falling intonation,
    and that is the whole difference between a groan and a held note."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 331)
    u = t / max(t[-1], 1e-9)
    f = midi(note) * 2 ** (-fall / 12 * u ** 2.2)
    vib = 1 + (0.004 + 0.016 * u) * np.sin(2 * np.pi * (4.4 + 1.2 * u) * t)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    x = saw_ph(ph, midi(note) * 1.8, kmax=26) + rs.randn(n) * 0.10
    st = stereo(x)
    out = sum(bandpass(st, fc / size * 0.66, fc / size * 1.45) * g
              for fc, g in zip(FORMANTS[vowel], (1.0, 0.8, 0.45)))
    out = (1 - rasp) * out + rasp * np.tanh(3.0 * out)
    env = adsr(n, a=0.12, r=0.45) * (0.55 + 0.45 * np.exp(-u * 1.6))
    return norm(out * env[:, None], 0.9) * gain * 1.4      # centred: see labourchoir

@cached
def chant(note=55, dur_steps=2, gain=1.0, vowel='ah', size=1.2, rasp=0.26,
          voices=3, drop=1.2, seed=0):
    """One shouted syllable. A work song exists to put a crowd's effort on the
    same beat as the machine; this is the syllable, and the arrangement decides
    where it lands."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 353)
    u = t / max(t[-1], 1e-9)
    f0 = midi(note)
    l = np.zeros(n); r = np.zeros(n)
    for v in range(voices):
        det = 2 ** (rs.uniform(-22, 22) / 1200)
        f = f0 * det * (1 + 0.05 * np.exp(-t / 0.03)) * 2 ** (-drop / 12 * u ** 3)
        sig = saw_ph(2 * np.pi * np.cumsum(f) / SR, f0 * 1.7, kmax=24)
        ang = ((v / max(voices - 1, 1)) * 1.5 - 0.75 + 1) * np.pi / 4
        l += sig * np.cos(ang); r += sig * np.sin(ang)
    noise = rs.randn(n) * 0.11
    st = (np.stack([l + noise, r + noise], 1) / voices).astype(np.float32)
    out = sum(bandpass(st, fc / size * 0.7, fc / size * 1.4) * g
              for fc, g in zip(FORMANTS[vowel], (1.0, 0.85, 0.5)))
    out = np.tanh((1 + rasp * 2.2) * out)   # enough edge to sound shouted, not clipped
    env = np.exp(-t / (0.09 * max(dur_steps / 2, 1))) * adsr(n, a=0.006, r=0.05)
    return out * env[:, None] * gain * 0.9                 # centred: see labourchoir

# ---- the megastructure ----
@cached
def press(dur_steps=16, tune=32.7, gain=1.0, metal=1.0, room=1.0, seed=0):
    """The big press. An octave under the forge hammer, with the structure
    ringing for a second and a half afterwards - the sound is not the impact,
    it is the building answering it."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 401)
    f = tune * (1 + 6.5 * np.exp(-t / 0.02))
    thud = np.tanh(3.5 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t / 0.45)
    out = stereo(thud)
    if metal:
        k = int(0.018 * SR)
        m = np.zeros(n)
        for p, a, d in ((1.0, 1.0, 1.5), (2.31, 0.62, 1.0), (3.77, 0.42, 0.7),
                        (5.19, 0.28, 0.45), (8.44, 0.16, 0.3)):
            m[k:] += a * np.sin(2 * np.pi * 97 * p * t[:n - k]) * np.exp(-t[:n - k] / d)
        out += metal * bandpass(stereo(np.tanh(1.3 * m)), 150, 7000) * 0.45
    if room:
        out += room * 0.5 * reverb(lp(out, 2200), decay=2.2, wet=0.9, tone=1500)[:n]
    return norm(widen(out * adsr(n, a=0.0005, r=0.1)[:, None], 0.9), 0.95) * gain * 0.6

@cached
def chains(dur_steps=4, gain=1.0, density=26, seed=0):
    """Chain dragged over steel: a scatter of short inharmonic clinks, never
    on the grid."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 431)
    x = np.zeros(n)
    for _ in range(density):
        k = int(rs.uniform(0, n * 0.92))
        m = min(int(rs.uniform(0.004, 0.016) * SR), n - k)
        if m < 8:
            continue
        tt = np.arange(m) / SR
        f = rs.uniform(900, 4200)
        x[k:k + m] += (np.sin(2 * np.pi * f * tt) + 0.6 * np.sin(2 * np.pi * f * 1.71 * tt)
                       + rs.randn(m) * 0.5) * np.exp(-tt / 0.004) * rs.uniform(0.3, 1.0)
    out = bandpass(stereo(np.tanh(1.8 * x)), 1200, 12000)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0013))
    return out * adsr(n, a=0.002, r=0.03)[:, None] * gain * 0.45

@cached
def bellow(dur_steps=32, gain=1.0, rate=0.55, seed=0):
    """Ventilation: the lungs of the building. A huge slow breath of filtered
    noise, so the room is never actually silent."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 457)
    breath = 0.5 - 0.5 * np.cos(2 * np.pi * rate * t / max(t[-1], 1e-9) * 4)
    nz = stereo(rs.randn(n))
    x = morph_lp(nz, 90, 1400, breath * 0.8 + 0.1, bands=6)
    x = x + lp(nz, 120) * 0.5
    out = widen(x, 2.2) * (0.3 + 0.7 * breath)[:, None]
    return out * adsr(n, a=0.5, r=0.8)[:, None] * gain * 0.5


# ---- acid: the 303 as the whole instrument ----
def poly_pattern(pat, cycle_steps, bars):
    """Repeat a pattern whose length is NOT 16 across `bars` bars.

    A 15-step line against a 16-step bar starts one step earlier every bar and
    only comes home after 15 of them. Nothing about the notes changes - the
    listener hears the same figure drifting against the drums and back, which
    is the cheapest way to make a loop feel like it is moving without moving.
    Give it a length coprime with 16: 15, 13, 9, 7."""
    out = []
    total = 16 * bars
    off = 0
    while off < total:
        for (st, n, d, a, sl) in pat:
            if off + st < total:
                out.append((off + st, n, d, a, sl))
        off += cycle_steps
    return out

def swirl(seg, rate=0.12, depth_ms=3.5, base_ms=1.0, mix=0.65, stages=2, seed=0):
    """Slow flanger: a delayed copy whose delay time sweeps, so the comb
    notches walk up and down the spectrum. This is what makes a static 303
    line sound like it is dissolving.

    Both channels share one LFO on purpose - a flanger with a different sweep
    per side is wider and turns into a comb filter the moment anything sums to
    mono, and this sits on the hook."""
    n = len(seg)
    t = np.arange(n) / SR
    out = seg.astype(np.float32).copy()
    ar = np.arange(n)
    for st in range(stages):
        lfo = 0.5 - 0.5 * np.cos(2 * np.pi * rate * t + st * 2.1 + seed)
        d = (base_ms + depth_ms * lfo) / 1000 * SR
        idx = np.clip(ar - d, 0, n - 1)
        dly = np.stack([np.interp(idx, ar, out[:, c]) for c in range(2)], 1)
        out = ((out + mix * dly) / (1 + mix * 0.7)).astype(np.float32)
    return out

def acid_throw(seg, steps_=3.0, times=5, fb=0.55, damp=600):
    """A delay throw for the 303: each repeat darker and narrower than the
    last, alternating sides. The oldest trick in acid and still the one that
    turns four bars into a room."""
    d = int(steps_ * STEP)
    out = np.zeros((len(seg) + d * times + 1, 2), dtype=np.float32)
    out[:len(seg)] += seg
    for i in range(1, times + 1):
        e = lp(seg, max(5200 - damp * i, 500)) * fb ** i
        e = panned(e, (0.75 if i % 2 else -0.75) * min(i / 2, 1.0))
        out[i * d:i * d + len(seg)] += e
    return out

def pitch_warp(seg, semis=(0, -2, -5), steps_=2.0, gain=1.0):
    """Chop a segment and drop each piece to a different pitch - the floor
    giving way. Used once or twice, never as a rhythm."""
    k = max(int(steps_ * STEP), 128)
    out = []
    for i, sm in enumerate(semis):
        piece = seg[i * k:(i + 1) * k]
        if len(piece) < 64:
            break
        out.append(fade_edges(pitched(piece, 2 ** (sm / 12)), 3.0) * gain)
    return np.concatenate(out).astype(np.float32) if out else seg[:0]

def autopan(seg, cycle_bars=8.0, depth=0.6, phase=0.0):
    """A slow equal-power sweep across the field.

    Movement that survives a mono sum: panning is a level difference, so
    summing gives back one signal with a gentle tremolo. Everything else that
    moves in stereo - Haas, flanging, chorus - is built from a delay, and a
    delay in mono is a comb filter. On a hook, use this."""
    n = len(seg)
    t = np.arange(n) / SR
    p = depth * np.sin(2 * np.pi * t / max(cycle_bars * BAR / SR, 1e-9) + phase)
    a = (p + 1) * np.pi / 4
    out = seg.astype(np.float32).copy()
    out[:, 0] *= np.cos(a) * 1.41
    out[:, 1] *= np.sin(a) * 1.41
    return out


# ---- hard acid ----
@cached
def hat909(dur_steps=0.6, open_=False, gain=1.0, tone=1.0, seed=0):
    """A 909-ish hat: noise band-limited, not merely highpassed.

    core's hat() keeps only what is above 8 kHz. One of those is a tick; a
    line of them on sixteenths is a continuous crackle at the top of the
    spectrum, because there is no body underneath for the ear to hear as an
    instrument. 3.8-12 kHz makes it a hi-hat again."""
    n, t = steps(dur_steps if not open_ else max(dur_steps, 2.6))
    rs = np.random.RandomState(seed + 77)
    x = bandpass(stereo(rs.randn(n)), 3800 * tone, 12000 * tone)
    dec = 0.20 if open_ else 0.028
    return x * (np.exp(-t / dec) * adsr(n, a=0.0006, r=0.008))[:, None] * gain * 0.55

def acid_hard(pattern, dur_bars=1, fold_amt=0.45, stage2=2.4, bite=0.8,
              gain=1.0, **kw):
    """The 303 put through a real distortion chain instead of one tanh.

    drive -> EQ -> drive -> fold. Every stage after an EQ makes harmonics the
    stage before it could not, which is why a chain screams and a single
    waveshaper only clips. `bite` is the band that gets re-driven - the
    200-2000 Hz an ear reads as force - and `fold_amt` is how far into the
    wavefolder it goes, which is where it stops sounding like a filter and
    starts sounding like something tearing."""
    seg = acidline(pattern, dur_bars, gain=1.0, **kw)
    seg = seg + bite * bandpass(seg, 200, 2000)                # EQ
    seg = np.tanh(stage2 * seg / (1 + bite * 0.5))             # drive it again
    if fold_amt:
        seg = (1 - fold_amt) * seg + fold_amt * fold(seg, 1.1 + fold_amt * 0.6)
    return hp(seg, 60, order=2).astype(np.float32) * gain * 0.62

def subacid(pattern, dur_bars=1, gain=1.0, sat=2.6, top=170, low=26, **kw):
    """The same line an octave down, saturated but never folded.

    A sub has room for exactly one clean thing. Saturation here is only to
    make the fundamental audible on small speakers - the 2nd and 3rd harmonics
    it generates sit at 80-250 Hz, which is what a phone reproduces and what
    the ear reconstructs the missing fundamental from."""
    pat = [(st, n - 12, d, a, sl) for st, n, d, a, sl in pattern]
    seg = acidline(pat, dur_bars, f_lo=60, f_hi=max(top * 1.6, 200), res=0.6,
                   drive=1.8, low=low, gain=1.0, **kw)
    seg = np.tanh(sat * seg) / np.tanh(sat)
    return lp(seg, top).astype(np.float32) * gain * 0.7

@cached
def resoscream(note=64, dur_steps=4, gain=1.0, res=7.0, decay=0.18, drift=0.35,
               seed=0):
    """A filter pushed until it sings on its own: a resonant band with almost
    no signal in it, swept. Not a note anybody played - the circuit's own
    pitch, which is the sound acid was named for."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 211)
    f0 = midi(note)
    f = f0 * (1 + drift * np.exp(-t / (decay * 1.6)))
    ph = 2 * np.pi * np.cumsum(f) / SR
    tone = np.sin(ph) + 0.3 * np.sin(2 * ph)
    nz = rs.randn(n) * 0.12
    x = stereo(tone * 0.9 + nz)
    out = res * bandpass(x, f0 * 0.7, f0 * 1.5) + 0.2 * x
    out = np.tanh(1.6 * out / (1 + res * 0.3))
    return out * (np.exp(-t / decay) * adsr(n, a=0.002, r=0.03))[:, None] * gain * 0.4


@cached
def industrialkick(dur_steps=2.0, tune=41.2, drive=13.0, decay=0.13, hiss=0.75,
                   ceil=0.62, air=0.55, body=1.4, gain=1.0, seed=0):
    """A kick that has been through a wall.

    Hard-clipped rather than saturated: a clipper flattens the top of the wave
    and leaves odd harmonics buzzing all the way up, where tanh rounds them
    off and stays polite. Behind the transient sits a filtered noise exhale -
    that is the 'pff', and a real industrial kick is half air. Short decay on
    purpose, because these are meant to be fired in rows."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 503)
    f = tune * (1 + 3.4 * np.exp(-t / 0.017))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR)
    x = np.clip(x * drive, -ceil, ceil) / ceil                   # hard clip, not tanh
    st = lp(stereo(x), 8000)
    st = st + body * bandpass(st, tune * 0.8, tune * 2.6)
    st = np.clip(st * 1.8, -1.0, 1.0)                            # and again
    st = norm(hp(st * np.exp(-t / decay)[:, None], 34), 0.88)
    if hiss:
        # the exhale gets its own envelope. Folded into the body's, the low
        # end wins the normalisation and the 'pff' disappears - which is what
        # happens to most attempts at this kick.
        nz = rs.randn(n)
        exhale = bandpass(stereo(nz), 800, 5600) * np.exp(-t / 0.070)[:, None]
        exhale += hp(stereo(nz), 5200) * np.exp(-t / 0.026)[:, None] * air
        exhale *= np.minimum(t / 0.0025, 1.0)[:, None]          # no click on its front
        st = st + hiss * exhale * 0.85
    return norm(st * adsr(n, a=0.0004, r=0.012)[:, None], 0.97) * gain

def kickbarrage(s, b, steps_, bus='drums', gain=1.0, tune=41.2, climb=0.0,
                duck=True, **kw):
    """A row of industrial kicks. Register every one: the pump is what makes a
    barrage read as rhythm instead of noise."""
    for i, st in enumerate(steps_):
        u = i / max(len(steps_) - 1, 1)
        t = s.pos(b, st)
        if duck:
            s.hit(t)
        s.place(t, industrialkick(tune=tune * (1 + climb * u), **kw), gain, bus)


# ---- dub techno ----
@cached
def dubchord(notes, dur_steps=2.0, gain=1.0, cutoff=1500, drift=7.0, drive=1.6,
             attack=0.008, seed=0):
    """The Basic Channel chord: a minor triad on detuned saws, filtered dark,
    struck short and thrown into a delay.

    Everything about it is slightly wrong on purpose - the voices are seven
    cents apart and drift against each other, the filter is closed far below
    where you would put a pad, and the attack is soft enough that it never
    quite starts. On its own it is a dull stab; the instrument is the chord
    plus the echo, which is why this is written to be fed to dubdelay()."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 811)
    x = np.zeros(n)
    for f in notes:
        for k, d in enumerate((-drift, 0.0, drift)):
            det = 2 ** (d / 1200) * (1 + 0.0006 * np.sin(2 * np.pi * (0.07 + 0.03 * k) * t))
            x += saw_ph(2 * np.pi * np.cumsum(f * det) / SR, f * 1.5, kmax=26)
    x /= 3 * len(notes)
    out = lp(stereo(np.tanh(drive * x)), cutoff)
    out = out + 0.3 * bandpass(out, cutoff * 0.7, cutoff * 1.4)
    a = max(int(attack * SR), 8)
    env = np.ones(n)
    env[:a] = np.linspace(0, 1, a) ** 1.4
    env *= np.exp(-t / (dur_steps * STEP / SR * 0.5))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0013))
    return out * env[:, None] * gain * 0.5

def dubdelay(seg, steps_=3.0, times=7, fb=0.62, damp=900, sat=1.4, spread=0.8):
    """A dub delay: each repeat darker, dirtier and further out than the last.

    A plain delay repeats a sound quieter. This one filters and saturates
    inside the feedback path, so the tenth repeat is a different sound from
    the first - a dark smear with no transient left - which is the whole
    point of the technique and the reason dub records sound like weather."""
    d = int(steps_ * STEP)
    out = np.zeros((len(seg) + d * times + 1, 2), dtype=np.float32)
    out[:len(seg)] += seg
    tail = seg.copy()
    for i in range(1, times + 1):
        tail = lp(tail, max(6000 - damp * i, 380))
        tail = np.tanh(sat * tail) / np.tanh(sat)
        e = tail * (fb ** i)
        e = panned(e, (spread if i % 2 else -spread) * min(i / 3, 1.0))
        a = i * d
        out[a:a + len(e)] += e
    return out


# ---- the wall ----
@cached
def glare(notes, dur_steps=38, gain=1.0, voices=3, detune=17.0, walk=8.0,
          roll=0.042, f_lo=300.0, f_hi=7200.0, open0=0.06, open1=0.9,
          curve=1.5, attack=0.32, release=0.30, drive=2.6, bite=0.8,
          fold_amt=0.22, res=0.30, air=0.5, hpf=250.0, width=1.5, seed=0):
    """The thing that arrives over the machine and does not stop it.

    An industrial record made entirely of menace has nowhere to go at six in
    the morning. What lifts a room then is not a breakdown - it is something
    enormous and consonant landing ON TOP of the kick while the kick keeps
    going. This is that voice, and it is built from two halves of the engine
    that already existed separately and never met.

    From `ens()`: the behaviour of a section rather than a chord. The notes
    enter in pitch order 30-70 ms apart, each voice wanders on its own slow
    random walk of a few cents and never comes home, and the top of the chord
    is quieter and sheds first. A block chord - every note on one sample,
    one envelope, one fixed spectrum - reads as a preset pasted in no matter
    how good the oscillator is.

    From `acid_hard()`: the material. drive -> EQ -> drive -> fold, so the
    wall is made of the same distortion as everything else on the record. A
    clean supersaw over a driven kick does not sound euphoric, it sounds like
    two records playing at once.

    And the filter opens across the whole call rather than per note, so the
    spectrum is still moving after four bars. `open0`/`open1` are where in
    the bank it starts and ends; ramp them from section to section and the
    wall grows over thirty bars instead of pulsing every two.

    Render it LONGER than the chord and place it on the chord change: the
    tails overlap, so the change is voice-led instead of switched. `notes`
    is a tuple of frequencies - the segment is cached.
    """
    n, t = steps(dur_steps, floor=int(0.25 * SR))
    rs = np.random.RandomState(seed + 977)
    out = np.zeros((n, 2), dtype=np.float64)
    order = sorted(range(len(notes)), key=lambda i: notes[i])
    for k, idx in enumerate(order):
        f = float(notes[idx])
        lag = int((roll * k + rs.uniform(0.004, 0.016)) * SR)   # low note first
        m = n - lag
        if m < 128:
            continue
        w = uniform_filter1d(rs.randn(m), max(int(0.45 * SR), 3))
        w = w * (walk / max(float(np.abs(w).max()), 1e-9))      # cents, wandering
        ratio = 2.0 ** ((rs.uniform(-4, 4) + w) / 1200.0)
        ph = 2 * np.pi * np.cumsum(f * ratio) / SR + rs.rand() * 6.28
        y = sawstack(ph, f * 1.04, voices=voices, detune=detune,
                     seed=seed + k * 7, kmax=110)
        pan = ((k / max(len(order) - 1, 1)) - 0.5) * 1.7 * width
        ang = (np.clip(pan, -1, 1) + 1) * np.pi / 4
        lvl = 1.0 / (1 + 0.32 * k)                              # the top is quieter
        out[lag:, 0] += y * np.cos(ang) * lvl
        out[lag:, 1] += y * np.sin(ang) * lvl
    out = (out / max(len(notes), 1) ** 0.7).astype(np.float32)

    env = open0 + (open1 - open0) * (np.linspace(0, 1, n) ** curve)
    out = morph_lp(out, f_lo, f_hi, env, bands=9, res=res)

    out = np.tanh(drive * out)                                  # drive
    out = out + bite * bandpass(out, 400, 2600)                 # EQ
    out = np.tanh(1.6 * out / (1 + bite * 0.5))                 # drive again
    if fold_amt:
        out = (1 - fold_amt) * out + fold_amt * fold(out, 1.05 + fold_amt * 0.7)
    if air:
        # Mechanism: the amplifier leaning back. It swells with the filter
        # rather than sitting under it, so something is making the sound.
        nz = bandpass(np.stack([rs.randn(n), rs.randn(n)], 1).astype(np.float32),
                      2600, 11000, 2)
        out = out + nz * (air * 0.055 * env).astype(np.float32)[:, None]

    out = hp(out, hpf, order=2)                                 # off the rumble
    a = min(int(attack * SR), n // 2)
    r = min(int(release * SR), n // 2)
    amp = np.ones(n, dtype=np.float32)
    amp[:a] = np.linspace(0, 1, a) ** 1.7
    amp[-r:] *= np.linspace(1, 0, r) ** 1.2
    return (out * amp[:, None]).astype(np.float32) * gain * 0.5


@cached
def sheet(dur_steps=32, gain=1.0, bands=7, lo=2600.0, hi=12000.0, rate=0.11,
          drive=1.7, seed=0):
    """A steel sheet under a slow scrape: the top of the room.

    Every industrial record this project has measured came out with under 2%
    of its energy above 3 kHz, which on a big rig is a blanket thrown over
    the whole thing. An air shelf does not fix it - a shelf lifts whatever is
    already there, and in a genre whose brightest instrument is a closed hat
    there is nothing there to lift. This puts something there.

    Same construction as `grind()` two octaves up, with one deliberate
    difference: `grind` tunes its bands to the root and is therefore pitched,
    and a bright ringing pitched thing above 3 kHz reads as a glockenspiel
    and makes a dark record sound cheerful. These bands are tuned to nothing.
    An untuned bright object is a room; a tuned one is a toy.
    """
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 733)
    nz = np.stack([rs.randn(n), rs.randn(n)], 1).astype(np.float32)
    out = np.zeros((n, 2), dtype=np.float32)
    for i, f in enumerate(np.geomspace(lo, hi, bands)):
        b = bandpass(nz, f * 0.84, f * 1.19, order=2)
        breath = 0.22 + 0.78 * (0.5 - 0.5 * np.cos(
            2 * np.pi * rate * (0.5 + 0.42 * i) * t + rs.rand() * 6))
        out += b * (breath / (1 + i * 0.28)).astype(np.float32)[:, None]
    out = np.tanh(drive * out * 2.4) / np.tanh(drive)
    out = hp(out, lo * 0.8, order=2)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0017))
    env = np.ones(n, dtype=np.float32)
    a = min(int(0.25 * SR), n // 2); r = min(int(0.35 * SR), n // 2)
    env[:a] = np.linspace(0, 1, a); env[-r:] *= np.linspace(1, 0, r)
    return out * env[:, None] * gain * 0.22


# ---- the 303 as the bassline ----
def deepacidline(pattern, dur_bars=1, cutoff=0.16, res=5.6, envmod=0.60,
                 decay=0.24, cut_decay=0.105, drive=4.2, acc_amt=0.55,
                 sag=0.30, f_lo=76.0, f_hi=2400.0, split=105.0, sine=0.34,
                 sub_oct=0.0, even=0.14, tame=6200.0, low=44.0, wave='saw', bands=11,
                 slide_tau=0.060, glide_ms=2.0, knob=None, gain=1.0):
    """A TB-303 played DOWN THERE - the acid line as the bass part.

    Every 303 in this project so far high-passes itself at 165-240 Hz on the
    principle that the sub belongs to the kick, which is correct when the
    line is a hook riding over a bassline. It is the wrong instrument for the
    kind of acid techno where there IS no separate bassline: the 303 is at
    F#1-F#2, the filter rests below 150 Hz, and what the room feels is the
    resonant peak crawling around in the low harmonics.

    Doing that naively turns the low end to mud, because the overdrive that
    makes a 303 sound like a 303 is generating intermodulation products all
    over the sub. So the drive is applied to a SPLIT signal:

        filter (three-pole) -> supply sag -> split at `split` Hz
                                              |          |
                                    clean, mono          driven, folded
                                              \\________ /
                                                  sum

    which is the same rule every bass in this engine obeys - one clean thing
    at the bottom - applied to a 303 rather than to a layered synth. `sine`
    adds a tracked sine at the fundamental underneath, so the note keeps its
    weight even at the cutoff settings where the filter has taken it away.

    Three things it inherits from `minimallib.acidline`, which is the most
    faithful 303 here and the reason that one and not `acidline` was the
    starting point: an 18 dB/octave filter rather than 24, so the resonant
    peak sits on a bed of harmonics instead of on silence; the overdrive
    AFTER the filter; and `cutoff` and `envmod` as two knobs rather than one.

    `knob` sweeps the resting cutoff across the whole call - the hand on the
    control while the pattern stays fixed, which is what playing one means.
    """
    n = int(round(dur_bars * BAR + 1.5 * STEP))
    fs, amp, cut = core._line_envs(pattern, n, decay, cut_decay, acc_amt, 0.0,
                                   glide_ms, slide_tau)
    ph = 2 * np.pi * np.cumsum(fs) / SR
    top = float(fs.max())
    if wave == 'square':
        x = (2 / np.pi) * sum(np.sin(k * ph) / k for k in range(1, 46, 2)) * 2
    else:
        x = saw_ph(ph, top, kmax=72)

    base = cutoff
    if knob is not None:
        k = np.atleast_1d(np.asarray(knob, dtype=np.float64))
        base = k[0] if len(k) == 1 else np.interp(np.linspace(0, 1, n),
                                                  np.linspace(0, 1, len(k)), k)
    env = np.clip(base + envmod * cut, 0.0, 1.0)

    st = stereo(x * amp)
    out = morph_lp(st, f_lo, f_hi, env, bands=bands, res=res, order=3)
    out = out / (1 + res * 0.30)
    out = out * accent_sag(pattern, n, sag, step=STEP)[:, None]

    if split:
        lo = lp(out, split, order=4)                   # the one clean thing
        hi = hp(out, split, order=4)
    else:
        lo, hi = np.zeros_like(out), out               # split=0 drives all of it
    hi = np.tanh(drive * hi) / np.tanh(drive)
    if even:
        y = hi * hi * np.sign(hi)
        hi = hi + even * (y - y.mean(axis=0, keepdims=True))
    out = lo + hi
    if sine:
        out = out + sine * stereo(np.sin(ph) * amp) * 0.7
    if sub_oct:
        # The line's own octave down, as a clean tracked sine. A 303 written
        # at F#2 has its fundamentals at 92-185 Hz, which IS the 120-300 band
        # - so a record whose bass is the 303 comes out low-MIDDLE rather
        # than low, and measures 48% there against 29% under 120 Hz. This is
        # the fix, and it has to be a sine and it has to be clean, because it
        # is the one thing allowed down there.
        out = out + sub_oct * lp(stereo(np.sin(0.5 * ph) * amp), 115, order=2) * 0.9

    out = lp(out, tame, order=2)
    out = hp(out, low, order=2)
    return fade_edges(out.astype(np.float32), 2.0) * gain * 0.55

@cached
def _deepacid_cached(key, dur_bars, **kw):
    return deepacidline(list(key), dur_bars, **kw)

def deepacid(pattern, dur_bars=1, **kw):
    """cached deepacidline - the knob positions are part of the key, so a
    swept line is a sequence of distinct cached phrases rather than one
    phrase repeated"""
    k = kw.pop('knob', None)
    if k is not None:
        k = tuple(np.atleast_1d(k).tolist())
    return _deepacid_cached(tuple(tuple(p) for p in pattern), dur_bars,
                            knob=k, **kw)


@cached
def openhat(dur_steps=4.0, gain=1.0, tone=1.0, decay=0.42, strike=0.05,
            metal=0.6, air=1.0, hpf=6200.0, seed=0):
    """A 909 open hat: metal that rings, not a burst of noise.

    `hat909(open_=True)` is band-passed white noise under one exponential
    decay. As a CLOSED hat - 28 ms - that is exactly right, because a 28 ms
    noise tick is what a closed hat is. Opened out it stops working, for
    three reasons which the ear reads as a rattle rather than as a cymbal:

    - **It is noise only.** A hi-hat is two metal discs, and the pitched,
      inharmonic partials are most of what makes it one.
    - **One envelope**, so every frequency decays together. Real metal sheds
      its top first, which is why a cymbal changes colour while it rings; a
      sound whose spectrum is fixed while it fades is a sample being turned
      down.
    - **One seed.** `hat909` draws from RandomState(77) every call, so every
      open hat in a record is bit-identical. Nothing in a kit repeats
      exactly, and a short bright sound that does stops being an instrument
      and becomes a tick.

    Six squares at the 808's inharmonic ratios supply the metal, a noise
    layer supplies the sizzle and decays faster than the metal does, and
    `hpf` keeps all of it above the 2-5 kHz band - a bright short sound down
    there is an ice-pick, not air.
    """
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 313)
    base = 317.0 * tone * (1.0 + 0.02 * (rs.rand() - 0.5))       # per-hit detune
    m = sum(square(base * p, t) for p in
            (1.0, 1.342, 1.612, 1.996, 2.441, 2.786)) / 6.0
    m = np.tanh(2.4 * m)
    body = stereo(m) * np.exp(-t / decay)[:, None]
    top = hp(stereo(m), hpf * 1.6) * np.exp(-t / (decay * 0.40))[:, None]
    nz = hp(stereo(rs.randn(n)), hpf) * np.exp(-t / (decay * 0.28))[:, None]
    out = metal * (body + 0.55 * top) + air * 0.5 * nz
    out = out + hp(stereo(rs.randn(n)), 9000) * np.exp(-t / strike)[:, None] * 0.30
    out = hp(out, hpf, order=2)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0009))
    return out * adsr(n, a=0.0005, r=0.03)[:, None] * gain * 0.42


# ---- the fabrication shop ----
# Everything above this line is a drum, a one-shot or a bed. A machine shop is
# none of those. It is several machines, each running its own cycle, none of
# them agreeing with the music or with each other, and none of them stopping
# between the hits - the idling is what makes the gaps sound like a factory
# rather than like a silence. These are those machines.

@cached
def weight(tune=43.65, dur_steps=2.6, decay=0.10, gain=1.0):
    """The third layer of the kick: one clean sine at the root, mono, short.

    The punch (`techkick`, `industrialkick`) is 20-120 Hz of transient and
    the growl (`rumble`) is the room it stands in, and neither of them is the
    weight. The first industrial records this project measured came out with
    more energy in 120-300 Hz than under 120 - all growl and no floor - and
    this is the floor. No distortion, no reverb, ducked with everything else.

    It does NOT follow the kick onto the eighths. Eight sine hits a bar at
    44 Hz is not eight times the weight, it is one long smear: the weight
    stays on the four beats and the offbeats are pure punch.
    """
    n, t = steps(dur_steps)
    return (sub(tune, dur_steps) * np.exp(-t / decay)[:, None]).astype(np.float32) * gain


@cached
def mill(dur_steps=64, cycle=6.0, note=36, gain=1.0, motor=0.5, bite=1.0,
         cut=0.7, screech=0.8, hiss=0.45, offset=0.0, whine=1870.0,
         tool=1180.0, pan=0.0, seed=0):
    """A machine tool running its cycle.

    Per cycle the tool bites - a short ring of tool steel, a band of
    broadband cut noise and a resonant SCREECH that sweeps while the edge is
    in the metal - and the spindle labours behind it, bending down in pitch
    under load with its gear whine climbing, which is what a machine taking a
    cut actually does. Then it comes free and exhales. The motor runs
    continuously underneath all of it, because the idling is what makes the
    gaps in a factory sound like a factory rather than a silence.

    The screech is not decoration. A first pass of this with a motor, a
    strike and cut noise measured 68% of its energy in 120-300 Hz and 1%
    above 3 kHz, which is a lathe recorded through a wall - and every
    industrial record this project has measured has failed in exactly that
    direction. Metal being cut is a scream, and it lives at 2-7 kHz.

    `cycle` is in STEPS and should be EVEN. Six steps repeats every three
    bars and drifts against the bar the whole way, which is the point: a shop
    is several machines and none of them agree. But every hit still lands on
    an eighth, so the ear keeps a reference. Give a machine with a pitch and
    a ring an ODD cycle and it never lands on a beat or an offbeat eighth at
    all, and that is not heard as polymeter - it is heard as a second machine
    playing badly.

    Two or three of these at 6, 10 and 14 steps, panned apart, IS the record.
    """
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 619)
    f = midi(note)
    cyc = max(int(round(cycle * STEP)), 512)
    k0 = int(round(offset * STEP))

    # ---- the motor, which never stops
    u = ((np.arange(n) + k0) % cyc) / cyc                 # 0..1 through the cycle
    load = np.clip(1.0 - u / 0.42, 0.0, 1.0) ** 0.7       # in the metal for 42% of it
    fm = f * (1 - 0.055 * load) * (1 + 0.005 * np.sin(2 * np.pi * 0.31 * t + rs.rand() * 6))
    ph = 2 * np.pi * np.cumsum(fm) / SR
    mo = saw_ph(ph, f * 1.25, nyq=13000.0, kmax=36) * 0.6 + 0.45 * np.sin(2 * ph)
    mo = morph_lp(stereo(np.tanh(1.7 * mo)), 300.0, 3000.0, 0.10 + 0.75 * load, bands=6)
    fw = whine * (1 - 0.07 * load)
    wh = np.sin(2 * np.pi * np.cumsum(fw) / SR + rs.rand() * 6) * (0.18 + 0.82 * load)
    mot = mo * 0.55 + stereo(wh).astype(np.float32) * 0.30

    # ---- the cut: a resonant band walking up while the edge is in the metal
    scr = np.zeros((n, 2), dtype=np.float32)
    if screech:
        nz = np.stack([rs.randn(n), rs.randn(n)], 1).astype(np.float32)
        drag = uniform_filter1d(np.abs(rs.randn(n)), int(0.012 * SR))
        drag = drag / max(float(drag.max()), 1e-9)
        e = np.clip(load * (0.45 + 0.55 * drag), 0, 1)
        scr = morph_lp(hp(nz, 1800), 2100.0, 7600.0, 0.18 + 0.82 * e,
                       bands=7, res=0.55) * (e ** 1.4).astype(np.float32)[:, None]

    # ---- strike, swarf, exhale. Every cycle is different, because a machine
    # that produces a bit-identical transient a thousand times in a record is
    # a metronome, not a machine.
    strike = np.zeros(n)
    swarf = np.zeros(n)
    puff = np.zeros(n)
    c = 0
    while True:
        a = c * cyc - k0
        c += 1
        if a >= n:
            break
        if a + int(0.25 * SR) < 0:
            continue
        det = rs.uniform(0.94, 1.07)
        amp = rs.uniform(0.72, 1.0)
        a0 = max(a, 0)
        m = min(int(0.13 * SR), n - a0)
        if m > 64:
            tt = np.arange(m) / SR
            sk = np.zeros(m)
            for p, g_, d in ((1.0, 1.0, 0.042), (2.37, 0.74, 0.026), (3.91, 0.55, 0.016),
                             (6.13, 0.38, 0.010), (9.71, 0.24, 0.006)):
                sk += g_ * np.sin(2 * np.pi * tool * det * p * tt) * np.exp(-tt / d)
            sk /= 2.91                                    # normalise BEFORE any drive
            sk += rs.randn(m) * np.exp(-tt / 0.0022) * 1.1
            strike[a0:a0 + m] += sk * amp
        mm = min(int(0.26 * SR), n - a0)
        if mm > 64:
            tc = np.arange(mm) / SR
            swarf[a0:a0 + mm] += rs.randn(mm) * np.exp(-tc / rs.uniform(0.035, 0.075)) * amp
        h = a + int(cyc * 0.47)
        h0 = max(h, 0)
        mh = min(int(0.16 * SR), n - h0)
        if h < n and mh > 64:
            th = np.arange(mh) / SR
            puff[h0:h0 + mh] += rs.randn(mh) * np.minimum(th / 0.006, 1.0) \
                * np.exp(-th / rs.uniform(0.030, 0.060)) * rs.uniform(0.5, 1.0)

    out = motor * mot
    out += bite * bandpass(stereo(np.tanh(1.5 * strike)), 600, 14000) * 1.5
    out += cut * bandpass(stereo(swarf), 1900, 11000) * 0.9
    out += screech * scr * 0.85
    out += hiss * hp(stereo(puff), 4200) * 0.5
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0016))
    if pan:
        out = panned(out, pan)
    env = np.ones(n, dtype=np.float32)
    aa = min(int(0.10 * SR), n // 2); rr = min(int(0.14 * SR), n // 2)
    env[:aa] = np.linspace(0, 1, aa); env[-rr:] *= np.linspace(1, 0, rr)
    return (out * env[:, None]).astype(np.float32) * gain * 0.35


@cached
def pipe(note=45, dur_steps=8, gain=1.0, knocks=6, decay=0.55, rattle=0.7,
         air=0.4, stretch_=0.0016, drive=1.6, seed=0):
    """Sanitary pipework, hit from the inside.

    Not `anvil`, which is a plate. A plate's modes are irrational and it is
    struck once and rings. A pipe is a tube, so its modes are the ODD
    harmonics of its length, slightly stretched by the stiffness of the wall -
    and it is not struck once, because whatever is travelling down it hits it
    several times inside one decay. Between the knocks the bracket it is
    clamped to buzzes for as long as the tube is still moving hard enough,
    and that buzz is what makes this read as plumbing rather than as tuned
    percussion. `air` is the column itself: the hollow note you hear when you
    put your ear to a cold riser.
    """
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 787)
    f = midi(note)
    x = np.zeros(n)
    ks = np.sort(np.concatenate([[0.0], rs.uniform(0.03, 0.86, max(knocks - 1, 0))
                                 * (n / SR)]))
    for j, kt in enumerate(ks):
        a = int(kt * SR)
        m = n - a
        if m < 256:
            continue
        tt = np.arange(m) / SR
        lvl = 1.0 if j == 0 else rs.uniform(0.25, 0.7)
        det = 1.0 + rs.uniform(-0.004, 0.004)
        y = np.zeros(m)
        for i in range(7):
            h = 2 * i + 1                                  # a closed tube: odd only
            fk = f * det * h * (1 + stretch_ * h * h)
            if fk > SR * 0.44:
                break
            y += (np.sin(2 * np.pi * fk * tt + rs.rand() * 6)
                  * np.exp(-tt / (decay / (1 + i * 1.35))) / (1 + i * 0.9))
        y /= 2.4                                           # before the drive, always
        y += rs.randn(m) * np.exp(-tt / 0.0014) * 0.8      # the contact
        x[a:] += y * lvl
    if air:
        col = bandpass(stereo(rs.randn(n)), f * 0.88, f * 1.14, order=2)[:, 0]
        col += bandpass(stereo(rs.randn(n)), f * 2.9, f * 3.2, order=2)[:, 0] * 0.5
        x += air * col * 2.4 * np.exp(-t / (decay * 1.8))
    out = bandpass(stereo(np.tanh(drive * x)), max(f * 0.55, 90), 13000)
    if rattle:
        # the bracket. It only buzzes while the tube is moving, so the gate is
        # the tube's own envelope - and it clatters at its own rate, which has
        # nothing to do with the pitch.
        e = uniform_filter1d(np.abs(x), 96)
        thr = 0.30 * max(float(e.max()), 1e-9)
        g = np.clip((e - thr) / max(thr, 1e-9), 0, 1) ** 0.8
        clat = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * (74.0 + 46.0 * rs.rand()) * t
                                          + 2.1 * np.sin(2 * np.pi * 11.3 * t)))
        bz = hp(stereo(rs.randn(n)), 2400) * (g * clat)[:, None]
        out = out + rattle * bz * 0.55
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0011))
    return out * adsr(n, a=0.0008, r=0.04)[:, None] * gain * 0.4


@cached
def girder(f0=43.65, f1=0.0, dur_steps=128, gain=1.0, modes=6, friction=0.55,
           drive=1.8, curve=1.0, hpf=95.0, width=1.4, seed=0):
    """A megastructure under load, moving.

    Everything else in this palette is a machine hitting something. This is
    the building: a beam the size of a room being winched across it. The
    pitch is carried by bar modes - 1, 2.76, 5.40, 8.93, 13.34, 18.6 - and
    they are excited by FRICTION rather than by a strike, so it has no attack
    at all and never arrives; it is simply already happening. `friction` is
    how uneven the drag is, and it is the only thing that keeps a set of
    sines from being an organ.

    And it GLIDES, `f0` to `f1` across the whole call. That is the surreal
    part and it is the reason this exists: an object that size cannot change
    pitch, and this one takes forty seconds to slide a tritone.

    On a record with no acid it is the only voice carrying a note across a
    section, and it carries it as one gesture rather than as a sequence of
    them. Render it over a whole section and place it on the section line.
    """
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 853)
    f1 = f1 or f0
    fr = f0 * (f1 / f0) ** (np.linspace(0, 1, n) ** curve)
    RAT = (1.0, 2.756, 5.404, 8.933, 13.34, 18.64, 24.75)
    x = np.zeros(n)
    tot = 0.0
    for i, r in enumerate(RAT[:modes]):
        if fr.max() * r > SR * 0.42:
            break
        ph = 2 * np.pi * np.cumsum(fr * r) / SR + rs.rand() * 6.28
        # the drag: a slow, uneven pull on each mode, and no two modes are
        # being dragged the same way, which is what a real surface does
        w = uniform_filter1d(np.abs(rs.randn(n)), max(int((0.24 / (1 + i * 0.6)) * SR), 3))
        w = w / max(float(w.max()), 1e-9)
        a = (1 - friction) + friction * w
        g = 1.0 / (1 + i * 0.78)
        x += np.sin(ph) * a * g
        tot += g
    x /= max(tot, 1e-9)                                    # before the drive
    out = drive_asym(stereo(x), drive, asym=0.22)
    # the surfaces themselves: a band of noise walking with the glide, so you
    # can hear that something is being dragged and not merely sounded
    if friction:
        nz = np.stack([rs.randn(n), rs.randn(n)], 1).astype(np.float32)
        env = np.clip(0.15 + np.log2(np.maximum(fr, 1e-6) / f0) * 1.4, 0, 1)
        sc = morph_lp(hp(nz, 500), 900.0, 8200.0, env, bands=7, res=0.40)
        gg = uniform_filter1d(np.abs(rs.randn(n)), int(0.09 * SR))
        gg = gg / max(float(gg.max()), 1e-9)
        out = out + sc * (0.30 * friction * (0.22 + 0.78 * gg)).astype(np.float32)[:, None]
    out = hp(out, hpf, order=2)
    out = widen(out, width)
    env = np.ones(n, dtype=np.float32)
    aa = min(int(1.1 * SR), n // 2); rr = min(int(1.4 * SR), n // 2)
    env[:aa] = np.linspace(0, 1, aa) ** 1.5
    env[-rr:] *= np.linspace(1, 0, rr) ** 1.2
    return (out * env[:, None]).astype(np.float32) * gain * 0.42


@cached
def shear(pattern, dur_steps=32, gain=1.0, rates=(1, 1, 2, 2, 4, 4, 8, 8),
          tear=(0.20, 0.75), sub=1.0, body=0.55, drive=6.0, res=3.0, crush=0,
          f_lo=95.0, f_hi=4200.0, split=92.0, curve=1.0, glide=0.022,
          rel=0.020, depth=0.45, width=0.35, seed=0):
    """The moment the plate lets go: a sub that comes apart under load.

    Nothing else in this palette is a bass instrument. `rumble` is a room,
    `weight` is a floor and `distbass` fills an offbeat - none of them is the
    thing a drop lands on.

    `pattern` is `(step, midi, length_in_steps)` and it is not optional. One
    held pitch under a moving filter is not a bass LINE however violent the
    filter is: with no articulation and no note changes the ear has nothing
    to separate, and what it reports is low-frequency noise. The frequency
    comes from `core._ftrack`, so the oscillator is continuous across the
    whole call and the note changes GLIDE - nothing is retriggered, and there
    is no phase discontinuity to click - while the gate is built from the
    note lengths, so the gaps are real gaps.

    Three layers, and only one of them is torn:

    - the **weight**, below `split`: one clean sine, centred, untouched. Two
      distorted fundamentals under 90 Hz intermodulate and the low end gets
      smaller, which is why every bass in this project is split.
    - the **body**, `body`: the 2nd and 3rd harmonics, lightly saturated and
      band-limited to 120-800 Hz. This is the layer that says which note it
      is. Without it the character layer's harmonic structure is folded into
      a buzz and the part reads as a texture rather than as a pitch.
    - the **tear**: a wavefolder whose amount ramps from `tear[0]` to
      `tear[1]` across the call, fed through a resonant lowpass moved by a
      `scanlane` - a lane whose RATE is sequenced rather than its value, so
      the crackle accelerates from a quarter to a thirty-second inside notes
      that are never retriggered. `tanh` stops making partials the moment it
      is flat and a folder does not.

    `depth` is how much of the lane goes on the LEVEL as well as the cutoff.
    It has to be small: a deep amplitude lane is not a rattle, it is a
    tremolo, and a tremolo on the loudest element of the record is heard as
    the mix changing volume.

    `crush` is off by default and should usually stay off. `bitcrush` with
    `downsample=2` decimates without an anti-alias filter, so everything
    above 11 kHz folds back down as inharmonic noise - on a bass that is not
    grit, it is a low frequency crackling, which is exactly what it sounds
    like.
    """
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 941)
    pat = [(float(st), int(nt), float(d)) for st, nt, d in pattern]
    f = core._ftrack([(st, nt) for st, nt, _ in pat], n, glide)
    ph = 2 * np.pi * np.cumsum(f) / SR

    gate = np.zeros(n)
    for st, _, d in pat:
        a0 = min(int(st * STEP), n)
        b0 = min(int((st + d) * STEP), n)
        if b0 > a0:
            gate[a0:b0] = 1.0
    gate = uniform_filter1d(gate, max(int(rel * SR), 3)).astype(np.float32)

    # the weight: clean, centred, and out of the way of everything above it
    low = lp(stereo(np.sin(ph) * 0.85 + 0.15 * np.sin(2 * ph)), split, order=4)

    # the body: which note this is
    bod = np.sin(2 * ph) * 0.75 + np.sin(3 * ph) * 0.40 + np.sin(4 * ph) * 0.18
    bod = bandpass(stereo(np.tanh(1.9 * bod / 1.33)), 118, 820)

    # the tear: the same phase, coming apart
    x = saw_ph(ph, f.mean(), nyq=16000.0, kmax=96) * 0.62 + square(f.mean(), t, kmax=44) * 0.38
    lane = scanlane(n, rates, lo=0.0, hi=1.0, shape='sine', curve=1.15, smooth=0.004)
    y = morph_lp(stereo(x * 0.55), f_lo, f_hi, 0.10 + 0.90 * lane, bands=8, res=res)
    y = np.tanh(drive * y)
    ten = (tear[0] + (tear[1] - tear[0]) * np.linspace(0, 1, n) ** curve).astype(np.float32)
    y = np.sin((1.0 + 2.2 * ten)[:, None] * np.pi * 0.5 * np.clip(y, -2, 2))
    y = np.clip(y * (1.20 + 0.60 * ten)[:, None], -1.0, 1.0)
    if crush:
        y = bitcrush(y, bits=crush, downsample=2)
    y = hp(y, split, order=4)
    y = y * (1.0 - depth + depth * lane ** 0.7).astype(np.float32)[:, None]
    y[:, 1] = np.roll(y[:, 1], int(SR * 0.0006 * width))

    out = (sub * low * 0.62 + body * bod * 0.55 + y * 0.95) * gate[:, None]
    aa = min(int(0.010 * SR), n // 2); rr = min(int(0.030 * SR), n // 2)
    env = np.ones(n, dtype=np.float32)
    env[:aa] = np.linspace(0, 1, aa); env[-rr:] *= np.linspace(1, 0, rr)
    return (out * env[:, None]).astype(np.float32) * gain * 0.66


@cached
def ratchet(dur_steps=16, rate=9.0, accel=3.0, note=64, gain=1.0, rmax=88.0,
            body=1.0, pawl=0.45, spin=0.22, seed=0):
    """A pawl clicking over a gear wheel as it spins up.

    `servo()` does the same structural job - an accelerating train of clicks,
    which is the cheapest way to raise density into a transition - and it
    does not belong in a machine shop. Its clicks are 10 ms, band-passed
    1800-11000 Hz and accelerate to 340 a second, and that combination is an
    electrical arc: no object was struck, so it has no body and nothing in
    the room answers it.

    This is the mechanical version of the same gesture, and the three things
    that separate them are all physical:

    - **A body.** Every click is a small struck object - four inharmonic
      partials around `note` with the top ones dying first - not a burst of
      band-passed noise.
    - **A pawl.** The spring-loaded catch has mass, so each click carries a
      low thud at a fixed pitch of its own. That thud is most of what makes
      it read as a mechanism rather than as a spark.
    - **A top speed.** `rmax` is 88 a second, not 340. Past about a hundred
      clicks a second the ear stops hearing separate impacts and starts
      hearing a buzz, and a buzz in that band is electrical again whatever
      it is made of.

    The whole thing is band-limited to 180-6500 Hz, so it never reaches the
    band a spark lives in.
    """
    n, t = steps(dur_steps)
    dur_s = n / SR
    rs = np.random.RandomState(seed + 577)
    f = midi(note)
    ts, cur, r = [], 0.0, rate
    while cur < dur_s:
        ts.append(cur)
        cur += 1.0 / r
        r = min(r * accel ** (1.0 / max(rate * dur_s, 1)), rmax)
    x = np.zeros(n)
    low = np.zeros(n)
    for i, c in enumerate(ts):
        k = int(c * SR)
        m = min(int(0.075 * SR), n - k)
        if m <= 32:
            break
        tt = np.arange(m) / SR
        det = rs.uniform(0.95, 1.06)
        amp = rs.uniform(0.68, 1.0)
        hit = np.zeros(m)
        for p, g_, d in ((1.0, 1.0, 0.030), (1.71, 0.62, 0.019),
                         (2.63, 0.40, 0.012), (4.11, 0.24, 0.007)):
            hit += g_ * np.sin(2 * np.pi * f * det * p * tt) * np.exp(-tt / d)
        hit /= 2.26                                       # before any drive
        hit += rs.randn(m) * np.exp(-tt / 0.0016) * 0.95  # the contact
        x[k:k + m] += hit * amp * body
        if pawl:
            # the catch has mass, and its pitch does not change with the rate
            pw = np.sin(2 * np.pi * 152.0 * (1 + 0.02 * (rs.rand() - 0.5)) * tt)
            low[k:k + m] += pw * np.exp(-tt / 0.024) * amp * pawl
    out = bandpass(stereo(np.tanh(1.7 * x)), 180, 6500)
    out = out + bandpass(stereo(low), 110, 340) * 0.45
    if spin:
        # the wheel itself, speeding up with the pawl
        u = np.clip(np.arange(n) / max(n - 1, 1), 0, 1)
        fw = 96.0 * (1 + 1.9 * u)
        wh = saw_ph(2 * np.pi * np.cumsum(fw) / SR, 120.0, nyq=7000.0, kmax=22)
        out = out + bandpass(morph_lp(stereo(np.tanh(1.4 * wh)), 420.0, 2400.0,
                                      0.15 + 0.7 * u, bands=5), 300, 4200) * spin * 0.45
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0012))
    return out * adsr(n, a=0.004, r=0.03)[:, None] * gain * 0.5
