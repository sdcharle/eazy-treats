"""
Thai up the loose ends. (ugh)

5/24/2014 SDC

PUT these in settings.py:
RESTAURANT_ID
PRIVATE_KEY
ACCOUNT_EMAIL
ACCOUNT_PASSWORD
CC_NICK
ADDRESS 
CITY
ZIP
TRAY
FIRST_NAME
LAST_NAME
EMAIL
CURRENT_PASSWORD

"""

import threading
import ordrin
import requests
import time
from settings import *

DELIVERY_CHECK_INTERVAL = 10
CONNECTION_GOOD = False
DELIVERING = False

def checkDelivery():
    rez = False
    try:
        stuff = oapi.delivery_check('ASAP', RESTAURANT_ID, ADDRESS, CITY, ZIP)
        print stuff
        if stuff["delivery"] == 1:
            rez = True
        CONNECTION_GOOD = True
    except requests.ConnectionError:
        print "Oh snap, connection is out"
        CONNECTION_GOOD = False
    except Exception, val:
        print "Giant fail: %s val: %s" %(Exception, val)
    return rez

def deliveryCheckThread():
    while True:
        print "Check Delivery"
        DELIVERING = checkDelivery()
        if DELIVERING == True:
            print "yo they delivering"
        else:
            print "they not delivering"
        time.sleep(DELIVERY_CHECK_INTERVAL)

def checkInputs():
    while True:
        time.sleep(.2)
        print "Input checked"

def placeOrder(tray):
    rez = False
    try:
        print "yo it's order time"
    
        stuff = oapi.order_user(rid = RESTAURANT_ID, tray = tray, tip =  "3.00", first_name = FIRST_NAME,
                                last_name = LAST_NAME, email = EMAIL,
                                current_password = CURRENT_PASSWORD,
                                nick = "mehome", card_nick = "thing" , delivery_date = "ASAP") 
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