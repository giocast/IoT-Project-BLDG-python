from network import WLAN
from mqtt import MQTTClient
import machine
import time
#from random import random
#import random

serialWipy = "000001"

def sub_cb(topic, msg):
   print(msg)

wlan = WLAN(mode=WLAN.STA)
wlan.connect("VLLC", auth=(WLAN.WPA2, "vallavlciol"), timeout=5000)

while not wlan.isconnected():
    machine.idle()
print("Connected to WiFi\n")
pycom.rgbled(0xff0000)
client = MQTTClient("wipy", "io.adafruit.com",user="bldg", password="aio_WGqg64ap2BHmSOGHt61U8Zkp9Ltd", port=1883)

client.set_callback(sub_cb)
client.connect()
client.subscribe(topic="bldg/feeds/bldgdata")



while True:
    print("Sending value")

    msg=""+serialWipy

    client.publish(topic="bldg/feeds/bldgdata", msg=msg)
    time.sleep(1)
    #print("Sending OFF")
    #client.publish(topic="bldg/feeds/bldgdata", msg="OFF")
    client.check_msg()

    time.sleep(1)
