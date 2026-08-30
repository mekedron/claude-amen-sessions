"""Funky DnB: slap-style bassline with octave pops, clav stabs, wah'd break, swung ghosts.
A dorian, Roni Size / Full Cycle energy.
"""
from amenlib import *

s = Session(22)

A1, G1, E1, C2, D2, E2, A2 = (midi(n) for n in (33, 31, 28, 36, 38, 40, 45))
Am7 = [midi(57), midi(60), midi(64), midi(67)]
D9  = [midi(50), midi(54), midi(57), midi(64)]
G6  = [midi(55), midi(59), midi(62), midi(64)]

def bass_a(b):
    """main funk line: root, ghost, octave pop on the offbeat"""
    s.place(s.pos(b, 0),    funkbass(A1, 2), 0.42)
    s.place(s.pos(b, 2.5),  funkbass(A1, 0.5), 0.2)          # ghost
    s.place(s.pos(b, 3),    funkbass(C2, 1), 0.38)
    s.place(s.pos(b, 6),    funkbass(A1, 1.5), 0.4)
    s.place(s.pos(b, 7.5),  funkbass(A2, 1, pop=True), 0.3)  # pop!
    s.place(s.pos(b, 10),   funkbass(G1, 2), 0.4)
    s.place(s.pos(b, 12),   funkbass(A1, 2), 0.42)
    s.place(s.pos(b, 14.5), funkbass(E2, 1, pop=True), 0.28)

def bass_b(b):
    """answer line: walks down to E"""
    s.place(s.pos(b, 0),    funkbass(A1, 2), 0.42)
    s.place(s.pos(b, 3),    funkbass(G1, 1), 0.38)
    s.place(s.pos(b, 4.5),  funkbass(A1, 0.5), 0.2)
    s.place(s.pos(b, 6),    funkbass(D2, 1.5), 0.38)
    s.place(s.pos(b, 8),    funkbass(C2, 1.5), 0.38)
    s.place(s.pos(b, 10.5), funkbass(A2, 1, pop=True), 0.3)
    s.place(s.pos(b, 12),   funkbass(E1, 2), 0.42)
    s.place(s.pos(b, 14),   funkbass(G1, 2), 0.4)

def stabs(b, late=False):
    """clav hits sit on the funky offbeats"""
    if late:
        s.place(s.pos(b, 3.5), clav(D9, 2), 0.3)
        s.place(s.pos(b, 11), clav(Am7, 2), 0.32)
        s.place(s.pos(b, 14.5), clav(G6, 1.5), 0.26)
    else:
        s.place(s.pos(b, 2), clav(Am7, 2), 0.32)
        s.place(s.pos(b, 7), clav(Am7, 1.5), 0.26)
        s.place(s.pos(b, 11), clav(D9, 2), 0.3)

# intro: wah break sneaks in, clav teases
s.place(s.pos(0), wah(bar_of(0), 1.5), 0.8)
s.place(s.pos(1), wah(bar_of(1), 2.5), 0.85)
s.place(s.pos(1, 11), clav(Am7, 2), 0.25)
s.place(s.pos(2), bar_of(0))
stabs(2)
s.place(s.pos(3), bar_of(1)[:int(12 * STEP)])
s.pat(3, [(12, SN1, 0.6), (13.5, SN1, 0.75), (14, SN1, 0.9), (15, SN1)])
s.place(s.pos(4) - len(CR), rev(CR), 0.9)

# groove 1: full funk machine
for b in range(4, 12):
    s.place(s.pos(b), bar_of([0, 1, 2, 1][b % 4]))
    s.place(s.pos(b, 5.5), G, 0.4)                        # swung ghost hats
    s.place(s.pos(b, 13.5), G, 0.35)
    (bass_a if b % 2 == 0 else bass_b)(b)
    stabs(b, late=b % 4 == 3)
s.place(s.pos(4), CR, 0.9)
s.pat(11, [(12, SN1, 0.75), (13, SN1, 0.85), (14, SN1), (15, rev(SN1), 0.8)])

# mid: drums thin out, bass and clav jam
for b in (12, 13):
    s.pat(b, [(0, K), (4, SN, 0.9), (8, K2, 0.8), (10.5, G, 0.5), (12, S2, 0.85)])
bass_a(12); s.place(s.pos(12, 4), clav(Am7, 3), 0.34)
bass_b(13); s.place(s.pos(13, 4), clav(D9, 3), 0.34); s.place(s.pos(13, 12), clav(G6, 3), 0.3)
s.place(s.pos(14), wah(bar_of(2), 4.0), 0.9)              # fast wah bar
bass_a(14)
s.pat(15, [(0, K), (2, K2), (4, SN), (6, SN1, 0.5), (8, SN1, 0.6),
           (10, SN1, 0.7), (12, SN1, 0.85), (13.5, SN1, 0.9), (14, SN1), (15, SN1)])
s.place(s.pos(15, 0), funkbass(A1, 3), 0.4)
s.place(s.pos(16) - len(CR), rev(CR), 0.9)

# groove 2: wah on the break itself + everything
for b in range(16, 20):
    src = bar_of([0, 3, 2, 1][b - 16])
    s.place(s.pos(b), wah(src, [2.0, 3.0, 2.0, 5.0][b - 16]) if b % 2 else src, 0.95)
    s.place(s.pos(b, 5.5), G, 0.4)
    (bass_a if b % 2 == 0 else bass_b)(b)
    stabs(b, late=b % 2 == 1)
s.place(s.pos(16), CR, 0.9)

# outro: one last lick
s.place(s.pos(20), bar_of(0))
s.place(s.pos(20, 0), funkbass(A1, 2), 0.42)
s.place(s.pos(20, 3), funkbass(C2, 1), 0.36)
s.place(s.pos(20, 6), funkbass(D2, 1.5), 0.36)
s.place(s.pos(20, 8), funkbass(E2, 1, pop=True), 0.3)
s.place(s.pos(20, 10), funkbass(A2, 4, pop=True), 0.32)
s.place(s.pos(20, 4), clav(Am7, 3), 0.3)
s.pat(21, [(0, K), (4, SN), (8, pitched(CR, 0.5), 0.9)])
s.place(s.pos(21, 0), funkbass(A1, 4), 0.4)
s.place(s.pos(21, 0), sub(A1, 10), 0.22)

s.render('amen_funk_174.wav', drive=1.3)
