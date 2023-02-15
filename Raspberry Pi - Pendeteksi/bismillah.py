# import library tfluna
import time
import sys
import tfli2c as tfl    # Import `tfli2c` module v0.0.1

# import library gps
from gps import *

# import library kamera
import cv2

# import library lcd
from rpi_lcd import LCD #lcd
from signal import signal, SIGTERM, SIGHUP, pause

# import library mpu9250
from mpu9250_i2c import *

# import library lora
import serial
import time
import datetime
import binascii

# set awal
running = True
time.sleep(1) # delay necessary to allow mpu9250 to settle
lcd = LCD(0x27)
cpt = 1

# konfigurasi tfluna (cek i2c)
I2CPort = 1     # I2C(4), /dev/i2c-4, GPIO 8/9, pins 24/21
I2CAddr = 0x10   # Device address in Hex, Decimal 16
if( tfl.begin( I2CAddr, I2CPort)):
    print( "I2C mode: ready")
else:
    print( "I2C mode: not ready")
    sys.exit()   

# def lcd
def safe_exit(signum, frame):
    exit(1)

# def gps
def getPositionData(gps):
    nx = gpsd.next()
    # For a list of all supported classes and fields refer to:
    # https://gpsd.gitlab.io/gpsd/gpsd_json.html
    if nx['class'] == 'TPV':
        latitude = getattr(nx,'lat', "Unknown")
        longitude = getattr(nx,'lon', "Unknown")
        waktuTx = datetime.datetime.now()
        #print('Your position: lon = ' + str(longitude) + ', lat = ' + str(latitude))
        semua = "{},{},{}".format(latitude,longitude,waktuTx)
        print(semua)
        ls.setParam(0,(semua))
        ls.closeTx()
        time.sleep(1)

#gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

def gpsc():
    waktuTx = datetime.datetime.now()
    latitude=-7.2769057
    longitude=112.7948995
    semua = "{},{},{}".format(latitude,longitude,waktuTx)
    print(semua)
    ls.setParam(0,(semua))
    ls.closeTx()
    time.sleep(1)
def cam():
    vidStream = cv2.VideoCapture(0) # index of your camera
    global cpt
    ret, frame = vidStream.read() # read frame and return code.
    if not ret: # if return code is bad, abort.
        sys.exit(0)
    cv2.imwrite("/home/pi/bismillah/gambar ke %03i.jpg" %cpt, frame)
    cpt += 1
    print("sukses menangkap gambar %i" %cpt)

# def mpu
def conrun():
    time.sleep(0.47)   # Add 47ms delay for 20Hz loop-rate
    ax,ay,az,wx,wy,wz = mpu6050_conv()
    #print('accel [g]: x = {0:2.2f}, y = {1:2.2f}, z {2:2.2f}= '.format(ax,ay,az))
    #print('gyro [dps]:  x = {0:2.2f}, y = {1:2.2f}, z = {2:2.2f}'.format(wx,wy,wz))
    if ax>0.2 or ax<-0.2:
        if ay>0.12 or ay<-0.12:
            if tfl.getData():
                #signal(SIGTERM, safe_exit)
                #signal(SIGHUP, safe_exit)
                # Display distance in centimeters,
                # print( f"Dist:{tfl.dist:{4}}cm", end= " | ")
                # display signal-strength or quality,
                # print( f"Flux:{tfl.flux:{6}d}",  end= " | ")
                # and display temperature in Centigrade.
                # print( f"Temp:{tfl.temp:{3}}°C",  )
                if tfl.dist>50 or tfl.dist<46:
                    signal(SIGTERM, safe_exit)
                    signal(SIGHUP, safe_exit)
                    lcd.text("Jalan", 1)
                    lcd.text("Bergelombang", 2)
                    print('jalan bergelombang')
                    #getPositionData(gpsd)
                    gpsc()
                    cam()
                    
                else:
                    signal(SIGTERM, safe_exit)
                    signal(SIGHUP, safe_exit)
                    lcd.text("Indikasi", 1)
                    lcd.text("Gelombang", 2)
                    print('indikasi gelombang')
            else:                  # If the command fails...
                tfl.printStatus()  # display the error status
        else:
            time.sleep(0.0407)
    else:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)
        lcd.text("Jalan", 1)
        lcd.text("Aman", 2)
        print('jalan aman')

# def tfl
def readtfl():
    time.sleep(0.47)   # Add 47ms delay for 20Hz loop-rate
    if tfl.getData():
        # Display distance in centimeters,
        print( f"Dist:{tfl.dist:{4}}cm", end= " | ")
        # display signal-strength or quality,
        print( f"Flux:{tfl.flux:{6}d}",  end= " | ")
        # and display temperature in Centigrade.
        print( f"Temp:{tfl.temp:{3}}°C",  )
        if tfl.dist>51 or tfl.dist<40:
            print('jalan bergelombang')
            getPositionData(gpsd)
    else:                  # If the command fails...
        tfl.printStatus()  # display the error status
        
# class loraa
class loraSender:
    def __init__(self):
        self.ser = serial.serial_for_url('/dev/serial0',115200)
        self.messageSend = None
        self.messageRecv = None    
    
    def decodeData(self,message):
        data = message.decode().strip()
        data = data.split(",")
        dataEnc = data[-1].encode()
        messageOrig = binascii.unhexlify(dataEnc).decode()
        return messageOrig

    def encodeData(self,message):
        data = message.encode()
        messageHex = binascii.hexlify(data).decode()
        return messageHex

    def commandExec(self,inputCommand,confirmMessage):
        command = "{}\r\n".format(inputCommand)
        if self.ser.isOpen():
            self.ser.write(str.encode(command))
            z = self.ser.read_until()
            while z.find(str.encode(confirmMessage))<0:
                z=self.ser.read_until()
            return 1

    def initLora(self):
        if (self.commandExec("at+reset=0","Welcome to RAK811")):
            print("sukses initialisasi")

    def setFreq(self):
        if (self.commandExec("at+mode=1","OK")):
            print("sukses set p2p")

    def paramRadio(self):
        setParam1 = "at+rf_config=867700000,10,0,1,8,14s"
        if (self.commandExec(setParam1,"OK")):
            print("sukses set Param")

    def setParam(self,radioType,message="AA"):
        if(radioType == 0):
            message = self.encodeData(message)
            setParam2 = "at+txc=1,1000,{}".format(message)
            if (self.commandExec(setParam2,"OK")):
                print("sukses mengirim pesan")            
        else:
            setParam2 = "at+rxc=1"
            if (self.commandExec(setParam2,"OK")):
                print("sukses set sebagai Rx")
            z = self.ser.read_until()
            while z.find(b'OK')<0:
                if z!="":
                    msg = self.decodeData(z)
                    print(msg)
                z=self.ser.read_until()

    def closeTx(self):
        setParam = "at+tx_stop"
        command = "{}\r\n".format(setParam)
        if self.ser.isOpen():
            self.ser.write(str.encode(command))
    def closeRx(self):
        setParam = "at+rx_stop"
        command = "{}\r\n".format(setParam)
        if self.ser.isOpen():
            self.ser.write(str.encode(command))

    def closeConnection(self):
        self.ser.close()



# set tfluna dan lora
tfAttempt = 0
ls = loraSender()
ls.initLora()    
ls.setFreq()
ls.paramRadio()

while tfAttempt < 3:
    try:
        while True:
            conrun()
            #readtfl()
    except KeyboardInterrupt:
        print( 'Keyboard Interrupt')
        ls.closeConnection()
        break
    except:
        eType = sys.exc_info()[0]  #  Return exception type
        print( eType)
        tfAttempt += 1
        print( "Attempts: " + str(tfAttempt))
        time.sleep(2.0)

ls.closeConnection()
sys.exit()
