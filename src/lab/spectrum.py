"""Where the energy is - per segment, per section, per bar.

`verify.py` answers questions about a finished WAV on disk: is it loud
enough, does it clip, does it survive mono. These are the questions you ask
while you are still building the thing - about one voice, about one bus,
about bar 6 - and every one of them was written inline half a dozen times in
the session that produced `blendung`, `finsternis` and `heimweg` before it
became obvious they should be functions.
"""
import numpy as np

SR = 44100
BANDS = ((20, 60), (60, 120), (120, 300), (300, 800),
         (800, 3000), (3000, 10000), (10000, 20000))


def _mono(x):
    x = np.asarray(x, dtype=np.float64)
    return x.mean(axis=1) if x.ndim == 2 else x


def shares(x, bands=BANDS):
    """Percentage of a segment's energy in each band. The single most-used
    measurement there is: it is how you find out that a 'bass' is actually a
    low-mid, that a 'bright' hat lives in the ice-pick band, or that a kick
    has put 43% of itself below 40 Hz."""
    m = _mono(x)
    sp = np.abs(np.fft.rfft(m * np.hanning(len(m)))) ** 2
    f = np.fft.rfftfreq(len(m), 1 / SR)
    tot = max(sp.sum(), 1e-12)
    return [float(sp[(f >= lo) & (f < hi)].sum() / tot * 100) for lo, hi in bands]


def width(x):
    """Side energy as a percentage of mid. Around 0 is mono, 100 is wide,
    past ~200 the two channels are close to uncorrelated and the thing will
    lose level the moment anything sums it."""
    x = np.asarray(x, dtype=np.float64)
    if x.ndim != 2:
        return 0.0
    m = x.mean(axis=1)
    return float(np.sqrt(((x[:, 0] - x[:, 1]) ** 2).mean())
                 / max(np.sqrt((m ** 2).mean()), 1e-12) * 100)


def _header(bands):
    return (f"{'':22s} {'width':>6s} | "
            + " ".join(f"{lo:>6d}" for lo, _ in bands))


def band_table(items, bands=BANDS, header=True):
    """A table of (label, segment) pairs. Use it to compare a voice against
    the voice it is replacing, or a bus against the bus it has to sit beside -
    the numbers only ever mean something next to another set of numbers."""
    if header:
        print(_header(bands))
    out = {}
    for label, seg in items:
        sh = shares(seg, bands)
        out[label] = sh
        print(f"{label:22s} {width(seg):5.0f}% | " + " ".join(f"{v:6.1f}" for v in sh))
    return out


def sections(x, bpm, marks, bands=BANDS, beats=4):
    """The arrangement, measured. `marks` is [(name, first_bar, end_bar), ...].

    Prints loudness, stereo width and the band shares for each named section,
    and then the three things the shape has to satisfy: the curve rises
    overall, the minimum comes immediately before the maximum, and the peak
    lands 60-90% of the way through.

    This is the function that catches the failure this project keeps making -
    every section given different PARTS and none given a different LEVEL, so
    the void measures as loud as the drop. See the memory
    `section-contrast-belongs-in-level`.
    """
    import verify
    bar = SR * 60.0 / bpm * beats
    print(_header(bands).replace(f"{'':22s}", f"{'section':14s} {'LUFS':>6s}"))
    rows = []
    for name, a, b in marks:
        seg = np.asarray(x)[int(a * bar):int(b * bar)]
        if not len(seg):
            continue
        l, _ = verify._block_loudness(seg if seg.ndim == 2 else np.stack([seg, seg], 1))
        l = l[l > -70]
        lufs = float(np.mean(l)) if len(l) else -99.0
        sh = shares(seg, bands)
        rows.append((name, a, b, lufs, sh))
        print(f"{name:14s} {lufs:6.1f} {width(seg):5.0f}% | "
              + " ".join(f"{v:6.1f}" for v in sh))
    if len(rows) > 2:
        lo = min(rows, key=lambda r: r[3])
        hi = max(rows, key=lambda r: r[3])
        span = hi[3] - lo[3]
        total = rows[-1][2]
        at = hi[1] / max(total, 1) * 100
        print(f"  range {span:.1f} dB   quietest '{lo[0]}'   loudest '{hi[0]}' "
              f"at {at:.0f}% of the way through"
              + ("" if 60 <= at <= 90 else "   <- a peak belongs at 60-90%"))
        if span < 4:
            print("  THE CURVE IS FLAT. Different parts is not different level; "
                  "ride the buses.")
        if rows.index(lo) > rows.index(hi):
            print("  the quietest section comes AFTER the loudest - nothing sets "
                  "the peak up")
    return rows


def walk(x, bpm, first=0, last=16, bands=((20, 60), (60, 300), (300, 3000),
                                          (3000, 10000), (10000, 20000)), beats=4):
    """Bar by bar, so a jump can be located rather than guessed at.

    Written because a listener said "ровно с десятой секунды начинается
    тряск" and the only honest way to answer that is to print every bar
    around it and look for the row where a column changes. At 142 BPM the
    tenth second is bar 6, and bar 6 was where a lowpass came off a kick and
    an open hat entered on the same beat.
    """
    bar = SR * 60.0 / bpm * beats
    print(f"{'bar':>4s} {'t':>7s} | " + " ".join(f"{lo:>7d}" for lo, _ in bands))
    for b in range(first, last):
        seg = np.asarray(x)[int(b * bar):int((b + 1) * bar)]
        if not len(seg):
            break
        print(f"{b:4d} {b * bar / SR:6.2f}s | "
              + " ".join(f"{v:7.3f}" for v in shares(seg, bands)))
