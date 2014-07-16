"""
Thai up the loose ends. (ugh)

5/24/2014 SDC

PUT these in settings.py:
RESTAURANT_ID
PRIVATE_KEY
CARD_NICK
ADDR_NICK
ADDRESS 
CITY
ZIP
TRAY
FIRST_NAME
LAST_NAME
EMAIL
CURRENT_PASSWORD

My most excellent food delivery panel
SDC 5/22/2014

LEDs
Power (obvious)
CONNECTION = 3 = GPIO27
Delivering = 2 = GPIO17

5/26/2014 SDC
Basics in place. need to give thought to what do do if delivery fails. And either way, do we just stop accepting
orders after success, and for how long?

7/15/2014 SDC 
geez man for a long time the ordr.in API just wasn't doing it.
but today, seems OK!

"""

import RPi.GPIO as GPIO
import threading
import ordrin
import requests
import time
from settings import *

# Use GPIO numbers not pin numbers
GPIO.setmode(GPIO.BCM)

CONNECTION_LED = 27
DELIVERING_LED = 17
BUTTON = 23 
DELIVERY_CHECK_INTERVAL = 10
CONNECTION_GOOD = False
DELIVERING = False

# set up the GPIO channels - one input and one output
GPIO.setup(CONNECTION_LED, GPIO.OUT)
GPIO.setup(DELIVERING_LED, GPIO.OUT)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def connectionState(state):
    global CONNECTION_GOOD # hm.
    if (state != CONNECTION_GOOD):
        GPIO.output(CONNECTION_LED,state)
        CONNECTION_GOOD = state

def deliveryState(state):
    global DELIVERING
    if state != DELIVERING:
        GPIO.output(DELIVERING_LED, state)
        DELIVERING = state  

def checkDelivery():
    rez = False
    try:
        stuff = oapi.delivery_check('ASAP', RESTAURANT_ID, ADDRESS, CITY, ZIP)
        print stuff
        if stuff["delivery"] == 1:
            rez = True
        connectionState(True)       
    except requests.ConnectionError:
        print "Oh snap, connection is out"
        connectionState(False)
    except Exception, val:
        print "Giant fail: %s val: %s" %(Exception, val)
    deliveryState(rez)
    return rez

def deliveryCheckThread():
    while True:
        print "Check Delivery"
        checkDelivery()
        time.sleep(DELIVERY_CHECK_INTERVAL)
        
"""
just see if  button
what to do if order bad though????
"""

def checkInputs():
    while True:
        time.sleep(.2)
        if DELIVERING and not GPIO.input(BUTTON):
            if placeOrder(TRAY):
                orderGood()
            else:
                orderBad()

def orderGood():
    # little flashy
    for i in range(10):
        GPIO.output(DELIVERING_LED, False)        
        time.sleep(.1)
        GPIO.output(DELIVERING_LED, True)        
        time.sleep(.1)
    time.sleep(10) # wait at least 10 seconds. better would be just turn off delivering for at least a couple hours!

# need something better from a UI standpoint to indicate fails.

def orderBad():
    for i in range(3):
        GPIO.output(DELIVERING_LED, False)        
        time.sleep(.4)
        GPIO.output(DELIVERING_LED, True)        
        time.sleep(.4)
    GPIO.output(DELIVERING_LED,False)
    time.sleep(10) 

def placeOrder(tray):
    rez = False
    GPIO.output(DELIVERING_LED, False)        
    try:
        print "yo it's order time"
        print "TRAY: %s RESTAURANT_ID: %s" %(tray, RESTAURANT_ID) 
        stuff = oapi.order_user(rid = RESTAURANT_ID, tray = tray, tip =  "3.00", first_name = FIRST_NAME,
                                last_name = LAST_NAME, email = EMAIL,
                                current_password = CURRENT_PASSWORD,
                                nick = ADDR_NICK, card_nick = CARD_NICK , delivery_date = "ASAP") 
        print stuff        
        if stuff["msg"] == "Success":
            print "yo you a winner."
            rez = True            
    except requests.ConnectionError:
        print "Oh snap, bad connection"
        CONNECTION_GOOD = False
    except Exception, val:
        print "Giant fail: %s val: %s" %(Exception, val)
    return rez

if __name__ == "__main__":
    oapi = ordrin.APIs(PRIVATE_KEY, ordrin.TEST)

    t = threading.Thread(target=deliveryCheckThread, args = ())
    u = threading.Thread(target=checkInputs, args = ())
    t.start()
    u.start()   
