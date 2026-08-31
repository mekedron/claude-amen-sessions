"""The deep house layer: 123 BPM, and a room with the doors open.

House is the one dance genre that is not built out of impact. There is no
drop, nothing detonates, and the arrangement is an accumulation followed by
a subtraction - so everything the record has to say, it says through timbre
and groove over four to six minutes. That changes what the engine needs.

123 BPM is the middle of the deep-house range and it is chosen for the body
rather than for the genre chart: 488 ms a beat is a walking pace, fast
enough that the shoulders move and slow enough that nothing is in a hurry.
The kick is on every beat, so the felt pulse is the tempo.

What is here that `core` did not have, and why:

`hkick`   a round floor, not a punch. A house kick dives from 140 Hz rather
          than the 909's 220, over 24 ms rather than 15, and its beater is a
          *thud* in the 700-2600 Hz band with no 4 kHz tick at all. `mkick`
          is deliberately clean and 138 ms long so a minimal bass can roll
          under it; this one runs 300 ms and fills two thirds of the beat,
          because in this genre the low end is continuous and warm and the
          bass plays around it rather than through it.

`hhat`    the offbeat open hat is the genre's signature, so it cannot be a
          noise burst. Six squares at inharmonic ratios through a high-pass -
          the 808/909 topology - quantised to 8 bits, and re-seeded per hit
          so eight hats a bar are eight different hats.

`chord`   the voice this genre is actually made of, and it is SUBTRACTIVE.
          Two sawtooths a few cents apart per note, summed with no shared
          waveshaper before the filter - which is what keeps four notes
          sounding like four notes rather than one - through a gentle lowpass
          that opens over 30 ms and shuts behind it, then a bucket brigade.
          A saw at 200 Hz under a 1.6 kHz lowpass has ten harmonics between
          the fundamental and 2 kHz, so it fills the band the ear locates
          things in with nothing bright anywhere in it. `ep` next to it is an
          FM Rhodes and it is the wrong instrument for this: raise its index
          far enough to reach that band and 1:7 and 1:14 make a BELL, which
          is what those ratios are for.

`solina`  a string machine, which is not a pad. A divide-down organ has one
          oscillator per pitch running continuously from the moment it is
          switched on; the keys only open gates. So this renders a whole
          section as one bank of oscillators that never restart, and the
          chord changes are crossfades of their gates. Then three modulated
          delay lines at 0.38, 0.91 and 1.63 Hz with opposite phases per
          channel - the ARP Solina's three-phase bucket brigade, which is
          most of what a string machine actually is.

`vibes`   a vibraphone, built the way `theory/90-memories` says struck metal
          has to be: modes, not a sine with a tremolo on it. An undercut
          aluminium bar is tuned to 1 : 4 : 10.7, each mode with its own
          decay, so the timbre falls apart across the note. The tremolo is
          not applied to the bar at all - it is the rotating disc at the top
          of the RESONATOR TUBE, so only the fundamental fed through the tube
          pulses while the upper modes radiate steadily. That split is the
          difference between a vibraphone and a sine with an LFO. It is here
          for a record that wants one; `terrasa` does not, and neither does
          most of this genre - see `bells-are-not-a-default-top-layer`.

`sax`     an alto, one oscillator per phrase. A reed does not restart between
          slurred notes - the column of air keeps going and the fingers
          change its length - so a phrase is a frequency track, not a row of
          notes. What makes it a saxophone rather than a saw is that its body
          resonances near 700 Hz and 1500 Hz do NOT move with the pitch, and
          that the brightness follows blowing pressure rather than a filter
          envelope. `funklib.saxline` is a tenor written for punchy boogie
          lines; this one is higher, breathier and much softer, and it has a
          subtone articulation - the lounge sound, where the note is more air
          than reed.

The bass is `core.line` with house settings (`hbass`), not a new engine: a
whole bar as one oscillator, a clean sine under 100 Hz and a filtered saw
above it, and the buffer running past the bar line so the note on the last
offbeat rings into the next chord instead of dying at it.

Usage:
    from houselib import *
    s = Session(176, tail=4.0)
    t = s.pos(0); s.hit(t)
    s.place(t, hkick(), bus='drums')
    s.place(s.pos(0), hbass(BASS_A), 0.5, 'bass')
    s.render('house_something_123.wav', drive=0.0, clip=1.05, limit=0.94)
"""
import numpy as np
import core
from core import *
from scipy.ndimage import uniform_filter1d

BAR, STEP = core.set_grid(bpm=123)
BPM = core.BPM

def set_tempo(bpm, beats=4):
    """Re-grid the module. 123 is where this record runs; the palette is not
    tied to it. Every cached segment was rendered against the old grid, so
    the cache goes with the grid."""
    global BAR, STEP, BPM
    BAR, STEP = core.set_grid(bpm=bpm, beats=beats)
    BPM = core.BPM
    core._SEG_CACHE.clear()
    return BAR, STEP

# Deep house breathes; it does not pump. The bass gets out of the way
# completely, the keys and the strings dip about 3 dB, and the percussion box
# is untouched - a shaker that ducks on every beat is a shaker with a hole in
# it. `duck=0.62` at the master is -4.2 dB, which is the genre.
Session.DUCKED = {'bass': 1.00, 'keys': 0.42, 'pad': 0.55, 'lead': 0.22,
                  'music': 0.42, 'air': 0.30, 'gtr': 0.34}

# Every second 16th lands 6.5% of a step late - about 53.5% swing. Under the
# threshold where you hear a shuffle and over the one where the box sounds
# like a box. It goes on the hats, the shaker and the percussion; the kick
# and the clap stay dead on the grid, which is what makes it house and not
# garage.
SWING = 0.065

def sw(st, amt=None):
    """swing a step: odd 16ths land late, even ones do not"""
    a = SWING if amt is None else amt
    return st + (a if int(round(st)) % 2 else 0.0)


# ============================================================== the floor ===
@cached
def hkick(dur_steps=4.0, tune=51.0, top=140.0, tau=0.024, decay=0.245,
          body=1.0, beater=1.0, drive=2.1, gain=1.0, sub=1.0):
    """The round one.

    Three layers and none of them is a click. A house kick is *felt* before
    it is heard, so the weight is a sine diving from 140 Hz onto 51 (about
    G#1, a fifth under the key) over 24 ms - slow enough that the dive itself
    is audible as a thump rather than as a tick - decaying over 300 ms, which
    at this tempo is two thirds of a beat and leaves a third of it empty.

    The middle layer at 92 Hz is the part a small speaker reproduces, and the
    beater is band-limited to 700-2600 Hz. Everything above 3 kHz belongs to
    the hats: a kick with a bright tick in it turns a warm record into a
    techno one, and that single decision is most of the difference between
    the two floors."""
    n, t = steps(max(dur_steps, 2.4), floor=int(0.30 * SR))
    f = tune * (top / tune) ** np.exp(-t / tau)
    ph = 2 * np.pi * np.cumsum(f) / SR
    env = np.minimum(t / 0.0016, 1.0) * np.exp(-t / decay)
    x = np.sin(ph) * env * sub
    x += body * 0.62 * np.sin(2 * np.pi * 92.0 * t) * np.exp(-t / 0.095)
    x += body * 0.22 * np.sin(2 * np.pi * 148.0 * t) * np.exp(-t / 0.032)
    st = stereo(x)
    if beater:
        rs = np.random.RandomState(51)
        b = rs.standard_normal(n) * np.exp(-t / 0.0105)
        st = st + bandpass(stereo(b), 700, 2600, order=2) * 0.62 * beater
    # Asymmetric, so the harmonics it makes are even as well as odd. A wide
    # symmetric tanh on a sine is a square wave, and a square wave at 51 Hz
    # is not warmth, it is a buzz.
    st = drive_asym(st, drive, asym=0.30)
    st = hp(st, 26, order=2)
    return (st * adsr(n, a=0.0004, r=0.020)[:, None]).astype(np.float32) * gain * 0.92


@cached
def hclap(dur_steps=3.0, gain=1.0, spread=1.0, room=1.0, seed=0):
    """Four hands, not one.

    A clap is several people not quite together, and the 'not quite' is the
    whole sound: four noise bursts 9 ms apart with the spacing jittered, each
    one placed somewhere different across the stereo field, then a longer
    body burst underneath them. Width built out of four different signals in
    four places survives a mono sum; width built out of one signal delayed
    does not, and a club sums the low end anyway."""
    n, t = steps(max(dur_steps, 2.5), floor=int(0.32 * SR))
    rs = np.random.RandomState(300 + seed)
    st = np.zeros((n, 2), dtype=np.float32)
    for i, (off, lvl, p) in enumerate(((0.000, 1.00, -0.18), (0.0092, 0.86, 0.22),
                                       (0.0181, 0.74, -0.30), (0.0268, 0.62, 0.34))):
        d = int((off + 0.0016 * rs.rand()) * SR)
        m = n - d
        tm = np.arange(m) / SR
        b = rs.standard_normal(m) * np.exp(-tm / 0.0042)
        one = np.zeros((n, 2), dtype=np.float32)
        one[d:] = panned(bandpass(stereo(b), 950, 3900, order=2), p * spread) * lvl
        st += one
    tail = rs.standard_normal(n) * np.exp(-t / 0.085)
    st = st * 0.55 + bandpass(stereo(tail), 700, 2400, order=2) * 0.45
    st = hp(st, 380, order=2)
    if room:
        st = st + room * 0.30 * plate(st, decay=0.42, tone=5200)[:n]
    return (st * adsr(n, a=0.0004, r=0.030)[:, None]).astype(np.float32) * gain * 0.62


@cached
def hsnare(dur_steps=2.0, gain=1.0, tone=1.0, seed=0):
    """The soft one that hides under the clap. Two tuned sines with a fast
    drop plus a short band of noise - just enough body at 190 Hz to give the
    clap a floor, and nothing above 7 kHz where the hats live."""
    n, t = steps(max(dur_steps, 1.6), floor=int(0.20 * SR))
    rs = np.random.RandomState(700 + seed)
    fdrop = 2 ** (-1.4 * np.minimum(t / 0.018, 1.0))
    x = (np.sin(2 * np.pi * 192 * fdrop * t) * 0.9
         + np.sin(2 * np.pi * 288 * fdrop * t) * 0.5) * np.exp(-t / 0.055)
    nz = rs.standard_normal(n) * np.exp(-t / 0.070)
    st = stereo(x) * 0.55 + bandpass(stereo(nz), 260, 6200 * tone, order=2) * 0.45
    st = hp(st, 150, order=2)
    return (st * adsr(n, a=0.0004, r=0.020)[:, None]).astype(np.float32) * gain * 0.42


# The 808/909 hat: six squares at ratios that are deliberately not a harmonic
# series, so the stack has no pitch at all - only a metal colour.
_HAT_R = (1.0, 1.342, 1.613, 1.995, 2.443, 2.791)

@cached
def hhat(dur_steps=1.0, open_=False, gain=1.0, tone=1.0, base=317.0,
         bits=8, seed=0):
    """The offbeat open hat is the one sound that says house out loud, so it
    is built rather than sampled from noise: six square waves at inharmonic
    ratios through a high-pass, which is exactly how Roland did it and why
    those hats have a colour that filtered noise never gets.

    `seed` re-rolls the phases and the noise, so eight hats in a bar are
    eight different hats. A drum machine repeating one recording is what
    fatigue sounds like at four minutes."""
    dec = 0.130 if open_ else 0.026
    n, t = steps(max(dur_steps, 0.5), floor=int(0.36 * SR))
    rs = np.random.RandomState(900 + seed * 17)
    x = np.zeros(n)
    for r in _HAT_R:
        x += np.sign(np.sin(2 * np.pi * base * r * t + rs.rand() * 6.283))
    x = x / len(_HAT_R) + 0.55 * rs.standard_normal(n)
    st = hp(stereo(x), (5400 if open_ else 7200) * tone, order=4)
    st = st - 0.28 * bandpass(st, 9000, 11500, order=2)      # the metal's own dip
    env = np.exp(-t / dec)
    if open_:
        # 130 ms and then TRUNCATED, which is what the machine did: the 909's
        # open hat is a sample, and a sample ends. An exponential that is
        # merely long leaves the tail of every hat underneath the next one,
        # and four of those a bar at 123 BPM is 1.6 seconds of noise inside a
        # 1.95 second bar - the record turns to sand and nothing on the
        # offbeat reads as an event any more. The cost of the truncation is a
        # click, so it is a raised cosine rather than a cut.
        k0, k1 = int(0.150 * SR), min(int(0.300 * SR), n)
        if k1 > k0:
            env[k0:k1] *= 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, k1 - k0))
        env[k1:] = 0.0
    st = st * env[:, None]
    if bits:
        st = bitcrush(st, bits=bits, downsample=1)
    st[:, 1] = np.roll(st[:, 1], int(SR * 0.00035))
    return (st * adsr(n, a=0.0002, r=0.006)[:, None]).astype(np.float32) * gain * 0.30


@cached
def shaker(dur_steps=1.0, gain=1.0, vel=1.0, seed=0):
    """Beads leaving one end of the shell and arriving at the other. The
    envelope RISES to its peak and then stops - that swell is the whole
    difference between a shaker and a noise burst, and it is why a shaker
    can hold a 16th-note line for six minutes without becoming a hiss."""
    n, t = steps(max(dur_steps, 0.55), floor=int(0.09 * SR))
    rs = np.random.RandomState(1300 + seed * 7)
    a = 0.010
    env = (t / a) * np.exp(1.0 - t / a)                     # peaks exactly at a
    env = env * np.exp(-t / 0.036)
    # Lower than the hats and narrower. Two noise sources in the same octave
    # are one noise source twice as loud, and the second one buys nothing.
    st = bandpass(stereo(rs.standard_normal(n)), 3400, 9500, order=2)
    return (st * env[:, None]).astype(np.float32) * gain * vel * 0.34


@cached
def rimtick(dur_steps=1.0, gain=1.0, note=76, seed=0):
    """A stick on a rim: three close inharmonic partials and a contact tick,
    gone in forty milliseconds. Wood, not skin."""
    n, t = steps(max(dur_steps, 0.5), floor=int(0.09 * SR))
    rs = np.random.RandomState(1700 + seed)
    f = midi(note)
    x = sum(w * np.sin(2 * np.pi * f * q * t + rs.rand() * 6.283)
            for q, w in ((1.0, 1.0), (2.61, 0.42), (4.83, 0.18)))
    x *= np.exp(-t / 0.028)
    tick = rs.standard_normal(n) * np.exp(-t / 0.0011)
    st = stereo(x) * 0.7 + bandpass(stereo(tick), 1800, 8000, order=2) * 0.4
    st = hp(st, 400, order=2)
    return (st * adsr(n, a=0.0003, r=0.008)[:, None]).astype(np.float32) * gain * 0.34


@cached
def tamb(dur_steps=2.0, gain=1.0, seed=0):
    """Jingles: a dozen thin discs at unrelated frequencies, all short."""
    n, t = steps(max(dur_steps, 1.0), floor=int(0.20 * SR))
    rs = np.random.RandomState(2100 + seed)
    x = np.zeros(n)
    for _ in range(14):
        f = 5200 + 4200 * rs.rand()
        d = 0.004 * rs.rand()
        e = np.exp(-np.maximum(t - d, 0) / (0.045 + 0.06 * rs.rand()))
        x += np.sin(2 * np.pi * f * t + rs.rand() * 6.283) * e * (0.5 + rs.rand())
    st = hp(stereo(x / 14 + 0.25 * rs.standard_normal(n) * np.exp(-t / 0.05)),
            4800, order=2)
    st[:, 0] *= 1.12; st[:, 1] *= 0.88
    return (st * adsr(n, a=0.0004, r=0.020)[:, None]).astype(np.float32) * gain * 0.30


@cached
def conga(note=53, stroke='open', dur=2.0, gain=1.0, seed=0, vel=1.0,
          shell=1.0, size=1.0):
    """A tumbadora, from `core.membrane` - the same physical model the Cuban
    module plays a tumbao on, tuned for a house record: softer hands, more of
    the shell, and rolled off above 6 kHz so it sits behind the hats instead
    of competing with them."""
    n, t = steps(max(dur, 0.9), floor=int(0.10 * SR))
    x = membrane(midi(note), n, stroke, load=0.93, damp=0.60,
                 tight=1.0 / max(vel, 0.35) ** 0.30, seed=seed + note)
    st = stereo(np.tanh(1.35 * x * vel))
    if shell:
        w = shell * (0.30 if stroke in ('slap', 'tip', 'toe') else 1.0)
        f = 168.0 / size
        st = st + w * 0.50 * bandpass(st, f * 0.78, f * 1.30, order=2)
        st = st + w * 0.15 * bandpass(st, f * 2.4, f * 3.6, order=2)
    st = st - 0.22 * bandpass(st, 620, 1150)
    st = lp(hp(st, 58, order=2), 6200)
    return (st * adsr(n, a=0.0004, r=0.014)[:, None]).astype(np.float32) * gain * 0.52



@cached
def bongo(note=72, stroke='open', dur=1.6, gain=1.0, seed=0, vel=1.0,
          shell=1.0, damp=0.95):
    """The small drum, and it is not a conga pitched up.

    A bongo head is a third the diameter of a tumbadora and tuned far
    tighter, so it loads much less air: its modes sit closer to the ideal
    Bessel ratios, which is why a bongo rings with an audible PITCH where a
    conga gives a thud. `load=0.86` against the conga's 0.93 is that
    difference, and the fast `damp` is the second half of it - a small head
    under high tension has almost no sustain, so what the ear gets is a
    transient with a note printed on it.

    That is exactly what this record wants at the top. A shaker or a ride
    holding a line is a noise bed, and a noise bed at 6-9 kHz is what starts
    to hurt after ninety seconds; two dozen short wooden and skin transients
    a bar cover the same band and never accumulate, because the ear takes
    each one as an event and then forgets it."""
    n, t = steps(max(dur, 0.7), floor=int(0.09 * SR))
    x = membrane(midi(note), n, stroke, load=0.86, damp=damp,
                 tight=1.0 / max(vel, 0.40) ** 0.25, seed=seed + note)
    st = stereo(np.tanh(1.5 * x * vel))
    if shell:
        # a shallow wooden shell, an octave and a half above the conga's
        f = 430.0
        st = st + shell * 0.34 * bandpass(st, f * 0.82, f * 1.28, order=2)
    st = lp(hp(st, 180, order=2), 9500)
    return (st * adsr(n, a=0.0003, r=0.010)[:, None]).astype(np.float32) * gain * 0.46

# ================================================================= space ===
def plate(seg, decay=1.6, tone=5200, hp_hz=420, predelay=0.0):
    """Wet only: a bright, dense tail with no early reflections and no low
    end. A plate is a sheet of steel, not a room - it has no walls, so it has
    no discrete bounces, and it is the reverb every clap and every Rhodes on
    a house record is sitting in."""
    wet = reverb(seg, decay=decay, wet=1.0, tone=tone,
                 predelay=predelay)[len(seg) and slice(None)]
    wet = wet - np.concatenate([seg, np.zeros((len(wet) - len(seg), 2),
                                              dtype=np.float32)])
    return hp(wet, hp_hz, order=2).astype(np.float32)


def throw(s, t, seg, gain=1.0, steps_=3.0, times=5, fb=0.52, bus='air'):
    """One hit sent to a long delay and then left alone. The dub move, and
    the cheapest way to make a loop that has played forty times feel like
    something just happened."""
    for i in range(1, times + 1):
        e = lp(seg, max(5200 - 800 * i, 900)) * fb ** i
        e = panned(e, 0.65 if i % 2 else -0.65)
        s.place(t + int(i * steps_ * STEP), e, gain, bus)


# ================================================================== keys ===
@cached
def ep(notes, dur_steps=8, level=1.0, vel=0.80, ring=2.6, tine=1.0,
       tone=4600, ph_rate=0.17, ph_depth=0.70, trem=0.09, take=0):
    """A Rhodes, as two operators and a hammer.

    The tine is a modulator at fourteen times the carrier whose index dies in
    70 ms - a bell that stops being a bell almost immediately, which is what
    a struck steel tine does - sitting over a body at 1:1 that rings for two
    and a half seconds. Velocity moves the INDEX, not the level: press
    harder and it barks, which is the one thing an electromechanical piano
    does that a sampled one from the same decade could not.

    Three operators, because two of them leave a hole. A 1:1 pair at any
    sane index reaches its fourth partial and stops, so for a chord voiced
    around 200-600 Hz everything it owns sits under 1 kHz - it measures
    beautifully and it vanishes into a mix, because the band the ear uses to
    locate a sound has nothing in it. The 1:14 tine fills 3-8 kHz for 200 ms
    and then it is gone. The operator that matters is the one at 1:7: its
    sidebands land on the sixth and eighth partial, which for these voicings
    is 1.2-4 kHz, and it lasts as long as the note does. Its index has to be
    over about 2 to matter: at 0.5 the carrier keeps 88% of the energy and
    the sidebands are 0.9% of the voice, which measures as nothing.

    Then the phaser. Four notches sweeping between 300 Hz and 1.9 kHz once
    every six seconds, so no two bars of a four-minute record have the same
    chord colour, and a slow auto-pan on top of it. That combination is not
    decoration on a deep house chord - it IS the deep house chord."""
    n, t = steps(dur_steps, floor=int(0.45 * SR))
    body = np.zeros(n)
    ping = np.zeros(n)
    for nt in notes:
        ph = 2 * np.pi * midi(nt) * t
        i_t = 2.9 * vel * np.exp(-t / 0.070) + 0.05
        i_m = 2.60 * vel * np.exp(-t / 0.34) + 0.55
        i_b = 1.55 * vel * np.exp(-t / 0.50) + 0.30
        body += np.sin(ph + i_b * np.sin(ph)) * np.exp(-t / ring)
        ping += 0.46 * np.sin(ph + i_m * np.sin(7 * ph)) * np.exp(-t / (ring * 0.62))
        ping += 0.40 * np.sin(ph + i_t * np.sin(14 * ph)) * np.exp(-t / 0.28)
    k = max(len(notes), 1)
    # The two operators are filtered SEPARATELY, and that is not a detail.
    # The tine's sidebands sit at thirteen and fifteen times the note, so one
    # lowpass over the sum at the body's cutoff deletes the entire attack and
    # leaves an instrument that is uniformly dull at every dynamic. A struck
    # tine is bright and 200 ms long; the body under it is warm and lasts.
    # `tone` darkens the body only.
    out = lp(stereo(np.tanh(1.15 * body / k)), tone)
    out = out + tine * lp(stereo(np.tanh(1.30 * ping / k)), 7800)
    out = phaser(out, rate=ph_rate, lo=300.0, hi=1900.0, stages=4,
                 depth=ph_depth, bands=6)
    tr = 1 + trem * np.sin(2 * np.pi * 3.1 * t + take)
    out[:, 0] *= tr
    out[:, 1] *= 2 - tr                                  # tremolo that is auto-pan
    out = hp(out, 130, order=2)
    return (out * adsr(n, a=0.004, r=0.055)[:, None]).astype(np.float32) * level * 0.50


@cached
def chord(notes, dur_steps=6.0, level=1.0, vel=0.60, cutoff=1600, det=7.0,
          attack=0.040, decay=0.85, drive=1.05, hp_hz=140, take=0):
    """The chord this record is built on: a JUNO, not a Rhodes.

    An FM electric piano was the wrong instrument and it took a listener two
    minutes to say so. Two operators at 1:7 and 1:14 with an index high
    enough to reach the presence band are, by construction, a BELL - those
    are the ratios and the indices you use when you want one - and four notes
    of it through a shared waveshaper intermodulate into a single metallic
    event rather than a chord. Everything that made it measure well made it
    sound like a cowbell.

    So: subtractive, and soft. Two sawtooths a few cents apart per note,
    summed with NO shared saturator before the filter - that is what keeps
    four notes sounding like four notes - through one gentle lowpass that
    opens over 30 ms and closes again, and a bucket-brigade chorus after it.
    A saw at 200 Hz under a 1.6 kHz lowpass has ten harmonics spread from the
    fundamental to 2 kHz, so the chord fills the band the ear locates things
    in without a single bright transient anywhere in it.

    `attack` is the other half of soft. A chord that arrives in 4 ms is a
    stab however warm its spectrum; 30 ms is a key being pressed."""
    n, t = steps(dur_steps, floor=int(0.55 * SR))
    x = np.zeros(n)
    for i, nt in enumerate(notes):
        f = midi(nt)
        ph = 2 * np.pi * f * t
        x += sawstack(ph, f, voices=2, detune=det, seed=take * 11 + i, kmax=64)
    x /= max(len(notes), 1)
    # the filter opens with the key and shuts behind it - a fixed cutoff with
    # an amplitude envelope only changes how loud the chord is
    env = np.minimum(t / attack, 1.0) * (0.30 + 0.70 * np.exp(-t / (decay * 0.55)))
    st = morph_lp(stereo(x), 300.0, cutoff, 0.10 + 0.90 * env, bands=7, res=0.25)
    st = np.tanh(drive * st) / np.tanh(drive)
    st = _bbd(st, mix=0.55, tone=5200, seed=take)
    st = lp(hp(st, hp_hz, order=2), 4600)
    amp = np.minimum(t / attack, 1.0) * np.exp(-t / decay)
    rel = min(int(0.045 * SR), n)
    amp[n - rel:] *= np.linspace(1, 0, rel) ** 1.4
    return (st * amp[:, None]).astype(np.float32) * level * vel * 0.62


@cached
def stab(notes, dur_steps=2, level=1.0, cutoff=4200, res=1.4, det=9.0,
         drive=1.5, take=0):
    """The offbeat chord hit. Saws through a filter that shuts in 90 ms, so
    the chord is bright for one sixteenth and gone - the jack, the thing that
    makes a groove move sideways instead of forward."""
    n, t = steps(max(dur_steps, 1.4), floor=int(0.22 * SR))
    x = np.zeros(n)
    for i, nt in enumerate(notes):
        f = midi(nt)
        ph = 2 * np.pi * f * t
        x += sawstack(ph, f, voices=2, detune=det, seed=take * 7 + i)
    x /= max(len(notes), 1)
    cut = np.exp(-t / 0.090)
    st = morph_lp(stereo(x), 420, cutoff, 0.05 + 0.95 * cut, bands=7, res=res)
    st = np.tanh(drive * st)
    st = hp(st, 260, order=2)
    env = np.minimum(t / 0.004, 1.0) * (0.18 + 0.82 * np.exp(-t / 0.115))
    st[:, 1] = np.roll(st[:, 1], int(SR * 0.0011))
    return (st * (env * adsr(n, a=0.001, r=0.030))[:, None]).astype(np.float32) * level * 0.36


# ======================================================== the string bank ===
def _bbd(seg, mix=0.85, tone=6200, seed=0):
    """Three modulated delay lines at 0.38, 0.91 and 1.63 Hz, each one in
    opposite phase between the channels. That is an ARP Solina's bucket
    brigade, and it is not a chorus preset: three rates that never line up
    are why a string machine shimmers where a single-rate chorus warbles.
    The line loses its top end and adds its own hiss, both of which are part
    of the sound rather than a defect to be modelled out."""
    n = len(seg)
    t = np.arange(n) / SR
    base = np.arange(n, dtype=np.float64)
    rs = np.random.RandomState(4400 + seed)
    wet = np.zeros((n, 2), dtype=np.float32)
    for rate, dep, bs, phs in ((0.38, 5.6, 17.0, 0.0),
                               (0.91, 3.6, 21.0, 2.10),
                               (1.63, 2.4, 13.0, 4.20)):
        for c in range(2):
            pc = phs + (0.0 if c == 0 else np.pi)
            dl = (bs + dep * np.sin(2 * np.pi * rate * t + pc)) / 1000.0 * SR
            wet[:, c] += np.interp(base - dl, base, seg[:, c]).astype(np.float32)
    wet = lp(wet / 3.0, tone)
    wet += (rs.standard_normal((n, 2)) * 2.2e-4).astype(np.float32)
    return ((1 - mix * 0.5) * seg + mix * wet).astype(np.float32)


def solina(chords, level=1.0, tone=3300, attack=0.34, release=0.90,
           tail_steps=10.0, hp_hz=135, drift=3.2, seed=0, mix=0.85):
    """A string machine, rendered a whole section at a time.

    `chords` is one note-list per bar. A divide-down organ has one oscillator
    per note running from the moment the instrument is switched on - the keys
    only open gates - so this builds a bank of oscillators that start at
    sample zero and never restart, and the chord changes are crossfades
    between their gates. A part that retriggers every bar is a pad; this is
    an instrument.

    Octaves are locked in phase, because on a real divide-down every octave
    IS the same top-octave oscillator divided by two - one oscillator per
    pitch class, and the lower notes are counted down from it. Measured on
    the bank alone, an octave's amplitude ripples 0.035 and a major third
    0.115: the octave is dead still and the third beats, which is the sound
    of the machine. The bucket brigade afterwards then moves everything
    against everything, and that is the sound of the record."""
    nb = len(chords)
    n = int(round(nb * BAR + tail_steps * STEP))
    t = np.arange(n, dtype=np.float64) / SR
    pitches = sorted({p for ch in chords for p in ch})
    if not pitches:
        return np.zeros((n, 2), dtype=np.float32)
    rs = np.random.RandomState(5100 + seed)
    ph0 = {pc: rs.rand() * 6.283 for pc in range(12)}
    dph = {pc: rs.randn() for pc in range(12)}
    lo, hi = min(pitches), max(pitches)
    out = np.zeros((n, 2), dtype=np.float32)
    a_n, r_n = max(int(attack * SR), 2), max(int(release * SR), 2)
    for p in pitches:
        on = np.array([p in ch for ch in chords])
        env = np.zeros(n)
        b = 0
        while b < nb:
            if not on[b]:
                b += 1; continue
            e = b
            while e < nb and on[e]:
                e += 1
            a = int(round(b * BAR)); z = int(round(e * BAR))
            seg = np.ones(min(z + r_n, n) - a)
            k = min(a_n, len(seg))
            seg[:k] = np.linspace(0, 1, k) ** 1.4
            k2 = min(r_n, len(seg) - (z - a)) if z - a < len(seg) else 0
            if k2 > 0:
                seg[z - a:z - a + k2] = np.exp(-np.linspace(0, 4.2, k2))
                seg[z - a + k2:] = 0.0
            np.maximum(env[a:a + len(seg)], seg, out=env[a:a + len(seg)])
            b = e
        if env.max() < 1e-6:
            continue
        # one oscillator per pitch class, divided down: the octave is exact
        f = midi(p) * (1 + drift / 1200.0 * np.log(2)
                       * np.sin(2 * np.pi * (0.041 + 0.013 * dph[p % 12]) * t
                                + dph[p % 12] * 3))
        ph = 2 * np.pi * np.cumsum(f) / SR + ph0[p % 12]
        # A string machine's top end is a 3 kHz lowpass, so a low note does
        # not need forty harmonics that are about to be thrown away.
        km = int(np.clip(tone * 1.6 / midi(p), 8, 42))
        x = saw_ph(ph, float(f.max()) * 1.02, kmax=km) * env
        # low notes sit in the middle, high notes open outward
        u = (p - lo) / max(hi - lo, 1)
        out += panned(stereo(x), (u - 0.5) * 0.85 * (0.35 + 0.65 * u))
    out = out / max(len(pitches) ** 0.62, 1.0)
    out = lp(hp(out, hp_hz, order=2), tone)
    out = _bbd(out, mix=mix, seed=seed)
    return np.tanh(1.25 * out).astype(np.float32) * level * 0.55


# ============================================================ the mallets ===
# An undercut aluminium bar. A plain bar's modes sit at 1 : 2.76 : 5.40 - the
# free-free flexural series - and a maker removes metal from the underside
# until the second and third land on 4 and 10 times the fundamental, which is
# what makes a vibraphone a pitched instrument rather than a clang. Every
# mode above those is left where physics put it.
_BAR_R = (1.000, 3.984, 10.65, 17.90, 24.60, 31.2)
_BAR_A = (1.000, 0.280, 0.132, 0.052, 0.024, 0.011)
_BAR_T = (2.400, 0.400, 0.105, 0.035, 0.018, 0.011)

@cached
def vibes(note=79, dur_steps=8, gain=1.0, vel=0.80, fan=0.85, fan_hz=4.6,
          tube=1.0, mallet=1.0, seed=0, take=0):
    """A vibraphone bar over its resonator tube.

    The tremolo is the reason this is not a sine with an LFO on it. The disc
    at the top of each tube opens and closes the tube's mouth, so the ONLY
    thing that pulses is the fundamental the tube is tuned to; the second and
    third modes radiate straight off the bar and are dead steady while the
    bottom of the note breathes. Model it as one amplitude modulation over
    the whole voice and you get a tremolo. Model it as two paths and you get
    a vibraphone.

    Velocity lights the upper modes rather than raising the level - a hard
    mallet stroke puts energy into the short modes and a soft one does not,
    which is why the same bar hit twice is two different sounds."""
    n, t = steps(dur_steps, floor=int(0.75 * SR))
    rs = np.random.RandomState(6300 + seed * 31 + note + take)
    f0 = midi(note)
    ph0 = 2 * np.pi * f0 * t + rs.rand() * 6.283
    direct = np.zeros(n)
    for k, (r, a, tau) in enumerate(zip(_BAR_R, _BAR_A, _BAR_T)):
        if f0 * r > SR * 0.45:
            break
        w = a * vel ** (0.30 * k)                 # the strike, not the fader
        d = np.sin(2 * np.pi * f0 * r * t + rs.rand() * 6.283) * np.exp(-t / tau)
        direct += (0.30 if k == 0 else 1.0) * w * d
    # the tube: the fundamental only, stored and given back, chopped by the disc
    am = (1 - fan) + fan * (0.5 + 0.5 * np.sin(2 * np.pi * fan_hz * t
                                               + rs.rand() * 6.283))
    tubed = 0.70 * np.sin(ph0) * np.exp(-t / 2.9) * am * tube
    x = direct + tubed
    if mallet:
        m = min(n, int(0.030 * SR))
        tm = np.arange(m) / SR
        hit = rs.standard_normal(m) * np.exp(-tm / 0.0034)
        hit = bandpass(stereo(hit), 500, 2600 * (0.6 + 0.8 * vel), order=2)[:, 0]
        x[:m] += hit * 0.075 * mallet * vel        # soft yarn: felt, not heard
    st = stereo(x * np.minimum(t / 0.0008, 1.0))
    st = lp(st, 11000)
    st[:, 1] = np.roll(st[:, 1], int(SR * 0.0013))
    return (st * adsr(n, a=0.0005, r=0.060)[:, None]).astype(np.float32) * gain * 0.52


# ============================================================== the alto ===
def _reed(ph, f_max, odd=1.9, kmax=52, nyq=16500.0):
    """The wave a beating reed makes: a saw whose ODD partials are stronger.

    A sawtooth's own even/odd energy ratio is 1.32 - it has more even
    harmonics than odd ones, because 1/2 + 1/4 + 1/6 beats 1/3 + 1/5 + 1/7.
    A real tenor measures 0.4-0.7, the other way round, because the reed
    slams shut against the mouthpiece rather than closing smoothly and the
    bore is not a plain cone. Weighting the odd partials up is the cheapest
    honest way to put that back, and without it the horn reads as a filtered
    saw however good the formants are."""
    x = np.zeros(len(ph)); k = 1
    while f_max * k < nyq and k < kmax:
        x += (odd if k % 2 else 1.0) * np.sin(k * ph) / k
        k += 1
    return x * (2 / np.pi) / (0.5 + 0.5 * odd)


def _sax_envs(phrase, n, glide_ms, vib_cents, vib_hz):
    """frequency, blowing pressure and air, per sample, for a whole phrase"""
    fs = np.zeros(n); pr = np.zeros(n); air = np.zeros(n); vam = np.zeros(n)
    for ev in phrase:
        st, note, dur, art = ev[0], ev[1], ev[2], (ev[3] if len(ev) > 3 else 'n')
        a = int(round(st * STEP)); b = min(int(round((st + dur) * STEP)), n)
        if a >= n or b <= a:
            continue
        m = b - a
        tt = np.arange(m) / SR
        f = midi(note)
        track = np.full(m, f)
        if '^' in art:                       # scooped into from a semitone under
            track = f * 2 ** (-0.075 * np.exp(-tt / 0.032))
        if 'f' in art:                       # and the fall a player uses for a full stop
            k = int(m * 0.60)
            track[k:] *= 2 ** (-np.linspace(0, 5.0, m - k) ** 1.6 / 12)
        fs[a:b] = track
        breathy = 'b' in art
        at = 0.060 if breathy else (0.014 if '>' in art else 0.026)
        lvl = 0.58 if breathy else (1.00 if '>' in art else 0.84)
        e = np.minimum(tt / at, 1.0) * (1.0 - 0.16 * np.minimum(tt / 1.3, 1.0))
        rel = min(int(0.055 * SR), m)
        e[m - rel:] *= np.linspace(1, 0, rel) ** 1.3
        np.maximum(pr[a:b], lvl * e, out=pr[a:b])
        np.maximum(air[a:b], (2.1 if breathy else 1.0) * lvl * e, out=air[a:b])
        np.maximum(vam[a:b], np.clip((tt - 0.30) / 0.40, 0, 1), out=vam[a:b])
    idx = np.maximum.accumulate(np.where(fs > 0, np.arange(n), 0))
    fs = fs[idx]
    fs[fs <= 0] = midi(phrase[0][1]) if phrase else 440.0
    k = max(int(glide_ms / 1000.0 * SR), 3)
    fs = uniform_filter1d(fs, k)
    tt = np.arange(n) / SR
    fs = fs * 2 ** (vib_cents / 1200.0 * vam * np.sin(2 * np.pi * vib_hz * tt))
    # uniform_filter1d returns about -1e-14 over a run of zeros, and every one
    # of those becomes a NaN the moment it meets a fractional power below.
    pr = np.maximum(uniform_filter1d(pr, 128), 0.0)
    air = np.maximum(uniform_filter1d(air, 96), 0.0)
    return fs, pr, air


def sax(phrase, dur_steps=32, level=1.0, breath=1.0, bright=1.0, drive=1.25,
        glide_ms=13.0, vib_cents=22.0, vib_hz=5.1, tail_steps=6.0, odd=1.9,
        seed=0):
    """An alto saxophone. `phrase` is (step, midi, dur_steps, articulation):

        'n' plain   '>' accented   '^' scooped up into   'f' falls off
        'b' subtone - blown soft and wide, more air than reed, which is the
            entire sound of a saxophone in a room where people are talking

    One oscillator for the whole phrase. A reed does not restart between
    slurred notes: the column of air keeps going and the fingers change its
    length, so the pitch is a track and the tonguing is a change in pressure,
    not a new note. Rendering a sax note by note is what makes it sound like
    a sampler.

    Two things make it a saxophone rather than a filtered saw. The body
    resonances near 700 Hz and 1500 Hz are FIXED - they belong to the horn,
    not to the note, so they stay put while the pitch moves, which is exactly
    what a formant is and exactly why a synth lead is not one. And the
    brightness follows blowing pressure through a waveshaper: a reed's wave
    steepens as it is driven, so loud is a different spectrum, not a louder
    one."""
    n = int(round(dur_steps * STEP + tail_steps * STEP))
    fs, pr, air = _sax_envs(phrase, n, glide_ms, vib_cents, vib_hz)
    t = np.arange(n) / SR
    ph = 2 * np.pi * np.cumsum(fs) / SR
    x = _reed(ph, float(fs.max()), odd=odd)
    prn = np.clip(pr / max(pr.max(), 1e-9), 0, 1)
    st = stereo(x * pr)
    st = morph_lp(st, 430, 5600 * bright, 0.10 + 0.90 * prn ** 0.75, bands=8)
    # the horn: three fixed resonances that do not follow the pitch
    st = st + 0.50 * bandpass(st, 620, 880, order=2)
    st = st + 0.40 * bandpass(st, 1280, 1760, order=2)
    st = st + 0.24 * bright * bandpass(st, 2300, 3200, order=2)
    st = norm(st, 0.9)
    st = drive_asym(st, drive, asym=0.10)          # even harmonics: a horn, not a square
    st = lp(hp(st, 150, order=2), 8200)
    if breath:
        rs = np.random.RandomState(7700 + seed)
        nz = bandpass(stereo(rs.standard_normal(n)), 1500, 7200, order=2)
        st = st + nz * (air ** 1.3)[:, None] * 0.085 * breath
    st[:, 1] = np.roll(st[:, 1], int(SR * 0.0009))
    return (st * adsr(n, a=0.004, r=0.050)[:, None]).astype(np.float32) * level * 0.46


# =============================================================== the bass ===
def hbass(pattern, dur_bars=1, level=1.0, f_hi=2800.0, decay=0.52,
          cut_decay=0.155, hold=0.30, sub=0.66, drive=1.75, res=0.9,
          detune=0.006, tail_steps=6.0, glide_ms=6.0):
    """`core.line` with house settings, and the reasons for each of them.

    A whole bar as ONE oscillator, because a bass rendered note by note
    retriggers a string that never stopped and the fundamental breaks into
    pieces the ear hears as grit. `sub=0.90` puts a clean mono sine on the
    same phase under 115 Hz and lets the saw and the drive live above it -
    the split every modern bass patch is built on. `hold=0.30` is the deep
    house compromise: the note does not sustain flat like a pad and it does
    not shut like a techno roll, it settles to a third of its attack and
    stays there, which is a finger on a string.

    `f_hi` and `drive` are set high for a genre this warm on purpose. A sub
    with no harmonics above 100 Hz is silent on a phone, a laptop and a car
    dashboard - the ear reconstructs a missing fundamental from its overtones
    and cannot reconstruct anything from nothing. The saw layer above 95 Hz
    is what makes the bass line audible as a LINE rather than as pressure.

    `tail_steps=6` is not a detail. The figure puts the fifth on the last
    offbeat of the bar so it leans into the next chord; cut at the bar line
    that note dies at the moment it is meant to arrive, and the first half of
    every bar goes quiet."""
    return cached_line(pattern, dur_bars, wave='saw', detune=detune,
                       f_lo=95.0, f_hi=f_hi, res=res, decay=decay,
                       cut_decay=cut_decay, hold=hold, acc_amt=0.42,
                       drive=drive, glide_ms=glide_ms, base=0.09, bands=7,
                       sub=sub, sub_lp=105.0, low=0.0, gain=level * 0.70,
                       spread=0.0, tail_steps=tail_steps)


# ============================================================== the guitar ===
def combo(x, warm=1.55, tone=4400, tight=95.0, cone=0.85, presence=0.72,
          seed=0, mic=1.0):
    """A clean combo, which is not `punklib.amp` with the gain turned down.

    That chain is three clipping stages into a 4x12, and its whole job is to
    make harmonics that were not there. This one has ONE valve stage run
    barely into its curve - enough that a hard strum is a slightly different
    spectrum from a soft one, which is the only thing a clean amp actually
    does - and a single twelve-inch speaker rather than four. The cabinet is
    tighter in the low end (`low=88`, because a combo has no 4x12's port),
    has less of the cone resonance that makes a stack sound big, and less
    presence, because bite is what this record is trying not to have.

    The valve is asymmetric on purpose. A symmetric shaper produces odd
    harmonics only, and odd harmonics are hollow and hard; the second
    harmonic is an octave and the fourth is two, so an asymmetric curve is
    heard as warmth rather than as distortion."""
    st = x if x.ndim == 2 else stereo(x)
    st = hp(st, tight, order=2)
    st = drive_asym(st, warm, asym=0.22)
    st = cab(st, seed=seed, low=88.0, high=5400.0, cone=cone,
             presence=presence, mic=mic)
    return lp(st, tone).astype(np.float32)


@cached
def gtr(notes, dur_steps=3.0, level=1.0, vel=0.72, decay=0.60, damp=0.042,
        bright=0.90, strum=0.0068, pick=0.21, pickup=0.14, res_hz=2400.0,
        res_q=2.1, warm=1.55, tone=4400, chorus=0.42, hp_hz=150.0,
        cone=0.85, presence=0.72, tight=95.0, tilt_base=0.35, take=0):
    """The chord this record is built on: an electric guitar, comped.

    A pad states harmony and a guitar PLAYS it, and the difference is
    entirely in the attack. Six strings do not arrive together - the plectrum
    crosses them over six or seven milliseconds - and every one of them is a
    few cents out from the others, because a guitar is tempered by a person
    with their fingers. Strike four notes at one instant, in tune, and the
    result is an organ however good the timbre is.

    `core.string` supplies the physics: stiffness, so the upper partials go
    progressively sharp and the note reads as an object rather than a tone;
    two polarisations at slightly different frequencies and very different
    decay rates, which is why a plucked note drops a few dB at once and then
    rings; the comb of where it was picked and where the pickup sits; and the
    coil's own resonance, which is where an electric guitar gets the word
    electric from. `res_hz=2400` is a neck humbucker - dark and round. A
    single coil sits nearer 3.5 kHz and is the wrong instrument for this.

    `vel` is not a fader. A soft stroke puts less energy into the high modes,
    so it is DARKER as well as quieter, and that is most of what makes a comp
    breathe across a bar instead of pulsing. Measured on one Bb3: a hard
    stroke puts 20% of the note in 800-3000 Hz and a soft one 12%.

    `pick` and `pickup` are two independent combs, and where their nulls land
    decides whether this instrument has a presence band at all. The obvious
    warm settings - picking over the neck at 0.33, a neck pickup at 0.22 - put
    BOTH nulls on the fourth and fifth harmonics, which for a chord voiced
    around Bb3 is exactly 800-2000 Hz, and the guitar then measures 98% inside
    its own first three harmonics: a mid-range blob with nothing for the ear
    to locate. Picking nearer the bridge moves the nulls up past the band the
    record needs, and the amp's lowpass is where the warmth comes back.

    `tilt_base` is the right hand. A plectrum is a hard edge and bends the
    string into a sharp corner; a fingertip is soft and rounds it off, so the
    same note picked with a finger has audibly fewer high modes in it. That is
    a real difference between two techniques on one instrument, and it is not
    a tone control - dropping `tilt_base` toward zero for a fingerpicked part
    is what stops it screaming in 800-3000 Hz where a strummed comp is happy.

    `tight` is the amp's input highpass, and on a comp it is a compositional
    control rather than a corrective one. A guitar voiced from A3 up has its
    lowest fundamentals at 220-260 Hz, right where a house record's warmth
    already lives; letting them through makes the instrument sit on the floor,
    and cutting under them makes it float above the bass instead. Nothing else
    in the chain moves an instrument that far for that little.

    `decay` is the right hand: 0.6 s is a chord allowed to ring into the next
    beat, 0.18 s is the heel of the palm resting on the bridge. Both are the
    same instrument, and alternating them is what a guitarist does instead of
    playing louder."""
    n, t = steps(dur_steps, floor=int(0.34 * SR))
    x = np.zeros(n)
    rng = np.random.default_rng(4200 + take * 97 + int(sum(notes)))
    for i, nt in enumerate(sorted(notes)):
        f = midi(nt) * (1 + 0.0022 * (rng.random() - 0.5) * 2)
        d = int((strum * i + 0.0011 * rng.random()) * SR)
        if d >= n:
            break
        s_ = string(f, n - d, decay=decay * (1 - 0.07 * i), damp=damp,
                    pick=pick + 0.06 * rng.random(), pickup=pickup,
                    B=1.3e-4 * (82.0 / f) ** 0.4, bright=bright,
                    tilt=tilt_base - 0.55 * (1.0 - vel), res_hz=res_hz, res_q=res_q,
                    top=6200.0,
                    seed=int(7919 * take + 13 * nt))
        x[d:] += s_ * (1.0 - 0.09 * i)
    x /= max(len(notes), 1)
    st = combo(x, warm=warm, tone=tone, cone=cone, presence=presence,
               tight=tight, seed=take % 3)
    if chorus:
        # A Jazz Chorus is a bucket brigade, and so is a Solina - the same
        # circuit doing the same job. Three rates that never line up is why
        # it shimmers where a single-rate chorus warbles.
        st = _bbd(st, mix=chorus, tone=5600, seed=take + 40)
    st = hp(st, hp_hz, order=2)
    return (st * adsr(n, a=0.0004, r=0.030)[:, None]).astype(np.float32) * level * vel * 0.72
