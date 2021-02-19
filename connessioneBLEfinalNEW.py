from network import Bluetooth
import time
import struct
from funzioneConnessioneWiFiMQTTdataTransfer import inviaDati

bt = Bluetooth()
bt.start_scan(-1)


intervalloEsposizione = 0;
numeroDiMisureSingole = 0; #assumerà valori sempre maggiori se permane lo stato (es ESITO 0 o 1), se cambia viene riportata a 0 elementi
tipoDiEsitoCorrente = 0;
soglia = 5; #means che 10 secondi di intervallo minimo possono essere passati con MQTT ---> successivamente metteremo 30 (ossia un minuto)
#def char_notify_callback(char):
    #char_value = (char.value())
    #print("Got new char: {} value: {}".format(char.uuid(), char_value))




while True:
  print('Sono un while loopppp con esito di scan a ',bt.isscanning())
  adv = bt.get_adv()
  if adv and bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL) == 'BLDG Arduino Nano 33 BLE':
      while True:
          try:
              conn = bt.connect(adv.mac)
              services = conn.services()
              for service in services:
                  time.sleep(2) #attendo 2 sec per uniformarmi con i tempi di arduino
                  #if type(service.uuid()) == bytes:
                      #print('Reading chars from service = {}'.format(service.uuid()))
                  #else:
                      #print('Reading chars from service = %x' % service.uuid())

                  chars = service.characteristics()
                  i = 0 #contatore ignorante per considerare le varie caratteristiche (prima contatore, poi ESITO ESPOSIZIONE)
                  for char in chars:
                      if (char.properties() & Bluetooth.PROP_NOTIFY):
                          print("sono una caratteristica di un servizio ")
                          print(char.read())
                          #eventualmente prendere a i=0 la caratteristica e valitare valore diverso dal precedente, inutile per via della temporizzazione 2 sec (utile se problemi di arduino)
                          if (i==1):
                              #QUI SO DI LAVORARE CON LA CARATTERISTICA ESITO (0 o 1)
                              #prelevo da explode o qualcosa del genere il numero 0 o 1 dalla stringa

                              letturaEsito = char.read()
                              esitoX = struct.unpack('i', letturaEsito)
                              #->exploso = letturaEsito.split("x")
                              #->esito = exploso[1]
                              #letturaEsito = io.BytesIO(char.read())
                              #cesso = letturaEsito.read(3) #per evitare dinscartare senza variabile
                              #esito = letturaEsito.read(1)
                              print("Esito: ", esitoX[0])
                              esito = esitoX[0]
                              #valuto variabile globale numeroDiMisureSingole per vedere se formo un intervallo sulla base dei precedenti esiti pescati
                              #SI DEFINISCE UN INTERVALLO UN NUMERO DI MISURAZIONI SINGOLE (2 sec ciascuna) PARI A 10 secondi -> 5 MISURAZIONI
                              #!!!!!possibile passaggio ad 1 minuto -> 30 misurazioni
                              if (esito==tipoDiEsitoCorrente):
                                  #verifico se coincide con esito precedente
                                  #poi incremento la durata (numeroDiMisureSingole)
                                  #global numeroDiMisureSingole #per poter mpodificare il valore della var globale
                                  numeroDiMisureSingole+=1 #incremento
                              else:
                                  #vado a salvare i precedenti valori di numeroDiMisureSingole e tipoDiEsitoCorrente per salavre precedente misurazione
                                  #MA SE numeroDiMisureSingole RIUSPETTA SOGLIA (salvo solo se ho ottenuto dei periodi di esposizione di interesse)
                                  if (numeroDiMisureSingole>=soglia):
                                      durata = numeroDiMisureSingole*2 #durata di esposizione o nonn esposizione = numeor di misure fatte per 2 (durata dell'intervallino di trasmissione)
                                      print('Durata calcolata che rispetta soglia e che viene salvata:',durata) #durata sarà SEMPRE in secondi

                                      print("Inizo funz invio dati")



                                      try:
                                          inviaDati(durata,tipoDiEsitoCorrente)
                                      except Exception as e:
                                          print(e)



                                      print("Fine funz invio dati")
                                  #controllo della SOGLIA
                                  #tipoDiEsitoCorrente
                                  #!!!!!!!!!!!!!!!!!!HO DURATA e tipoDiEsitoCorrente E LI SCRIVO SU MQTT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                                  #in ogni caso vado a resettare il nuovo stato (posso avere precedentemente salvato o meno lo stato prec a seconda di SOGLIA)
                                  #global tipoDiEsitoCorrente
                                  tipoDiEsitoCorrente = esito
                                  #global numeroDiMisureSingole
                                  numeroDiMisureSingole = 1 #reinizializzazione
                          i+=1


                          #char.callback(trigger=Bluetooth.CHAR_NOTIFY_EVENT, handler=char_notify_callback, arg=None)
              #conn.disconnect()
              #break
              print("Numero misure singole, ",numeroDiMisureSingole," Esito corrente ", tipoDiEsitoCorrente)
          except:
              conn.disconnect()
#conn.disconnect()
