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

3.7 GSVを正しく解析できない問題をとりあえずCpython向けで解消。micropython向けは今後の課題。

(詳細はVersion.mdに記載)

# 依存ライブラリ (micropython)
- micropython-decimal-number

### Raspberry Pi Pico 1/2向けのGPS解析ライブラリです。
### 通常のPythonにも対応しているため、pyserialなどと併用することで直接解析することができます
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
POINT

**分類するセンテンスが6以上になるとmicropythonではエラーで実行が止まる。よって必要なセンテンスを選択することが好ましい。(特にGSV)
デフォルト:($GPGSV,$BDGSV,$GQGSV,$GLGSV,$GAGSV,$GBGSV)
上記から不要なセンテンスを消すことで、動作する。**

# 機能
- GSVのデータを解析でき、衛星の情報を取得できます。(ほぼ完全)
- GGAのデータを解析でき、緯度、経度、高度、UTC時刻、測位精度、DGPS情報を取得できます。
- RMCのデータを解析でき、UTC時刻、緯度、経度、速度、進行方向、日付、磁気偏角、磁気偏角方向を取得できます。
- RMCの解析ではLocaltimeを出力し、経度と連携した時刻を取得できます。([経度] / 15 = 小数点以下切り捨て という単純なプログラムで動いているため、サマータイムや0.5時間単位での時刻の取得はできません。）

# 使い方

/example.pyに環境にあったサンプルコード(Windows用)があります。どうぞ好きに使ってください。

最新バージョン3.5での使い方
**サンプルを実行し、環境での動作を確認してからプログラムを制作してください**
```python:main.py
import pygps2
import serial
import time

###
gps = serial.Serial('COM3', 115200, timeout=1)#1Hzで出力されるGPSモジュールの場合はtimeoutを1にする。(理論的には1)
###
module = pygps2.pygps2(op0=True, op1=True, op2=True, op3=True, op4=True)#オプション機能の設定
while True:
    raw = gps.read(16384) #バッファ
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
            module.analyze(data)
            print(module.GGA)　#GGAの解析結果を表示
gps.close()
#tryなどでcloseしていないのであまり良くないプログラムですが、動作確認用です。

```
**1 ~serial.Serial('COM3', 115200, timeout=1)~について**
WindowsではCOM3を接続しているポートに合わせて変更してください。

Linuxでは/dev/ttyUSB0や/dev/serial0等にしてください。

ボーレートも接続しているGPSモジュールに合わせて変更してください。

timeoutは1Hzで出力されるGPSモジュールの場合は1にしてください。
**ですが本番環境では、GPSモジュールとのやり取りの時間より少し大きい(+0.1ほど)値を設定してください。**
**まとまりのセンテンス一つを受信し終わる時間(だいたい)+0.1 ぐらいがちょうどいいです。**

# 動作確認済み環境
- CPython (Python3.14)
- Raspberry Pi Pico 2
- MicroPython v1.24.1 on 2024-11-29; Raspberry Pi Pico2 with RP2350
- GPSモジュール: AT6668 (M5Stack GPSモジュールv1.1)
- GPSモジュール: AT6558 (Air530Z)
- GPS受信機: GT-505GGBL5-DR-N(秋月電子)

- モジュールによってはGSVやGSAなどのセンテンスを正しく解析できないかもしれません。GGAなどは解析できると思います。
