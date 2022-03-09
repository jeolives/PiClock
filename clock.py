#!/usr/bin/env python
"""This programme displays the date and time on an RGBMatrix display."""

import time
import datetime
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix
from rgbmatrix import RGBMatrixOptions


# Load up the font (use absolute paths so script can be invoked
# from /etc/rc.local correctly)
def loadFont(font):
    global fonts
    fonts[font] = graphics.Font()
    fonts[font].LoadFont("/root/clockdisplay/rpi-rgb-led-matrix/fonts/" + font + ".bdf")

flip = True
tick = True
scroller = 128

# init the RGB matrix as 64 Rows, 128 Cols, 1 chain
MyMatrix = RGBMatrixOptions()
MyMatrix.rows = 64
MyMatrix.cols = 128
MyMatrix.chain_length = 1
MyMatrix.hardware_mapping = 'regular'
MyMatrix.gpio_slowdown = 3

# Sets brightness level. Default: 100. Range: 1..100"
MyMatrix.brightness = 50

# set colour
ColorWHI = graphics.Color(255, 255, 255)
RED = graphics.Color(255, 0, 0)
GREEN = graphics.Color(0, 255, 0)
BLUE = graphics.Color(0, 0, 255)
YELLOW = graphics.Color(255, 255, 0)
PURPLE = graphics.Color(255, 0, 255)

lastDateFlip = int(round(time.time() * 1000))
lastSecondFlip = int(round(time.time() * 1000))
lastScrollTick = int(round(time.time() * 1000))

fonts = {}

loadFont('10x20')
loadFont('8x13')

# Create the buffer canvas
MyMatrix1 = RGBMatrix(options = MyMatrix)
MyMatrix1.pwmBits = 8
MyOffsetCanvas = MyMatrix1.CreateFrameCanvas()
while(1):
    currentDT = datetime.datetime.now()

    if currentDT.hour < 23:
        time.sleep(0.02)
        scrollColour = BLUE
        fulldate = currentDT.strftime(" %a"+" "+"%d %b %Y")
        if currentDT.day < 10:
            fulldate = fulldate[1:]
    #else:
    #    time.sleep(0.025)
    #   scrollColour = PURPLE
    #   fulldate = "ERR"

    sizeofdate = len(fulldate)*14

    Millis = int(round(time.time() * 1000))

    if Millis-lastSecondFlip > 1000:
        lastSecondFlip = int(round(time.time() * 1000))
        tick = not tick

    if Millis-lastDateFlip > 5000:
        lastDateFlip = int(round(time.time() * 1000))
        flip = not flip

    scroller = scroller-1
    if scroller == (-sizeofdate):
        scroller = 128

    thetime = currentDT.strftime("%l"+":"+"%M"+":"+"%S")

    thetime = str.lstrip(thetime)
    sizeoftime = (50 - (len(thetime) * 18) / 3.75)

    # theday = currentDT.strftime("%A")
    # sizeofday = (32 - (len(theday)* 7)/2)

    pmam = currentDT.strftime("%p")

    graphics.DrawText(MyOffsetCanvas, fonts['10x20'], scroller, 56,
                      scrollColour, fulldate)

    graphics.DrawText(MyOffsetCanvas, fonts['10x20'], sizeoftime, 28, RED,
                      thetime)

    graphics.DrawText(MyOffsetCanvas, fonts['8x13'], 100, 28, GREEN, pmam)

    MyOffsetCanvas = MyMatrix1.SwapOnVSync(MyOffsetCanvas)
    MyOffsetCanvas.Clear()
