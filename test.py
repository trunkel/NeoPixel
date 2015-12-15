from cheerlights import *
from neopixel import *
import random
import time

def getColor(colors):
    colors.updateColor()
    return Color(colors.getRed(), colors.getGreen(), colors.getBlue())

def blinkAndFade(strip, colors, duration_s=60, min_wait_ms=150, max_wait_ms=1000):
    # Set initial pixel state
    status = ['On','Off','Fade'];
    state = [random.choice(status) for x in range(strip.numPixels())]
    countdown = [random.randint(min_wait_ms,max_wait_ms) for x in range(strip.numPixels())]
    
def blinker(strip, colors, duration_s=60, min_wait_ms=150, max_wait_ms=1000):
    # Set initial pixel state
    countdown = [random.randint(min_wait_ms,max_wait_ms) for x in range(strip.numPixels())]
    state = [random.randint(0,3) for x in range(strip.numPixels())]

    for i in range(0, duration_s*1000, min_wait_ms):
        for j in range(strip.numPixels()):
            # Decrement pixel countdown values
            countdown[j] = max(0, countdown[j] - min_wait_ms);

            if countdown[j] == 0:
                # Update state of pixels which have timed out
                state[j] = random.randint(0,3)
                countdown[j] = random.randint(min_wait_ms, max_wait_ms)

                # Update pixel color
                if state[j] == 0:
                    strip.setPixelColor(j, Color(0, 0, 0))    # off pixel
                else:
                    strip.setPixelColor(j, getColor(colors))  # color pixel

        strip.show()
        time.sleep(min_wait_ms/1000.0)

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)
                
def main():
    colors = CheerLights()
    colors.updateColor()

    strip = Adafruit_NeoPixel(40, 0)
    strip.begin()

    blinker(strip, colors)

    #colorWipe(strip, Color(255, 0, 0))  # Red wipe
    #colorWipe(strip, Color(0, 255, 0))  # Green wipe    
    #colorWipe(strip, Color(0, 0, 255))  # Blue wipe    

    #time.sleep(60) # delays for 60 seconds
    
if __name__ == "__main__":
    main()
