# ver3.1 
import pygps2
from machine import UART, Pin
import time
gps = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
while True:
    raw = gps.read(8192)
    if raw is not None:
        try:
            raw = raw.replace(b'\r', b'').replace(b'\n', b'')
            raw = raw.replace(b'/', b'')
            data = raw.decode("utf-8", "ignore")
            del raw
        except Exception as e:
            print(f"error: {e}")
            continue 
        analyzed_data = pygps2.analyze(data)
        #program here to use the analyzed_data
        del data
    time.sleep(0.01)
