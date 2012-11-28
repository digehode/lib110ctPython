#!/usr/bin/python

import sys
sys.path.append("../src/")

#Tests raisePen() and lowerPen() and general drawing


import Py110
from random import randint
import random
a=Py110.Py110(400,300,12)

random.seed(1)
a.showCursor(True)
t=a.getTurtle()
t.setSpeed(9)
t.setPenSize(1)


col=[255,255,255]

t.setPos((a.w/2,a.h/2))




for i in range(72):
    t.lowerPen()
    t.forward(-40)
    t.left(15)
    t.raisePen()
    t.forward(25)
    t.right(8)
    
a.write("Press any key to quit.")

a.showCursor(False)
a.nextChar()
a.end()
