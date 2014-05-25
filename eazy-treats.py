"""
Thai up the loose ends. (ugh)

5/24/2014 SDC

"""

import threading
import ordrin
import requests
import time

# meny/qty,opt opt opt
TRAY = "4508321/1+4508589/1,4508591"
# pad kee mao chicken, chicken satay
# 4508515/1,4508517
# musman
# 4508589/1,4508591

RESTAURANT_ID = '10399'
PRIVATE_KEY = 'bllpr4xR0YE1ARqU99uSMBv6_hvupEammAX3NKuSKj0'
ACCOUNT_EMAIL = 'mistasteve@gmail.com'
ACCOUNT_PASSWORD = 'mepassword'
# question, these accounts are specific to me/my key, right?
CC_NICK = 'hackcard'

DELIVERY_CHECK_INTERVAL = 10
CONNECTION_GOOD = False
DELIVERING = False

def checkDelivery():
    rez = False
    try:
        stuff = oapi.delivery_check('ASAP',RESTAURANT_ID,'3856 S Millstone Way','Bloomington','47401')
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
    
        stuff = oapi.order_user(rid = RESTAURANT_ID, tray = tray, tip =  "3.00", first_name = "Steve",
                                last_name = "Charlesworth", email = "mistasteve@gmail.com",
                                current_password = "mepassword",
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

"""
other notes



"""

if __name__ == "__main__":
    oapi = ordrin.APIs(PRIVATE_KEY, ordrin.TEST)

    t = threading.Thread(target=deliveryCheckThread, args = ())
    u = threading.Thread(target=checkInputs, args = ())
    t.start()
    u.start()
    
    