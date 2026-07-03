import pygps2
import serial
import time

###
gps = serial.Serial('COM3', 115200, timeout=1)
###
module = pygps2.pygps2()
while True:
    raw = gps.read(16384) #
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
            analyzed_data = module.analyze(data)
gps.close()
