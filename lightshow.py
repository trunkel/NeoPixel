from cheerlights import *
from neopixel import *
import random
import time


# LED strip configuration:
LED_COUNT   = 150     # Number of LED pixels.
LED_PIN     = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
LED_INVERT  = False   # True to invert the signal (when using NPN transistor level shift)


def getCheerlight(colors):
    colors.updateColor()
    return colors.getColor()

def getRandomColor():
    return Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))

def clear(strip):
    """Clear all pixels"""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()

def blinkAndFade(strip, get_color, duration_s=60, min_wait_ms=50, max_wait_ms=500):
    # Set initial pixel state
    state = [random.choice(['On','Off']) for x in range(strip.numPixels())]
    countdown = [random.randint(min_wait_ms,max_wait_ms) for x in range(strip.numPixels())]

    for i in range(0, duration_s*1000, 50):
        for j in range(strip.numPixels()):
            if state[j] == 'On' or state[j] == 'Off':
                # Decrement pixel countdown value if it's on/off
                countdown[j] = max(0, countdown[j] - 50)

                if countdown[j] == 0:
                    if state[j] == 'On':
                        # Pixel is currently 'On'. Start fading to 'Off' state.
                        state[j] = 'Fade'
                    else:
                        # Pixel is currently 'Off'. Transition to 'On' state.
                        countdown[j] = random.randint(min_wait_ms, max_wait_ms)
                        state[j] = 'On'

                        # Set pixel color
                        strip.setPixelColor(j, get_color())

            if state[j] == 'Fade':
                # Get current pixel color
                color = strip.getPixelColor(j)

                # Reduce all color intensities by 8
                red   = max(0, ((color >> 16) & 0xFF) - 8)
                green = max(0, ((color >> 8) & 0xFF) - 8)
                blue  = max(0, (color & 0xFF) - 8)

                # Set new pixel color
                newColor = Color(red, green, blue)
                strip.setPixelColor(j, newColor)

                if newColor == 0:
                    # Pixel has faded to 0. Transition to 'Off' state.
                    countdown[j] = random.randint(min_wait_ms, max_wait_ms)
                    state[j] = 'Off'                    

        strip.show()
        time.sleep(50/1000.0)                    
    
def main():
    colors = CheerLights()
    colors.updateColor()

    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT)
    strip.begin()

    print 'Press Ctrl-C to quit.'
    try:
        while True:
            blinkAndFade(strip, lambda: getRandomColor())
            blinkAndFade(strip, lambda: getCheerlight(colors))

    except KeyboardInterrupt:
        clear(strip)
    
if __name__ == "__main__":
    main()
