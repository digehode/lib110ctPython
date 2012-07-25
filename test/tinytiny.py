#!/usr/bin/python

import sys
sys.path.append("../src/")


import Py110
from random import randint
import random
a=Py110.Py110(640,480,16)

random.seed(1)
a.showCursor(True)
t=a.getTurtle()
t.setSpeed(9)
t.setPenSize(1)


#TODO: draw vertical lines

col=[255,255,255]

t.setPos((a.w*0.4,a.h*0.9))


fractions=[1,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1]
maxL=150


t.angle=0
for fraction in fractions:
    a.write("Drawing in %f pixel steps\n"%fraction)
    t.push()
    for i in range(int(maxL/fraction)):
        t.forward(fraction)    
    t.pop()
    t.x+=10

t.push()
a.write("Drawing single line of %d pixels\n"%maxL)
t.forward(maxL)
t.pop()

t.x+=10
t.angle=25
for fraction in fractions:
    a.write("Drawing in %f pixel steps\n"%fraction)
    t.push()
    for i in range(int(maxL/fraction)):
        t.forward(fraction)    
    t.pop()
    t.x+=10

a.write("Drawing single line of %d pixels\n"%maxL)
t.forward(maxL)


a.write("Press any key to quit.")

a.showCursor(False)
a.nextChar()
a.end()
