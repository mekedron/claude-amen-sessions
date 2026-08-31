"""ZUB4ATKA (~3:52, 168 bars @174) - drill'n'bass in F# minor, the Aphex school.

Three things carry this one, and all three are the engine that was already here,
tuned rather than replaced:

  ratchet()   the instrument of the genre: one hit stamped n times across a span
              with the gap accelerating or dragging, the pitch sweeping through
              the burst, the bit depth collapsing as it goes.
  acid303()   a real 303 instead of a filtered saw: ONE oscillator running the
              whole bar so slides actually slide, a resonant filter that moves
              inside every note, accents that raise level and cutoff together,
              overdrive after the filter, and a cutoff that opens across a whole
              section instead of jumping about at random. Random cutoff per note
              is why an acid line sounds flat - it twitches instead of travelling.
  arp()       a stream, not a loop: the note sequence runs on a cycle coprime
              with 16 (5, 7, 9, 11) and never restarts at a bar line, so it lands
              on a different beat every bar and takes 7 or 11 bars to come round.
              A 4- or 8-note arp always hits the same step - that is why arps
              sound identical everywhere.

Harmony: F#m9 - Emaj9 - Dmaj7 - C#m7, one bar each. The bass walks F# E D C#,
the tune never moves, so every note changes meaning under it: 11th, 13th, 9th,
root. Emaj9 carries D#, the dorian 6th - the only light in the key.

  b0-7     the box, alone, tape drifting, the first ratchets
  b8-19    the break walks in and starts twitching; the arp begins and never stops
  b20-43   mangle I: euclidean gating, scattered micro-slices, the acid opens
  b44-51   the window: halftime, the pad opens, the tune sings
  b52-83   mangle II: polymeter 5/7/11, ratchet walls, beat-repeat, a 15/16 bar
  b84-87   the collapse: tape stop
  b88-119  the reward: the groove locks, tune and chaos in the same bar
  b120-151 the last storm: everything at once, the count still holding
  b152-167 the spring runs out
"""
import numpy as np
from amenlib import *

rng = np.random.default_rng(0xA9EF)
np.random.seed(0xA9EF)
s = Session(168, tail=3.0)

# ---------------------------------------------------------------- the key ----
CHORDS = [[54, 57, 61, 64, 68],      # F#m9   F# A  C# E  G#
          [52, 56, 59, 63, 66],      # Emaj9  E  G# B  D# F#   (D# = dorian 6th)
          [50, 54, 57, 61],          # Dmaj7  D  F# A  C#
          [49, 52, 56, 59]]          # C#m7   C# E  G# B
SUBS = [30, 28, 26, 25]              # F#1 E1 D1 C#1 - the lament bass, walking down.
                                     # It goes below what a phone can move, which is what
                                     # the driven MIDS layer is for: it puts the same line
                                     # two octaves up and lets the ear rebuild the root.
MIDS = [42, 40, 38, 37]              # two octaves up: what phones actually hear

# The tune: 32 steps, 3+3+2 both bars, arch peaking at step 22. Every note is a
# chord tone or a legal tension over all four chords, so it never has to move.
TUNE = [(0, 78), (3, 81), (6, 85), (8, 83), (11, 81), (14, 78),
        (16, 80), (19, 83), (22, 88), (24, 85), (27, 83), (30, 80)]

TICK32 = int(0.5 * STEP)
TICK64 = int(0.25 * STEP)

def blend(*segs):
    """sum segments of unequal length - layering a bell over a pluck"""
    n = max(len(x) for x in segs)
    out = np.zeros((n, 2), dtype=np.float32)
    for x in segs:
        out[:len(x)] += x
    return out

def euclid(k, n):
    """E(k,n): k hits spread as evenly as possible over n steps"""
    return [int(np.floor(i * k / n) != np.floor((i - 1) * k / n)) for i in range(n)]

# ------------------------------------------------------ cutting the break ----
def scatter(b, n=16, keep=(0, 4, 8, 12), seed=0, gain=0.85, warp=0.0, src=0):
    """cut a bar into n pieces and deal them out again in a new order, with the
    anchors nailed down: the count survives, everything between it moves"""
    r = np.random.default_rng(0xC0FFEE + seed)
    pieces = amen.chop(n, bar=src)
    order = list(range(n))
    free = [i for i in order if i * 16 // n not in keep]
    r.shuffle(free)
    it = iter(free)
    out = [i if i * 16 // n in keep else next(it) for i in order]
    for slot, pick in enumerate(out):
        seg = pieces[pick]
        if warp and r.random() < warp:
            seg = [rev, lambda x: pitched(x, 0.5), lambda x: pitched(x, 2.0),
                   lambda x: bitcrush(x, 4, 6)][int(r.integers(4))](seg)
        s.place(s.pos(b) + int(slot * 16 / n * STEP), seg,
                gain if pick * 16 // n in keep else gain * 0.72)

def gate_bar(b, k=9, n=16, gain=0.9, src=0, shift=0, crush=0):
    """run a whole bar of the break through a euclidean gate - the bar keeps its
    own internal timing, the holes are cut out from over the top"""
    bar = bar_of(src)
    if crush:
        bar = bitcrush(bar, crush, 5)
    pat = euclid(k, n)
    pat = pat[shift:] + pat[:shift]
    step = len(bar) / n
    for i, on in enumerate(pat):
        if not on:
            continue
        a = int(i * step)
        s.place(s.pos(b) + a, fade_edges(bar[a:int(a + step)], 2.0), gain)

def layered(b, gain=0.9):
    """two readings of the same break at once: the bar underneath, and a
    half-speed copy of another bar over the top, filtered out of its way"""
    s.place(s.pos(b), bar_of(0), gain)
    s.place(s.pos(b), hp(pitched(bar_of(3), 0.5), 900)[:int(BAR)], gain * 0.28)

# --------------------------------------------------------------- ratchets ----
def ratchet(t, seg, n=6, span=2.0, gain=0.7, curve=0.65, pitch=0.0,
            shape='down', crush=0.0, pan=0.0, bus='main'):
    """One hit stamped n times across `span` steps - the sound of this track.
    curve < 1 packs them toward the end (accelerating, the classic); curve > 1
    drags them apart. pitch = semitones swept across the whole burst."""
    u = np.linspace(0.0, 1.0, n) ** curve
    for i in range(n):
        f = i / max(n - 1, 1)
        p = seg
        if pitch:
            p = pitched(p, 2.0 ** (pitch * f / 12.0))
        if crush:
            p = bitcrush(p, bits=max(3, int(8 - crush * f * 5)),
                         downsample=1 + int(crush * f * 6))
        lv = {'down': 1 - 0.55 * f, 'up': 0.40 + 0.60 * f, 'flat': 1.0,
              'bow': 1 - 1.6 * abs(0.5 - f)}[shape]
        if pan:
            p = panned(p, pan * (1 if i % 2 else -1))
        s.place(t + int(u[i] * span * STEP), p, gain * lv, bus)

def beatrepeat(t_src, len_steps, t_dst, times, gain=1.0, decay=0.88,
               crush=0.0, pitch=0.0, bus='main'):
    """read back what is already on the bus and stamp it down again: the
    hardware beat-repeat, the loop eating its own tail"""
    buf = s._buf(bus)
    a = int(t_src); e = min(a + int(len_steps * STEP), len(buf))
    grab = fade_edges(np.array(buf[a:e]), 1.5)
    if len(grab) < 32:
        return
    for i in range(times):
        p = grab
        if pitch:
            p = pitched(p, 2.0 ** (pitch * i / 12.0))
        if crush:
            p = bitcrush(p, bits=max(3, int(7 - crush * i)), downsample=1 + i)
        s.place(t_dst + int(i * len_steps * STEP), p, gain * decay ** i, bus)

# ------------------------------------------------------------- the acid -----
ACID_SEQ = [   # (step, midi, len_steps, accent, slide)
    [(0, 42, 1, 1, 0), (2, 42, .5, 0, 0), (3, 54, 1.5, 0, 1), (5, 45, 1, 0, 0),
     (6, 42, .5, 0, 0), (7, 49, 1.5, 1, 1), (10, 42, 1, 0, 0), (11, 52, .5, 0, 1),
     (12, 42, 1, 0, 0), (14, 50, 2, 1, 1)],
    [(0, 42, 1.5, 1, 0), (2, 49, 1, 0, 1), (4, 42, .5, 0, 0), (5, 42, .5, 0, 0),
     (6, 54, 2, 1, 1), (9, 47, 1, 0, 0), (10, 42, .5, 0, 0), (11, 45, 1, 0, 1),
     (13, 57, 1.5, 1, 1), (15, 42, 1, 0, 0)],
    [(0, 30, 2, 1, 0), (3, 42, 1, 0, 1), (4, 44, .5, 0, 0), (5, 42, 1, 0, 0),
     (7, 49, 1, 1, 1), (8, 42, .5, 0, 0), (10, 52, 1.5, 0, 1), (12, 42, 1, 1, 0),
     (13, 45, .5, 0, 0), (14, 61, 2, 1, 1)],
    [(0, 42, 1, 1, 0), (1, 42, .5, 0, 0), (2.5, 47, 1, 0, 1), (4, 42, 1, 0, 0),
     (6, 50, 1.5, 1, 1), (8, 42, .5, 0, 0), (9, 54, 1, 0, 1), (11, 42, 1, 0, 0),
     (12.5, 45, 1, 0, 0), (14, 42, 2, 1, 1)],
]

def acid303(b, seq, gain=0.22, cut=(300, 2400), res=6.0, drive=2.4, glide=0.05,
            bands=8, pan=0.0, bus='music', transpose=0, dur=16):
    """One oscillator across the whole bar, a filter that moves inside every
    note, drive after the filter. This is why it sounds like a machine being
    played rather than a saw being gated."""
    n = int(round(dur * STEP))
    f_i = np.zeros(n); amp = np.zeros(n); cen = np.full(n, float(cut[0]))
    prev = None
    for st, note, ln, acc, sl in seq:
        a = int(st * STEP); e = min(int((st + ln) * STEP), n)
        if a >= n or e <= a:
            continue
        f = midi(note + transpose); m = e - a; tt = np.arange(m) / SR
        f_i[a:e] = (f + (prev - f) * np.exp(-tt / glide)) if (sl and prev) else f
        dc = 0.055 if acc else 0.115                      # accents are shorter
        amp[a:e] = np.maximum(amp[a:e], (1.0 if acc else 0.70) * np.exp(-tt / dc))
        top = cut[1] * (2.0 if acc else 1.0)              # ...and much brighter
        cen[a:e] = np.maximum(cen[a:e],
                              cut[0] + (top - cut[0]) * np.exp(-tt / (dc * 1.7)))
        prev = f
    # hold the last pitch through the gaps so the oscillator never restarts
    idx = np.where(f_i > 0)[0]
    if len(idx) == 0:
        return np.zeros((n, 2), dtype=np.float32)
    f_i[:idx[0]] = f_i[idx[0]]
    fill = np.maximum.accumulate(np.where(f_i > 0, np.arange(n), 0))
    f_i = f_i[fill]

    ph = 2 * np.pi * np.cumsum(f_i) / SR
    x = saw_ph(ph, float(f_i.max()) * 4) * 0.85 + 0.22 * np.sign(np.sin(ph))
    x = stereo(x * amp)

    lo, hi = 170.0, 5400.0                                # the moving filter
    fcs = np.geomspace(lo, hi, bands)
    posn = np.interp(np.log(np.clip(cen, lo, hi)), np.log(fcs), np.arange(bands))
    out = np.zeros((n, 2), dtype=np.float32)
    for i, fc in enumerate(fcs):
        w = np.clip(1.0 - np.abs(posn - i), 0.0, 1.0)
        if w.max() < 1e-3:
            continue
        band = lp(x, fc * 1.25) + res * bandpass(x, fc * 0.86, fc * 1.16)
        out += (band * w[:, None]).astype(np.float32)
    out = np.tanh(drive * out / (1.0 + res * 0.55)).astype(np.float32)
    out = hp(out, 90)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0009))
    return panned(out, pan) * gain if pan else out * gain

# ------------------------------------------------------------- the arp ------
def _shape(c, kind):
    if kind == 'up':        return c
    if kind == 'down':      return c[::-1]
    if kind == 'updown':    return c + c[-2:0:-1]
    if kind == 'thumb':     return [v for nn in c[1:] for v in (c[0], nn)]
    if kind == 'spread':    return [c[0], c[2] + 12, c[1], c[-1], c[0] + 12, c[3 % len(c)]]
    if kind == 'converge':  return [v for pr in zip(c, c[::-1]) for v in pr][:len(c) + 2]
    if kind == 'skip':      return c[::2] + [n + 12 for n in c[1::2]]
    return c

def _cycle(c, kind, cycle):
    """Force the sequence to exactly `cycle` notes, climbing an octave each time
    it runs out. The length MUST NOT divide 16 or the arp restarts on the same
    step of every bar - which is exactly what makes an arp sound like wallpaper.
    All the cycles used here (5, 7, 9, 11) are odd, so they never do."""
    base = _shape(c, kind) or list(c)
    seq, o = list(base), 0
    while len(seq) < cycle:
        o += 12
        seq += [n + o for n in base]
    seq = seq[:cycle]
    if 16 % len(seq) == 0:
        seq.append(seq[0] + 12)
    return seq

ARP_N = 0          # the running note counter: the arp never restarts at a bar

def arp(b, ci, kind='updown', cycle=7, gate=(11, 16), gain=0.085, oct_span=1,
        timbre='pluck', dur=1.5, pan=0.55, bus='music', stride=1.0, up=12):
    """A stream on a cycle coprime with 16, carried across bar lines by ARP_N,
    with a euclidean gate for its rhythm - so it lands somewhere new every bar
    and takes `cycle` bars to come back round."""
    global ARP_N
    seq = _cycle([n + up for n in CHORDS[ci % 4]], kind, cycle)
    g = euclid(*gate)
    for i in range(int(16 / stride)):
        st = i * stride
        if not g[int(st) % gate[1]]:
            ARP_N += 1
            continue
        note = seq[ARP_N % len(seq)] + 12 * ((ARP_N // len(seq)) % (oct_span + 1))
        f = midi(note)
        if timbre == 'pluck':   seg = pluck(f, dur)
        elif timbre == 'bell':  seg = bell(f, dur * 1.6, 0.75)
        elif timbre == 'clav':  seg = clav([f], dur, 0.7)
        else:                   seg = blend(pluck(f, dur), bell(f, dur, 0.35))
        s.place(s.pos(b, st), panned(seg, np.sin(ARP_N * 1.9) * pan), gain, bus)
        ARP_N += 1

# ------------------------------------------------------------ the melody ----
def box(b0, gain=0.13, detune=1.0, notes=None, dur=2.6, wet=0.42, drift=0.0,
        shift=0, oct_=0):
    for st, note in (notes or TUNE):
        f = midi(note + shift + 12 * oct_) * detune
        seg = blend(bell(f, dur), pluck(f, dur * 0.6, 0.55))
        if drift:
            seg = wow(seg, depth_ms=drift, rate=0.31)
        s.place(s.pos(b0) + int(st * STEP),
                reverb(panned(seg, np.sin(st * 1.7) * 0.55), decay=2.6, wet=wet),
                gain, 'music')

def frag(keep):
    return [(st, n) for i, (st, n) in enumerate(TUNE) if i % keep[0] in keep[1:]]

def chord(b, i, dur=16, gain=0.085, cut=1500):
    s.place(s.pos(b), pad([midi(n) for n in CHORDS[i % 4]], dur, cut), gain, 'pad')

def bassline(b, i, sub_g=0.30, mid_g=0.0, dur=16):
    s.place(s.pos(b), sub(midi(SUBS[i % 4]), dur), sub_g, 'bass')
    if mid_g:
        # driven and high-passed off the sub: this layer is what a phone hears
        mid = dirty(hp(reese(midi(MIDS[i % 4]), dur, 620), 95), 2.2)
        s.place(s.pos(b), shelf(mid, 400, 3.0), mid_g, 'bass')

# --------------------------------------------------------- the chopping -----
PHRASES = [
    [(1, 0, 6, 1), (2.5, 0, 8, 1.5), (5, 3, 2, 1), (6, 0, 10, 2), (9, 0, 6, 1),
     (10.5, 3, 10, 1.5), (13, 0, 2, 1), (15, 0, 8, 1)],
    [(2, 0, 10, 2), (3.5, 0, 6, .5), (6, 2, 12, 1), (7, 0, 8, 1), (9, 0, 0, 1),
     (11, 3, 2, 2), (14, 0, 6, 1), (15, 0, 6, 1)],
    [(1.5, 3, 10, 1), (3, 0, 8, 1), (5.5, 0, 2, 1.5), (8.5, 0, 6, 1),
     (10, 0, 10, 2), (13.5, 2, 12, 1), (15, 0, 4, 1)],
    [(1, 0, 2, 1), (2, 0, 6, 1), (3, 0, 8, 1), (6.5, 0, 10, 1.5), (9, 3, 2, 1),
     (11, 0, 6, 2), (14.5, 0, 8, 1.5)],
]

def mangle(b, heat=1.0, anchors=True, skip=0.0):
    """the count is sacred - kick on 1, snares on 2 and 4, full volume;
    chaos lives between the anchors, quieter, and gets hotter with `heat`"""
    r = np.random.default_rng(0xBEE + b * 7)
    if anchors:
        s.place(s.pos(b, 0), K); s.hit(s.pos(b, 0))
        s.place(s.pos(b, 4), SN)
        s.place(s.pos(b, 12), S2)
        if r.random() < 0.45:
            s.place(s.pos(b, 10), K2, 0.8); s.hit(s.pos(b, 10))
    for st, sb, ss, ln in PHRASES[b % 4]:
        if anchors and st in (4.0, 12.0):
            continue
        if r.random() < skip:
            continue
        seg = get(sb, ss, max(ln, 1.0)); t = s.pos(b, st); d = r.random()
        if d < 0.22 * heat:
            ratchet(t, seg[:TICK32], n=int(r.integers(4, 10)),
                    span=float(r.choice([1.0, 1.5, 2.0])), gain=0.62,
                    curve=float(r.choice([0.5, 0.65, 1.6])),
                    pitch=float(r.choice([0, 0, 7, -5, 12])),
                    shape=str(r.choice(['down', 'up', 'bow'])),
                    crush=float(r.choice([0.0, 0.0, 1.2])),
                    pan=float(r.choice([0.0, 0.5])))
            continue
        if d < 0.33 * heat:   seg = pitched(seg, float(r.choice([.5, .75, 1.5, 2., .66])))
        elif d < 0.43 * heat: seg = rev(seg)
        elif d < 0.53 * heat: seg = bitcrush(seg, int(r.integers(4, 7)), int(r.choice([3, 5, 8])))
        elif d < 0.59 * heat: seg = pitched(seg, 0.35)          # timestretch smear
        s.place(t, seg, float(r.uniform(0.45, 0.72)))

def polyperc(b0, b1, cycle=7, gain=0.11, src=None, bus='main', bright=3.5):
    src = src if src is not None else G
    src = shelf(src[:TICK32], 5000, bright)
    for i in range(int((b1 - b0) * 16 / cycle)):
        s.place(s.pos(b0) + int(i * cycle * STEP),
                panned(src, np.sin(i * 2.1) * 0.7), gain, bus)

# ============================ b0-7: the box, alone ============================
s.place(s.pos(0), crackle(128), 0.42, 'fx')
s.place(s.pos(0), wind(128, 0.5), 0.10, 'fx')
for i, b in enumerate((0, 2, 4, 6)):
    box(b, 0.145, detune=1.0 - i * 0.0015, drift=1.4 + i * 0.4)
for i, b in enumerate((0, 2, 4, 6)):
    chord(b, i, 32, 0.052)
s.place(s.pos(3, 14), G[:TICK32], 0.25)
ratchet(s.pos(5, 12), G[:TICK64], n=5, span=1.0, gain=0.22, curve=0.5, pitch=5)
for b in (6, 7):                                        # the acid, far away
    s.place(s.pos(b), lp(acid303(b, ACID_SEQ[b % 4], 0.10, (240, 900), 4.0, 1.8), 1400),
            1.0, 'music')
ratchet(s.pos(7, 8), SN1[:TICK32], n=9, span=6.0, gain=0.30, curve=0.45,
        pitch=-3, shape='up', crush=1.0)

# ============================ b8-19: entrance ================================
s.place(s.pos(8), CR, 0.7)
for b in range(8, 20):
    i = b % 4
    if b in (11, 15, 17, 18, 19):
        mangle(b, heat=0.6 + (b - 8) * 0.03)
    elif b in (13, 16):
        gate_bar(b, k=11, shift=b % 3, gain=0.88)
    else:
        layered(b, 0.9); s.hit(s.pos(b, 0)); s.hit(s.pos(b, 10))
        if b % 2 == 1:
            ratchet(s.pos(b, float(rng.choice([7, 14.5, 15]))), SN1[:TICK32],
                    n=int(rng.integers(3, 7)), span=1.0, gain=0.5, curve=0.6)
    bassline(b, i, 0.33 if b < 14 else 0.39, 0.0 if b < 14 else 0.19)
    chord(b, i, 16, 0.07)
    if b >= 12:
        arp(b, i, 'updown', 7, (11, 16), 0.075, timbre='pluck', up=12)
    if b >= 16:
        s.place(s.pos(b), acid303(b, ACID_SEQ[i], 0.15, (300, 1500), 5.0, 2.0),
                1.0, 'music')
for b in (8, 12, 16):
    box(b, 0.115, detune=0.9985, drift=0.8)
ratchet(s.pos(19, 8), SN1[:TICK32], n=13, span=8.0, gain=0.55, curve=0.5,
        pitch=7, shape='up', crush=1.4)

# ============================ b20-43: mangle I ===============================
s.place(s.pos(20), subdrop(8, 82, 30), 0.46, 'bass')
s.place(s.pos(20), CR, 0.9)
ARP_SHAPES = ['updown', 'spread', 'thumb', 'skip', 'converge', 'down']
for b in range(20, 44):
    i = b % 4
    if b % 8 == 4:    gate_bar(b, k=9 + b % 3, shift=b % 5, gain=0.9, crush=0 if b % 16 else 5)
    elif b % 8 == 6:  scatter(b, 16, (0, 4, 12), seed=b, warp=0.35)
    else:             mangle(b, heat=0.95)
    bassline(b, i, 0.36, 0.23)
    chord(b, i, 16, 0.055, 1250)
    # the acid opens across the whole section instead of jumping about
    u = (b - 20) / 23.0
    s.place(s.pos(b), acid303(b, ACID_SEQ[(b + b // 8) % 4], 0.20,
                              (280 + 120 * u, 1500 + 1700 * u), 5.0 + 2.5 * u,
                              2.0 + 0.9 * u, pan=0.25 * np.sin(b * 0.7)),
            1.0, 'music')
    arp(b, i, ARP_SHAPES[(b // 4) % len(ARP_SHAPES)], [7, 9, 5, 11][(b // 6) % 4],
        (11, 16) if b % 2 else (9, 16), 0.085,
        timbre=['pluck', 'clav', 'both'][(b // 8) % 3], up=12)
polyperc(20, 44, 7, 0.135)
polyperc(20, 44, 5, 0.095, src=rim(1, 0.8))
for b in (22, 30, 38):
    box(b, 0.105, detune=float(rng.choice([1.0, 0.9975])), drift=1.0,
        notes=frag((2, 0)) if b == 30 else None)
s.place(s.pos(35), bitcrush(bar_of(3), 4, 6), 0.85)
beatrepeat(s.pos(39, 12), 1.0, s.pos(39, 13), 3, 0.9, 0.9, crush=1.2)
ratchet(s.pos(43, 8), SN1[:TICK32], n=15, span=8.0, gain=0.6, curve=0.42,
        pitch=10, shape='up', crush=1.8)
s.place(s.pos(42), riser(32), 0.42, 'fx')

# ============================ b44-51: the window =============================
s.place(s.pos(44), impact(24), 0.35, 'fx')
for b in range(44, 52):
    i = b % 4
    s.pat(b, [(0, K, 0.9), (8, SN, 0.88), (14, K2, 0.55)])
    s.hit(s.pos(b, 0))
    s.place(s.pos(b, 6), G, 0.35)
    if b % 4 == 3:
        ratchet(s.pos(b, 12), G[:TICK32], n=6, span=3.0, gain=0.34, curve=0.7,
                pitch=4, shape='bow')
    bassline(b, i, 0.34, 0.16)
    chord(b, i, 16, 0.115, 2000)
    arp(b, i, 'spread', 9, (7, 16), 0.075, timbre='bell', dur=2.2, up=12)
for b in (44, 46, 48, 50):
    box(b, 0.165, drift=0.6, wet=0.5)
s.place(s.pos(48), strings([midi(n) for n in CHORDS[0]], 64, 0.055), 1.0, 'pad')
s.pat(51, [(12, SN1, .6), (13, SN1, .75), (14, SN1, .9), (15, SN1, 1.)])
s.place(s.pos(50), riser(32, 0.5, 200, 900), 1.0, 'fx')

# ============================ b52-83: mangle II ==============================
s.place(s.pos(52), subdrop(10, 90, 27), 0.52, 'bass')
s.place(s.pos(52), CR, 0.95)
for b in range(52, 84):
    i = b % 4
    heat = 1.0 + (b - 52) * 0.012
    if b == 70:                                        # the bar that trips: 15/16
        for st, sb, ss, ln in PHRASES[2]:
            s.place(s.pos(b, max(st - 1, 0)), get(sb, ss, max(ln, 1.0)), 0.6)
        s.place(s.pos(b, 0), K); s.hit(s.pos(b, 0))
    elif b % 8 == 3:  gate_bar(b, k=13, shift=b % 7, gain=0.9)
    elif b % 8 == 5:  scatter(b, 32, (0, 4, 12), seed=b * 3, warp=0.45)
    else:             mangle(b, heat=heat, skip=0.12 if b % 8 == 6 else 0.0)
    bassline(b, i, 0.37, 0.25)
    if b % 2 == 0:
        chord(b, i, 16, 0.05, 1150)
    u = (b - 52) / 31.0
    s.place(s.pos(b), acid303(b, ACID_SEQ[(b + b // 5) % 4], 0.225,
                              (300 + 260 * u, 2200 + 2100 * u), 6.0 + 2.5 * u,
                              2.4 + 1.0 * u, glide=0.038,
                              pan=0.3 * np.sin(b * 0.9),
                              transpose=[0, 0, -5, 0, 7, 0, 0, -12][b % 8]),
            1.0, 'music')
    arp(b, i, ARP_SHAPES[(b // 3) % len(ARP_SHAPES)], [9, 7, 11, 5][(b // 4) % 4],
        [(11, 16), (13, 16), (9, 16)][(b // 5) % 3], 0.08,
        timbre=['clav', 'pluck', 'both', 'bell'][(b // 6) % 4],
        stride=1.0 if b % 4 else 0.5, up=12, oct_span=1)
    if b % 8 == 5:
        s.place(s.pos(b, float(rng.choice([2, 6, 10]))),
                hoover(midi(int(rng.choice([54, 57, 61]))), 2), 0.22, 'music')
polyperc(52, 84, 7, 0.145)
polyperc(52, 84, 5, 0.105, src=rim(1, 0.8))
polyperc(54, 84, 11, 0.085, src=hat(0.5, gain=0.7))
for b in (56, 64, 74, 80):
    box(b, 0.10, detune=float(rng.choice([0.995, 0.9975, 1.0])), drift=1.6,
        notes=frag((3, 0, 2)) if b in (64, 80) else None)
ratchet(s.pos(59, 8), K[:TICK32], n=12, span=8.0, gain=0.55, curve=0.45,
        pitch=-7, shape='flat', crush=1.5, pan=0.5)
beatrepeat(s.pos(63, 8), 2.0, s.pos(63, 10), 3, 0.95, 0.92, pitch=-2)
ratchet(s.pos(67, 12), SN1[:TICK64], n=17, span=4.0, gain=0.42, curve=0.4,
        pitch=14, shape='up', crush=2.0, pan=0.6)
beatrepeat(s.pos(71, 12), 1.0, s.pos(71, 13), 3, 1.0, 0.95, crush=1.5, pitch=3)
s.place(s.pos(75), bitcrush(pitched(bar_of(3), 0.75), 4, 7), 0.8)
ratchet(s.pos(79, 4), S2[:TICK32], n=8, span=4.0, gain=0.5, curve=1.7,
        pitch=-12, shape='down')
beatrepeat(s.pos(82, 0), 0.5, s.pos(82, 8), 8, 0.85, 0.94, crush=1.0, pitch=1)
for st in np.arange(8, 16, 0.5):
    s.place(s.pos(83, st), SN1, 0.45 + (st - 8) * 0.055)
s.place(s.pos(82), riser(32, 0.5, 240, 1100), 1.0, 'fx')

# ============================ b84-87: the collapse ===========================
s.place(s.pos(84), tape_stop(bar_of(0), 0.9), 0.85)
s.place(s.pos(84), downlifter(16, 0.45), 1.0, 'fx')
s.place(s.pos(85), crackle(64), 0.5, 'fx')
box(85, 0.11, detune=0.9935, drift=3.5, wet=0.6)
chord(85, 2, 32, 0.06, 900)
s.place(s.pos(86, 8), rev(reverb(S2, decay=3.0, wet=0.9)), 0.3, 'fx')
ratchet(s.pos(87, 0), G[:TICK64], n=19, span=15.5, gain=0.34, curve=0.38,
        pitch=12, shape='up', crush=2.2)
s.place(s.pos(86), riser(32, 0.55), 1.0, 'fx')

# ============================ b88-119: the reward ============================
s.place(s.pos(88), subdrop(10, 85, 28), 0.5, 'bass')
s.place(s.pos(88), CR, 0.9)
for b in range(88, 120):
    i = b % 4
    if b % 8 == 7:    mangle(b, heat=0.85)
    elif b % 8 == 3:  gate_bar(b, k=13, shift=b % 4, gain=0.9)
    else:
        layered(b, 0.92); s.hit(s.pos(b, 0)); s.hit(s.pos(b, 10))
        if b % 4 == 2:
            ratchet(s.pos(b, 14), G[:TICK32], n=5, span=2.0, gain=0.4,
                    curve=0.6, pitch=7, shape='up')
    s.place(s.pos(b), wobble(midi(SUBS[i]), 16, 2.2 if b % 2 == 0 else 3.3),
            0.40, 'bass')
    s.place(s.pos(b), shelf(dirty(hp(reese(midi(MIDS[i]), 16, 640), 95), 2.2), 400, 3.0), 0.22, 'bass')
    chord(b, i, 16, 0.085, 1700)
    arp(b, i, ARP_SHAPES[(b // 4) % len(ARP_SHAPES)], [7, 11, 9][(b // 8) % 3],
        (11, 16), 0.08, timbre=['bell', 'pluck', 'both'][(b // 8) % 3],
        dur=1.8, up=12)
    if b % 4 in (1, 3):
        s.place(s.pos(b), acid303(b, ACID_SEQ[i], 0.17, (340, 2600), 6.5, 2.5,
                                  pan=0.3 * np.sin(b)), 1.0, 'music')
for b in range(88, 120, 2):
    box(b, 0.145, drift=0.5, wet=0.45,
        notes=frag((2, 1)) if b % 8 == 4 else None)
for b in (96, 112):
    s.place(s.pos(b), strings([midi(n) for n in CHORDS[b % 4]], 64, 0.05), 1.0, 'pad')
polyperc(92, 120, 7, 0.115)
beatrepeat(s.pos(103, 12), 1.0, s.pos(103, 13), 3, 0.9, 0.9)
s.place(s.pos(104), CR, 0.6)
ratchet(s.pos(119, 8), SN1[:TICK32], n=15, span=8.0, gain=0.6, curve=0.42,
        pitch=12, shape='up', crush=1.6)

# ============================ b120-151: the last storm =======================
s.place(s.pos(120), subdrop(12, 95, 26), 0.55, 'bass')
s.place(s.pos(120), CR, 1.0)
for b in range(120, 152):
    i = b % 4
    if b % 8 == 2:    scatter(b, 32, (0, 4, 12), seed=b * 5, warp=0.5)
    elif b % 8 == 6:  gate_bar(b, k=13, shift=b % 6, gain=0.92)
    else:             mangle(b, heat=1.25)
    s.place(s.pos(b), wobble(midi(SUBS[i]), 16, 3.3 if b % 2 else 2.2), 0.39, 'bass')
    s.place(s.pos(b), hp(growl(midi(MIDS[i]), 16, 4.5, 3.0), 95), 0.23, 'bass')
    chord(b, i, 16, 0.06, 1300)
    u = (b - 120) / 31.0
    s.place(s.pos(b), acid303(b, ACID_SEQ[(b * 3 + b // 4) % 4], 0.235,
                              (360 + 300 * u, 2800 + 2400 * u), 7.0 + 2.0 * u,
                              2.8 + 1.2 * u, glide=0.032,
                              pan=0.35 * np.sin(b * 1.3),
                              transpose=[0, 0, 7, -5, 0, 12, 0, -12][b % 8]),
            1.0, 'music')
    arp(b, i, ARP_SHAPES[(b // 2) % len(ARP_SHAPES)], [11, 9, 7, 5][(b // 3) % 4],
        [(13, 16), (11, 16)][(b // 4) % 2], 0.085,
        timbre=['clav', 'both', 'pluck'][(b // 5) % 3],
        stride=0.5 if b % 8 == 0 else 1.0, up=12, oct_span=1)
polyperc(120, 152, 7, 0.145)
polyperc(120, 152, 5, 0.11, src=rim(1, 0.8))
polyperc(121, 152, 11, 0.09, src=hat(0.5, gain=0.7))
for b in range(120, 152, 4):
    box(b, 0.135, detune=1.0 if b % 8 == 0 else 0.9975, drift=1.2,
        notes=frag((2, 0)) if b % 8 == 4 else None)
ratchet(s.pos(127, 8), K[:TICK32], n=14, span=8.0, gain=0.55, curve=0.42,
        pitch=-9, shape='flat', crush=1.6, pan=0.55)
beatrepeat(s.pos(131, 8), 2.0, s.pos(131, 10), 3, 0.95, 0.9, pitch=-3)
ratchet(s.pos(135, 10), SN1[:TICK64], n=21, span=6.0, gain=0.4, curve=0.36,
        pitch=17, shape='up', crush=2.2, pan=0.65)
beatrepeat(s.pos(139, 0), 0.5, s.pos(139, 8), 8, 0.85, 0.93, crush=1.2, pitch=2)
ratchet(s.pos(143, 12), S2[:TICK32], n=11, span=4.0, gain=0.5, curve=0.4,
        pitch=-14, shape='down', crush=1.4)
beatrepeat(s.pos(147, 12), 1.0, s.pos(147, 13), 3, 1.0, 0.96, crush=1.8, pitch=5)
for st in np.arange(8, 16, 0.25):
    s.place(s.pos(151, st), SN1[:TICK32], 0.35 + (st - 8) * 0.06)

# ============================ b152-167: the spring runs out ==================
for b in range(152, 158):
    s.pat(b, [(0, K, 0.8 - (b - 152) * .08), (8, SN, .75 - (b - 152) * .08)])
    s.place(s.pos(b), sub(midi(SUBS[b % 4]), 16), 0.22 - (b - 152) * .02, 'bass')
    chord(b, b % 4, 16, 0.075, 1400)
    if b < 155:
        arp(b, b % 4, 'down', 7, (7, 16), 0.06, timbre='bell', dur=2.4, up=12)
s.place(s.pos(152), acid303(152, ACID_SEQ[0], 0.13, (300, 1400), 5.0, 1.9), 1.0, 'music')
box(152, 0.15, drift=0.6, wet=0.5)
box(154, 0.13, detune=0.9985, drift=1.2, wet=0.55)
s.place(s.pos(156), crackle(112), 0.45, 'fx')
s.place(s.pos(156), wind(120, 0.5), 0.12, 'fx')
chord(158, 0, 64, 0.075, 1100); chord(162, 3, 64, 0.065, 900)

t0 = s.pos(158); gap = 2.05                              # each tick lower, later
for i, (st, note) in enumerate(TUNE):
    seg = reverb(wow(blend(bell(midi(note), 3.0), pluck(midi(note), 1.6, 0.4)),
                     depth_ms=2.2 + i * 0.35, rate=0.27), decay=4.0, wet=0.55)
    s.place(t0 + int(st * gap ** (i / 7.0) * STEP), pitched(seg, 1 - i * 0.021),
            0.135 * (1 - i * 0.058), 'music')
ratchet(s.pos(163, 8), G[:TICK32], n=7, span=6.0, gain=0.16, curve=2.2,
        pitch=-9, shape='down')                          # the ratchet, dying
s.place(s.pos(165), reverb(pitched(bell(midi(78), 4), 0.88), decay=7.0, wet=0.85),
        0.11, 'music')
s.place(s.pos(166, 0), K, 0.35)
s.place(s.pos(166, 0), sub(midi(18), 12), 0.14, 'bass')

def cut(b, st, length, fade_ms=2.0, buses=('main', 'bass', 'music', 'pad')):
    """the kill switch: a hole punched straight through the finished mix, the
    way a hand does it on stage. It removes masking so whatever lands next hits
    a rested ear - which is why it is worth more than any riser."""
    a = s.pos(b, st); e = a + int(length * STEP)
    for name in buses:
        if name not in s.bus:
            continue
        buf = s.bus[name]; e2 = min(e, len(buf))
        if a >= len(buf) or e2 <= a:
            continue
        env = np.zeros(e2 - a, dtype=np.float32)
        k = min(int(SR * fade_ms / 1000), (e2 - a) // 2)
        if k > 0:
            env[:k] = np.linspace(1, 0, k); env[-k:] = np.linspace(0, 1, k)
        buf[a:e2] *= env[:, None]

cut(109, 12.5, 1.5)                     # a hole where nothing was wrong
cut(119, 14, 2.0)                       # ...and the one that sets up the storm
cut(151, 15, 1.0, buses=('main', 'bass', 'music', 'pad', 'fx'))

# the break carries the top of this record: point it
s.bus['main'] = shelf(s.bus['main'], 5200, 3.2)
s.bus['main'] = shelf(s.bus['main'], 200, -0.7, 'low')   # room for the bass

# Everything above 150 Hz can be as wide as it likes; the sub is mono or a
# club system that sums it will cancel what it cannot hear going out of phase.
s.bus['music'] = mono_below(s.bus['music'], 150)
s.bus['bass'] = mono_below(s.bus['bass'], 120)

# Levels set so the bus sum arrives near 1.0: the clipper then shaves the tips
# of the kick transients and the saturator only has about a dB left to do. Left
# louder, the tanh flattens every transient in the track instead of gluing it -
# and in drum & bass the transient IS the record.
GAINS = {'main': 1.02, 'bass': 0.57, 'music': 0.66, 'pad': 1.04, 'fx': 0.72}
s.report(GAINS)
s.render('amen_zub4atka_174.wav', drive=1.3, duck=0.36, limit=0.93,
         clip=1.02, gains=GAINS)
