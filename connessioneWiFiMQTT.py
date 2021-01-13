from network import WLAN
from mqtt import MQTTClient
import machine
import time
import utime

serialWipy = "000001"
#seriale della Wipy/codice univoco assegnato dai progettisti

def sub_cb(topic, msg):
   print(msg)

wlan = WLAN(mode=WLAN.STA)
wlan.connect("VLLC", auth=(WLAN.WPA2, "vallavlciol"), timeout=5000)

while not wlan.isconnected():
    machine.idle()
print("Connected to WiFi\n")
pycom.rgbled(0x00ff00)
client = MQTTClient("wipy", "io.adafruit.com",user="bldg", password="aio_WGqg64ap2BHmSOGHt61U8Zkp9Ltd", port=1883)

client.set_callback(sub_cb)
client.connect()
client.subscribe(topic="bldg/feeds/bldgdata")



while True:
    print("Sending value")

    dataInizio=utime.localtime()
    time.sleep(2) #ipotetico intervallo
    dataFine=utime.localtime()
    durataIntervallo=str(dataFine[5]-dataInizio[5])
    valoreMisurato=str(1)
    #per ogni messaggio aggiungiamo: seriale, data inizio intervallo, data fine intervallo, dimensione intervallo (in s) valore misurazione in intervallo


    msg=serialWipy+"-"+str(dataInizio)+"-"+str(dataFine)+"-"+durataIntervallo+"-"+valoreMisurato+"\n\n"
    #per ogni messaggio aggiungiamo: seriale, data inizio intervallo, data fine intervallo, dimensione intervallo (in s) valore misurazione in intervallo

    client.publish(topic="bldg/feeds/bldgdata", msg=msg)
    time.sleep(1)
    #print("Sending OFF")
    #client.publish(topic="bldg/feeds/bldgdata", msg="OFF")
    client.check_msg()

    time.sleep(1)

    print("vllc")
