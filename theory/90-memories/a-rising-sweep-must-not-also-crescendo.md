He heard the first pass of `revashol` and reported it in one sentence:
**"очень много каких-то скримеров получилось. Прям очень страшных... из
белого шума, потом крики какие-то резко, они очень-очень резкие. Уши режут"**
- and then, in the same breath, that the groove, the guitar and the bass were
exactly right. So it was not the mix, not the balance and not any instrument.
It was three separate things, all of them transitions.

**1. A rising glissando that also gets louder is a scream.** `sweep()` ran a
string section from B1 up two and a half octaves with a level envelope going
`0.35 -> 1.00` across the sweep. The ear is already most sensitive at 2-5 kHz,
so a rising sweep at CONSTANT amplitude is heard as a crescendo on its own;
putting a real one under it doubles a curve that was already there. The fix
is two lines and it is not a fader:

    env    holds flat (0.88 -> 1.00), not 0.35 -> 1.00
    cutoff CLOSES as the pitch rises - morph_lp(y, c*0.34, c, 1 - 0.72*u)

so the partial count falls as the fundamental climbs and the brightness
stays roughly where it started. Cap the top of the sweep too: ending on
MIDI 79 instead of 93 is the difference between a lift and a siren.

**2. A reverse whoosh is a horror-film device.** Nine of them at nine seams.
Noise that rises into a bang is the sound of a jump scare, and no amount of
level makes it not that. The seam of a genre with a string section is the
section walking up four notes of the chord, which is a part rather than an
effect.

**3. The clipper was doing the mixing.** `mixdown` reported `1.12 peak, 14%
of samples shaped (THIS IS EATING THE BODY)` because the bus sum arrived at
5.6. At fourteen percent a clipper is not shaving transients, it is
distorting everything continuously, and that is a harshness with no single
source - which is exactly what "уши режут" without naming a sound means.

**How to apply:** scale the bus sum to a known peak BEFORE the clipper, so
`clip=` only ever sees the tip:

    _sum = sum(bus * GAINS[k] for k, bus in S.bus.items())
    GAINS = {k: v * (2.00 / abs(_sum).max()) for k, v in GAINS.items()}

Then `clip=1.5` shapes 0.00% and the master is honest. And when he reports
harshness, measure it as **the 2-5 kHz peak over the local mean per 200 ms**
rather than as a band share: a band share cannot see an event, and an event
is what he is describing. Median -0.5 dB with a 99th percentile of 7.5 dB is
a record with no screamers in it.

Related: [[mix-checks-before-handing-over-a-track]], [[loud-masters-need-a-true-peak-limiter]]
