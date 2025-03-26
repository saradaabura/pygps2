import pygps2
from machine import UART, Pin
gps = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
analyzed_data = pygps2.init()
while True:
    raw = gps.read(192)
    if raw is not None:
        try:
            raw = raw.replace(b'\r', b'').replace(b'\n', b'')
            raw = raw.replace(b'/', b'')
            data = raw.decode("utf-8", "ignore")
            del raw
        except Exception as e:
            print(f"error: {e}")
            continue
        analyzed_data = pygps2.analyze(data, oldata=analyzed_data)
