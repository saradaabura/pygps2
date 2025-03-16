# 出力データと内容

**GSVデータ**
```
{'hdop': '2.8', 'vdop': '4.1', 'mode2': '3', 'satellites_used': ['09', '66', '02', '06', '22', '17'], 'pdop': '5.0', 'mode1': 'A'}
```
- hdop : HDOP
- vdop : VDOP
- mode2 : Fix状態(1:NoFix 2:2DFix 3:3Dfix)
- satellites_used : 使用衛星PRN番号
- pdop : PDOP
- mode1 : 使用しているGPSモジュールによって異なる(センテンス2番目を参照)

**GSVデータ**
```
{'num_messages': '7', 'num_satellites': '7', 'satellites_info': [{'snr': '17', 'elevation': '06', 'prn': '22', 'type': 'GP', 'azimuth': '204'}, {'snr': '24', 'elevation': '56', 'prn': '66', 'type': 'GL', 'azimuth': '192'}, {'snr': '28', 'elevation': '0.0', 'prn': '19', 'type': 'GA', 'azimuth': '0.0'}, {'snr': '0.0', 'elevation': '26', 'prn': '34', 'type': 'BD', 'azimuth': '131'}, {'snr': '28', 'elevation': '28', 'prn': '02', 'type': 'GQ', 'azimuth': '195'}], 'message_num': '1'}
```
- num_messages : メッセージ数
- num_satellites : 衛星数
- satellites_info : 衛星情報
  - snr : SNR
  - elevation : 仰角
  - prn : PRN番号
  - type : 衛星識別子
  - azimuth : 方位角
- message_num : メッセージ番号

**GGAデータ**
```
{'gps_quality': '1', 'hdop': '2.8', 'altitude': '88.29', 'geoid_units': 'M', 'dgps_station_id': '', 'geoid_height': '36.37', 'dgps_age': '', 'altitude_units': 'M', 'num_satellites': '06', 'latitude': 0.0, 'longitude': 0.0, 'timestamp': '094023.00'}
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
- latitude : 緯度 (度で出力される)
- longitude : 経度　(度で出力される)
- timestamp : タイムスタンプ (生データ)

**RMCデータ**
```
{'longitude': 0.0, 'latitude': 0.0, 'course_over_ground': '0.0', 'status': 'A', 'mag_var_direction': '', 'magnetic_variation': '0.0', 'mode_indicator': 'A', 'timestamp': '094023.00', 'speed_over_ground': '0.50', 'date': '160325'}
```
- longitude : 経度 (度で出力される)
- latitude : 緯度 (度で出力される)
- course_over_ground : 移動方向の角度
- status : ステータス
- mag_var_direction : 磁気偏角方向
- magnetic_variation : 磁気偏角
- mode_indicator : モードインジケータ
- timestamp : タイムスタンプ (生データ)
- speed_over_ground : 地上速度
- date : 日付 (生データ)

**GLLデータ**
```
{'longitude': 0.0, 'latitude': 0.0, 'timestamp': '094023.00', 'status': 'A', 'mode_indicator': 'A'}
```
- longitude : 経度 (度で出力される)
- latitude : 緯度 (度で出力される)
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
