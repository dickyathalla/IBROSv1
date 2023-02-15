import serial
import requests
import time
import binascii
import datetime
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
            setParam2 = "at+recv_ex=1"
            if (self.commandExec(setParam2,"OK")):
                print("sukses set RSSI SNR")
            setParam2 = "at+rxc=1"
            if (self.commandExec(setParam2,"OK")):
                print("sukses set sebagai Rx")
            z = self.ser.read_until()
            while z.find(b'OK')<0:
                if z!="":
                    msg = self.decodeData(z)
                    waktuRx = datetime.datetime.now()
                    spliter = msg.split(",")
                    waktu = spliter[2]
                    waktucv = datetime.datetime.strptime(waktu,"%Y-%m-%d %H:%M:%S.%f")
                    delay = waktuRx-waktucv
                    print(delay)
                    print(msg)
                    requests.get("http://192.168.50.164:9000/data/{}".format(msg))
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


ls = loraSender()
try:
    ls.initLora()    
    ls.setFreq()
    ls.paramRadio()
    ls.setParam(1)
except Exception as e:
    print(e)
    ls.closeRx()
    ls.closeConnection()
