# Japanese 日本語
# pygps2
このライブラリは自由に使用してください。

![IMG_20260215_113919721 (1)](https://github.com/user-attachments/assets/5637aa1f-178d-46ff-b375-fa0fd419bc30)
最初はmicropython向けに開発してたんですが、CPythonがメインになっちゃいましたね。ちゃんと目標決めないから...
# バージョン情報
https://github.com/saradaabura/pygps2/blob/master/Version.md

# 依存ライブラリ (micropython)
- micropython-decimal-number

### Raspberry Pi PicoやESP32・RPi4などのMicroPython・CPython向けのGPS/NMEA解析ライブラリです。
### 通常のPythonに対応(CPython)しているため、WindowsやLinuxなどの環境でも使用できます。
# 対応センテンス
基本的にすべてのセンテンスに対応していますが、使用する受信機に合わせてください。
特に、北斗のGSVセンテンスであるBDGSVとGBGSVは受信機によって異なるので注意してください。
```
GGA:$GNGGA, $GPGGA, $BDGGA
GLL:$GNGLL, $GPGLL, $BDGLL
GSA:$GNGSA, $GPGSA, $BDGSA
GSV:$GPGSV, $BDGSV, $GQGSV, $GLGSV, $GAGSV, $GBGSV
RMC:$GNRMC, $GPRMC, $BDRMC
VTG:$GNVTG, $GPVTG, $BDVTG
GST:$GNGST, $GPGST, $BDGST
DHV:$GNDHV, $GPDHV, $BDDHV
ZDA:$GNZDA, $GPZDA, $BDZDA
TXT:$GNTXT, $GPTXT, $BDTXT
```

# 機能
- GSVのデータを解析でき、衛星の情報を取得できます。
- GGAのデータを解析でき、緯度、経度、高度、UTC時刻、測位精度、DGPS情報を取得できます。
- RMCのデータを解析でき、UTC時刻、緯度、経度、速度、進行方向、日付、磁気偏角、磁気偏角方向を取得できます。
- RMCの解析ではLocaltimeを出力し、経度と連携した時刻を取得できます。(サマータイムや0.5時間単位での時刻の取得はできません。）

# MicroPythonでの使い方
examples/for_micropython.py環境にあったサンプルコード(Raspberry Pi Pico用)があります。
**サンプルを実行し、環境で動作を確認してからプログラムを制作することをおすすめします。**
### 問題
**3.85の時点で、Pico2やESP32などのMicroPythonの環境ではメモリリークが発生します。**
**また、NMEAを完全にパースすることができません。これは1センテンスごとに解析するプログラムによるものです。1センテンスの解析にかかる時間が長く、次のセンテンスを受信しそびれるためです。**
**MPyでは制約があります。Mpy(CPyにも)向けに解析するセンテンスを選択できるようにしたいと思います。**

<details><summary>サンプルの表示</summary>

```example.py

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

```　
</details>

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
WindowsではCOMの番号と速度をUSBシリアル変換器やRS232の設定に合わせて変更してください。
Linuxでは/dev/ttyUSB0や/dev/serial0など、環境に合わせて変更してください。

# 動作確認済み環境
- CPython (Python3.14)
- Raspberry Pi Pico 2
- MicroPython v1.24.1 on 2024-11-29; Raspberry Pi Pico2 with RP2350
- GPSモジュール: AT6668 (M5Stack GPSモジュールv1.1)
- GPSモジュール: AT6558 (Air530Z)
- GPS受信機: GT-505GGBL5-DR-N(秋月電子)

- モジュールによってはセンテンスを正しく解析できないかもしれません。NMEA 1Hzなら大丈夫だと思います...
