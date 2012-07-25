#!/usr/bin/python

import sys
sys.path.append("../src/")


import Py110
from random import randint
import random
a=Py110.Py110(1024,768,20)

random.seed(1)
a.showCursor(True)
t=a.getTurtle()
t.setSpeed(9)
t.setPenSize(1)


col=[255,255,255]


def kochLine(l,minL):
    l=float(l)
    for i in range(3):
        col[i]+=randint(-10,10)
        if col[i]>255: col[i]=255
        if col[i]<60: col[i]=60
                 
    t.setColour(col)
    if l<=minL:
        t.forward(l)
    else:
        kochLine(l/3,minL)
        t.left(60)
        kochLine(l/3,minL)
        t.right(120)
        kochLine(l/3,minL)
        t.left(60)
        kochLine(l/3,minL)


t.setPos((800,550))
t.left(90)

l=600        
ml=1

for i in range(3):
    kochLine(l,ml)
    t.right(120)


a.setPosition(55,20)
a.write("Koch Snowflake\n")


#t.forward(l)
a.setPosition(50,22)
a.write("Press any key to quit.")

a.showCursor(False)
a.nextChar()
a.end()
