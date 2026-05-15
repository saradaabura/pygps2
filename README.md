# Japanese
# pygps2
このライブラリは自由に使用してください。

![IMG_20260215_113919721 (1)](https://github.com/user-attachments/assets/5637aa1f-178d-46ff-b375-fa0fd419bc30)
# バージョン情報
https://github.com/saradaabura/pygps2/blob/master/Version.md

# 依存ライブラリ (micropython)
- micropython-decimal-number (設定により依存)

### Raspberry Pi PicoやESP32・RPi4などのMicroPython・CPython向けのGPS/NMEA解析ライブラリです。
### 通常のPythonにも対応(CPython)しているため、WindowsやLinuxなどの環境でも使用できます。
# 対応センテンス
基本的にすべてのセンテンスに対応しています。
```
GGA:$GNGGA, $GPGGA, $BDGGA
GLL:$GNGLL, $GPGLL, $BDGLL
GSA:$GNGSA, $GPGSA, $BDGSA
GSV:$GPGSV, $BDGSV, $GQGSV, $GLGSV, $GAGSV, $GBGSV
RMC:$GNRMC, $GPRMC, $BDRMC
VTG:$GNVTG, $GPVTG, $BDVTG
GST:$GNGST, $GPGST, $BDGST
ZDA:$GNZDA, $GPZDA, $BDZDA
TXT:$GNTXT, $GPTXT, $BDTXT
```

# MicroPythonでの使い方
examples/for_micropython.py環境にあったサンプルコード(Raspberry Pi Pico用)があります。Raspberry Pi Picoではそのまま使えます。ESP32ではピンを変えれば動くと思います。

MicroPythonで利用する場合、一括で解析する方法を取ったほうがいいです。
**サンプルを実行し、環境で動作を確認してからプログラムをつくることをおすすめします。**

# CPythonでの使い方
examples/for_cpython_example.pyというサンプルコード(Windows用)を使います。
**サンプルを実行し、環境で動作を確認してからプログラムを制作することをおすすめします。**
```python:main.py
import threading
import serial
import time
from pygps2 import pygps2

class GPSReader:
    def __init__(self, port="COM6", baud=460800):
        self.port = port
        self.baud = baud
        self.running = False
        self.thread = None
        self.gps = pygps2()
        self.lock = threading.Lock()
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
    def _loop(self):
        try:
            ser = serial.Serial(self.port, self.baud, timeout=1)
        except Exception as e:
            print("Serial open error:", e)
            return
        print(f"[GPSReader] Reading {self.port} @ {self.baud}")
        while self.running:
            try:
                line = ser.readline().decode(errors="ignore").strip()
                if not line:
                    continue
                with self.lock:
                    self.gps.analyze_sentence(line)
            except Exception as e:
                print("Error in GPS thread:", e)
        ser.close()
        print("[GPSReader] Stopped")
    def get(self, key):
        with self.lock:
            return getattr(self.gps, key, None)
if __name__ == "__main__":
    gps_reader = GPSReader("COM6", 460800)
    gps_reader.start()

    try:
        while True:
            rmc = gps_reader.get("RMC"); gsv = gps_reader.get("GSV")
            if rmc:
                print("Lat:", rmc["latitude"], "Lon:", rmc["longitude"])
            if gsv:
                print("GPS:", gsv["GP"]["num_satellites"] if gsv["GP"] else 0,
                      "BD:", gsv["GB"]["num_satellites"] if gsv["GB"] else 0,
                      "GA:", gsv["GA"]["num_satellites"] if gsv["GA"] else 0)

            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping...")
        gps_reader.stop()
```
Serialのポートとボーレートは環境に合わせて変更してください。

# 動作確認済み環境
- CPython (Python3.14)
- Windows 11
- Linux(Raspberry Pi Zero 2W with DietPi)
- Raspberry Pi Pico 2
- Raspberry Pi Pico 2 W
- MicroPython v1.24.1 on 2024-11-29; Raspberry Pi Pico2 with RP2350
- MicroPython v1.27.0 on 2025-12-09; Raspberry Pi Pico2 with RP2350
- MicroPython v1.28.0 on 2026-04-06; Raspberry Pi Pico 2 W with RP2350
- ESP32-DevKitC-VE ESP32-WROVER-E開発ボード 8MB
- MicroPython v1.27.0 on 2025-12-09; Generic ESP32 module with SPIRAM with ESP32
- GPSモジュール: AT6668 (M5Stack GPSモジュールv1.1)
- GPSモジュール: AT6558 (Air530Z)
- GPSモジュール: GT-505GGBL5-DR-N(秋月電子)
- ボーレート 9600,115200,460800(一括解析orCPyのみ対応)
#
- Python3 serialが使えること
- machineのuartが使えること
- NMEA0183をUARTで受信できること
# 問題
- 一括解析をする場合、チェックサムが使われない。(いつか直す...)
