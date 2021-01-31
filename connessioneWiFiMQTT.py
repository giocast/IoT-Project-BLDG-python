from network import WLAN
from mqtt import MQTTClient
import machine
import time
import utime

idKit = "000001"
#seriale Kit/codice univoco assegnato dai progettisti

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
    #imp diff tra (tuple) e [list] -> posso accedere a tuple con tupla[2] ma non a lista (lista si append)
    dataInizio=utime.localtime()
    time.sleep(2) #ipotetico intervallo
    dataFine=utime.localtime()
    durataInt=[(dataFine[0]-dataInizio[0]),(dataFine[1]-dataInizio[1]),(dataFine[2]-dataInizio[2]),(dataFine[3]-dataInizio[3]),(dataFine[4]-dataInizio[4]),(dataFine[5]-dataInizio[5])]
    #durataInt.append(dataFine[0]-dataInizio[0])
    #durataInt.append(dataFine[1]-dataInizio[1])

    #for per scandire
    # se prendo elemento !=0 devo moltiplicare per ottenere il valore in secondi

    #for elemento in durataInt:
    #    if elemento != 0:
    length = len(durataInt)
    i = 0
    sommaPeriodoSecondi = 0

    while i < length:
        if durataInt[i] != 0:

            if i == 3:
                #ora
                print("prova3")
                sommaPeriodoSecondi += durataInt[i]*3600
            elif i == 4:
                #min
                print("prova4")
                sommaPeriodoSecondi += durataInt[i]*60
            elif i == 5:
                #sec
                print("prova5")
                sommaPeriodoSecondi += durataInt[i]
            else:
                print("else")
        i += 1

    durataIntervallo=str(sommaPeriodoSecondi)
    valoreMisurato=str(1)
    #per ogni messaggio aggiungiamo: seriale, data inizio intervallo, data fine intervallo, dimensione intervallo (in s) valore misurazione in intervallo


    msg=idKit+"-"+str(dataInizio)+"-"+str(dataFine)+"-"+durataIntervallo+"-"+valoreMisurato+"\n\n"
    #per ogni messaggio aggiungiamo: seriale, data inizio intervallo, data fine intervallo, dimensione intervallo (in s) valore misurazione in intervallo

    client.publish(topic="bldg/feeds/bldgdata", msg=msg)
    time.sleep(1)
    #print("Sending OFF")
    #client.publish(topic="bldg/feeds/bldgdata", msg="OFF")
    client.check_msg()

    time.sleep(1)
