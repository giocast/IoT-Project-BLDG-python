import pycom
import time
from network import WLAN
import machine

pycom.heartbeat(False)

wlan = WLAN(mode=WLAN.STA)

wlan.connect(ssid='VLLC', auth=(WLAN.WPA2, 'vallavlciol'))
while not wlan.isconnected():
    machine.idle()
print("WiFi connected succesfully")
pycom.rgbled(0xff0000)
print(wlan.ifconfig())

#genero numeri, li pongo in buffer...nel frattempo un altro script prende dati da buffer (li toglie) e li trasmette
#genero data misurazione
#definisco l'intervallo
