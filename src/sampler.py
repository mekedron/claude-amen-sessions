"""Sample layer: feed in any audio file, lock it to a grid, cut it up.

Nothing here knows about the Amen break - that is just the first `Sample` the
repo happened to load (see amenlib.py). Every instance carries its own bar
length, so several samples at different tempos can play in one session: call
`.fit()` and each one is resampled onto the session grid, jungle-style, pitch
moving with the speed.

    from phonklib import *              # any engine module sets the grid
    from sampler import Sample, prepare

    brk  = Sample('samples/funky_drummer.wav', bars=4).fit()
    vocs = Sample('samples/acapella.wav', bars=8).fit()
    s.place(s.pos(4), brk.bar(0))
    s.place(s.pos(4), rev(vocs.get(2, 8, 4)), 0.6)

`.kit()` runs the spectral analysis and hands back the hits it found, so a
break you have never seen before still gives you kick / snare / ghost / crash.
"""
import os, subprocess, numpy as np
import core
from core import SR, load, save, fade_edges, lp, hp, bandpass

def prepare(src, dst, trim=None, length=None, speed=None, rate=SR):
    """decode anything to a wav, optionally trimming and speed-shifting it.
    Needs ffmpeg (decode) and sox (trim/speed) on PATH. No-op if dst exists."""
    if os.path.exists(dst):
        return dst
    os.makedirs(os.path.dirname(dst) or '.', exist_ok=True)
    stem = os.path.splitext(dst)[0]
    raw = stem + '_raw.wav'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', src, '-ar', str(rate), raw], check=True)
    cur = raw
    if trim is not None or length is not None:
        cut = stem + '_trim.wav'
        args = ['sox', cur, cut, 'trim', str(trim or 0)]
        if length is not None:
            args.append(str(length))
        subprocess.run(args, check=True)
        os.remove(cur); cur = cut
    if speed and abs(speed - 1.0) > 1e-6:
        sp = stem + '_speed.wav'
        subprocess.run(['sox', cur, sp, 'speed', str(speed)], check=True)
        os.remove(cur); cur = sp
    os.replace(cur, dst)
    return dst

class Sample:
    """One audio file on its own bar grid.

    bars = how many bars the file holds (the whole file is assumed to be a
    clean loop). Slice accessors take (bar, step) in 16ths of that grid;
    everything they return is a plain stereo float32 array."""

    def __init__(self, path_or_array, bars=4, name=None, beats=4):
        if isinstance(path_or_array, str):
            self.x = load(path_or_array)
            self.name = name or os.path.splitext(os.path.basename(path_or_array))[0]
        else:
            self.x = np.asarray(path_or_array, dtype=np.float32)
            self.name = name or 'sample'
        if self.x.ndim == 1:
            self.x = np.stack([self.x, self.x], 1)
        self.bars = bars
        self.bar_len = len(self.x) / bars
        self.step_len = self.bar_len / 16.0
        self.bpm = SR * 60.0 * beats / self.bar_len

    def __len__(self): return len(self.x)

    def __repr__(self):
        return f"<Sample {self.name}: {self.bars} bars, {self.bpm:.1f} BPM, {len(self.x)/SR:.2f}s>"

    # ---- slicing ----
    def get(self, bar, step=0.0, n=1.0, fade=3.0):
        """n steps of audio starting at (bar, step)"""
        a = int(round(bar * self.bar_len + step * self.step_len))
        b = int(round(bar * self.bar_len + (step + n) * self.step_len))
        return fade_edges(self.x[max(a, 0):b], fade)

    def bar(self, i, fade=2.0):
        a = int(round(i * self.bar_len))
        return fade_edges(self.x[a:int(round((i + 1) * self.bar_len))], fade)

    def beat(self, bar, i, fade=3.0):
        return self.get(bar, i * 4, 4, fade)

    def chop(self, n=16, bar=None):
        """cut into n equal pieces - the whole file, or one bar of it"""
        src = self.x if bar is None else self.bar(bar, fade=0.5)
        edges = np.linspace(0, len(src), n + 1).astype(int)
        return [fade_edges(src[a:b], 2.0) for a, b in zip(edges[:-1], edges[1:])]

    def seconds(self, a, b, fade=3.0):
        return fade_edges(self.x[int(a * SR):int(b * SR)], fade)

    # ---- retiming ----
    def resampled(self, factor, name=None):
        """new Sample read at `factor` speed; pitch moves with it, as on a deck"""
        n = len(self.x)
        idx = np.arange(0, n - 1, factor)
        y = np.stack([np.interp(idx, np.arange(n), self.x[:, c]) for c in range(2)], 1)
        return Sample(y.astype(np.float32), self.bars, name or self.name + f'@{factor:.3f}')

    def fit(self, bar_samples=None, name=None):
        """snap one of its bars onto the session grid (core.BAR by default)"""
        target = float(bar_samples or core.BAR)
        return self.resampled(self.bar_len / target, name)

    def at_bpm(self, bpm, name=None):
        return self.resampled(bpm / self.bpm, name)

    # ---- analysis ----
    def analyze(self):
        """per-16th energy and spectral centroid over the whole file"""
        out = []
        for i in range(int(self.bars) * 16):
            seg = self.get(i // 16, i % 16, 1, fade=1.0)
            m = seg.mean(axis=1)
            if len(m) < 32:
                out.append({'step': i, 'bar': i // 16, 'energy': 0.0, 'centroid': 0.0,
                            'low': 0.0, 'high': 0.0, 'kind': 'rest'})
                continue
            spec = np.abs(np.fft.rfft(m * np.hanning(len(m))))
            f = np.fft.rfftfreq(len(m), 1 / SR)
            e = float(np.sqrt((m ** 2).mean()))
            c = float((spec * f).sum() / max(spec.sum(), 1e-9))
            low = float(spec[f < 200].sum() / max(spec.sum(), 1e-9))
            high = float(spec[f > 5000].sum() / max(spec.sum(), 1e-9))
            out.append({'step': i, 'bar': i // 16, 'energy': e, 'centroid': c,
                        'low': low, 'high': high, 'kind': None})
        loud = float(np.median([d['energy'] for d in out])) or 1e-9
        lowmed = float(np.median([d['low'] for d in out]))
        for d in out:
            hot = d['energy'] > loud * 1.15
            if d['energy'] < loud * 0.45:
                d['kind'] = 'rest'
            elif d['low'] > max(lowmed * 1.8, 0.10):          # bass in the hit
                d['kind'] = 'kick' if hot else 'ghost'
            elif hot and d['high'] > 0.62 and d['centroid'] > 6000:
                d['kind'] = 'crash'
            elif hot:
                d['kind'] = 'snare'
            elif d['high'] > 0.5:
                d['kind'] = 'hat'
            else:
                d['kind'] = 'ghost'
        return out

    def find(self, kind):
        """[(bar, step), ...] of every 16th the analysis called `kind`"""
        return [(d['bar'], d['step'] % 16) for d in self.analyze() if d['kind'] == kind]

    def kit(self, n=1):
        """{'kick': seg, 'snare': seg, ...}: the first clean hit of each kind"""
        k = {}
        for d in self.analyze():
            if d['kind'] not in k and d['kind'] != 'rest':
                k[d['kind']] = self.get(d['bar'], d['step'] % 16, n)
        return k
