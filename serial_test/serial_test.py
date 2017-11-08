#!/usr/bin/python

import serial

ser = serial.Serial('/dev/ttyACM0',9600)
s= [0,1]

while True:
    read_serial=ser.readline()
#    s[0] = str(int(ser.readline(),16)) # In hexadecimal base
#    s[0] = str(int(ser.readline(),10))  # In decimal base
#    print s[0]
    print "Raw line ", read_serial

