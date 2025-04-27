# Japanese 日本語
# pygps2
# バージョン情報

2.0 作成

2.1 GSV解析に対し、衛星の種類を取得できるように変更

2.2 衛星のデュアルバンドによるカウント重複の解消

2.3 GST解析関数追加

2.4 RMCに経度から計算したローカル時刻を追加

2.5 DHV ZDA TXT追加 RMC日付初期値 2000/01/01へ変更

2.6 未知のパターンのデータを処理できるように変更

2.7 decimal関数を用いてissues#2を解消→micropython-decimal-numberを使用　LATやLONにはstr()で変換する必要がある。

2.8 cpythonとmicropythonで互換性を保つ処理を追加

2.9 チェックサムの機能を追加

3.0 軽量化

3.1 analyzeで解析できるようになった。

3.2 メモリ対策のため以前のデータを保持する機能を追加(差分方式)

(詳細はVersion.mdに記載)

# 依存ライブラリ
- micropython-decimal-number

### Raspberry Pi Pico 1/2向けのGPS解析ライブラリです。
# 対応センテンス
基本的にすべてのセンテンスに対応。
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
- GSVのデータを解析でき、衛星の情報を取得できます。(不完全)
- GGAのデータを解析でき、緯度、経度、高度、UTC時刻、測位精度、DGPS情報を取得できます。(不完全)
- RMCのデータを解析でき、UTC時刻、緯度、経度、速度、進行方向、日付、磁気偏角、磁気偏角方向を取得できます。
- RMC関数ではLocaltimeの出力できます
- すべてのセンテンスに対応しています
- メモリ対策があります
# 使い方
最新バージョン3.2での使い方
**複雑になったので、とりあえずサンプルを実行することをおすすめします**
```python:main.py
import pygps2
from machine import UART, Pin
gps = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
analyzed_data = pygps2.init()
while True:
    raw = gps.read(8192)# 128~
    if raw is not None:
        try:
            raw = raw.replace(b'\r', b'').replace(b'\n', b'')
            raw = raw.replace(b'/', b'')
            data = raw.decode("utf-8", "ignore")
            del raw
        except Exception as e:
            print(f"error: {e}")
            continue
        analyzed_data = pygps2.analyze(data, oldata=analyzed_data)


```
# 詳細な使い方
1.デコードしたデータをpygps2.analyzeに入力します。(pygps2.analyze(decoded)みたいにする)

2.returnで戻ったデータは解析済み

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
- GPS受信機: GT-505GGBL5-DR-N(秋月電子
モジュールによっては動作しないかもしれません。その場合出力データを載せてissueを立ててください。

# English 英語
# pygps2
# Version information

2.0 Created

2.1 Changed to allow satellite type to be obtained for GSV analysis

2.2 Eliminated duplicate counts due to dual band satellites

2.3 Added GST analysis function

2.4 Added local time calculated from longitude to RMC

2.5 Added DHV ZDA TXT Changed RMC date initial value to 2000/01/01

2.6 Changed to allow processing of data with unknown patterns

2.7 Fixed issues#2 using decimal function → Use micropython-decimal-number. LAT and LON require conversion with str().

2.8 Added processing to maintain compatibility between cpython and micropython

2.9 Added checksum function

3.0 Lightweight

3.1 Now can be analyzed with analyze.

(Details are given in Version.md)

# Dependent libraries
- micropython-decimal-number

### A GPS analysis library for Raspberry Pi Pico 1/2.
# Supported sentences
Basically supports all sentences.
```
GGA:$GNGGA, $GPGGA, $BDGGA
GLL:$GNGLL, $GPGLL, $BDGLL
GSA:$GNGSA, $GPGSA, $BDGSA
GSV:$GPGSV, $BDGSV, $GQGSV, $GLGSV, $GAGSV
RMC:$GNRMC, $GPRMC, $BDRMC
VTG:$GNVTG, $GPVTG, $BDVTG
GST:$GNGST, $GPGST, $BDGST
DHV:$GNDHV, $GPDHV, $BDDHV
ZDA:$GNZDA, $GPZDA, $BDZDA
TXT:$GNTXT, $GPTXT, $BDTXT
```
# Function
- It can analyze GSV data and obtain satellite information. (Incomplete)
- GGA data can be analyzed to obtain latitude, longitude, altitude, UTC time, positioning accuracy, and DGPS information. (Incomplete)
- RMC data can be analyzed to obtain UTC time, latitude, longitude, speed, heading, date, magnetic declination, and magnetic declination direction.
- RMC functions can output localtime
- All sentences are supported.
# How to use
```python:main.py
# ver3.1
import pygps2
from machine import UART, Pin
import time
gps = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
while True:
 raw = gps.read(8192)
 if raw is not None:
 try:
 raw = raw.replace(b'\r', b'').replace(b'\n', b'')
 raw = raw.replace(b'/', b'')
 data = raw.decode("utf-8", "ignore")
 del raw
 except Exception as e:
 print(f"error: {e}")
 continue
 analyzed_data = pygps2.analyze(data)
 #program here to use the analyzed_data
 del data
 time.sleep(0.01)

````
# Detailed usage
1. Input the decoded data into pygps2.analyze. (Use pygps2.analyze(decoded))
2. Data returned by return has been analyzed
If it doesn't work, try using main.py above.
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