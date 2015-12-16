from cheerlights import *
from neopixel import *
import random
import time

def getColor(colors):
    colors.updateColor()
    return Color(colors.getRed(), colors.getGreen(), colors.getBlue())

def blinkAndFade(strip, colors, duration_s=60, min_wait_ms=150, max_wait_ms=2000):
    # Set initial pixel state
    state = [random.choice(['On','Off']) for x in range(strip.numPixels())]
    countdown = [random.randint(min_wait_ms,max_wait_ms) for x in range(strip.numPixels())]

    for i in range(0, duration_s*1000, min_wait_ms):
        for j in range(strip.numPixels()):
            if state[j] == 'On' or state[j] == 'Off':
                # Decrement pixel countdown value if it's on/off
                countdown[j] = max(0, countdown[j] - min_wait_ms)

                if countdown[j] == 0:
                    if state[j] == 'On':
                        # Pixel is currently 'On'. Start fading to 'Off' state.
                        state[j] = 'Fade'
                    else:
                        # Pixel is currently 'Off'. Transition to 'On' state.
                        countdown[j] = random.randint(min_wait_ms, max_wait_ms)
                        state[j] = 'On'

                        # Set pixel color
                        strip.setPixelColor(j, getColor(colors))

            if state[j] == 'Fade':
                # Get current pixel color
                color = strip.getPixelColor(j)

                # Reduce all color intensities by 16
                red   = max(0, ((color >> 16) & 0xFF) - 16)
                green = max(0, ((color >> 8) & 0xFF) - 16)
                blue  = max(0, (color & 0xFF) - 16)

                # Set new pixel color
                newColor = Color(red, green, blue)
                strip.setPixelColor(j, newColor)

                if newColor == 0:
                    # Pixel has faded to 0. Transition to 'Off' state.
                    countdown[j] = random.randint(min_wait_ms, max_wait_ms)
                    state[j] = 'Off'                    

        strip.show()
        time.sleep(min_wait_ms/1000.0)                    
    
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

    #blinker(strip, colors)
    blinkAndFade(strip, colors)

    #colorWipe(strip, Color(255, 0, 0))  # Red wipe
    #colorWipe(strip, Color(0, 255, 0))  # Green wipe    
    #colorWipe(strip, Color(0, 0, 255))  # Blue wipe    

    #time.sleep(60) # delays for 60 seconds
    
if __name__ == "__main__":
    main()
