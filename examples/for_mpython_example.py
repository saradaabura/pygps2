import _thread
from machine import UART, Pin
import time
from pygps2 import pygps2
import gc

# GNSS parser instance
gnss = pygps2()

# UART setting
uart = UART(
    0,
    baudrate=460800,
    tx=Pin(0),
    rx=Pin(1),
    timeout=1
)
running = True
# reading...
def gps_thread():
    global running
    print("[GPS] Thread started")

    while running:
        raw = uart.readline()
        if raw:
            try:

                raw = raw.replace(b'\r', b'').replace(b'\n', b'')
                raw = raw.replace(b'/', b'')
                data = raw.decode("utf-8", "ignore")

                if data.startswith("$"):
                    #st = time.ticks_ms()
                    gnss.analyze_sentence(data)
                    #print(data)
                    #print(time.ticks_ms() - st, ",", gc.mem_free())
                    #print(gc.mem_free())

            except Exception as e:
                print("GPS thread error:", e)

    print("[GPS] Thread stopped")

# Thread starts
_thread.start_new_thread(gps_thread, ())

# MAIN LOOP
try:
    while True:
        
        rmc = gnss.GGA
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
    running = False
    time.sleep(0.5)


