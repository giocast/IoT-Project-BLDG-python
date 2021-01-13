from machine import RTC

#metti in boot.py
rtc = RTC()
rtc.init((2021, 1, 13, 20, 8, 0, 0, 0))
print(rtc.now())
