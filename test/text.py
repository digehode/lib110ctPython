#!/usr/bin/python
lines=["I must go down to the sea again, ",
"to the lonely sea and the sky;",
"I left my shoes and socks there - ",
"I wonder if they're dry? "]
import sys
sys.path.append("../src/")


import Py110

a=Py110.Py110(1024,768,20)

a.setFont("YanoneTagesschrift.ttf",18)

for l in lines:
    a.writeN(l)
    
a.writeN()


a.writeN("Press any key to quit.")

a.showCursor(False)
a.nextChar()
a.end()
