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

#t.hideIcon(True)
angle=60

def makeJaggie(l,s):
    """Draw a line of jaggies of length l with s spikes"""
    if s==0:
        t.forward(l)
        return
    lineLength=l/float(s)
    for i in range(s):
        t.left(60)
        t.forward(lineLength)
        t.right(120)
        t.forward(lineLength)
        t.left(60)

a.write("Checking lines of different lengths start/end in the right places")
l=200
nums=[1,2,4,8,16,32,l]
p=10
for i in nums:
    c=(256/max(nums))*i
    c2=(1-(1-c/256.0)**p)*256
    print c,c2

    t.push()
    t.setColour((200,256-c2,c2))
    a.write("Drawing with %d spikes\n"%i)
    makeJaggie(l,i)
    t.pop()


a.write("Press any key to quit.")

a.showCursor(False)
a.nextChar()
a.end()
