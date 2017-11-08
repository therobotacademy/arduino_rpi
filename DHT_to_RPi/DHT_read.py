#!/usr/bin/python

import serial
import re

ser = serial.Serial('/dev/ttyACM0',9600)
numbers= [0,10] # Array to hold all the numbers read from sensors
                # Increase the size if you have more than 10

while True:
    str=ser.readline()
    print str
    numbers_str = re.findall(r"[-+]?\d*\.\d+|\d+", str)
    numbers = [float(s) for s in numbers_str]
    print numbers
    print "-----"

