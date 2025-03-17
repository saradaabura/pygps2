# pygps2
# バージョン情報

2.0 作成

2.1 GSV解析に対し、衛星の種類を取得できるように変更

2.2 衛星のデュアルバンドによるカウント重複の解消

2.3 GST解析関数追加

2.4 RMCに経度から計算したローカル時刻を追加

# Japanese 日本語
Raspberry Pi Pico 1/2向けのGPS解析ライブラリです。
# 機能
- GSVのデータを解析でき、衛星の情報を取得できます。(不完全)
- GGAのデータを解析でき、緯度、経度、高度、UTC時刻、測位精度、DGPS情報を取得できます。(不完全)
- RMCのデータを解析でき、UTC時刻、緯度、経度、速度、進行方向、日付、磁気偏角、磁気偏角方向を取得できます。
- RMC関数ではLocaltimeの出力できます
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
# 詳細な使い方
1.デコードしたデータを一行でpygps2.parse_nmea_sentencesに入力する。

2.returnで返されるデータをpygps2.analyze_nmea_dataに入力する。

3.returnで戻るので変数に代入する。

動かない場合は上記のmain.pyを使ってみてください。

UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))は接続されているピンに合わせて変更してください。
# サンプル
出力されるデータの例(analyze_nmea_dataが返す)
```python
{'GSA': [{'hdop': '0.6', 'vdop': '0.8', 'mode2': '3', 'satellites_used': {'snr': '26', 'prn': '14', 'elevation': '24', 'azimuth': '181'}, {'snr': '34', 'prn': '24', 'elevation': '48', 'azimuth': '052'}, {'snr': '23', 'prn': '25', 'elevation': '62', 'azimuth': '296'}, {'snr': '42', 'prn': '33', 'elevation': '43', 'azimuth': '203'}, {'snr': '10', 'prn': '35', 'elevation': '08', 'azimuth': '043'}, {'snr': '37', 'prn': '38', 'elevation': '14', 'azimuth': '213'}, {'snr': '23', 'prn': '40', 'elevation': '14', 'azimuth': '187'}, {'snr': '38', 'prn': '44', 'elevation': '22', 'azimuth': '086'}, {'snr': '38', 'prn': '59', 'elevation': '46', 'azimuth': '181'}, {'snr': '43', 'prn': '33', 'elevation': '43', 'azimuth': '203'}, {'snr': '25', 'prn': '35', 'elevation': '08', 'azimuth': '043'}, {'snr': '39', 'prn': '44', 'elevation': '22', 'azimuth': '086'}, {'snr': '42', 'prn': '02', 'elevation': '66', 'azimuth': '174'}, {'snr': '38', 'prn': '04', 'elevation': '51', 'azimuth': '201'}, {'snr': '36', 'prn': '07', 'elevation': '44', 'azimuth': '202'}], 'message_num': '1'}], 'GGA': [{'gps_quality': '1', 'hdop': '0.6', 'altitude': '62.75', 'geoid_units': 'M', 'dgps_station_id': '', 'geoid_height': '36.37', 'dgps_age': '', 'altitude_units': 'M', 'num_satellites': '30', 'latitude': 0.0, 'longitude': 0.0, 'timestamp': '211311.00'}], 'RMC': [{'longitude': 0.0, 'latitude': 0.0, 'course_over_ground': '0.0', 'status': 'A', 'mag_var_direction': '', 'magnetic_variation': '0.0', 'mode_indicator': 'A', 'timestamp': '211311.00', 'speed_over_ground': '0.27', 'date': '120325'}], 'GLL': [{'longitude': 0.0, 'latitude': 0.0, 'timestamp': '211311.00', 'status': 'A', 'mode_indicator': 'A'}], 'VTG': [{'reference_t': 'T', 'mode_indicator': 'A', 'speed_kmh': '0.50', 'course_over_ground_m': '0.0', 'reference_m': 'M', 'speed_knots': '0.27', 'units_knots': 'N', 'units_kmh': 'K', 'course_over_ground_t': '0.0'}]}
```
# 動作確認済み環境
- Raspberry Pi Pico 2
- MicroPython v1.24.1 on 2024-11-29; Raspberry Pi Pico2 with RP2350
- GPSモジュール: AT6668 (M5Stack GPSモジュールv1.1)
- GPSモジュール: AT6558 (Air530Z)
モジュールによっては動作しないかもしれません。その場合出力データを載せてissueを立ててください。
# English 英語
I use Google Translate, so there may be some strange sentences.

A GPS analysis library for Raspberry Pi Pico 1/2.
# Functions
- Can analyze GSV data and obtain satellite information. (Incomplete)
- Can analyze GGA data and obtain latitude, longitude, altitude, UTC time, positioning accuracy, and DGPS information. (Incomplete)
- Can analyze RMC data and obtain UTC time, latitude, longitude, speed, heading, date, magnetic declination, and magnetic declination direction.
# How to use
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
 data = '\r\n'.join(sentences) + '\r\n' parsed_data = pygps2.parse_nmea_sentences(data)
analyzed_data = pygps2.analyze_nmea_data(parsed_data)
print(analyzed_data)
time.sleep(0.01) # CPU timing Adjust to your CPU timing
```
# Detailed usage
1. Enter the decoded data in one line into pygps2.parse_nmea_sentences.
1. 
2. Enter the data returned by return into pygps2.analyze_nmea_data.
1. 
3. Assign the data to a variable when it returns with return.

If it doesn't work, try using the main.py above.

Change UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1)) to match the connected pins.
# Sample
Example of output data (returned by analyze_nmea_data)
```python
{'GSA': [{'hdop': '0.6', 'vdop': '0.8', 'mode2': '3', 'satellites_used': {'snr': '26', 'prn': '14', 'elevation': '24', 'azimuth': '181'}, {'snr': '34', 'prn': '24', 'elevation': '48', 'azimuth': '052'}, {'snr': '23', 'prn': '25', 'elevation': '62', 'azimuth': '296'}, {'snr': '42', 'prn': '33', 'elevation': '43', 'azimuth': '203'}, {'snr': '10', 'prn': '35', 'elevation': '08', 'azimuth': '043'}, {'snr': '37', 'prn': '38', 'elevation': '14', 'azimuth': '213'}, {'snr': '23', 'prn': '40', 'elevation': '14', 'azimuth': '187'}, {'snr': '38', 'prn': '44', 'elevation': '22', 'azimuth': '086'}, {'snr': '38', 'prn': '59', 'elevation': '46', 'azimuth': '181'}, {'snr': '43', 'prn': '33', 'elevation': '43', 'azimuth': '203'}, {'snr': '25', 'prn': '35', 'elevation': '08', 'azimuth': '043'}, {'snr': '39', 'prn': '44', 'elevation': '22', 'azimuth': '086'}, {'snr': '42', 'prn': '02', 'elevation': '66', 'azimuth': '174'}, {'snr': '38', 'prn': '04', 'elevation': '51', 'azimuth': '201'}, {'snr': '36', 'prn': '07', 'elevation': '44', 'azimuth': '202'}], 'message_num': '1'}], 'GGA': [{'gps_quality': '1', 'hdop': '0.6', 'altitude': '62.75', 'geoid_units': 'M', 'dgps_station_id': '', 'geoid_height': '36.37', 'dgps_age': '', 'altitude_units': 'M', 'num_satellites': '30', 'latitude': 0.0, 'longitude': 0.0, 'timestamp': '211311.00'}], 'RMC': [{'longitude': 0.0, 'latitude': 0.0, 'course_over_ground': '0.0', 'status': 'A', 'mag_var_direction': '', 'magnetic_variation': '0.0', 'mode_indicator': 'A', 'timestamp': '211311.00', 'speed_over_ground': '0.27', 'date': '120325'}], 'GLL': [{'longitude': 0.0, 'latitude': 0.0, 'timestamp': '211311.00', 'status': 'A', 'mode_indicator': 'A'}], 'VTG': [{'reference_t': 'T', 'mode_indicator': 'A', 'speed_kmh': '0.50', 'course_over_ground_m': '0.0', 'reference_m': 'M', 'speed_knots': '0.27', 'units_knots': 'N', 'units_kmh': 'K', 'course_over_ground_t': '0.0'}]}
```
# Verified environment
- Raspberry Pi Pico 2
- MicroPython v1.24.1 on 2024-11-29; Raspberry Pi Pico2 with RP2350
- GPS module: AT6668 (M5Stack GPS module v1.1)
- GPS module: AT6558 (Air530Z)
Some modules may not work. In that case, please post an issue with the output data.