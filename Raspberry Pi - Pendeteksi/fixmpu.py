# import library mpu9250
from mpu9250_i2c import * 


time.sleep(1) # delay necessary to allow mpu9250 to settle

def mpurun():
    ax,ay,az,wx,wy,wz = mpu6050_conv()
    time.sleep(0.0407)
    print('accel [g]: x = {0:2.2f}, y = {1:2.2f}, z {2:2.2f}= '.format(ax,ay,az))
    print('gyro [dps]:  x = {0:2.2f}, y = {1:2.2f}, z = {2:2.2f}'.format(wx,wy,wz))
    if ax>0.25 or ax<-0.25:
        if ay>0.12 or ay<-0.12:
            print('gelombang terdeteksi')
            time.sleep(0.0407)
        else:
            print('indikasi gelombang')
            time.sleep(0.0407)
    else:
        print('jalan aman')
    
while True:
    try:
        mpurun()
    except KeyboardInterrupt:
        print( 'Keyboard Interrupt')
        break
