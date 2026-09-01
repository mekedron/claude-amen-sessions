"""What a neurofunk bass measures, so a version of it can be checked.

theory/20-genres/04a-neurofunk.md lists what finished records in the style
actually contain. These are those numbers, computed from a rendered array -
either one bass phrase or a whole mix.

    attacks   onsets per bar in 200 Hz - 1.2 kHz. A bassline is 4-6. Twelve
              to eighteen is an arpeggio wearing the genre's clothes.
    duty      the fraction of the bar the low end is sounding. 81-85%.
    rate      how much of the 200 Hz - 1.2 kHz envelope's movement sits at
              10-90 Hz, i.e. how much of what is heard is modulation rather
              than notes. 40-48% in a finished record, 15-25% in a run of
              short notes.
    spread    the third-octave spectrum from 300 Hz to 11 kHz, loudest band
              minus quietest, in dB. The genre's own target is flat within
              3 dB; a first pass usually measures 7-8 and reads as "глухой".
    side      side energy against mid at 400-1200 Hz (95-135%) and below
              120 Hz (5-7%).
"""
import numpy as np
from scipy.signal import butter, sosfiltfilt

SR = 44100


def _bp(x, lo, hi, order=3):
    sos = butter(order, [max(lo, 15.0), min(hi, SR * 0.47)], 'band', fs=SR, output='sos')
    return sosfiltfilt(sos, x, axis=0)


def _env(x, ms=3.0):
    w = max(int(ms / 1000 * SR), 3)
    return np.convolve(np.abs(x), np.ones(w) / w, mode='same')


def bassnumbers(x, bpm=174.0, label='', beats=4):
    x = np.asarray(x, dtype=np.float64)
    m = x.mean(axis=1) if x.ndim > 1 else x
    bar = SR * 60.0 / bpm * beats
    bars = max(len(m) / bar, 1e-6)

    mid = _env(_bp(m, 200, 1200), 4.0)
    # An onset is a RISE against what the band was doing 12 ms ago, not an
    # absolute level: the note never stops in this genre, so a threshold on
    # the envelope itself finds either everything or nothing.
    k = max(int(0.012 * SR), 2)
    prev = np.concatenate([np.full(k, mid[0]), mid[:-k]])
    floor = np.percentile(mid, 90) * 0.20
    # 2.6x, not 1.5x. A sine-shaped filter LFO peaks about 1.5 times above
    # where it was 12 ms earlier, so a gentler threshold counts every cycle
    # of the modulation and reports twenty "attacks" a bar in a part that
    # has four. This finds re-articulations - gates and note onsets - and
    # ignores the movement they happen inside.
    rise = (mid > 2.6 * prev) & (mid > floor)
    on, last = 0, -1e9
    for i in np.flatnonzero(rise):
        if i - last > 0.045 * SR:
            on += 1
            last = i
    attacks = on / bars

    low = _env(_bp(m, 30, 160), 6.0)
    duty = float((low > np.percentile(low, 92) * 0.25).mean()) * 100

    e = mid - mid.mean()
    sp = np.abs(np.fft.rfft(e * np.hanning(len(e)))) ** 2
    f = np.fft.rfftfreq(len(e), 1 / SR)
    rate = 100 * sp[(f >= 10) & (f < 90)].sum() / max(sp[(f >= 0.5) & (f < 400)].sum(), 1e-12)

    edges = np.geomspace(300, 11000, 17)
    pw = [float((_bp(m, a, b) ** 2).mean()) for a, b in zip(edges[:-1], edges[1:])]
    db = 10 * np.log10(np.maximum(pw, 1e-14))
    spread = float(db.max() - db.min())

    if x.ndim > 1:
        s = x[:, 0] - x[:, 1]
        def r(lo, hi):
            return 100 * np.sqrt((_bp(s, lo, hi) ** 2).mean()) / max(
                np.sqrt((_bp(m, lo, hi) ** 2).mean()), 1e-12)
        side_mid, side_low = r(400, 1200), r(30, 120)
    else:
        side_mid = side_low = 0.0

    print(f"  {label:20s} attacks/bar {attacks:4.1f} (4-6)  duty {duty:4.1f}% (81-85)"
          f"  rate {rate:4.1f}% (40-48)  spread {spread:4.1f} dB (<3)"
          f"  side {side_mid:3.0f}%/{side_low:3.0f}%")
    return dict(attacks=attacks, duty=duty, rate=rate, spread=spread,
                side_mid=side_mid, side_low=side_low)
