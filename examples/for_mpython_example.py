# 3,92と互換性あり。
import _thread
from machine import UART, Pin
import time
from pygps2 import pygps2
import gc

# machine.freq(285_000_000)
#For RPi Pico2

# GNSS parser instance
gnss = pygps2(op4=False, op5=False)

# UART setting
uart = UART(
    0,
    baudrate=115200,
    tx=Pin(0),
    rx=Pin(1),
    timeout=1
)
running = True
# reading...
def gps_thread():
    global running; global gnss
    print("[GPS] Thread started")

    while running:
        raw = uart.readline()
        if raw:
            try:

                raw = raw.replace(b'\r', b'').replace(b'\n', b'')
                raw = raw.replace(b'/', b'')
                data = raw.decode("utf-8", "ignore")

                if data.startswith("$"):
                    st = time.ticks_ms()
                    print(data)
                    gnss.analyze_sentence(data, en_gsv=True, en_gsa=True)
                    #print(gnss.GSV)
                    print(time.ticks_ms() - st, ",", gc.mem_free())
                    #print(gc.mem_free())

            except Exception as e:
                print("GPS thread error:", e)

    print("[GPS] Thread stopped")

# Thread starts
_thread.start_new_thread(gps_thread, ())

# MAIN LOOP
try:
    while True:
        rmc = gnss.RMC
        gsv = gnss.GSV
        if rmc:
            print("Lat:", rmc["latitude"], "Lon:", rmc["longitude"])

        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping...")
    running = False
    time.sleep(0.5)