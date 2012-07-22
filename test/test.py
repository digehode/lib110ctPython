#!/usr/bin/python

import sys
sys.path.append("../src/")


import Py110
from random import randint

a=Py110.Py110(640,480,20)

i=0
a.showCursor(True)
t=a.getTurtle()
t.setSpeed(9)
t.setPenSize(1)
a.write("How many corners?\nEnter an int: ")
n= a.nextInt()

for i in range(n):
    a.setTextColour((randint(128,255),randint(128,255),randint(128,255)))
    a.write("That's number %d\n"%(i+1))
    t.forward(10)
    t.right(110)
    
a.write("Press any key to quit.")
a.showCursor(False)
a.nextChar()
a.end()
