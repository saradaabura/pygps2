from machine import UART, Pin, I2C
import time
from pygps2 import pygps2

# GNSS parser
gnss = pygps2()

# open serial port
ser = UART(0, baudrate=460800, tx=Pin(0), rx=Pin(1))

print("[GPS] Reading COM6 @ 460800")

while True:
    try:
        raw = ser.readline()
        if raw is not None:
            try:
                raw = raw.replace(b'\r', b'').replace(b'\n', b'')
                raw = raw.replace(b'/', b'')
                data = raw.decode("utf-8", "ignore")
                del raw
            except Exception as e:
                print(f"error: {e}")
                continue
            if data.startswith("$"):
                gnss.analyze_sentence(data)

            # RMC
            rmc = gnss.RMC
            # GSV
            gsv = gnss.GSV

            if rmc:
                print("Lat:", rmc["latitude"], "Lon:", rmc["longitude"])

            if gsv:
                print(
                    "GPS:", gsv["GP"]["num_satellites"] if gsv["GP"] else 0,
                    "BD:",  gsv["GB"]["num_satellites"] if gsv["GB"] else 0,
                    "GA:",  gsv["GA"]["num_satellites"] if gsv["GA"] else 0
                )

            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping...")
        break


