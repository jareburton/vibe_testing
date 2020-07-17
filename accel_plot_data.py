#!/usr/bin/env python3

import os, sys, getopt
import matplotlib.pyplot as plt
import numpy as np
import csv, math

#assign defaults
dt = 1./500
file_name = 'accel_data_default.csv'
out_name = 'accel_plot.png'

#allow user to input custom arguments
opts, args = getopt.getopt(sys.argv[1:],'hf:i:o:',['freq=','input_file=','output_file='])
for opt, arg in opts:
    if opt in ('-h'):
        print('accel_plot_data.py -f <frequency_hz> -i <input_file_csv> -o <output_file_image>')
        sys.exit(2)
    elif opt in ('-f', '--freq'):
        f = float(arg)
        dt = 1./f
    elif opt in ('-i', '--input_file'):
        file_name = str(arg)
    elif opt in ('-o', '--output_file'):
        out_name = str(arg)

#open and read file if available
if not os.path.exists(file_name):
    print('Input file does not exist, exiting.')
    sys.exit(2)
times = []
x = []
y = []
z = []
mag = []
num_readings = 0
with open(file_name) as accel_data_csv:
    csvReader = csv.reader(accel_data_csv)
    for row in csvReader:
        times.append(float(row[0]))
        ax = float(row[1])
        ay = float(row[2])
        az = float(row[3])
        x.append(ax)
        y.append(ay)
        z.append(az)
        mag.append(math.sqrt(ax**2 + ay**2 + az**2))
        num_readings += 1
print('num_readings: ' + str(num_readings))

tmin = times[0]
tmax = times[-1]

#plot accel data
ax = plt.subplot(4, 1, 1)
ax.plot(times, x)
ax.set_xticks(np.linspace(tmin, tmax, 10))

ax = plt.subplot(4, 1, 2)
ax.plot(times, y)
ax.set_xticks(np.linspace(tmin, tmax, 10))

ax = plt.subplot(4, 1, 3)
ax.plot(times, z)
ax.set_xticks(np.linspace(tmin, tmax, 10))

ax = plt.subplot(4, 1, 4)
ax.plot(times, mag)
ax.set_xticks(np.linspace(tmin, tmax, 10))

plt.savefig(out_name)
print('Plot saved at: ' + out_name)
#plt.show()

