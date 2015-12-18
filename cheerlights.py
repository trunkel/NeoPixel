from datetime import *
import urllib

# Setup paramters
cheerlightsUrl = "http://api.thingspeak.com/channels/1417/field/1/last.txt"

colorMap = { "red"      : 0xFF0000,
             "green"    : 0x008000,
             "blue"     : 0x0000FF,
             "cyan"     : 0x00FFFF,
             "white"    : 0xFFFFFF,
             "oldlace"  : 0xFDF5E6,
             "warmwhite": 0xFDF5E6,
             "purple"   : 0x800080,
             "magenta"  : 0xFF00FF,
             "yellow"   : 0xFFFF00,
             "orange"   : 0xFFA500,
             "pink"     : 0xFFC0CB }

class CheerLights(object):
    def __init__(self):
        self._lastUpdate = datetime.now() + timedelta(hours=-1)
        self.updateColor()

    def updateColor(self):
        current = datetime.now()
        diff = current - self._lastUpdate                   # Get time since last update

        if diff.seconds > 60:                               # Only update every 60 seconds
            self._lastUpdate = current

            cheerlights = urllib.urlopen(cheerlightsUrl)    # Open cheerlights file via URL
            colorName = cheerlights.read()                  # Read the last cheerlights color
            cheerlights.close()                             # Close cheerlights file

            if colorMap.has_key(colorName):                 # If we recognise this color name then ...
                self._current = colorMap[colorName]           # Get the color code for that name
            else:                                           # Otherwise ...
                self._current = 0                             # Use the color of black / off

    def getRed(self):
        return ((self._current >> 16) & 0xFF)

    def getGreen(self):
        return ((self._current >> 8) & 0xFF)

    def getBlue(self):
        return (self._current & 0xFF)

    def getColor(self):
        return self._current
