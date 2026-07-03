import pygps2
from machine import UART, Pin
import time

#ESP32
gps = UART(2, baudrate=460800, tx=Pin(2), rx=Pin(15))

#For Pico
#gps = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

module = pygps2.pygps2()

while True:
    raw = gps.read(32768) #
    if raw is not None:
        try:
            raw = raw.replace(b'\r', b'').replace(b'\n', b'')
            raw = raw.replace(b'/', b'')
            data = raw.decode("utf-8", "ignore")
            del raw
        except Exception as e:
            print(f"error: {e}")
            continue
        if data != '' or data != None:
            module.analyze(data)
            print(data)
            if module.GGA != None:
                if module.GGA["latitude"] != None and module.GGA["longitude"] != None:
                    print(f"LA:{module.GGA["latitude"]}")
                    print(f"LO:{module.GGA["longitude"]}")
            """
            if module.GGA != None and module.GGA != []:
              if module.GGA["latitude"] != None and module.GGA["longitude"] != None:
                    print(f"LA:{module.GGA["latitude"]}")
                    print(f"LO:{module.GGA["longitude"]}")
            """
