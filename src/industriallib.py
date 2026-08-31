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
from scipy.signal import fftconvolve

BAR, STEP = core.set_grid(bpm=152)
BPM = core.BPM

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
             body=1.1, mid=1.6, click=1.0, grit=0.35, tone=7000, gain=1.0):
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
        g = np.tanh(6 * saw_ph(ph, tune * 11))
        g = bandpass(stereo(g), 350, 5200) * np.exp(-t / 0.035)[:, None]
        x = x + grit * fold(g, 1.0)
    x = x * np.exp(-t / decay)[:, None]
    if click:
        c = np.random.RandomState(7).randn(n) * np.exp(-t / 0.0016) * 0.9
        c += np.sin(2 * np.pi * 2100 * t) * np.exp(-t / 0.0028) * 0.45
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
    r = np.tanh(drive * r * 3.2) / np.tanh(drive)
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
def servo(dur_steps=4, rate=26.0, accel=2.4, note=72, gain=1.0, seed=0):
    """A stepper motor. Very short metallic clicks whose repetition rate
    accelerates - machine percussion, and the cheapest way to raise rhythmic
    density without adding a drum."""
    n, t = steps(dur_steps)
    dur_s = n / SR
    ts, cur, r = [], 0.0, rate
    while cur < dur_s:
        ts.append(cur)
        cur += 1.0 / r
        r *= accel ** (1.0 / max(rate * dur_s, 1))
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
             bands=9, sub=0.0, base=0.06, low=170):
    """A whole bar of 303 as one continuous monophonic voice. The oscillator
    never restarts, so a slide really slides; accents open the filter further
    and hit harder; the bar goes through one moving resonant lowpass.

    pattern: list of (step, note, dur_steps, accent, slide)
    """
    n = int(round(dur_bars * BAR))
    fs, amp, cut = _line_envelopes(pattern, n, decay, cut_decay, acc_amt)
    ph = 2 * np.pi * np.cumsum(fs) / SR
    top = float(fs.max())
    x = saw_ph(ph, top, kmax=48) if wave == 'saw' else \
        (2 / np.pi) * sum(np.sin(k * ph) / k for k in range(1, 40, 2)) * 2
    if sub:
        x = x + sub * np.sin(0.5 * ph)
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
