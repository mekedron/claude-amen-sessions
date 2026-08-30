"""Rave / breakbeat hardcore: hoover stabs (A minor), rolls, big-room energy."""
from amenlib import *

s = Session(22)

A2, C3, G2, E3, D3 = midi(45), midi(48), midi(43), midi(52), midi(50)
A1 = midi(33)
HV = 0.42

# intro: break builds, lone hoover calls
s.place(s.pos(0), bar_of(0))
s.place(s.pos(1), bar_of(1))
s.place(s.pos(1, 8), hoover(A2, 4), HV * 0.7)
s.place(s.pos(2), bar_of(0))
s.place(s.pos(2, 8), hoover(C3, 4), HV * 0.8)
s.pat(3, [(0, K), (2, K2), (4, SN), (8, SN1, 0.6), (10, SN1, 0.7),
          (12, SN1, 0.85), (13, SN1, 0.9), (14, SN1), (15, SN1)])
s.place(s.pos(4) - len(CR), rev(CR), 0.95)

# drop 1: offbeat hoover riff over rolling break
for b in range(4, 12):
    s.place(s.pos(b), bar_of([0, 1, 2, 3][b % 4]))
    if b % 2 == 0:
        s.place(s.pos(b, 2), hoover(A2, 3), HV)
        s.place(s.pos(b, 6), hoover(A2, 3), HV * 0.9)
        s.place(s.pos(b, 10), hoover(C3, 3), HV)
        s.place(s.pos(b, 14), hoover(G2, 2), HV * 0.9)
    else:
        s.place(s.pos(b, 2), hoover(A2, 3), HV)
        s.place(s.pos(b, 8), hoover(E3, 4), HV)
        s.place(s.pos(b, 13), hoover(D3, 3), HV * 0.9)
    s.place(s.pos(b, 0), sub(A1, 3), 0.3)
    s.place(s.pos(b, 8), sub(A1, 2), 0.26)
s.place(s.pos(4), CR, 0.95)
s.pat(11, [(12, SN1, 0.8), (13, SN1, 0.85), (14, SN1, 0.95), (15, SN1)])

# breakdown: drums drop out, hoovers ring alone, roll rebuilds
s.place(s.pos(12, 0), hoover(A2, 8), HV)
s.place(s.pos(12, 8), hoover(C3, 8), HV)
s.place(s.pos(13, 0), hoover(D3, 8), HV)
s.place(s.pos(13, 8), hoover(E3, 8), HV * 1.1)
s.pat(14, [(0, K), (8, K, 0.9)])
s.place(s.pos(14, 0), hoover(A2, 16), HV * 0.8)
s.pat(15, [(0, SN1, 0.5), (2, SN1, 0.55), (4, SN1, 0.6), (6, SN1, 0.7),
           (8, SN1, 0.75), (10, SN1, 0.8), (12, SN1, 0.9), (13, SN1, 0.9),
           (14, SN1), (15, SN1)])
s.place(s.pos(16) - len(CR), rev(CR), 0.95)

# drop 2: stab pattern doubles up
for b in range(16, 20):
    s.place(s.pos(b), bar_of([0, 3, 0, 2][b - 16]))
    s.place(s.pos(b, 2), hoover(A2, 2), HV)
    s.place(s.pos(b, 5), hoover(A2, 2), HV * 0.85)
    s.place(s.pos(b, 8), hoover(C3 if b % 2 == 0 else E3, 3), HV)
    s.place(s.pos(b, 12), hoover(G2 if b % 2 == 0 else D3, 3), HV)
    s.place(s.pos(b, 0), sub(A1, 3), 0.3)
    s.place(s.pos(b, 10), sub(A1, 2), 0.26)
s.place(s.pos(16), CR, 0.95)

# outro: last stab rings out
s.place(s.pos(20), bar_of(0))
s.place(s.pos(20, 2), hoover(A2, 6), HV)
s.pat(21, [(0, K), (4, SN), (8, pitched(CR, 0.5), 0.9)])
s.place(s.pos(21, 0), hoover(A2 / 2, 12), HV * 0.8)

s.render('amen_rave_174.wav', drive=1.4)
