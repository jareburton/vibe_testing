#!/usr/bin/env python3

import os, sys, getopt
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd

#assign defaults
dt = 1./500
file_name = 'accel_data_default.csv'
out_name = 'accel_fft_default.csv'
out_name_image = 'accel_fft_plot.png'

#allow user to input custom arguments
opts, args = getopt.getopt(sys.argv[1:],'hf:i:o:io:',['freq=','input_file=','output_file=','image_output_file='])
for opt, arg in opts:
    if opt in ('-h'):
        print('accel_fft.py -f <frequency_hz> -i <input_file_csv> -o <output_file_csv> -io <output_file_image>')
        sys.exit(2)
    elif opt in ('-f', '--freq'):
        f = float(arg)
        dt = 1./f
    elif opt in ('-i', '--input_file'):
        file_name = str(arg)
    elif opt in ('-o', '--output_file'):
        out_name = str(arg)
    elif opt in ('-io', '--image_output_file'):
        out_name_image = str(arg)

#open and read file if available
if not os.path.exists(file_name):
    print('Input file does not exist, exiting.')
    sys.exit(2)
times = []
x = []
y = []
z = []
num_readings = 0
with open(file_name) as accel_data_csv:
    csvReader = csv.reader(accel_data_csv)
    for row in csvReader:
        times.append(float(row[0]))
        x.append(float(row[1]))
        y.append(float(row[2]))
        z.append(float(row[3]))
        num_readings += 1
print('num_readings: ' + str(num_readings))

# compute fft
fft_x = np.fft.rfft(x)*2/num_readings
fft_y = np.fft.rfft(y)*2/num_readings
fft_z = np.fft.rfft(z)*2/num_readings
fft_x[0] = fft_x[0]/2
fft_y[0] = fft_y[0]/2
fft_z[0] = fft_z[0]/2

fft_x_mag = np.absolute(fft_x)
fft_y_mag = np.absolute(fft_y)
fft_z_mag = np.absolute(fft_z)

fs = np.fft.rfftfreq(num_readings, dt)
df = fs[1]-fs[0]

psd_x = np.square(fft_x_mag)/(2*df)
psd_y = np.square(fft_y_mag)/(2*df)
psd_z = np.square(fft_z_mag)/(2*df)
psd_x[0] = 0
psd_y[0] = 0
psd_z[0] = 0

#put data in dataframe and save to csv
df = pd.DataFrame({'fs':fs, 'fft_x_mag':fft_x_mag, 'fft_y_mag':fft_y_mag, 'fft_z_mag':fft_z_mag, 'psd_x':psd_x, 'psd_y':psd_y, 'psd_z':psd_z})
df.to_csv(out_name, index=False)
print('FFT output saved at: ' + out_name)

fmin = fs[0]
fmax = fs[-1]

#plot accel data
ax = plt.subplot(6, 1, 1)
ax.plot(fs, fft_x_mag)
ax.grid()
plt.xlabel('Freq (Hz)')
plt.ylabel('Accel x (m.s^-2)')
plt.title('Acceleration x fft')
ax.set_xticks(np.linspace(fmin, fmax, 10))

ax = plt.subplot(6, 1, 2)
ax.plot(fs, fft_y_mag)
ax.grid()
plt.xlabel('Freq (Hz)')
plt.ylabel('Accel y (m.s^-2)')
plt.title('Acceleration y fft')
ax.set_xticks(np.linspace(fmin, fmax, 10))

ax = plt.subplot(6, 1, 3)
ax.plot(fs, fft_z_mag)
ax.grid()
plt.xlabel('Freq (Hz)')
plt.ylabel('Accel z (m.s^-2)')
plt.title('Acceleration z fft')
ax.set_xticks(np.linspace(fmin, fmax, 10))

ax = plt.subplot(6, 1, 4)
ax.plot(fs, psd_x)
ax.grid()
plt.xlabel('Freq (Hz)')
plt.ylabel('Accel x (m^2.s^-4.Hz^-1)')
plt.title('Acceleration x PSD w/ mean removed')
ax.set_xticks(np.linspace(fmin, fmax, 10))

ax = plt.subplot(6, 1, 5)
ax.plot(fs, psd_y)
ax.grid()
plt.xlabel('Freq (Hz)')
plt.ylabel('Accel y (m^2.s^-4.Hz^-1)')
plt.title('Acceleration y PSD w/ mean removed')
ax.set_xticks(np.linspace(fmin, fmax, 10))

ax = plt.subplot(6, 1, 6)
ax.plot(fs, psd_z)
ax.grid()
plt.xlabel('Freq (Hz)')
plt.ylabel('Accel z (m^2.s^-4.Hz^-1)')
plt.title('Acceleration z PSD w/ mean removed')
ax.set_xticks(np.linspace(fmin, fmax, 10))

plt.savefig(out_name_image)
print('Plot saved at: ' + out_name_image)
#plt.show()

