# Raspberry pi Pico 1/2êÍóp / Only for Raspberry Pi Pico 1/2
from machine import UART, Pin
import pygps2
import time
gps = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
while True:
    raw = gps.read(8192)
    if raw is not None:
        try:
            raw = raw.replace(b'\r', b'').replace(b'\n', b'')
            raw = raw.replace(b'/', b'')
            data = raw.decode("utf-8", "ignore")
        except Exception as e:
            print(f"error: {e}")
            print(raw)
            continue
        sentences = data.split('$')
        sentences = ['$' + sentence for sentence in sentences if sentence]
        data = '\r\n'.join(sentences) + '\r\n'
        parsed_data = pygps2.parse_nmea_sentences(data)
        analyzed_data = pygps2.analyze_nmea_data(parsed_data)
        print(analyzed_data)
    time.sleep(0.01)