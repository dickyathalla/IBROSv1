from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
from gps import *
import time

running = True

lcd = LCD(0x27)

def safe_exit(signum, frame):
    exit(1)

def getPositionData(gps):
    nx = gpsd.next()
    # For a list of all supported classes and fields refer to:
    # https://gpsd.gitlab.io/gpsd/gpsd_json.html
    if nx['class'] == 'TPV':
        latitude = getattr(nx,'lat', "Unknown")
        longitude = getattr(nx,'lon', "Unknown")
        print('Your position: lon = ' + str(longitude) + ', lat = ' + str(latitude))
        
        lcd.text("lat="+str(lat), 1)
        lcd.text("long="+str(longitude), 2)

gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

try:
    print('Application started!')
    while running:
        print("oke")
        
        getPositionData(gpsd)

        pause()

except KeyboardInterrupt:
    pass

finally:
    lcd.clear()