# Japanese 日本語
# pygps2
このライブラリは自由に使用してください。どんな場合でもOKです
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

3.22~3.3 詳細な設定ができるよう、CONFIGを追加した。

(詳細はVersion.mdに記載)

# 依存ライブラリ (micropython)
- micropython-decimal-number

### Raspberry Pi Pico 1/2向けのGPS解析ライブラリです。
### 通常のPythonにも対応しているため、pyserialなどで動作できます
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
POINT
分類するセンテンスが6以上になるとmicropythonではエラーで実行が止まる。よって必要なセンテンスを選択することが好ましい。(特にGSV)
デフォルト:($GPGSV,$BDGSV,$GQGSV,$GLGSV,$GAGSV,$GBGSV)
上記から不要なセンテンスを消すことで、動作する。

# 機能
- GSVのデータを解析でき、衛星の情報を取得できます。(不完全)
- GGAのデータを解析でき、緯度、経度、高度、UTC時刻、測位精度、DGPS情報を取得できます。(不完全)
- RMCのデータを解析でき、UTC時刻、緯度、経度、速度、進行方向、日付、磁気偏角、磁気偏角方向を取得できます。
- RMC関数ではLocaltimeの出力できます
- すべてのセンテンスに対応しています
- メモリ対策があります
# 使い方

/example.pyに環境にあったサンプルコードがあります。どうぞ好きに使ってください。

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
出力されるデータの例(analyzeが返す)
```python
{'GGA': [{'timestamp': '124311.000', 'latitude': '0.0', 'longitude': '0.0', 'gps_quality': '1', 'num_satellites': '57', 'hdop': '0.46', 'altitude': '52.981', 'altitude_units': 'M', 'geoid_height': '37.106', 'geoid_units': 'M', 'dgps_age': '', 'dgps_station_id': ''}], 'GLL': [{'latitude': '0.0', 'longitude': '0.0', 'timestamp': '124311.000', 'status': 'A', 'mode_indicator': 'A'}], 'RMC': [{'timestamp': '124311.000', 'status': 'A', 'latitude': '0.0', 'longitude': '0.0', 'speed_over_ground': '0.03', 'course_over_ground': '297.23', 'date': '020525', 'magnetic_variation': '0.0', 'mag_var_direction': '', 'mode_indicator': 'A', 'utc_datetime': '2025-05-02 12:43:11', 'local_datetime': '2025-05-02 21:43:11'}], 'VTG': [{'course_over_ground_t': '297.23', 'reference_t': 'T', 'course_over_ground_m': '0.0', 'reference_m': 'M', 'speed_knots': '0.03', 'units_knots': 'N', 'speed_kmh': '0.05', 'units_kmh': 'K', 'mode_indicator': 'A'}], 'GST': [{'timestamp': '124311.000', 'rms': '5.5', 'std_lat': '2.4', 'std_lon': '2.3', 'std_alt': '9.5'}], 'ZDA': [{'timestamp': '124311.000', 'day': '02', 'month': '05', 'year': '2025', 'timezone_offset_hour': '', 'timezone_offset_minute': ''}], 'GSA': [{'fix_select': 'A', 'fix_status': '3', 'satellites_used': [('15', '1'), ('24', '1'), ('199', '1'), ('05', '1'), ('18', '1'), ('23', '1'), ('13', '1'), ('195', '1'), ('22', '1'), ('194', '1'), ('14', '1'), ('67', '2'), ('68', '2'), ('77', '2'), ('78', '2'), ('76', '2'), ('82', '2'), ('06', '3'), ('09', '3'), ('04', '3'), ('11', '3'), ('23', '3'), ('10', '3'), ('21', '3'), ('12', '3'), ('36', '3'), ('19', '4'), ('39', '4'), ('16', '4'), ('36', '4'), ('20', '4'), ('22', '4'), ('06', '4'), ('09', '4'), ('35', '4'), ('44', '4'), ('38', '4'), ('37', '4')], 'pdop': '0.82', 'hdop': '0.46', 'vdop': '0.68'}], 'GSV': [{'num_messages': '21', 'message_num': '1', 'num_satellites': '20', 'satellites_info': [{'prn': '196', 'type': 'QZS', 'elevation': '86', 'azimuth': '228', 'snr': '18', 'band': [1, 8]}, {'prn': '15', 'type': 'GP', 'elevation': '70', 'azimuth': '009', 'snr': '18', 'band': [1]}, {'prn': '24', 'type': 'GP', 'elevation': '63', 'azimuth': '221', 'snr': '18', 'band': [1, 8]}, {'prn': '199', 'type': 'QZS', 'elevation': '43', 'azimuth': '202', 'snr': '22', 'band': [1, 8]}, {'prn': '05', 'type': 'GP', 'elevation': '43', 'azimuth': '135', 'snr': '29', 'band': [1]}, {'prn': '18', 'type': 'GP', 'elevation': '41', 'azimuth': '263', 'snr': '22', 'band': [1, 8]}, {'prn': '23', 'type': 'GP', 'elevation': '41', 'azimuth': '315', 'snr': '28', 'band': [1, 8]}, {'prn': '13', 'type': 'GP', 'elevation': '40', 'azimuth': '058', 'snr': '29', 'band': [1]}, {'prn': '195', 'type': 'QZS', 'elevation': '34', 'azimuth': '197', 'snr': '37', 'band': [1, 8]}, {'prn': '22', 'type': 'GP', 'elevation': '23', 'azimuth': '071', 'snr': '19', 'band': [1]}, {'prn': '14', 'type': 'GP', 'elevation': '17', 'azimuth': '053', 'snr': '0.0', 'band': [1, 8]}, {'prn': '194', 'type': 'QZS', 'elevation': '10', 'azimuth': '171', 'snr': '21', 'band': [1, 8]}, {'prn': '20', 'type': 'GP', 'elevation': '09', 'azimuth': '141', 'snr': '0.0', 'band': [1]}, {'prn': '12', 'type': 'GP', 'elevation': '03', 'azimuth': '172', 'snr': '17', 'band': [1]}, {'prn': '10', 'type': 'GP', 'elevation': '01', 'azimuth': '314', 'snr': '0.0', 'band': [1]}, {'prn': '67', 'type': 'GL', 'elevation': '50', 'azimuth': '054', 'snr': '17', 'band': [1]}, {'prn': '68', 'type': 'GL', 'elevation': '46', 'azimuth': '330', 'snr': '17', 'band': [1]}, {'prn': '77', 'type': 'GL', 'elevation': '45', 'azimuth': '057', 'snr': '16', 'band': [1]}, {'prn': '78', 'type': 'GL', 'elevation': '44', 'azimuth': '151', 'snr': '33', 'band': [1]}, {'prn': '84', 'type': 'GL', 'elevation': '18', 'azimuth': '322', 'snr': '0.0', 'band': [1]}, {'prn': '76', 'type': 'GL', 'elevation': '09', 'azimuth': '025', 'snr': '25', 'band': [1]}, {'prn': '82', 'type': 'GL', 'elevation': '09', 'azimuth': '216', 'snr': '30', 'band': [1]}, {'prn': '69', 'type': 'GL', 'elevation': '08', 'azimuth': '296', 'snr': '0.0', 'band': [1]}, {'prn': '06', 'type': 'GA', 'elevation': '70', 'azimuth': '353', 'snr': '20', 'band': [7, 1]}, {'prn': '09', 'type': 'GA', 'elevation': '57', 'azimuth': '299', 'snr': '18', 'band': [7, 1]}, {'prn': '04', 'type': 'GA', 'elevation': '55', 'azimuth': '048', 'snr': '21', 'band': [7, 1]}, {'prn': '36', 'type': 'GA', 'elevation': '44', 'azimuth': '282', 'snr': '0.0', 'band': [7, 1]}, {'prn': '11', 'type': 'GA', 'elevation': '39', 'azimuth': '211', 'snr': '22', 'band': [7, 1]}, {'prn': '23', 'type': 'GA', 'elevation': '28', 'azimuth': '088', 'snr': '25', 'band': [7, 1]}, {'prn': '10', 'type': 'GA', 'elevation': '21', 'azimuth': '187', 'snr': '31', 'band': [7, 1]}, {'prn': '31', 'type': 'GA', 'elevation': '20', 'azimuth': '142', 'snr': '0.0', 'band': [7]}, {'prn': '05', 'type': 'GA', 'elevation': '11', 'azimuth': '268', 'snr': '0.0', 'band': [7]}, {'prn': '34', 'type': 'GA', 'elevation': '10', 'azimuth': '326', 'snr': '0.0', 'band': [7]}, {'prn': '21', 'type': 'GA', 'elevation': '09', 'azimuth': '039', 'snr': '15', 'band': [7, 1]}, {'prn': '12', 'type': 'GA', 'elevation': '04', 'azimuth': '173', 'snr': '15', 'band': [7]}, {'prn': '19', 'type': 'GA', 'elevation': '04', 'azimuth': '076', 'snr': '08', 'band': [7]}, {'prn': '38', 'type': 'GB', 'elevation': '83', 'azimuth': '322', 'snr': '0.0', 'band': [1, 4]}, {'prn': '19', 'type': 'GB', 'elevation': '71', 'azimuth': '025', 'snr': '18', 'band': [1, 4]}, {'prn': '08', 'type': 'GB', 'elevation': '70', 'azimuth': '333', 'snr': '17', 'band': [1]}, {'prn': '57', 'type': 'GB', 'elevation': '59', 'azimuth': '243', 'snr': '0.0', 'band': [1]}, {'prn': '46', 'type': 'GB', 'elevation': '58', 'azimuth': '100', 'snr': '0.0', 'band': [1]}, {'prn': '13', 'type': 'GB', 'elevation': '53', 'azimuth': '321', 'snr': '0.0', 'band': [1]}, {'prn': '56', 'type': 'GB', 'elevation': '48', 'azimuth': '309', 'snr': '0.0', 'band': [1]}, {'prn': '01', 'type': 'GB', 'elevation': '47', 'azimuth': '174', 'snr': '28', 'band': [1]}, {'prn': '39', 'type': 'GB', 'elevation': '45', 'azimuth': '222', 'snr': '27', 'band': [1, 4]}]}]}
```
# 動作確認済み環境
- CPython
- Raspberry Pi Pico 2
- MicroPython v1.24.1 on 2024-11-29; Raspberry Pi Pico2 with RP2350
- GPSモジュール: AT6668 (M5Stack GPSモジュールv1.1)
- GPSモジュール: AT6558 (Air530Z)
- GPS受信機: GT-505GGBL5-DR-N(秋月電子)
モジュールによっては動作しないかもしれません。その場合出力データを載せてissueを立ててください。

# English 英語
# pygps2
Feel free to use this library. It's OK in any case
# Version information

2.0 Created

2.1 Changed to allow satellite type to be obtained for GSV analysis

2.2 Eliminated duplicate counts due to dual satellite bands

2.3 Added GST analysis function

2.4 Added local time calculated from longitude to RMC

2.5 Added DHV ZDA TXT Changed RMC date initial value to 2000/01/01

2.6 Changed to allow processing of data with unknown patterns

2.7 Fixed issues#2 using decimal function → Use micropython-decimal-number. LAT and LON require conversion with str().

2.8 Added processing to maintain compatibility between cpython and micropython

2.9 Added checksum function

3.0 Lightweight

3.1 Now can be analyzed with analyze.

3.2 Added a function to retain previous data to reduce memory usage (differential method)

3.22~3.3 Added CONFIG to allow detailed settings.

(Details are in Version.md)

# Dependent library (micropython)
- micropython-decimal-number

### GPS analysis library for Raspberry Pi Pico 1/2.
### Compatible with regular Python, so it can run with pyserial, etc.
# Supported sentences
Basically supports all sentences.
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
TXT:$GNTXT,$GPTXT, $BDTXT
```
POINT
If the number of sentences to be classified is 6 or more, micropython will stop execution with an error.
Therefore, it is recommended to select the necessary sentences. (especially GSV)
Default: ($GPGSV, $BDGSV, $GQGSV, $GLGSV, $GAGSV, $GBGSV)
It will work if you delete unnecessary sentences from here.

# Function
- It can analyze GSV data and obtain satellite information. (Incomplete)
- You can analyze GGA data and obtain latitude, longitude, altitude, UTC time, positioning accuracy, and DGPS information. (Incomplete)
- You can analyze RMC data and obtain UTC time, latitude, longitude, speed, heading, date, magnetic declination, and magnetic declination direction.
- RMC functions can output localtime
- Supports all sentences
- Memory management included
# How to use

There is sample code for your environment in /example.py. Please use it as you like.

How to use in the latest version 3.2
**It's become complicated, so I recommend running the sample first**
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
# Detailed usage
1. Input the decoded data into pygps2.analyze. (Like pygps2.analyze(decoded))

2. Data returned by return has been analyzed

If it doesn't work, try using main.py above.

Change UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1)) to match the connected pins.

# Sample
Example of output data (returned by analyze)
```python
{'GGA': [{'timestamp': '124311.000', 'latitude': '0.0', 'longitude': '0.0', 'gps_quality': '1', 'num_satellites': '57', 'hdop': '0.46', 'altitude': '52.981', 'altitude_units': 'M', 'geoid_height': '37.106', 'geoid_units': 'M', 'dgps_age': '', 'dgps_station_id': ''}], 'GLL': [{'latitude': '0.0', 'longitude': '0.0', 'timestamp': '124311.000', 'status': 'A', 'mode_indicator': 'A'}], 'RMC': [{'timestamp': '124311.000', 'status': 'A', 'latitude': '0.0', 'longitude': '0.0', 'speed_over_ground': '0.03', 'course_over_ground': '297.23', 'date': '020525', 'magnetic_variation': '0.0', 'mag_var_direction': '', 'mode_indicator': 'A', 'utc_datetime': '2025-05-02 12:43:11', 'local_datetime': '2025-05-02 21:43:11'}], 'VTG': [{'course_over_ground_t': '297.23', 'reference_t': 'T', 'course_over_ground_m': '0.0', 'reference_m': 'M', 'speed_knots': '0.03', 'units_knots': 'N', 'speed_kmh': '0.05', 'units_kmh': 'K', 'mode_indicator': 'A'}], 'GST': [{'timestamp': '124311.000', 'rms': '5.5', 'std_lat': '2.4', 'std_lon': '2.3', 'std_alt': '9.5'}], 'ZDA': [{'timestamp': '124311.000', 'day': '02', 'month': '05', 'year': '2025', 'timezone_offset_hour': '', 'timezone_offset_minute': ''}], 'GSA': [{'fix_select': 'A', 'fix_status': '3', 'satellites_used': [('15', '1'), ('24', '1'), ('199', '1'), ('05', '1'), ('18', '1'), ('23', '1'), ('13', '1'), ('195', '1'), ('22', '1'), ('194', '1'), ('14', '1'), ('67', '2'), ('68', '2'), ('77', '2'), ('78', '2'), ('76', '2'), ('82', '2'), ('06', '3'), ('09', '3'), ('04', '3'), ('11', '3'), ('23', '3'), ('10', '3'), ('21', '3'), ('12', '3'), ('36', '3'), ('19', '4'), ('39', '4'), ('16', '4'), ('36', '4'), ('20', '4'), ('22', '4'), ('06', '4'), ('09', '4'), ('35', '4'), ('44', '4'), ('38', '4'), ('37', '4')], 'pdop': '0.82', 'hdop': '0.46', 'vdop': '0.68'}], 'GSV': [{'num_messages': '21', 'message_num': '1', 'num_satellites': '20', 'satellites_info': [{'prn': '196', 'type': 'QZS', 'elevation': '86', 'azimuth': '228', 'snr': '18', 'band': [1, 8]}, {'prn': '15', 'type': 'GP', 'elevation': '70', 'azimuth': '009', 'snr': '18', 'band': [1]}, {'prn': '24', 'type': 'GP', 'elevation': '63', 'azimuth': '221', 'snr': '18', 'band': [1, 8]}, {'prn': '199', 'type': 'QZS', 'elevation': '43', 'azimuth': '202', 'snr': '22', 'band': [1, 8]}, {'prn': '05', 'type': 'GP', 'elevation': '43', 'azimuth': '135', 'snr': '29', 'band': [1]}, {'prn': '18', 'type': 'GP', 'elevation': '41', 'azimuth': '263', 'snr': '22', 'band': [1, 8]}, {'prn': '23', 'type': 'GP', 'elevation': '41', 'azimuth': '315', 'snr': '28', 'band': [1, 8]}, {'prn': '13', 'type': 'GP', 'elevation': '40', 'azimuth': '058', 'snr': '29', 'band': [1]}, {'prn': '195', 'type': 'QZS', 'elevation': '34', 'azimuth': '197', 'snr': '37', 'band': [1, 8]}, {'prn': '22', 'type': 'GP', 'elevation': '23', 'azimuth': '071', 'snr': '19', 'band': [1]}, {'prn': '14', 'type': 'GP', 'elevation': '17', 'azimuth': '053','snr': '0.0', 'band': [1, 8]}, {'prn': '194', 'type': 'QZS', 'elevation': '10', 'azimuth': '171', 'snr': '21', 'band': [1, 8]}, {'prn': '20', 'type': 'GP', 'elevation': '09', 'azimuth': '141', 'snr': '0.0', 'band': [1]}, {'prn': '12', 'type': 'GP', 'elevation': '03', 'azimuth': '172', 'snr': '17', 'band': [1]}, {'prn': '10', 'type': 'GP', 'elevation': '01', 'azimuth': '314', 'snr': '0.0', 'band': [1]}, {'prn': '67', 'type': 'GL', 'elevation': '50', 'azimuth': '054', 'snr': '17', 'band': [1]}, {'prn': '68', 'type': 'GL', 'elevation': '46', 'azimuth': '330', 'snr': '17', 'band': [1]}, {'prn': '77', 'type': 'GL', 'elevation': '45', 'azimuth': '057', 'snr': '16', 'band': [1]}, {'prn': '78', 'type': 'GL', 'elevation': '44', 'azimuth': '151', 'snr': '33', 'band': [1]}, {'prn': '84', 'type': 'GL', 'elevation': '18', 'azimuth': '322', 'snr': '0.0', 'band': [1]}, {'prn': '76', 'type': 'GL', 'elevation': '09', 'azimuth': '025', 'snr': '25', 'band': [1]}, {'prn': '82', 'type': 'GL', 'elevation': '09', 'azimuth': '216', 'snr': '30', 'band': [1]}, {'prn': '69', 'type': 'GL', 'elevation': '08', 'azimuth': '296', 'snr': '0.0', 'band': [1]}, {'prn': '06', 'type': 'GA', 'elevation': '70', 'azimuth': '353', 'snr': '20', 'band': [7, 1]}, {'prn': '09', 'type': 'GA', 'elevation': '57', 'azimuth': '299', 'snr': '18', 'band': [7, 1]}, {'prn': '04', 'type': 'GA', 'elevation': '55', 'azimuth': '048', 'snr': '21', 'band': [7, 1]}, {'prn': '36', 'type': 'GA', 'elevation': '44', 'azimuth': '282', 'snr': '0.0', 'band': [7, 1]}, {'prn': '11', 'type': 'GA', 'elevation': '39', 'azimuth': '211', 'snr': '22', 'band': [7, 1]}, {'prn': '23', 'type': 'GA', 'elevation': '28', 'azimuth': '088', 'snr': '25', 'band': [7, 1]}, {'prn': '10', 'type': 'GA', 'elevation': '21', 'azimuth': '187', 'snr': '31', 'band': [7, 1]}, {'prn': '31', 'type': 'GA', 'elevation': '20', 'azimuth': '142', 'snr': '0.0', 'band': [7]}, {'prn': '05', 'type': 'GA', 'elevation': '11', 'azimuth': '268', 'snr': '0.0', 'band': [7]}, {'prn': '34', 'type': 'GA', 'elevation': '10', 'azimuth': '326', 'snr': '0.0', 'band': [7]}, {'prn': '21', 'type': 'GA', 'elevation': '09', 'azimuth': '039', 'snr': '15', 'band': [7, 1]}, {'prn': '12', 'type': 'GA', 'elevation': '04', 'azimuth': '173', 'snr': '15', 'band': [7]}, {'prn': '19', 'type': 'GA', 'elevation': '04', 'azimuth': '076', 'snr': '08', 'band': [7]}, {'prn': '38', 'type': 'GB', 'elevation': '83', 'azimuth': '322', 'snr': '0.0', 'band': [1, 4]}, {'prn': '19', 'type': 'GB', 'elevation': '71', 'azimuth': '025', 'snr': '18', 'band': [1, 4]}, {'prn': '08', 'type': 'GB', 'elevation': '70', 'azimuth': '333', 'snr': '17', 'band': [1]}, {'prn': '57', 'type': 'GB', 'elevation': '59', 'azimuth': '243', 'snr': '0.0', 'band': [1]}, {'prn': '46', 'type': 'GB', 'elevation': '58', 'azimuth': '100', 'snr': '0.0', 'band': [1]}, {'prn': '13', 'type': 'GB', 'elevation': '53', 'azimuth': '321', 'snr': '0.0', 'band': [1]}, {'prn': '56', 'type': 'GB', 'elevation': '48', 'azimuth': '309', 'snr': '0.0', 'band': [1]}, {'prn': '01', 'type': 'GB', 'elevation': '47', 'azimuth': '174', 'snr': '28', 'band': [1]}, {'prn': '39', 'type': 'GB', 'elevation': '45', 'azimuth': '222', 'snr': '27', 'band': [1, 4]}]}]}
```
# Tested environment
- CPython
- Raspberry Pi Pico 2
- MicroPython v1.24.1 on 2024-11-29; Raspberry Pi Pico2 with RP2350
- GPS module: AT6668 (M5Stack GPS module v1.1)
- GPS module: AT6558 (Air530Z)
- GPS receiver: GT-505GGBL5-DR-N (Akizuki Electronics)
Depending on the module, it may not work. In that case, please post the output data and create an issue.
