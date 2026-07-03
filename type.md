# 出力データと内容

## GSAデータ
```
{'fix_select': 'A', 'fix_status': '3', 'satellites_used': [('24', '1'), ('23', '1'), ('199', '1'), ('20', '1'), ('195', '1'), ('18', '1'), ('12', '1'), ('05', '1'), ('194', '1'), ('74', '2'), ('75', '2'), ('23', '4'), ('16', '4'), ('37', '4'), ('06', '4'), ('20', '4')], 'self.parsed_dataop': '1.12', 'hdop': '0.8', 'vdop': '0.79'}
```
- hdop : HDOP
- vdop : VDOP
- fix_status_ : Fix状態(1:NoFix 2:2DFix 3:3Dfix)
- satellites_used : 使用衛星PRN番号とオプション機能の識別子 (PRN, CODE)
- pdop : PDOP
- fix_select : 測距モード(A:オート M:マニュアル)

## GSVデータ

```
{'num_messages': '8', 'message_num': '1', 'num_satellites': '6', 'satellites_info': [{'prn': '05', 'type': 'GP', 'elevation': '0.0', 'azimuth': '0.0', 'snr': [26.0], 'band': [1]}, {'prn': '195', 'type': 'QZS', 'elevation': '0.0', 'azimuth': '0.0', 'snr': [35.0, 29.0], 'band': [1, 8]}, {'prn': '59', 'type': 'GB', 'elevation': '0.0', 'azimuth': '0.0', 'snr': [37.0], 'band': [1]}, {'prn': '39', 'type': 'GB', 'elevation': '0.0', 'azimuth': '0.0', 'snr': [39.0, 25.0], 'band': [1, 4]}, {'prn': '03', 'type': 'GB', 'elevation': '0.0', 'azimuth': '0.0', 'snr': [29.0], 'band': [1]}, {'prn': '16', 'type': 'GB', 'elevation': '0.0', 'azimuth': '0.0', 'snr': [33.0], 'band': [1]}, {'prn': '01', 'type': 'GB', 'elevation': '0.0', 'azimuth': '0.0', 'snr': [33.0], 'band': [1]}, {'prn': '37', 'type': 'GB', 'elevation': '0.0', 'azimuth': '0.0', 'snr': [33.0], 'band': [1]}]}
```
- num_messages : メッセージ数
- num_satellites : 衛星数
- satellites_info : 衛星情報
  - snr : SNR
  - elevation : 仰角
  - prn : PRN番号
  - type : 衛星識別子
  - azimuth : 方位角
  - band : 周波数帯(オプション)
- message_num : メッセージ番号

## GGAデータ
```
{'timestamp': '000007.230', 'latitude': '0.0', 'longitude': '0.0', 'gps_quality': '0', 'num_satellites': '0', 'hdop': '0.0', 'altitude': '0.0', 'altitude_units': 'M', 'geoid_height': '0.0', 'geoid_units': 'M', 'dgps_age': '', 'dgps_station_id': ''}
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

## RMCデータ
```
{'timestamp': '000007.230', 'status': 'V', 'latitude': '0.0', 'longitude': '0.0', 'speed_over_ground': '0.0', 'course_over_ground': '0.0', 'date': '150326', 'magnetic_variation': '0.0', 'mag_var_direction': '', 'mode_indicator': 'N', 'utc_datetime': '2026-03-15 00:00:07', 'local_datetime': '2026-03-15 00:00:07'}
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

## GLLデータ
```
{'longitude': 0.0, 'latitude': 0.0, 'timestamp': '094023.00', 'status': 'A', 'mode_indicator': 'A'}
```
- longitude : 経度 (度で出力される) str型
- latitude : 緯度 (度で出力される) Sstr型
- timestamp : タイムスタンプ (生データ)
- status : ステータス
- mode_indicator : モードインジケータ

## VTGデータ
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

## ZDAデータ
```
[{'message': '18', 'additional_field1': '2025', 'timestamp': '063801.00', 'status': '03', 'additional_field2': None}]
```
- message : メッセージ数
- additional_field1 : カスタム(モジュールによって異なる)
- timestamp : タイムスタンプ (生データ)
- status : ステータス
- additional_field2 : カスタム(モジュールによって異なる)

## TXTデータ
```
[{'message': '01', 'additional_field1': 'JS=0', 'timestamp': '01', 'status': '02', 'additional_field2': None}]
```
何行かにわたって出力される
- message : メッセージ数(使用できない場合あり)
- additional_field1 : カスタム(モジュールによって異なる)
- timestamp : モジュールによって異なる。(今後変更予定)
- status : ステータス
- additional_field2 : カスタム(モジュールによって異なる)

## DHVデータ
```
{'ecef_x_speed': '-0.294', 'ecef_z_speed': '-0.315', '3d_speed': '0.43', 'ecef_y_speed': '0.033', 'horizontal_ground_speed': None, 'timestamp': '052745.00'}
```
- ecef_x_speed : x軸方向の速度
- ecef_z_speed : z軸方向の速度
- 3d_speed : 3次元速度
- ecef_y_speed : y軸方向の速度
- horizontal_ground_speed : 水平地上速度
- timestamp : タイムスタンプ(生データとしてのUTC時間)

## GSTデータ
```
{'rms': '30.9', 'std_lon': '32.9', 'timestamp': '052745.00', 'std_lat': '39.6', 'std_alt': '37.5'}
```
- rms: 平均二乗誤差(Root Mean Square Error)
- std_lon: 経度方向の標準偏差(メートル単位)
- timestamp: タイムスタンプ(生データとしてのUTC時間)
- std_lat: 緯度方向の標準偏差(メートル単位)
- std_alt: 高度方向の標準偏差(メートル単位)

## GNSデータ
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

## pygps2() クラス
使用例
```
gps = pygps2(op0=True, op1=True, op2=True, op3=True, op4=True, op5=True, op6="GGA", op7=callback)
```
op0~6はオプションである。
- op0はGSAに衛星識別子を取得するかどうかを設定できる
- op1はGSV解析時にバンド情報("band": [1, 8])を追加するかどうか指定できる
- op2はGSV解析時にQZSSを認識し、typeを"QZS"にするかどうか設定できる
- op3はGSV解析時にSBASを認識し、typeを"SBAS"にし、PRNを変換するかどうか設定できる
- op4はチェックサムを使ってセンテンスを解析するかどうか設定できる
- op5は経緯度を十進数に変換する際、decimalを使うかfloatを使うか選択できるようにするオプションである。
- op6はセンテンスのループの始まりを選択できるオプションである。(起点)
- op7は割り込み処理用の関数 op6で指定した(指定していない場合はGGA)センテンスが来たときに呼び出される。

## analyze_sentence
使用例
```
analyze_sentence(a_sentence, en_gsv=True, en_gsa=True, en_txt=True)
```
- a_sentenceは必須
 - デコードされた1センテンスを入力(一行のみ)
- ```en_gsv```,```en_gsa```,```en_txt```はオプション
 - GSV,GSA,TXTセンテンスの解析を有効にするかどうか指定できる。
## analyze_sentences_block
使用例
```
gnss.analyze_sentences_block(nmea_str)
```
- nmea_strには、str型のNMEAブロックを入れる。以下はその例。

```txt:nmea_str
'\r\n\r\n$GNGGA,145455.000,3543.0,N,138.3371320,E,1,21,1.69,93.384,M,11.063,M,,*45\r\n$GNGLL,3543.0,N,138.3371320,E,145455.000,A,A*4C\r\n$GNGSA,A,3,194,26,28,199,27,32,195,,,,,,2.59,1.69,1.96,1*35\r\n$GNGSA,A,3,67,88,,,,,,,,,,,2.59,1.69,1.96,2*0D\r\n$GNGSA,A,3,19,28,,,,,,,,,,,2.59,1.69,1.96,3*0F\r\n$GNGSA,A,3,29,08,22,,,,,,,,,,2.59,1.69,1.96,4*09\r\n$GPGSV,4,1,15,31,82,064,16,194,79,182,23,26,69,326,20,28,55,119,24,1*5B\r\n$GLGSV,1,1,04,68,33,300,11,67,33,237,15,86,27,044,,88,17,162,31,1*78\r\n$GAGSV,3,1,11,23,72,320,,04,58,263,,28,56,213,,06,42,299,,7*71\r\n$GBGSV,5,1,19,07,71,334,,57,62,030,,10,58,319,11,29,50,132,16,1*74\r\n$GBGSV,1,1,03,29,50,132,25,08,29,198,30,35,15,185,20,4*45\r\n$GNRMC,145455.000,A,3543.0,N,138.3371320,E,1.56,168.77,030726,,,A,V*0C\r\n$GNVTG,168.77,T,,M,1.56,N,2.88,K,A*2C\r\n$GNZDA,145455.000,03,07,2026,,*4E\r\n$GNGST,145455.000,3.6,8.2,4.1,174.6,8.1,4.1,15.9*42\r\n$GNGNS,145455.000,3543.0,N,138.3371320,E,AAAA,21,1.69,87.384,M,37.063,M,,,V*15\r\n$PAIRMSG,90,145455.000,1*5D\r\n$PAIRMSG,91,145455.000,1,0*40\r\n'
```
