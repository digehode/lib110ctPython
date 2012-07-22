#!/usr/bin/python


import threading,time
import math

import pygame as pg

__author__ = 'James Shuttleworth <csx239@coventry.ac.uk>'


#TODO: send kill event back to somewhere useful to be handled in user code

bgcol=(10,8,20)
fgcol=(255,255,255)
black=(0,0,0)
green=(0,100,0)
makeEnd=False

def sanitiseString(s, validChars):
    #The following line is probably bad for your health and it's not
    #even that great - always replaces with "0" and doesn't do
    #anything sophisticated enough to actually guarantee good numbers
    return "".join([x if x in validChars else "0" for x in s.strip()])

def sanitiseColour(colour):
    if (not len(colour) in [3,4] ) or type(colour)!=type((1,2,3)):
        raise TypeError("Colour must be a tuple of 3 or 4 integers (0-255) corresponding to R, G, B and (possibly) Alpha")
    if len(colour)==3:
        colour+=(255,)
    return colour



class Py110(object):
    def __init__(self,w,h,pitch):
        self.size=self.w,self.h=w,h
        self.pitch=pitch
        self.display=DisplayThread(w,h,pitch)
        self.display.start()
    def end(self):
        #Stop other thread and return
        self.display.end()


    def clear(self) :
        #Clears all text from the console (retaining background image)
        self.display.clear()
        pass
    def clearBack(self) :
        #TODO:
        #Clears the background image for the console (retaining text)
        pass
    def clearBack( self, x,  y,  width,  height) :
        #TODO:        
        #Clears a rectangular portion of the background image
        pass
    def clearChar(self) :
        #Clears the character at the current cursor position
        self.display.clearChar()
    def clearChars(self, nChars) :
        #Clears a number of characters, starting from the current cursor position
        oldPos=self.display.cursor
        for i in range(nChars):
            self.display.clearChar()
            self.display.cursorStep()
        self.display.cursor=oldPos
        pass
    def echo(on) :
        #Controls console behaviour during input
        self.display.echo=on
    def getBuffer(self) :
        #TODO:        
        #Returns the background image for the console (enables fun with graphics)
        pass
    def getTurtle(self) :        
        #Gets an MSW Logo style 'Turtle' for use in the console window.
        return self.display.turtle
    
    def getX(self) :
        #Returns the x coordinate of the current cursor position
        return self.display.cursorToXY()[0]


    def getY(self) :
        #Returns the y coordinate of the current cursor position        
        return self.display.cursorToXY()[1]


    def hideTurtle(self) :
        #Hides the turtle (retains anything the turtle has drawn)
        self.display.showTurtle=False

    def	next(self) :
        #Reads a string.
        return self.display.grab()
        

    def nextChar(self) :
        #Reads a single character.
        return self.display.grab(1)

    def nextDouble(self) :
        #Reads a double
        #strip all non digit, non ./- characters
        #Pretty rubbish, but:
        #1. user input shouldn't crash a program
        #2. If you want to do it differently, get the string and work from there
        s=sanitiseString(self.next(),"0123456789.-").strip()
        if s.find("-")>0 or s.count("-")>1 or s.count(".")>1 or s in["-","",".","-.",".-"]:
            return 0.0
        return float(s)

        

    def nextInt(self) :
        #Reads an integer
        s=sanitiseString(self.next(),"0123456789-").strip()
        if s.find("-")>0 or s.count("-")>1  or s in["-",""]:
            return 0
        return int(s)


    def setBackColour(colour) :
        #Sets the background colour for outputted text.
        pass

    def setPosition(self, x, y) :
        #TODO:        
        #Sets the cursor position (in character spaces, not pixels)
        pass

    def setTextColour(self, colour):
        #Sets the colour of the foreground text.
        self.display.tCol=sanitiseColour(colour)

    def getPos():
        return self.display.cursorToXY()
    
    def showCursor(self,on):
        #Set the cursor to show or not
        self.display.showCursor=on

    def showTurtle(self) :
        #Displays the turtle (turtle is displayed by default but this may be necessary following a call to hideTurtle()
        self.display.showTurtle=True

    def write(self,s) :
        #Writes a thing to the screen
        self.display.write(s)

class Turtle(object):
    def __init__(self,surface):
        self.surface=surface
        self.angle=0
        self.x,self.y=self.surface.get_rect().center
        self.res=10.0
        self.penDown=True
        self.colour=(255,255,255,255)
        self.penSize=1
        self.sleep=0
        self.setSpeed(8)
        self.showTurtle=True
    def clear(self):
        self.surface.fill((0,0,0,0)) #Fill with transparency
        self.__init__(self.surface) #re-call the constructor
    def setSpeed(self,s):
        """ Set the speed of drawing. Has no effect when pen is up. 0=slow, 10=fastest possible. """
        if s<0: s=0
        if s>10: s=10
        #Invert to use for delay
        s=10-s
        #Re-range between 0 and 0.001
        self.sleep=0.0001*s
        
    def forward(self,d):
        #pg.draw.circle(self.surface,(0,255,0,255),(int(self.x),int(self.y)),4)
        for i in range(int(d*self.res)):
            ox=self.x
            oy=self.y
            self.x=self.x+math.sin(math.radians(self.angle))*(d/self.res)
            self.y=self.y-math.cos(math.radians(self.angle))*(d/self.res)
            if self.penDown:                
                pg.draw.line(self.surface, self.colour, (ox,oy),(self.x,self.y),self.penSize)
                if self.sleep>0: time.sleep(self.sleep)
    def left(self,a):
        self.angle-=a
    def right(self,a):
        self.angle+=a
    def getPos(self):
        #Get the location (pixels) of the turtle        
        return (self.x,self.y)
    def setPos(self,pos):
        self.x=pos[0]
        self.y=pos[1]
    def setColour(self,colour):
        self.colour=sanitiseColour(colour)
    def setPenSize(self,s):
        if s>=1:
            self.penSize=s
            
class DisplayThread(threading.Thread):
    def __init__(self,w,h,pitch):        
        threading.Thread.__init__(self)
        self.screen_size = w,h
        self.tCol=(255,255,255,255)
        self.textBuffer=None
        self.clear()
                
        self.pitch=pitch
        pg.init()
        self.screen = pg.display.set_mode(self.screen_size)
        pg.display.set_caption("Py110")
        self.clock = pg.time.Clock()
        self.font1 = pg.font.Font(None, pitch)

        text = self.font1.render("H", 1, fgcol)
        self.charRect = text.get_rect()
        self.makeEnd=False
        #self.chars=[]

        self.showTurtle=True
        
        self.cursor=0
        self.showCursor=True
        
        self.MAX_CURSOR=(w/self.charRect.width)*(h/self.charRect.height)
        self.blinkSpeed=0.5
        self.cursorTimer=0.0



        self.echo=True

        self.captureState=False
        self.captureBuffer=""
        
        self.turtle=Turtle(pg.Surface(self.screen_size,flags=pg.SRCALPHA,depth=32))
        self.turtleIcon=[(-0.5,0.5),(0.0,-0.5),(0.5,0.5)]
        self.turtleIconScale=10

    def grab(self,n=0):
        self.captureBuffer=""
        self.captureState=True

        
        while (n==0 and self.captureState) or (n>0 and len(self.captureBuffer)!=n):
            time.sleep(0.0001)


        self.captureState=False
        return self.captureBuffer
        
    def drawCursor(self, clear=False):

        x,y=self.cursorToXY()
        self.charRect.left=x*self.charRect.width
        self.charRect.top=y*self.charRect.height

        if clear or time.time()-abs(self.cursorTimer)>self.blinkSpeed:
            if self.cursorTimer>0 and self.showCursor and not clear: 

                pg.draw.rect(self.textBuffer, self.tCol[0:3]+(128,), self.charRect,1)
                self.cursorTimer=-time.time()
            else:
                pg.draw.rect(self.textBuffer, (0,0,0,0), self.charRect,1)
                #self.textBuffer.fill((0,0,0,0),self.charRect)
                self.cursorTimer=time.time()

        
        
    def clear(self):
        #Clear text buffer
        self.cursor=0
        self.textBuffer=pg.Surface(self.screen_size,flags=pg.SRCALPHA,depth=32)
        
        

    def clearChar(self):
        x,y=self.cursorToXY()
        self.charRect.left=x*self.charRect.width
        self.charRect.top=y*self.charRect.height
        self.textBuffer.fill((0,0,0,0),self.charRect)
        
        
    def cursorStep(self,d=1):
        self.drawCursor(True)
        self.cursor=(self.cursor+d)%self.MAX_CURSOR

    def cursorToXY(self):
        
        return self.cursor % (self.screen_size[0]/self.charRect.width), \
               self.cursor/(self.screen_size[0]/self.charRect.width)
    
    def newLine(self):
        #Carriage return handling.  A bit hacky even for me.
        x,y=self.cursorToXY()
        while self.cursorToXY()[1]==y:
            self.cursorStep()
    def putC(self,c):
        
        if len(c)!=1 or type(c)!=type(""):
            raise TypeError("putC can only write a char (str of length 1), not a %s of length %d"%(str(type(c)),len(c)))
        if c=="\n":
            self.newLine()
            return
        x,y=self.cursorToXY()

        text = self.font1.render(c, 1, self.tCol)
        
        self.charRect.left=x*self.charRect.width
        self.charRect.top=y*self.charRect.height
        r=text.get_rect()
        r.center=self.charRect.center
        self.clearChar()
        self.textBuffer.blit(text,r)
        self.cursorStep()


    def write(self,v):
        v=str(v)
        for i in v:
            self.putC(i)

        
    def end(self):
        self.makeEnd=True

    def run(self):

        while True:
            #screen.fill(bgcol)
            if self.makeEnd:
                pg.quit()
                return


            pg.event.pump()            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return
                elif event.type == pg.KEYDOWN:
                    if not event.key in [pg.K_BACKSPACE, pg.K_TAB, pg.K_CLEAR, pg.K_RETURN, pg.K_PAUSE, pg.K_ESCAPE, pg.K_DELETE, pg.K_UP, pg.K_DOWN, pg.K_RIGHT, pg.K_LEFT, pg.K_INSERT, pg.K_HOME, pg.K_END, pg.K_PAGEUP, pg.K_PAGEDOWN, pg.K_F1, pg.K_F2, pg.K_F3, pg.K_F4, pg.K_F5, pg.K_F6, pg.K_F7, pg.K_F8, pg.K_F9, pg.K_F10, pg.K_F11, pg.K_F12, pg.K_F13, pg.K_F14, pg.K_F15, pg.K_NUMLOCK, pg.K_CAPSLOCK, pg.K_SCROLLOCK, pg.K_RSHIFT, pg.K_LSHIFT, pg.K_RCTRL, pg.K_LCTRL, pg.K_RALT, pg.K_LALT, pg.K_RMETA, pg.K_LMETA, pg.K_LSUPER, pg.K_RSUPER, pg.K_MODE, pg.K_HELP, pg.K_PRINT, pg.K_SYSREQ, pg.K_BREAK, pg.K_MENU, pg.K_POWER]:
                        if self.captureState:
                            self.captureBuffer+=str(event.unicode)
                        if self.echo:
                            self.putC(str(event.unicode))
                    elif event.key==pg.K_RETURN:
                        self.captureBuffer+="\n"
                        self.captureState=False
                        if self.echo: self.newLine()
                    elif event.key==pg.K_BACKSPACE:
                        self.captureBuffer=self.captureBuffer[:-1]
                        if self.echo:
                            self.drawCursor(True)#Force clear of cursor to prevent leaving trails
                            self.cursor=(self.cursor-1)%self.MAX_CURSOR
                            self.clearChar()
                        #TODO: take account of backspace, tab, space,... other?
                                          


                

                                
            self.drawCursor()
            self.screen.fill(bgcol)
            if self.showTurtle:
                self.screen.blit(self.turtle.surface,(0,0))
                pointlist=[]
                for i in range(len(self.turtleIcon)):
                    p1=self.turtleIcon[i]
                    #rotate point
                    p1=(p1[0]*math.cos(math.radians(self.turtle.angle))-p1[1]*math.sin(math.radians(self.turtle.angle)),
                        p1[0]*math.sin(math.radians(self.turtle.angle))+p1[1]*math.cos(math.radians(self.turtle.angle)))
                    #scale point
                    p1=(p1[0]*self.turtleIconScale,
                        p1[1]*self.turtleIconScale)
                    #Move point
                    p1=(p1[0]+self.turtle.x,
                        p1[1]+self.turtle.y)
                    pointlist.append(p1)

                #Draw black body
                pg.draw.polygon(self.screen,black,pointlist)
                #Use current colour to draw outline
                pg.draw.polygon(self.screen,self.turtle.colour,pointlist,1)


            self.screen.blit(self.textBuffer,(0,0))
            #Timing - limits to 10 frames per second. 
            self.clock.tick(10)
            #Flip the backbuffer to the main buffer
            pg.display.flip()


            
if __name__=="__main__":
    print """This module isn't meant to be run as a program.
    Instead, launch Python and import the  module. """
