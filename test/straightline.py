#!/usr/bin/python

import sys
sys.path.append("../src/")


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

t.setPos((a.w/2,a.h*0.9))

t.forward(100)
print t.x,t.y
a.write("Press any key to quit.")

a.showCursor(False)
a.nextChar()
a.end()
