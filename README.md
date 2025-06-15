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

3.5 class化をし、利便性を向上させた。

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

/example.pyに環境にあったサンプルコード(Windows用)があります。どうぞ好きに使ってください。

最新バージョン3.5での使い方
**複雑ですので、とりあえずサンプルを実行することをおすすめします**
```python:main.py
import pygps2
import serial
import time

###
gps = serial.Serial('COM3', 115200, timeout=0.05)
###
module = pygps2.pygps2()
while True:
    raw = gps.read(16384) #
    if raw is not None:
        try:
            raw = raw.replace(b'\r', b'').replace(b'\n', b'')
            raw = raw.replace(b'/', b'')
            data = raw.decode("utf-8", "ignore")
            del raw
        except Exception as e:
            print(f"error: {e}")
            continue
        if data != '':
            analyzed_data = module.analyze(data)
gps.close()

```
# 詳細な使い方
1.デコードしたデータをpygps2.analyzeに入力します。(pygps2.analyze(decoded)みたいにする)

2.pygps2のなかにGSAやGSVなどがある。

pygps2.GSA→GSA解析データ(以前のanalyzed_data["GSA"]と同じ内容)

"
動かない場合は上記のmain.pyを使ってみてください。

UARTの設定は接続されているピンに合わせて変更してください。

# 動作確認済み環境
- CPython
- Raspberry Pi Pico 2
- MicroPython v1.24.1 on 2024-11-29; Raspberry Pi Pico2 with RP2350
- GPSモジュール: AT6668 (M5Stack GPSモジュールv1.1)
- GPSモジュール: AT6558 (Air530Z)
- GPS受信機: GT-505GGBL5-DR-N(秋月電子)
モジュールによっては動作しないかもしれません
# Japanese Japanese
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

3.2 Added a function to save previous data to reduce memory (differential method)

3.22~3.3 Added CONFIG to allow detailed settings.

3.5 Classified to improve convenience.

(See Version.md for details)

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
TXT:$GNTXT, $GPTXT, $BDTXT
```
POINT
When the number of sentences to be classified is 6 or more, micropython stops execution with an error. Therefore, it is recommended to select the necessary sentences. (Especially GSV)
Default: ($GPGSV, $BDGSV, $GQGSV, $GLGSV, $GAGSV, $GBGSV)
It will work if you delete unnecessary sentences from the above.

# Function
- GSV data can be analyzed and satellite information can be obtained. (Incomplete)
- GGA data can be analyzed and latitude, longitude, altitude, UTC time, positioning accuracy, and DGPS information can be obtained. (Incomplete)
- RMC data can be analyzed and UTC time, latitude, longitude, speed, heading, date, magnetic declination, and magnetic declination direction can be obtained.
- Localtime can be output in RMC functions
- All sentences are supported
- Memory measures are available
# Usage

There is a sample code that suits your environment in /example.py. Please use it as you like.

How to use with the latest version 3.5
**It's complicated, so we recommend running the sample first**
```python:main.py
import pygps2
import serial
import time

###
gps = serial.Serial('COM3', 115200, timeout=0.05)
###
module = pygps2.pygps2()
while True:
raw = gps.read(16384) #
if raw is not None:
try:
raw = raw.replace(b'\r', b'').replace(b'\n', b'')
raw = raw.replace(b'/', b'')
data = raw.decode("utf-8", "ignore")
del raw
except Exception as e:
print(f"error: {e}")
continue
if data != '':
analyzed_data = module.analyze(data)
gps.close()

```
# Detailed usage
1. Input the decoded data into pygps2.analyze (like pygps2.analyze(decoded)).
2. GSA, GSV, etc. are included in pygps2.

pygps2.GSA -> GSA analysis data (same content as previous analyzed_data["GSA"])

"
If it doesn't work, try using the main.py above.

Change the UART settings to match the connected pins.

# Tested environment
- CPython
- Raspberry Pi Pico 2
- MicroPython v1.24.1 on 2024-11-29; Raspberry Pi Pico2 with RP2350
- GPS module: AT6668 (M5Stack GPS module v1.1)
- GPS module: AT6558 (Air530Z)
- GPS receiver: GT-505GGBL5-DR-N (Akizuki Electronics)
It may not work depending on the module. In that case, please post the output data and create an issue.いかもしれません。その場合出力データを載せてissueを立ててください。

