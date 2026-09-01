"""What a finished render actually contains.

The one thing this project cannot do is listen, so every claim about a mix has
to be a measurement. This module answers, for a WAV on disk, the questions a
mastering checklist asks:

    loudness        integrated LUFS to ITU-R BS.1770 (K-weighting, 400 ms
                    blocks, the -70 LUFS absolute and -10 LU relative gates)
    true peak       peak after 4x oversampling, which is what a lossy encoder
                    and a D/A converter will see
    crest / PLR     true peak minus integrated loudness: how much dynamic
                    range survived
    bands           where the energy is, as a percentage per octave-ish band
    mono            how much level is lost summing to mono, and the phase
                    correlation - a club system and a phone both do this
    low mono        how much of the sub is in the side channel, which is
                    energy a big rig throws away
    curve           short-term loudness per section, so an arrangement can be
                    checked for a shape rather than assumed to have one
    band crest      peak minus RMS PER BAND. One number for the whole file
                    cannot tell a dense low end under a transient top from a
                    mix that has been flattened everywhere; two columns can.
    pulse           the low band's energy per sixteenth of the bar, averaged
                    over the file, and the ratio of the on-beat steps to the
                    off-beat ones. Below about 1.1 the offbeats are hitting
                    harder than the beats and the track has no pulse however
                    fast it is - which is the first thing anyone hears.

Usage:
    python3 src/verify.py renders/some_track.wav [bpm] [bars_per_block]
    from verify import report; report('renders/some_track.wav', bpm=140)
"""
import sys, os, numpy as np
from scipy.signal import butter, sosfilt, resample_poly

SR = 44100
BANDS = ((20, 60), (60, 120), (120, 300), (300, 800),
         (800, 3000), (3000, 10000), (10000, 20000))


def ticks(x, band=3000.0, ratio=6.0, label='', floor_db=-58.0, bpm=None):
    """How much of the top end is isolated clicks rather than sound.

    `clicks()` finds discontinuities. This finds the other complaint - a
    texture of short high-frequency bursts, which is what a vinyl-crackle or
    dust layer turns into the moment it is too loud, and which the ear
    reports as "потрескивания" rather than as brightness.

    Count short excursions in the high band that stand more than `ratio`
    times above that band's own median. A record whose top end is instruments
    scores near zero; a record whose top end is a scatter of micro-clicks
    scores in the tens. Measured here: blendung 0.0/s, nebel 0.0/s,
    finsternis 6.4/s, and a draft of heimweg 19.5/s, which is the one the
    human heard.

    The floor matters as much as the count, in both directions. Ticks stand
    out against silence, so a quiet high band with a few in it is worse than
    a busy one with many - but below about -58 dB there is nothing up there
    to hear at all, and a purely relative test reports hundreds of ticks a
    second in a fade-out because every sample is above the median of nothing.
    `floor_db` is that guard, and without it this function cries wolf on
    every quiet section.
    """
    m = np.asarray(x).mean(axis=1)
    hi = np.abs(sosfilt(butter(4, band, 'high', fs=SR, output='sos'), m))
    w = max(int(0.003 * SR), 3)
    env = np.convolve(hi, np.ones(w) / w, mode='same')
    med = float(np.median(env[env > 0])) if (env > 0).any() else 0.0
    # Against the LOCAL surroundings, not the file's median. A tick is an
    # isolated event and stands above its own neighbourhood; a noise floor
    # does not, and measuring it against a global median reports every wiggle
    # in a fade-out as a click - 826 a second in one test, which is a
    # detector describing itself rather than the audio.
    lw = max(int(0.100 * SR), 9)
    ref = np.convolve(env, np.ones(lw) / lw, mode='same') + 1e-9
    absmin = 10 ** (floor_db / 20)
    pk = ((env[1:-1] > env[:-2]) & (env[1:-1] > env[2:])
          & (env[1:-1] > ref[1:-1] * ratio) & (env[1:-1] > absmin))
    rate = int(pk.sum()) / max(len(m) / SR, 1e-9)
    # A hi-hat is a tick too, and a record with sixteenths at 142 BPM has 9.5
    # of them a second by design. What separates a part from crackle is not
    # how many there are, it is whether they land on the grid: rhythmic ticks
    # share a phase within the step, scattered ones do not. `lock` is the
    # resultant vector length of those phases - near 1 is a hi-hat line,
    # near 0 is dust.
    lock = 0.0
    if bpm and pk.any():
        step = SR * 60.0 / bpm / 4.0
        ph = 2 * np.pi * ((np.flatnonzero(pk) + 1) % step) / step
        lock = float(np.abs(np.exp(1j * ph).mean()))
    verdict = 'clean' if rate < 3 else ('played' if lock > 0.55 else
                                        'CRACKLE' if rate > 8 else 'busy')
    print(f"  ticks{(' ' + label) if label else ''}: {rate:.1f}/s above {band:.0f} Hz, "
          f"floor {20 * np.log10(max(med, 1e-9)):.1f} dB"
          + (f", grid-lock {lock:.2f}" if bpm else "") + f"  ({verdict})")
    return rate


def clicks(x, bpm=None, thresh=8.0, limit=20, band=2000.0):
    """Where a render has a discontinuity, in seconds and in bars.

    The naive detector - a big jump between two samples - finds every kick
    and every hat, because a transient IS a big jump between two samples and
    is meant to be. The discriminator is the BAND. Low frequencies cannot
    move fast: a 46 Hz sine at full scale changes by 0.0066 per sample, so
    any step in the low band larger than a few percent is something that was
    cut rather than something that was played. Percussion transients live
    above this filter and are invisible to it.

    So: lowpass hard, take the first difference, and score it against a
    30 ms running mean of itself. What comes back is truncated envelopes,
    unfaded segment edges and spliced phrase boundaries - and if the hits
    land on a regular bar fraction, that number says which.
    """
    m = x.mean(axis=1)
    sos = butter(4, min(band, SR * 0.45), 'low', fs=SR, output='sos')
    lo = sosfilt(sos, m)
    d = np.abs(np.diff(lo))
    w = int(0.030 * SR)
    ref = np.convolve(d, np.ones(w) / w, mode='same') + 1e-7
    r = d / ref
    idx = np.where((r > thresh) & (d > 0.004))[0]
    if not len(idx):
        print(f"  clicks: none under {band:.0f} Hz above {thresh:.0f}x local slope")
        return []
    keep = []
    for i in idx[np.argsort(-r[idx])]:
        if all(abs(int(i) - k) > 0.02 * SR for k in keep):
            keep.append(int(i))
        if len(keep) >= limit:
            break
    keep.sort()
    print(f"  clicks: {len(keep)} distinct steps under {band:.0f} Hz "
          f"above {thresh:.0f}x the local slope")
    for i in keep:
        t = i / SR
        bar = t * bpm / 240 if bpm else 0
        loc = f"bar {bar:7.2f} (step {(bar % 1) * 16:5.2f})" if bpm else ""
        print(f"    {t:8.3f}s  {loc}  {r[i]:5.0f}x  step {d[i]:.4f}")
    return keep


def _read(path):
    """Any WAV, not only 16-bit. References arrive as 24-bit far more often
    than not, and a 24-bit file read as int16 is noise."""
    import wave
    w = wave.open(path, 'rb')
    n, ch, sw = w.getnframes(), w.getnchannels(), w.getsampwidth()
    raw = w.readframes(n)
    w.close()
    if sw == 2:
        x = np.frombuffer(raw, np.int16).astype(np.float64) / 32768
    elif sw == 3:
        b = np.frombuffer(raw, np.uint8).reshape(-1, 3).astype(np.int32)
        u = b[:, 0] | (b[:, 1] << 8) | (b[:, 2] << 16)
        x = np.where(u & 0x800000, u - (1 << 24), u).astype(np.float64) / (1 << 23)
    elif sw == 4:
        x = np.frombuffer(raw, np.int32).astype(np.float64) / (1 << 31)
    else:
        x = np.frombuffer(raw, np.uint8).astype(np.float64) / 128 - 1.0
    x = x.reshape(-1, ch)
    return x[:, :2] if ch >= 2 else np.repeat(x, 2, axis=1)


def _k_weight(x, sr=SR):
    """BS.1770 pre-filter: a head shelf then a high-pass, both as specified"""
    hs = butter(2, 1500, 'high', fs=sr, output='sos')      # shelf stand-in
    y = 1.0 * x + 0.585 * sosfilt(hs, x, axis=0)           # +4 dB above ~2 kHz
    hp = butter(2, 38.0, 'high', fs=sr, output='sos')
    return sosfilt(hp, y, axis=0)


def _block_loudness(x, sr=SR, block=0.400, overlap=0.75):
    """mean square per gating block, weighted and summed over channels"""
    y = _k_weight(x, sr)
    n = int(block * sr)
    hop = max(int(n * (1 - overlap)), 1)
    if len(y) < n:
        return np.array([]), np.array([])
    idx = np.arange(0, len(y) - n + 1, hop)
    p = np.empty(len(idx))
    for i, a in enumerate(idx):
        p[i] = (y[a:a + n] ** 2).mean(axis=0).sum()
    with np.errstate(divide='ignore'):
        return -0.691 + 10 * np.log10(np.maximum(p, 1e-20)), idx


def lufs(x, sr=SR):
    """integrated loudness with both BS.1770 gates"""
    l, _ = _block_loudness(x, sr)
    if not len(l):
        return -np.inf
    keep = l > -70.0
    if not keep.any():
        return -np.inf
    rel = _mean_db(l[keep]) - 10.0
    keep &= l > rel
    return _mean_db(l[keep]) if keep.any() else -np.inf


def _mean_db(l):
    return -0.691 + 10 * np.log10(np.mean(10 ** ((l + 0.691) / 10)))


def true_peak_db(x, oversample=4):
    y = resample_poly(x, oversample, 1, axis=0)
    return 20 * np.log10(max(np.abs(y).max(), 1e-12))


def band_share(x):
    m = x.mean(axis=1)
    S = np.abs(np.fft.rfft(m * np.hanning(len(m)))) ** 2
    f = np.fft.rfftfreq(len(m), 1 / SR)
    tot = max(S.sum(), 1e-20)
    return [S[(f >= lo) & (f < hi)].sum() / tot * 100 for lo, hi in BANDS]


def mono_loss_db(x):
    """level change on summing to mono. 0 dB means nothing cancels; a
    correlated stereo image loses a fraction of a dB, an out-of-phase one
    loses several and can lose an element entirely."""
    st = np.sqrt((x ** 2).mean())
    mo = np.sqrt((x.mean(axis=1) ** 2).mean())
    return 20 * np.log10(max(mo, 1e-12) / max(st, 1e-12))


def correlation(x):
    a, b = x[:, 0], x[:, 1]
    d = np.sqrt((a ** 2).mean() * (b ** 2).mean())
    return float((a * b).mean() / max(d, 1e-20))


def low_side_pct(x, hz=120):
    sos = butter(4, hz, 'low', fs=SR, output='sos')
    low = sosfilt(sos, x, axis=0)
    mid = (low[:, 0] + low[:, 1]) / 2
    side = (low[:, 0] - low[:, 1]) / 2
    return float(np.sqrt((side ** 2).mean()) / max(np.sqrt((mid ** 2).mean()), 1e-20) * 100)


def band_crest(x):
    """peak minus RMS in each band, in dB.

    The tell that one crest figure for the whole file cannot give: a record
    with a dense, near-constant low end under a transient top measures around
    11 dB low and 20 dB up, and a record that has simply been squashed
    measures the same everywhere."""
    m = x.mean(axis=1)
    out = []
    for lo, hi in BANDS:
        if lo <= 20:
            sos = butter(4, hi, 'low', fs=SR, output='sos')
        elif hi >= SR * 0.49:
            sos = butter(4, lo, 'high', fs=SR, output='sos')
        else:
            sos = butter(4, [lo, min(hi, SR * 0.49)], 'band', fs=SR, output='sos')
        y = sosfilt(sos, m)
        r = float(np.sqrt((y ** 2).mean()))
        out.append(20 * np.log10(max(np.abs(y).max(), 1e-12) / max(r, 1e-12)))
    return out


def pulse(x, bpm, beats=4, hz=160.0):
    """The low band's energy per sixteenth of the bar, and the on/off ratio.

    A track's felt speed is not its tempo. What the body counts is the rate of
    the pulse it could step on, so the question is where the LOW END lands,
    averaged over every bar in the file. A 6 ms max envelope, because the ear
    integrates over about that long and a raw sample peak measures the
    waveform rather than the hit.

    Returns (grid_16, on_over_off). Above about 1.1 the beats are winning."""
    from scipy.ndimage import maximum_filter1d
    sos = butter(4, hz, 'low', fs=SR, output='sos')
    low = np.abs(sosfilt(sos, x.mean(axis=1)))
    low = maximum_filter1d(low, int(0.006 * SR))
    bar = SR * 60.0 / bpm * beats
    nb = int(len(low) / bar)
    grid = np.zeros(16)
    for i in range(16):
        grid[i] = np.mean([low[int(b * bar + i * bar / 16):
                                int(b * bar + (i + 0.9) * bar / 16)].max()
                           for b in range(nb)])
    g = grid / max(grid.max(), 1e-12)
    return g, float(g[[0, 4, 8, 12]].mean() / max(g[[2, 6, 10, 14]].mean(), 1e-12))


def curve(x, sr=SR, seconds=None, bpm=None, bars=8):
    """short-term loudness per block, as (start_seconds, LUFS)"""
    if seconds is None:
        seconds = (bars * 4 * 60.0 / bpm) if bpm else 8.0
    n = int(seconds * sr)
    out = []
    for a in range(0, len(x) - n // 2, n):
        seg = x[a:a + n]
        if len(seg) > sr // 4:
            out.append((a / sr, lufs(seg, sr)))
    return out


def report(path, bpm=None, bars=8, show_curve=True):
    x = _read(path)
    li = lufs(x)
    tp = true_peak_db(x)
    print(f"\n{os.path.basename(path)}  {len(x)/SR:.1f}s")
    print(f"  integrated   {li:6.1f} LUFS")
    print(f"  true peak    {tp:6.2f} dBTP    {'OK' if tp <= -0.9 else 'ABOVE -1 dBTP'}")
    print(f"  PLR          {tp - li:6.1f} dB   "
          f"({'squashed' if tp - li < 6 else 'dense' if tp - li < 9 else 'dynamic'})")
    print(f"  sample peak  {20*np.log10(max(np.abs(x).max(),1e-12)):6.2f} dBFS")
    c = correlation(x)
    print(f"  mono sum     {mono_loss_db(x):+6.2f} dB    correlation {c:+.2f} "
          f"({'MONO - no image at all' if c > 0.995 else 'narrow' if c > 0.9 else 'wide' if c > 0.4 else 'CHECK PHASE'})")
    print(f"  side below 120 Hz: {low_side_pct(x):.1f}% of mid "
          f"({'mono' if low_side_pct(x) < 8 else 'NOT MONO - a rig will lose this'})")
    sh = band_share(x)
    print("  bands  " + "  ".join(f"{lo}-{hi}" for lo, hi in BANDS))
    print("         " + "  ".join(f"{v:>{len(str(lo))+len(str(hi))}.1f}"
                                  for v, (lo, hi) in zip(sh, BANDS)))
    print(f"  under 120 Hz: {sh[0]+sh[1]:.0f}%")
    bc = band_crest(x)
    print("  crest  " + "  ".join(f"{v:>{len(str(lo))+len(str(hi))}.1f}"
                                  for v, (lo, hi) in zip(bc, BANDS)))
    if bpm:
        g, ratio = pulse(x, bpm)
        print("  low-band pulse per 16th (1.00 = the bar's loudest step):")
        print("    " + " ".join(f"{v:4.2f}" for v in g))
        print(f"    on-beat / off-beat = {ratio:.2f}   "
              f"({'pulse holds' if ratio > 1.1 else 'NO PULSE - the offbeats are winning'})")
    if show_curve:
        c = curve(x, bpm=bpm, bars=bars)
        top = max(v for _, v in c if np.isfinite(v))
        print(f"  energy curve ({bars} bars per row)" if bpm else "  energy curve (8 s per row)")
        for t, v in c:
            n = int(np.clip((v - top + 18) / 18 * 44, 0, 44))
            print(f"   {int(t)//60:d}:{int(t)%60:02d} {v:6.1f} " + "#" * n)
    return li, tp


if __name__ == '__main__':
    p = sys.argv[1]
    bpm = float(sys.argv[2]) if len(sys.argv) > 2 else None
    bars = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    report(p, bpm, bars)
