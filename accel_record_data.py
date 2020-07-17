#!/usr/bin/env python3

import time
import board, busio, adafruit_adxl34x
import os, sys, getopt

## Board and accel setup
i2c = busio.I2C(board.SCL, board.SDA)
# For ADXL345
accelerometer = adafruit_adxl34x.ADXL345(i2c)
accelerometer.enable_freefall_detection()
accelerometer.disable_freefall_detection()
accelerometer.enable_motion_detection()
accelerometer.disable_motion_detection()
accelerometer.enable_tap_detection()
accelerometer.disable_tap_detection()

#assign defaults
accelerometer.data_rate = adafruit_adxl34x.DataRate.RATE_400_HZ
accelerometer.range = adafruit_adxl34x.Range.RANGE_16_G
dt = 1./500
num_readings = 4000
file_name = 'accel_data_default.csv'
remove_file = False

#allow user to input custom arguments
opts, args = getopt.getopt(sys.argv[1:],'rhn:f:o:',['num_samples=','freq=','output_file='])
for opt, arg in opts:
    if opt in ('-h'):
        print('accel_record_data.py -n <num_samples> -f <frequency_hz> -o <output_file_csv>')
        sys.exit(2)
    elif opt in ('-n', '--num_samples'):
        num_readings = int(arg)
    elif opt in ('-f', '--freq'):
        f = float(arg)
        if f > 500:
            print('Warning: requests to sample above 500 Hz may not be satisfied')
        dt = 1./f
    elif opt in ('-o', '--output_file'):
        file_name = str(arg)
    elif opt in ('-r'):
        remove_file = True

#open file (and remove if necessary)
if os.path.exists(file_name):
    if remove_file:
        print('Output file exists, removing file.')
        os.remove(file_name)
    else:
        print('Output file already exists. Specify -r to remove.')
        sys.exit(2)
f = open(file_name,'a')

count = 0
bt = time.time()
temp_t = bt
while count < num_readings:
    accel = accelerometer.acceleration
    f.write('{:.16f},{:.8f},{:.8f},{:.8f}\n'.format(time.time(), accel[0], accel[1], accel[2]))
    count += 1

    new_t = temp_t + dt
    while True:
        if time.time() >= new_t:
            break
    temp_t = new_t
et = time.time()
del_t = et-bt
print('time_elapsed: ' + str(del_t))
print('avg read freq: ' + str(num_readings/del_t))

