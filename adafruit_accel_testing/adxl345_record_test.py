import time
import board
import busio
import adafruit_adxl34x

i2c = busio.I2C(board.SCL, board.SDA)

# For ADXL345
accelerometer = adafruit_adxl34x.ADXL345(i2c)
#accelerometer.disable_freefall_detection()
#accelerometer.disable_motion_detection()
#accelerometer.disable_tap_detection()
accelerometer.data_rate = adafruit_adxl34x.DataRate.RATE_1600_HZ
accelerometer.range = adafruit_adxl34x.Range.RANGE_16_G
#dt = 1./800
num_readings = 10000

f = open('sensor_data.csv','a')

bt = time.time()
for i in range(num_readings):
    accel = accelerometer.acceleration
    f.write('{:.6f},{:.6f},{:.6f}\n'.format(accel[0], accel[1], accel[2]))
    #time.sleep(dt)
et = time.time()
del_t = et-bt
print('time_elapsed: ' + str(del_t))
print('avg read freq: ' + str(num_readings/del_t))

