# for future compatibility
from __future__ import division
from __future__ import print_function
from time import sleep, time
# for file access
import os
# for timed waits
import time

import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy import stats

class Device():

    """
    Simple usbmtc device
    """

    def __init__(self, device):
        self.FILE = open(device, 'w+', buffering=0)

    def __del__(self):
        self.FILE.close()

    def write(self, cmd):
        self.FILE.write(cmd)

    def read(self):
        return self.FILE.read()

    def query(self, cmd, timeout=0.001):
        self.write(cmd)
        time.sleep(timeout)
        return self.read()

    def reset():
        self.write("*RST")

osc=Device(device="/dev/usbtmc1")
gen=Device(device="/dev/usbtmc0")

#print(osc.query("*IDN?"))
#print(gen.query("*IDN?"))

gen.write("SOUR1:APPL:SIN 1000, 5, 2.5, 0")
gen.write("SOUR2:APPL:SIN 1000, 5, 2.5, 0")

gen.write("SOUR1:PHAS:INIT")
gen.write("SOUR2:PHAS:INIT")
gen.write("SOUR1:PHAS:SYNC")

gen.write("OUTP1:STAT ON")
gen.write("OUTP2:STAT ON")


phase=np.array(range(0, 210, 10))
average=np.zeros(len(phase))
output = file("/home/user/Desktop/PLL/12-03/SIN_PC2_3.csv","w")

for i in range(0,21,1):
	
	print ("Escribo SOUR2:PHAS "+str(10*i))
	gen.write("SOUR2:PHAS "+str(10*i))
	print ("Preg Vavg")
	average[i]=osc.query("MEAS:VAVG? CHAN1")
	print ("Joya osc")
	output.write("%f\t%f\n" % (phase[i], average[i]))
	
output.close()

#slope, intercept, r_value, p_value, std_err=stats.linregress(phase, average)
#print (slope, intercept, r_value, p_value, std_err)

plt.plot(phase, average, 'ro')
#plt.plot(phase, slope*phase+intercept, 'b-', label='Ajuste')
plt.show()

