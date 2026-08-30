"""Darkside: murky intro, half-time weight, reese bass in E minor, distorted break."""
from amenlib import *

s = Session(22)

s.place(s.pos(0), lp(bar_of(0), 350), 0.9)
s.place(s.pos(1), lp(bar_of(0), 350), 0.9)
s.place(s.pos(1, 12), rev(SN), 0.8)
for b in (2, 3):
    s.pat(b, [(0, K), (3, G, 0.6), (6, G, 0.5), (8, SN), (11, G, 0.6), (14, K2, 0.8)])
s.place(s.pos(4) - len(CR), rev(CR), 0.9)

for b in range(4, 12):
    s.place(s.pos(b), dirty(bar_of([0, 1, 2, 3][b % 4])), 0.95)
s.place(s.pos(4), CR, 0.9)
s.pat(11, [(8, SN1, 0.7), (10, SN1, 0.8), (12, SN1, 0.9), (13, SN1),
           (14, rev(SN), 0.9)])
for b in range(4, 12):
    if b % 4 == 3:
        s.place(s.pos(b, 0), reese(midi(31), 8), 0.4)            # G1
        s.place(s.pos(b, 8), reese(midi(26), 8, 300), 0.4)       # D1
    else:
        s.place(s.pos(b, 0), reese(midi(28), 6), 0.4)            # E1
        s.place(s.pos(b, 8), reese(midi(28), 4, 500), 0.35)
        s.place(s.pos(b, 12), reese(midi(29), 4, 300), 0.4)      # F1: b9 menace

for b in (12, 13, 14, 15):                                       # half-time middle
    s.pat(b, [(0, K), (4, G, 0.5), (8, SN), (10, G, 0.5),
              (12, K2, 0.7), (14, G, 0.6)])
    s.place(s.pos(b, 0), reese(midi(28), 14, 250), 0.42)
s.place(s.pos(15, 12), rev(CR), 0.85)

for b in range(16, 20):
    s.place(s.pos(b), dirty(bar_of([0, 2, 3, 2][b - 16])), 0.95)
    s.place(s.pos(b, 0), reese(midi(28 if b % 2 == 0 else 31), 7), 0.4)
    s.place(s.pos(b, 8), reese(midi(28 if b % 2 == 0 else 26), 7, 350), 0.4)
s.place(s.pos(16), CR, 0.9)
s.pat(20, [(0, K), (2, K2), (4, SN), (8, S2), (12, SN1, 0.8), (14, SN1)])
s.place(s.pos(20, 0), reese(midi(28), 16, 200), 0.4)
s.pat(21, [(0, K), (4, SN), (6, pitched(CR, 0.4), 0.85)])
s.place(s.pos(21, 0), sub(midi(28), 12), 0.32)

s.render('amen_darkside_174.wav', drive=1.6)
