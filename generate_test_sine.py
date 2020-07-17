import time
import os, sys
import numpy as np

#assign defaults
dt = 1./500
num_readings = 4000
file_name = 'accel_data_default.csv'

#open file (and remove if necessary)
if os.path.exists(file_name):
    print('Output file exists, removing file.')
    os.remove(file_name)
f = open(file_name,'a')

time = np.arange(0, dt*(num_readings), dt)
time = time + dt*np.random.random(len(time))/2

x = np.sin(2*np.pi*50*time) + np.random.random(len(time))/10
y = 10 + 0*time #np.sin(2*np.pi*100*time) + np.random.random(len(time))/10
z = 4*np.sin(2*np.pi*200*time) + np.random.random(len(time))/10

for i in range(num_readings):
    f.write('{:.16f},{:.8f},{:.8f},{:.8f}\n'.format(time[i], x[i], y[i], z[i]))


