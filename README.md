# pygps2
# Japanese 日本語
Raspberry Pi Pico 1/2向けのGPS解析ライブラリです。
# 機能
- GSVのデータを解析でき、衛星の情報を取得できます。(不完全)
- GGAのデータを解析でき、緯度、経度、高度、UTC時刻、測位精度、DGPS情報を取得できます。(不完全)
- RMCのデータを解析でき、UTC時刻、緯度、経度、速度、進行方向、日付、磁気偏角、磁気偏角方向を取得できます。
# 使い方
```python:main.py
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
    time.sleep(0.01) # CPU timing 各自調整 / Adjust to your CPU timing
```
詳細な使い方
1.デコードしたデータを一行でpygps2.parse_nmea_sentencesに入力する。
2.returnで返されるデータをpygps2.analyze_nmea_dataに入力する。
3.returnで戻るので変数に代入する。

動かない場合は上記のmain.pyを使ってみてください。
UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))は接続されているピンに合わせて変更してください。