from network import WLAN
from mqtt import MQTTClient
import machine
import time
import utime
import pycom
import math







def inviaDati(durataIntervallo,valoreMisurato):

    def sub_cb(topic, msg):
       print(msg)

    #seriale della Wipy/codice univoco assegnato dai progettisti
    serialWipy = "000001"
    print("INIZIO INVIO DATI")

    wlan = WLAN(mode=WLAN.STA)
    wlan.connect("VLLC", auth=(WLAN.WPA2, "vallavlciol"), timeout=5000)

    while not wlan.isconnected():
        machine.idle()
    print("Connected to WiFi\n")

    #CODICE GET DATA GIUSTA ITA
    rtc = machine.RTC()
    rtc.ntp_sync("it.pool.ntp.org")
    utime.sleep_ms(750)
    #print('\nRTC Set from NTP to UTC:', rtc.now())
    oraItalia = rtc.now()

    mese = oraItalia[1]

    if(mese >= 11 or mese <= 3):
        oraDaModificare = oraItalia[3]+1
        oraItalia = [oraItalia[0],oraItalia[1],oraItalia[2],oraDaModificare,oraItalia[4],oraItalia[5],oraItalia[6],oraItalia[7]]

    print("Ora esatta ", oraItalia)
    #FINE CODICE DATA ITA


    #pycom.rgbled(0x00ff00)
    client = MQTTClient("wipy", "io.adafruit.com",user="bldg", password="aio_WGqg64ap2BHmSOGHt61U8Zkp9Ltd", port=1883)

    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic="bldg/feeds/bldgdata")




    print("Sending value")
        #imp diff tra (tuple) e [list] -> posso accedere a tuple con tupla[2] ma non a lista (lista si append)

    #CI CALCOLIAMO DATA INIZIO A PARTIRE DA durataIntervallo IN SECONDI e dataFine
    #ESEMPIO IF 4680 sec -> 78min -> è intero-> calcolo le ore perchè >60 -> 78/60 = 1,3 = 1 ora -> calcolo i minuti 78-60*1 = 18 minuti -> calcolo i secondi 4680-18*60-3600*1 = 0 secondi come previsto
    #ESEMPIO ELSE 3125 sec -> 3125/60 = 52,0833333333 = 52 minuti -> minore di 60, calcolo i secondi -> 3125-60*52 ? 5 secondi
    numeroOre = 0
    numeroSecondi = 0

    numeroMinuti = durataIntervallo/60
    interoNumeroMinuti = int(numeroMinuti)

    if(interoNumeroMinuti>=60):
        numeroOre = int(interoNumeroMinuti/60)
        numeroMinuti = interoNumeroMinuti-(60*numeroOre)
        numeroSecondi = durataIntervallo-60*numeroMinuti-3600*numeroOre
    else:
        if (interoNumeroMinuti==0):
            numeroMinuti = 0
            numeroOre = 0 #hai minuti minori di 60
            numeroSecondi = durataIntervallo
        else:
            numeroOre = 0
            numeroMinuti = interoNumeroMinuti
            numeroSecondi = durataIntervallo-(60*interoNumeroMinuti)


    dataFine=oraItalia #ho QUESTO, HO DURATA DA ALTRO SCRIPT E CALCOLO DATA INIZIO sottraendo A DATA FINE la DURATA

    secondiInizio = dataFine[5]-numeroSecondi
    minutiInizio = dataFine[4]-numeroMinuti
    oreInizio = dataFine[3]-numeroOre

    #controlli per evitare anomalie (es swcondi negativi) -> se trovo nidificati dei negativi, scalo tutte e tre le variabili

    if (secondiInizio<0):
        secondiInizio = 60+secondiInizio #sottrazione
        minutiInizio = minutiInizio-1
        if (minutiInizio<0):
            oreInizio = oreInizio-1
            minutiInizio = 60+minutiInizio
            #if (oreInizio < 0):
                #evito per il momento questa condizione


    dataInizio=[(dataFine[0]-0),(dataFine[1]-0),(dataFine[2]-0),oreInizio,minutiInizio,secondiInizio,0,None]



    msg=serialWipy+"-"+str(dataInizio)+"-"+str(dataFine)+"-"+str(durataIntervallo)+"-"+str(valoreMisurato)+"\n\n"
        #per ogni messaggio aggiungiamo: seriale, data inizio intervallo, data fine intervallo, dimensione intervallo (in s) valore misurazione in intervallo
    print(msg)
    client.publish(topic="bldg/feeds/bldgdata", msg=msg)
    time.sleep(1)
        #print("Sending OFF")
        #client.publish(topic="bldg/feeds/bldgdata", msg="OFF")
    client.check_msg()
    print("FINE INVIO DATI")
