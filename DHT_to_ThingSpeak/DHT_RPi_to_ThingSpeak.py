#!/usr/bin/python

import serial
import re
import urllib2
from time import sleep

ser = serial.Serial('/dev/ttyACM0',9600)
numbers= [] # Array to hold all the numbers read from sensors

myDelay = 2 # how many seconds between readings of data
            # It should be the same or multiple of that in Arduino sketch (take into account that ThingSpeak
            # minimum span between consecutive sets of data is 15 s
myAPI = "X7EGQRWP7DR5SS6K"

baseURL= 'https://api.thingspeak.com/update?api_key=%s' % myAPI
print baseURL

while True:
    try:
        str_=ser.readline()
        print str_
        numbers_str = re.findall(r"[-+]?\d*\.\d+|\d+", str_)
        numbers = [float(s) for s in numbers_str]

        # Make sure the order is properly established
        humidity = numbers[0]
        temperature = numbers[1]
        # Send values to ThingSpeak
        f= urllib2.urlopen(baseURL + "&field1=%f&field2=%f" % (humidity,temperature))
        print f.read()
        print humidity , " " , temperature , " "
        print "-----"
        f.close
        sleep(myDelay)
    except:
        print 'NOT receiving data. I will try again'
        # break

    
    

