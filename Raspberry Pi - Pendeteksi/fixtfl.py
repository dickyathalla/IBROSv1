# import library tfluna
import time
import sys
import tfli2c as tfl    # Import `tfli2c` module v0.0.1

# konfigurasi tfluna (cek i2c)
I2CPort = 1     # I2C(4), /dev/i2c-4, GPIO 8/9, pins 24/21
I2CAddr = 0x10   # Device address in Hex, Decimal 16
if( tfl.begin( I2CAddr, I2CPort)):
    print( "I2C mode: ready")
else:
    print( "I2C mode: not ready")
    sys.exit()   

def readtfl():
    time.sleep(0.047)   # Add 47ms delay for 20Hz loop-rate
    if tfl.getData():
        # Display distance in centimeters,
        print( f"Dist:{tfl.dist:{4}}cm", end= " | ")
        # display signal-strength or quality,
        print( f"Flux:{tfl.flux:{6}d}",  end= " | ")
        # and display temperature in Centigrade.
        print( f"Temp:{tfl.temp:{3}}°C",  )
        if tfl.dist>51 or tfl.dist<46:
            print('jalan bergelombang')
    else:                  # If the command fails...
        tfl.printStatus()  # display the error status
        
# set tfluna condition
tfAttempt = 0

while tfAttempt < 3:
    try:
        while True:
            readtfl()
    except KeyboardInterrupt:
        print( 'Keyboard Interrupt')
        break
    except:
        eType = sys.exc_info()[0]  #  Return exception type
        print( eType)
        tfAttempt += 1
        print( "Attempts: " + str(tfAttempt))
        time.sleep(2.0)
sys.exit()