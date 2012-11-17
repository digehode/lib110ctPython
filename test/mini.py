#!/usr/bin/python

import sys
sys.path.append("../src/")


import Py110

a=Py110.Py110(400,300,12)
ch=65

a.write("Enter a char:")
print a.nextChar()

while True:
    a.write(chr(ch))
    ch+=1
    if ch>=65+26: ch=65
    
