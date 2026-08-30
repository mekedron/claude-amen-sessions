"""Jump-up: bouncy break + big talky saw bass ("пила") in E minor, sub glued under."""
from amenlib import *

s = Session(22)

E2, G2, A2, B2, D2 = midi(40), midi(43), midi(45), midi(47), midi(38)
E1 = midi(28)

def sawhit(b, st, f, ln, lfo=2.5):
    """mid saw + sub octave below, always together - jump-up glue"""
    s.place(s.pos(b, st), sawbass(f, ln, lfo), 0.4)
    s.place(s.pos(b, st), sub(f / 2, ln), 0.3)

# intro: dry break, teaser bass pokes
s.place(s.pos(0), bar_of(0))
s.place(s.pos(1), bar_of(1))
s.place(s.pos(2), bar_of(0))
sawhit(2, 10, E2, 2, 4.0)
s.place(s.pos(3), bar_of(1)[:int(12 * STEP)])
for i, st in enumerate([12, 13, 14, 15]):
    s.place(s.pos(3, st), SN1, 0.65 + i * 0.12)
s.place(s.pos(4) - len(CR), rev(CR), 0.9)

# drop 1: the bounce - E2 riff, answer on G2/A2
for b in range(4, 12):
    s.place(s.pos(b), bar_of([0, 1, 2, 1][b % 4]))
    if b % 2 == 0:
        sawhit(b, 0, E2, 4, 2.0)
        sawhit(b, 6, E2, 2, 5.0)
        sawhit(b, 10, G2, 2, 5.0)
        sawhit(b, 12, E2, 4, 2.5)
    else:
        sawhit(b, 0, E2, 4, 2.0)
        sawhit(b, 8, A2, 3, 3.5)
        sawhit(b, 12, G2, 2, 5.0)
        sawhit(b, 14, E2, 2, 5.0)
s.place(s.pos(4), CR, 0.9)
s.pat(11, [(12, SN1, 0.8), (13, SN1, 0.85), (14, SN1, 0.9), (15, SN1)])

# breakdown: bass alone talks, sparse kicks
for b in (12, 13):
    s.pat(b, [(0, K), (4, SN), (8, K2, 0.8), (12, S2, 0.9)])
sawhit(12, 0, E2, 6, 1.2)
sawhit(12, 8, G2, 6, 1.8)
sawhit(13, 0, A2, 6, 1.2)
sawhit(13, 8, B2, 4, 2.5)
sawhit(13, 12, G2, 4, 6.0)
s.place(s.pos(14) - len(CR), rev(CR), 0.9)

# drop 2: riff shifts up, rowdier
for b in range(14, 20):
    s.place(s.pos(b), bar_of([0, 3, 2][b % 3]))
    if b % 2 == 0:
        sawhit(b, 0, A2, 4, 2.0)
        sawhit(b, 6, A2, 2, 5.0)
        sawhit(b, 10, B2, 2, 5.0)
        sawhit(b, 12, G2, 4, 2.5)
    else:
        sawhit(b, 0, E2, 4, 2.0)
        sawhit(b, 8, D2, 3, 3.5)
        sawhit(b, 12, E2, 4, 5.0)
s.place(s.pos(14), CR, 0.9)
s.pat(19, [(8, SN1, 0.6), (10, SN1, 0.7), (12, SN1, 0.85), (14, SN1), (15, SN1)])

# outro
s.place(s.pos(20), bar_of(0)); s.place(s.pos(20), CR, 0.9)
sawhit(20, 0, E2, 8, 1.0)
s.pat(21, [(0, K), (4, SN), (8, pitched(CR, 0.5), 0.9)])
s.place(s.pos(21, 0), sub(E1, 12), 0.3)

s.render('amen_jumpup_174.wav', drive=1.4)
