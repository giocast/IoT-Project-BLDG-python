#import utime
#print(utime.localtime())

#from datetime import datetime
#print(date.today())

from machine import RTC

#metti in boot.py
rtc = RTC()
rtc.init((2021, 1, 13, 19, 50, 0, 0, 0))
print(rtc.now())

#prendere data da internet, settare RTC così che macchina continui da se
