#!/usr/bin/env python3

import time
import board, busio, adafruit_adxl34x
import os, sys, getopt
from math import ceil
import argparse

def record_accel_data(file_name='accel_data_default.csv', remove_file=False, num_readings=0, duration=0, frequency=500):
    if frequency > 500:
        print('Warning: requests to sample above 500 Hz may not be satisfied')
    if num_readings != 0 and duration != 0:
        print('Duration and number of readings cannot both be specified.')
        sys.exit(2)
    if num_readings == 0 and duration == 0:
        num_readings = 4000
    #calculate num samples according to time duration and freq
    if duration != 0:
        num_readings = ceil(duration*frequency)
    
    dt = 1.0/frequency
    
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

    #open file (and remove if necessary)
    if os.path.exists(file_name):
        if remove_file:
            print('Output file exists, removing file.')
            os.remove(file_name)
        else:
            print('Output file already exists.')
            sys.exit(2)
    f = open(file_name,'a')

    print('Capturing ' + str(num_readings) + ' samples...')
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
    f_avg = num_readings/del_t
    print('time_elapsed: ' + str(del_t))
    print('avg read freq: ' + str(f_avg))
    return (del_t, f_avg)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-r', action='store_true', help='removes output file if it exists')
    parser.add_argument('-n', '--num_samples', dest='n', type=int, default=0, help='sets number of samples')
    parser.add_argument('-t', '--time', dest='t', type=float, default=0, help='sets record duration (s)')
    parser.add_argument('-f', '--freq', dest='f', type=float, default=500.0, help='sets record frequency (Hz)')
    parser.add_argument('-o', '--output_file', dest='o', type=str, default='accel_data_default.csv', help='sets output file')
    args = parser.parse_args()

    record_accel_data(file_name=args.o, remove_file=args.r, num_readings=args.n, duration=args.t, frequency=args.f)

