# 出力データと内容

**GSAデータ**
```
'GSA': [{'fix_select': 'A', 'fix_status': '3', 'satellites_used': [('194', '1'), ('08', '1'), ('27', '1'), ('195', '1'), ('16', '1'), ('02', '1'), ('199', '1')], 'pdop': '0.8', 'hdop': '0.55', 'vdop': '0.58'}]
```
- hdop : HDOP
- vdop : VDOP
- fix_status_ : Fix状態(1:NoFix 2:2DFix 3:3Dfix)
- satellites_used : 使用衛星PRN番号とオプション機能の識別子 (PRN, CODE)
- pdop : PDOP
- fix_select : 測距モード(A:オート M:マニュアル)

**GSVデータ**
```
'GSV': [{'num_messages': '21', 'message_num': '1', 'num_satellites': '24', 'satellites_info': [{'prn': '194', 'type': 'QZS', 'elevation': '89', 'azimuth': '332', 'snr': '18', 'band': [1, 8]}]}]}
```
- num_messages : メッセージ数
- num_satellites : 衛星数(lenから取得する　修正)
- satellites_info : 衛星情報
  - snr : SNR
  - elevation : 仰角
  - prn : PRN番号
  - type : 衛星識別子
  - azimuth : 方位角
  - band : 周波数帯(オプション)
- message_num : メッセージ番号

**GGAデータ**
```
{'GGA': [{'timestamp': '298893.000', 'latitude': '0.0', 'longitude': '0.0', 'gps_quality': '1', 'num_satellites': '52', 'hdop': '0.55', 'altitude': '76.219', 'altitude_units': 'M', 'geoid_height': '37.106', 'geoid_units': 'M', 'dgps_age': '', 'dgps_station_id': ''}]
```
- gps_quality : GPS品質
- hdop : HDOP
- altitude : 標高
- geoid_units : ジオイド高さ単位
- dgps_station_id : DGPS基地局ID
- geoid_height : ジオイド高さ
- dgps_age : DGPSデータ系
- altitude_units : 標高単位
- num_satellites : 衛星数
- latitude : 緯度 (度で出力される) str型
- longitude : 経度　(度で出力される) str型
- timestamp : タイムスタンプ (生データ)

**RMCデータ**
```
[{'mode_indicator': 'N', 'date': '170325', 'mag_var_direction': '', 'utc_datetime': '2025-03-17 07:57:01', 'local_datetime': '2025-03-17 16:57:01', 'status': 'V', 'magnetic_variation': '0.0', 'course_over_ground': '0.0', 'speed_over_ground': '0.0', 'latitude': 0.0, 'longitude': 0.0, 'timestamp': '075701.00'}]
```
- longitude : 経度 (度で出力される) str型
- latitude : 緯度 (度で出力される) str型
- course_over_ground : 移動方向の角度
- status : ステータス
- mag_var_direction : 磁気偏角方向
- magnetic_variation : 磁気偏角
- mode_indicator : モードインジケータ
- timestamp : タイムスタンプ (生データ)
- speed_over_ground : 地上速度
- date : 日付 (生データ)
- local_datetime : 経度から算出されたローカル時刻
- utc_datetime : UTC時刻

**GLLデータ**
```
{'longitude': 0.0, 'latitude': 0.0, 'timestamp': '094023.00', 'status': 'A', 'mode_indicator': 'A'}
```
- longitude : 経度 (度で出力される) str型
- latitude : 緯度 (度で出力される) Sstr型
- timestamp : タイムスタンプ (生データ)
- status : ステータス
- mode_indicator : モードインジケータ

**VTGデータ**
```
{'reference_t': 'T', 'mode_indicator': 'A', 'speed_kmh': '0.92', 'course_over_ground_m': '0.0', 'reference_m': 'M', 'speed_knots': '0.50', 'units_knots': 'N', 'units_kmh': 'K', 'course_over_ground_t': '0.0'}
```
- reference_t : 真北, 磁北の判別(T:真北 M:磁北)
- mode_indicator : モードインジケータ
- speed_kmh : 地上速度(km/h)
- course_over_ground_m : 磁北を基準とした進路の角度
- reference_m : 真北, 磁北の判別(T:真北 M:磁北)
- speed_knots : 地上速度(knots)
- units_knots : 単位を示す
- units_kmh : 単位を示す
- course_over_ground_t : 真北を基準とした進路の角度

**ZDAデータ**
```
[{'message': '18', 'additional_field1': '2025', 'timestamp': '063801.00', 'status': '03', 'additional_field2': None}]
```
- message : メッセージ数
- additional_field1 : カスタム(モジュールによって異なる)
- timestamp : タイムスタンプ (生データ)
- status : ステータス
- additional_field2 : カスタム(モジュールによって異なる)

**TXTデータ**
```
[{'message': '01', 'additional_field1': 'JS=0', 'timestamp': '01', 'status': '02', 'additional_field2': None}]
```
何行かにわたって出力される
- message : メッセージ数(使用できない場合あり)
- additional_field1 : カスタム(モジュールによって異なる)
- timestamp : モジュールによって異なる。(今後変更予定)
- status : ステータス
- additional_field2 : カスタム(モジュールによって異なる)

**DHVデータ**
```
{'ecef_x_speed': '-0.294', 'ecef_z_speed': '-0.315', '3d_speed': '0.43', 'ecef_y_speed': '0.033', 'horizontal_ground_speed': None, 'timestamp': '052745.00'}
```
- ecef_x_speed : x軸方向の速度
- ecef_z_speed : z軸方向の速度
- 3d_speed : 3次元速度
- ecef_y_speed : y軸方向の速度
- horizontal_ground_speed : 水平地上速度
- timestamp : タイムスタンプ(生データとしてのUTC時間)

**GSTデータ**
```
{'rms': '30.9', 'std_lon': '32.9', 'timestamp': '052745.00', 'std_lat': '39.6', 'std_alt': '37.5'}
```
- rms: 平均二乗誤差(Root Mean Square Error)
- std_lon: 経度方向の標準偏差(メートル単位)
- timestamp: タイムスタンプ(生データとしてのUTC時間)
- std_lat: 緯度方向の標準偏差(メートル単位)
- std_alt: 高度方向の標準偏差(メートル単位)

**GNSデータ**
```
{'utc_time': '144530.000', 'latitude': '0.0'longitude': '0.0'mode_indicator': 'AAAA', 'use_sv': '36', 'hdop': '0.79', 'msl': '39.019', 'geoid_alt': '37.062', 'age_of_differential_data': '0.0', 'station_id': '0000'}
```
- utc_time: UTC時間
- latitude: 緯度 (度で出力される) str型
- longitude: 経度 (度で出力される) str型
- mode_indicator: 各衛星のモード 

例) A SPS , D DGPS ...
- use_sv: 使用衛星数
- hdop: 水平精度
- msl: 平均海面上の高度
- geoid_alt: ジオイド高さ
- age_of_differential_data: DGPSデータについて
- station_id: DGPS基地局ID

# 入力データと内容

# Version 3.5

```
import pygps2
gps_module_ = pygps2.pygps2()
analyzed_data = ag3335a.analyze(data)
```

dataにはデコードされたデータを入力する

exampleのように処理するのが望ましい
```
while True:
    raw = gps.read(8192)  # 8192バイト読み込み モジュールごとに調整
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
            analyzed_data = gps_module_.analyze(data)
```

# OLD

**analyze**
使用例
```analyze(data, just="gga gll rmc vtg gst dhv zda gns txt gsa gsv")```
複数のセンテンスを解析することができる。RAMが少ないMPyボードで使用する際に使う。
- dataは必須
 - デコードされたセンテンスを入力
- justはオプション
 - 解析するセンテンスをスペース区切りで指定する。指定しない場合はすべてのセンテンスを解析する。

## 以下はVer3.1以前のpygps2.pyを使用した際の入力データと内容
**analyze_nmea_date**

使用例
pygps2.analyze_nmea_data(parsed_data, [1, 1,1 ,1 ,1, 0, 0, 0, 1, 1])

- parsed_data : parse_nmea_sentencesで解析されたデータ
- [1,1,1,1,1,0,0,0,1,1] : 解析するデータの種類を指定するリスト
必須の項目ではない デフォルト値はすべて有効になっている([1, 1, 1, 1, 1, 1, 1 , 1, 1, 1])
  - 0 : 解析しない
  - 1 : 解析する
どれがどこに対応しているかは以下の通りである
```
enable_type:
[0]: GGA
[1]: GLL
[2]: RMC
[3]: VTG
[4]: GST
[5]: DHV
[6]: ZDA
[7]: TXT
[8]: GSA
[9]: GSV
```

機能
センテンス解析を行う関数

**parse_nmea_sentences**

使用例
pygps2.parse_nmea_sentences(data)

- data : 改行などを含んだ生データ

機能
生のセンテンスをリスト化
