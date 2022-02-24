#!/usr/bin/env python
"""This programme displays the date and time on an RGBMatrix display."""

import time
import datetime
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions

# Load up the font (use absolute paths so script can be invoked
# from /etc/rc.local correctly)
def loadFont(font):
    global fonts
    fonts[font] = graphics.Font()
    fonts[font].LoadFont("/root/clockdisplay/rpi-rgb-led-matrix/fonts/" + font + ".bdf")

flip = True
tick = True
scroller = 128

# init the RGB matrix 
MyMatrix = RGBMatrixOptions()
MyMatrix.rows = 64
MyMatrix.cols = 128
MyMatrix.chain_length = 1
MyMatrix.parallel = 1
MyMatrix.gpio_slowdown = 2

# Sets brightness level. Default: 100. Range: 1..100"
MyMatrix.brightness = 75

# set colour
RED = graphics.Color(255, 0, 0)
GREEN = graphics.Color(0, 255, 0)
BLUE = graphics.Color(0, 0, 255)

lastDateFlip = int(round(time.time() * 1000))
lastSecondFlip = int(round(time.time() * 1000))
lastScrollTick = int(round(time.time() * 1000))

fonts = {}

loadFont('7x13B')
loadFont('9x18B')
loadFont('6x9')

# Create the buffer canvas
DrawMatrix = RGBMatrix(options = MyMatrix, pwmBits = 8)
MyOffsetCanvas = DrawMatrix.CreateFrameCanvas()
while(1):
    currentDT = datetime.datetime.now()

    if currentDT.hour < 23:
        time.sleep(0.05)
        scrollColor = BLUE
        fulldate = currentDT.strftime("%A, %d-%b-%y")
        if currentDT.day < 10:
            fulldate = fulldate[1:]

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

    thetime = currentDT.strftime("%l"+(":" if tick else " ")+"%M")

    thetime = str.lstrip(thetime)
    sizeoftime = (50 - (len(thetime) * 18))

    # theday = currentDT.strftime("%A")
    # sizeofday = (32 - (len(theday)* 7)/2)

    pmam = currentDT.strftime("%p")

    graphics.DrawText(MyOffsetCanvas, fonts['7x13B'], scroller, 56,
                      scrollColor, fulldate)

    graphics.DrawText(MyOffsetCanvas, fonts['9x18B'], sizeoftime, 28, RED,
                      thetime)

    graphics.DrawText(MyOffsetCanvas, fonts['6x9'], 100, 28, GREEN, pmam)

    MyOffsetCanvas = DrawMatrix.SwapOnVSync(MyOffsetCanvas)
    MyOffsetCanvas.Clear()
