#!/usr/bin/python

import serial
import re
import urllib, urllib2
from time import sleep

#Setup the serial connection
ser = serial.Serial('/dev/ttyACM0',9600)
numbers= [] # Array to hold all the numbers read from sensors

# ThingSpeak setup
myDelay = 2 # how many seconds between readings of data
            # It should be the same or multiple of that in Arduino sketch (take into account that ThingSpeak
            # minimum span between consecutive sets of data is 15 s
myAPI = "X7EGQRWP7DR5SS6K"
baseURL= 'https://api.thingspeak.com/update?api_key=%s' % myAPI
print baseURL

# ThingTweet setup
MAX_TEMP = 20.0 # Temperature limit. Above this value, notification is posted to Twitter
BASE_URL = 'https://api.thingspeak.com/apps/thingtweet/1/statuses/update/'
KEY = '68LZC4LBMXLO6YDY' # This is the API key of your channel for posting to Twitter

def send_notification(temp): # Function that post a tweet when called from the main loop
    status = 'Temperatura de alarma =' + str(temp)
    data = urllib.urlencode({'api_key' : KEY, 'status': status})
    response = urllib2.urlopen(url=BASE_URL, data=data)
    print(response.read())

while True:
    try:
        str_=ser.readline() #Read a line from Arduino through the serial port
        print str_
        numbers_str = re.findall(r"[-+]?\d*\.\d+|\d+", str_) # Extract the numeric values and remove the text
        numbers = [float(s) for s in numbers_str] # Convert values (they are strings of characters) to float type numbers

        # Make sure the order is properly established
        humidity = numbers[0]
        temperature = numbers[1]
        # Send values to ThingSpeak
        f= urllib2.urlopen(baseURL + "&field1=%f&field2=%f" % (humidity,temperature))
        print f.read() # This post the data to ThingSpeak
        print humidity , " " , temperature , " "
        print "-----"
		if temperature > MAX_TEMP:  # Condition on temperature, above which it is reported to Twitter channel
				send_notification(temperature)
        f.close # Close the connection to ThingSpeak
        sleep(myDelay)
    except:
        print 'NOT receiving data. I will try again'
        # break

    
    

