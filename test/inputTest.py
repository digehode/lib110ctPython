#!/usr/bin/python

#Test input doesn't screw up output and that CRs are stripped from inputs

import sys
sys.path.append("../src/")


import Py110
from random import randint

a=Py110.Py110(640,480,20)

a.showCursor(True)

a.write("Enter text: ")
n= a.next()
a.write("No newline here!")
a.write("\nAny in your input?\n")
for i in n:
    a.write(str(ord(i))+"\n")


a.write("Press any key to quit.")
a.showCursor(False)
a.nextChar()
a.end()

