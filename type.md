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
- num_satellites : 衛星数(lenから取得する　修正)
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

## analyze_sentence
使用例
```
analyze_sentence(a_sentence, en_gsv=True, en_gsa=True)
```
- a_sentenceは必須
 - デコードされた1センテンスを入力(一行のみ)
- ```en_gsv```,```en_gsa```はオプション
 - GSV,GSAセンテンスの解析を有効にするかどうか指定できる。