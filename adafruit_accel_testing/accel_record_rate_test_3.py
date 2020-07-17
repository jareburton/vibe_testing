import time
import board
import busio
import adafruit_adxl34x
import os

i2c = busio.I2C(board.SCL, board.SDA)

# For ADXL345
accelerometer = adafruit_adxl34x.ADXL345(i2c)

accelerometer.enable_freefall_detection()
accelerometer.disable_freefall_detection()
accelerometer.enable_motion_detection()
accelerometer.disable_motion_detection()
accelerometer.enable_tap_detection()
accelerometer.disable_tap_detection()

accelerometer.data_rate = adafruit_adxl34x.DataRate.RATE_1600_HZ
accelerometer.range = adafruit_adxl34x.Range.RANGE_16_G
dt = 1./500
num_readings = 4000
file_name = 'sensor_data.csv'

if os.path.exists(file_name):
    os.remove(file_name)
f = open(file_name,'a')

count = 0
bt = time.time()
temp_t = bt
while count < num_readings:
    accel = accelerometer.acceleration
    f.write('{:.16f},{:.8f},{:.8f},{:.8f}\n'.format(time.time(), accel[0], accel[1], accel[2]))
    count += 1

    new_t = temp_t + dt#-0.0000045
    while True:
        if time.time() >= new_t:
            break
    temp_t = new_t
et = time.time()
del_t = et-bt
print('time_elapsed: ' + str(del_t))
print('avg read freq: ' + str(num_readings/del_t))

