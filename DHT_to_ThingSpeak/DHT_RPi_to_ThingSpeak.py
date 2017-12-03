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
myAPI = "X7EGQRWP7DR5SS6K" # This is the API key of your channel in ThingSpeak

baseURL= 'https://api.thingspeak.com/update?api_key=%s' % myAPI  # To this URL will be added the values of the readings of the sensors
print baseURL

while True:
    try:
        str_=ser.readline() #Read a line from Arduino through the serial port
        print str_
        numbers_str = re.findall(r"[-+]?\d*\.\d+|\d+", str_) # Extract the numeric values and remove the text
        numbers = [float(s) for s in numbers_str] # Convert values (they are strings of characters) to float type numbers

        # Make sure the order of the values of the sensors is properly established
        humidity = numbers[0]
        temperature = numbers[1]
        # Send values to ThingSpeak
        f= urllib2.urlopen(baseURL + "&field1=%f&field2=%f" % (humidity,temperature))
        print f.read() # This post the data to ThingSpeak
        print humidity , " " , temperature , " "   # This prints the value in the local console for checking by user 
        print "-----"
        f.close  # Close the connection to ThingSpeak
        sleep(myDelay) # Wait until the next reading event
    except:
        print 'NOT receiving data. I will try again'
        # break

    
    

