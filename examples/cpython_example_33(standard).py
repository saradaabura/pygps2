import pygps2
import serial
import time

###
gps = serial.Serial('COM8', 460800, timeout=0.01)
###

while True:
    raw = gps.read(32768)#Free
    if raw is not None:
        try:
            raw = raw.replace(b'\r', b'').replace(b'\n', b'')
            raw = raw.replace(b'/', b'')
            data = raw.decode("utf-8", "ignore")
            del raw
        except Exception as e:
            print(f"error: {e}")
            continue
        if data != '':
            analyzed_data = pygps2.analyze(data)
            print(analyzed_data)
gps.close()
