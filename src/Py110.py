#!/usr/bin/python


import threading,time
import math
from Queue import Queue

import pygame as pg

__author__ = 'James Shuttleworth <csx239@coventry.ac.uk>'
__version__="0.7"

cVersion=__version__
cDate="2012-12-05"

#To discuss with Mike
# setPos vs setPosition
# showHide vs setVisible


#TODO: send kill event back to somewhere useful to be handled in user code

# bgcol=(10,8,20)
# fgcol=(255,255,255)
black=(0,0,0)
green=(0,100,0)
makeEnd=False

def loadImg(filename):
	try:
		image = pg.image.load(filename)
		if image.get_alpha() is None:
			image = image.convert()
		else:
			image = image.convert_alpha()
	except pg.error, message:
        	print 'Cannot load image:', filename
        	raise SystemExit, message
	return image


def sanitiseString(s, validChars):
    #The following line is probably bad for your health and it's not
    #even that great - always replaces with "0" and doesn't do
    #anything sophisticated enough to actually guarantee good numbers
    return "".join([x if x in validChars else "0" for x in s.strip()])

def sanitiseColour(colour):
    if (not len(colour) in [3,4] ) or (not type(colour) in [type((1,2,3)), type([1,2,3])]) :
        raise TypeError("Colour must be a tuple of 3 or 4 integers (0-255) corresponding to R, G, B and (possibly) Alpha")
    if len(colour)==3:
        colour+=(255,)
    return colour



class Py110(object):
    def __init__(self,w,h,pitch):
        self.size=self.w,self.h=w,h
        self.pitch=pitch
        self.eventQueue=Queue()
        self.display=DisplayThread(w,h,pitch, self.eventQueue)
        self.display.start()
        print "Py110 version %s (%s)"%(cVersion, cDate)
        

        
    def setBackgroundImage(self,filename):
        """ Set the background image drawn begins everything else """
        self.display.bg=loadImg(filename)
    def clearBackgroundImage(self):
        """ Clear the background image """
        self.display.bg=None
        
    def queuePump(self):
        if self.display.ready:
            pg.event.pump()            
            for event in pg.event.get():
                self.eventQueue.put(event)

    
    def dummy(self):
        self.queuePump()
    
    def end(self):
        #Stop other thread and return
        self.queuePump()
        self.display.end()



    def clear(self) :
        """Clears all text from the console (retaining other graphics)"""
        self.display.clear()
        self.queuePump()
        pass
    def clearBack( self, rectangle=None) :
        #TODO:        
        """NOT IMPLEMENTED. Clears a rectangular portion of the background image. Rectangle is a tuple of (x,y,width,height).  If the rectangle is None, clear all of the background."""
        pass
        self.queuePump()
    def clearChar(self) :
        """Clears the character at the current cursor position"""
        self.display.clearChar()
        self.queuePump()
    def clearChars(self, nChars) :
        """Clears a number of characters, starting from the current cursor position"""
        oldPos=self.display.cursor
        for i in range(nChars):
            self.display.clearChar()
            self.display.cursorStep()
        self.display.cursor=oldPos
        self.queuePump()
        
    def echo(self,on) :
        """Controls console behaviour during input. When echo is off (False) keys pressed are not displayed on the screen."""
        self.display.echo=on
        self.queuePump()

    def getBuffer(self) :
        #TODO:        
        """NOT IMPLEMENTED. Sort of not, anyway. Returns the background image for the console (enables fun with graphics)"""
        self.queuePump()
        return self.display.screen

    def getTurtle(self) :        
        """Gets an Logo-style 'Turtle' for use in the console window."""
        self.queuePump()
        return self.display.turtle
    
    def getX(self) :
        """Returns the x coordinate of the current cursor position"""
        self.queuePump()
        return self.display.cursorToXY()[0]


    def getY(self) :
        """Returns the y coordinate of the current cursor position"""
        self.queuePump()
        return self.display.cursorToXY()[1]


    def hideTurtle(self) :
        """Hides the turtle (retains anything the turtle has drawn even though it will not be visible until showTurtle() is called)"""
        self.queuePump()
        self.display.showTurtle=False

    def	next(self) :
        """Reads a string from the keyboard"""
        self.queuePump()
        return self.display.grab(fn=lambda: self.queuePump()).strip()
        

    def nextChar(self) :
        """Reads a single character."""
        self.queuePump()
        return self.display.grab(1,fn=lambda: self.queuePump())

    def nextDouble(self) :
        """Reads a double from the keyboard"""
        #strip all non digit, non ./- characters
        #Pretty rubbish, but:
        #1. user input shouldn't crash a program
        #2. If you want to do it differently, get the string and work from there
        s=sanitiseString(self.next(),"0123456789.-").strip()
        if s.find("-")>0 or s.count("-")>1 or s.count(".")>1 or s in["-","",".","-.",".-"]:
            return 0.0
        self.queuePump()
        return float(s)

        

    def nextInt(self) :
        """Reads an integer from the keyboard"""
        s=sanitiseString(self.next(),"0123456789-").strip()
        if s.find("-")>0 or s.count("-")>1  or s in["-",""]:
            self.queuePump()
            return 0
        self.queuePump()
        return int(s)


    def setBackColour(self,colour) :        
        """NOT IMPLEMENTED Sets the background colour for outputted text."""
        #TODO: ???
        self.queuePump()
        pass

    def setPosition(self, x, y) :
        """Sets the cursor position (in character spaces, not pixels)"""
        #Doing it the lazy way:
        oldPos=self.display.cursor
        while (x,y)!=self.display.cursorToXY():
            self.display.cursorStep()
            if self.display.cursor==oldPos:
                break #Bad values given
        self.queuePump()
    def setTextColour(self, colour):
        """Sets the colour of the foreground text."""
        self.display.tCol=sanitiseColour(colour)
        self.queuePump()
    def getPos(self):
        """Returns tuple of current x,y cursor position (in characters, not pixels)"""
        self.queuePump()
        return self.display.cursorToXY()
    
    def showCursor(self,on):
        """Set the cursor to show or not"""
        self.queuePump()
        self.display.showCursor=on

    def showTurtle(self) :
        """Displays the turtle (turtle is displayed by default but this may be necessary following a call to hideTurtle()"""
        self.display.showTurtle=True
        self.queuePump()

    def write(self,s) :
        """Writes a "thing" to the screen.  Uses the __str__ function of the thing to decide what to display.  See also: writeN()"""
        self.display.write(str(s))
        self.queuePump()

    def writeN(self,s="") :
        """Writes a "thing" to the screen, followed by a newline.  Uses the __str__ function of the thing to decide what to display. See also write()"""
        
        self.display.write(str(s)+"\n")
        self.queuePump()

    def setFont(self,fontName,pitch):
        """ Set the font used for display. Can be a TTF filename
        (including path if not in current directory) or None for reset
        to system default. You don't *have* to clear the text on
        screen first, but if the font is a different size, it might
        not look good if you don't. """
        self.display.setFont(fontName,pitch)
        

class Turtle(object):
    def __init__(self,surface):
        self.surface=surface
        self.angle=0
        self.x,self.y=self.surface.get_rect().center
        self.x=float(self.x)
        self.y=float(self.y)
        self.res=8.0
        self.penDown=True
        self.colour=(255,255,255,255)
        self.penSize=1
        self.sleep=0
        self.setSpeed(8)
        self.showTurtle=True
        self.showIcon=True
        self.stack=[]
    def push(self):
        """Push the current position and angle onto a stack to be popped off later.
        You can use push() to remember a location and then pop() to go back to it later.
        Doesn't store any other parameters (size, colour, speed)."""
        self.stack.append((self.x,self.y,self.angle))
    def pop(self):
        """Popc the most recent  position and angle from a stack and place the turtle at those coordinates, at that angle.
        You can use push() to remember a location and then pop() to go back to it later.
        Doesn't set any other parameters (size, colour, speed)."""
        if len(self.stack)==0:
            return
        self.x,self.y,self.angle=self.stack[-1]
        self.stack=self.stack[:-1]
    
    def hideIcon(self,hide):
        """hideIcon(True) hides the visible Turtle - this is not the
        same as the lines drawn by the Turtle. hideIcon(False) unhides
        the icon"""
        self.showIcon=not hide
    def clear(self):
        """Clear the Turtle's trail and reset all parameters"""
        self.surface.fill((0,0,0,0)) #Fill with transparency
        self.__init__(self.surface) #re-call the constructor
    def setSpeed(self,s):
        """ Set the speed of drawing. Has no effect when pen is up. 0=slow, 10=fastest possible. """
        if s<0: s=0
        if s>10: s=10
        #Invert to use for delay
        s=10-s
        #Re-range between 0 and 0.005
        self.sleep=0.0005*s
        
    def forward(self,d):
        """Move forward by d pixels"""
        #This is all a bit more hacky than it was originally, but it
        #copes with small lines (even <1px) and accurately
        if d==0: return
        
        d=float(d)
        sx=float(self.x)
        sy=float(self.y)
        ex=sx+math.sin(math.radians(self.angle))*d
        ey=sy-math.cos(math.radians(self.angle))*d
        xd=ex-sx
        yd=ey-sy
        s=(xd**2+yd**2)**0.5
        unitx=xd/s
        unity=yd/s

        i=0
        ox=sx
        oy=sy
        
        while i+1<=d:
            ox=self.x
            oy=self.y
            self.x+=unitx
            self.y+=unity
        
            if self.penDown:                
                pg.draw.line(self.surface, self.colour, (ox,oy),(self.x,self.y),self.penSize)
                if self.sleep>0: time.sleep(self.sleep)
            i+=1
        #In case of bits less than 1 left over (shouldn't happen) or
        #lines less than 1 to start with.
        self.x=ex
        self.y=ey
        if self.penDown and (self.x-ox!=0 or self.y-oy!=0):                
            pg.draw.line(self.surface, self.colour, (ox,oy),(self.x,self.y),self.penSize)
            sleepscale=((self.x-ox)**2+(self.y-oy)**2)**0.5
            if self.sleep>0: time.sleep(self.sleep*sleepscale)
        

    def left(self,a):
        """Turn left by the given amount (degrees)."""
        self.angle-=a

    def right(self,a):
        """Turn right by the given amount (degrees)."""
        self.angle+=a

    def getPos(self):
        """Returns the x,y coordinates (in pixels with origin at top left) )of the turtle as a tuple"""
        #Get the location (pixels) of the turtle        
        return (self.x,self.y)

    def setPosition(self,pos):
        self.setPos(pos)
    
    
    def setPos(self,pos):
        """Set the position of the turtle to the x and y values given. The parameter should be a tuple."""
        self.x=pos[0]
        self.y=pos[1]
        
    def setColour(self,colour):
        """Set the colour of the Turtle. Colours are (R,G,B) tuples with each value between 0 and 255 or optionally (R,G,B,A) tuples where A is alpha."""
        self.colour=sanitiseColour(colour)
    def setPenSize(self,s):
        """Set pen size"""
        if s>=1:
            self.penSize=s
    def getColour(self):
        """Return the current pen colour as an RGB or RGBA tuple."""
        return self.colour
    def lowerPen(self):
        """Put the Turtle's pen down - that is, draw when moving"""
        self.penDown=True
    def raisePen(self):
        """Lift the Turtle's pen up - that is, don't draw when moving"""
        self.penDown=False            

class DisplayThread(threading.Thread):
    def __init__(self,w,h,pitch, eventQueue):        
        threading.Thread.__init__(self)
        self.ready=False
        self.eventQueue=eventQueue
        self.screen_size = w,h
        self.tCol=(255,255,255,255)
        self.textBuffer=None
        self.clear()
        self.bgCol=(10,8,20)
        self.pitch=pitch
        pg.init()
        self.screen = pg.display.set_mode(self.screen_size)
        pg.display.set_caption("Py110")
        self.clock = pg.time.Clock()
        self.setFont(None, pitch)
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
        self.ready=True
        self.bg=None
    
    def setFont(self,fontName,pitch):
        self.font1 = pg.font.Font(fontName, pitch)
        text = self.font1.render("W", 1, self.tCol)
        self.charRect = text.get_rect()

            

    def grab(self,n=0,fn=None):
	self.captureBuffer=""
	self.captureState=True
	while (n==0 and self.captureState) or (n>0 and len(self.captureBuffer)!=n):
	    time.sleep(0.01)
	    if fn!=None:
                fn()
	self.captureState=False
        #Weirdness: without the sleep, the carriage return at the end
        #of the user input is not converted to a visual linefeed and
        #text that follows (on the same line) is spaced weirdly -
        #spread out

        #It goes away if you just print the characters to stdout, too, but this is slightly better

        #Assuming some kind of race-condition that this plaster will
        #cover until it comes back to kill me
	time.sleep(0.1)

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
        #print "...[%s]%d"%(c,ord(c))
		
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

            if self.makeEnd:
                self.ready=False
                pg.quit()
                return


            # pg.event.pump()            
            # for event in pg.event.get():
            while not self.eventQueue.empty():
                event=self.eventQueue.get()
                if event.type == pg.QUIT:
                    pg.quit()
                    return
                elif event.type == pg.KEYDOWN:
                    if not event.key in [pg.K_BACKSPACE, pg.K_TAB, pg.K_CLEAR, pg.K_RETURN, pg.K_PAUSE, pg.K_ESCAPE, pg.K_DELETE, pg.K_UP, pg.K_DOWN, pg.K_RIGHT, pg.K_LEFT, pg.K_INSERT, pg.K_HOME, pg.K_END, pg.K_PAGEUP, pg.K_PAGEDOWN, pg.K_F1, pg.K_F2, pg.K_F3, pg.K_F4, pg.K_F5, pg.K_F6, pg.K_F7, pg.K_F8, pg.K_F9, pg.K_F10, pg.K_F11, pg.K_F12, pg.K_F13, pg.K_F14, pg.K_F15, pg.K_NUMLOCK, pg.K_CAPSLOCK, pg.K_SCROLLOCK, pg.K_RSHIFT, pg.K_LSHIFT, pg.K_RCTRL, pg.K_LCTRL, pg.K_RALT, pg.K_LALT, pg.K_RMETA, pg.K_LMETA, pg.K_LSUPER, pg.K_RSUPER, pg.K_MODE, pg.K_HELP, pg.K_PRINT, pg.K_SYSREQ, pg.K_BREAK, pg.K_MENU, pg.K_POWER]:
                        if self.captureState:
                            self.captureBuffer+=str(event.unicode)
                        if self.echo:
                            self.write(str(event.unicode))
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
            self.screen.fill(self.bgCol)
            if self.bg!=None:

                self.screen.blit(self.bg,(0,0))

            #TODO: Move all this drawing into the turtle by passing in/out another buffer for the icon
            if self.showTurtle:
                self.screen.blit(self.turtle.surface,(0,0))
                if self.turtle.showIcon:
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



class StopWatch(object):
    def __init__(self):
        self.running=False
        self.startTime=0
        self.elapsed=0
    def read(self):
        """Reads the current time from the watch, without stopping it"""
        if self.running:
            now=time.time()
            self.elapsed+=(now-self.startTime)
            self.startTime=now
        return self.elapsed
    def reset(self):
        """Resets the time to zero. Does not affect the started/stopped status of the stopwatch."""
        self.elapsed=0
        self.startTime=time.time()
    def start(self):
        """Starts the watch"""
        if not self.running:
            self.startTime=time.time()
            self.running=True
        
    def stop(self):
        """Stops the watch (does not reset time to zero)"""
        if self.running:
            self.elapsed+=time.time()-self.startTime;
            self.running=False
        return self.elapsed




        
            
if __name__=="__main__":
    print """This module isn't meant to be run as a program.
    Instead, launch Python and import the  module. """

    

    

#  LocalWords:  DisplayThread eventQueue
