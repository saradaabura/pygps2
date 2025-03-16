# �o�̓f�[�^�Ɠ��e

**GSV�f�[�^**
```
{'hdop': '2.8', 'vdop': '4.1', 'mode2': '3', 'satellites_used': ['09', '66', '02', '06', '22', '17'], 'pdop': '5.0', 'mode1': 'A'}
```
- hdop : HDOP
- vdop : VDOP
- mode2 : Fix���(1:NoFix 2:2DFix 3:3Dfix)
- satellites_used : �g�p�q��PRN�ԍ�
- pdop : PDOP
- mode1 : �g�p���Ă���GPS���W���[���ɂ���ĈقȂ�(�Z���e���X2�Ԗڂ��Q��)

**GSV�f�[�^**
```
{'num_messages': '7', 'num_satellites': '7', 'satellites_info': [{'snr': '17', 'elevation': '06', 'prn': '22', 'type': 'GP', 'azimuth': '204'}, {'snr': '24', 'elevation': '56', 'prn': '66', 'type': 'GL', 'azimuth': '192'}, {'snr': '28', 'elevation': '0.0', 'prn': '19', 'type': 'GA', 'azimuth': '0.0'}, {'snr': '0.0', 'elevation': '26', 'prn': '34', 'type': 'BD', 'azimuth': '131'}, {'snr': '28', 'elevation': '28', 'prn': '02', 'type': 'GQ', 'azimuth': '195'}], 'message_num': '1'}
```
- num_messages : ���b�Z�[�W��
- num_satellites : �q����
- satellites_info : �q�����
  - snr : SNR
  - elevation : �p
  - prn : PRN�ԍ�
  - type : �q�����ʎq
  - azimuth : ���ʊp
- message_num : ���b�Z�[�W�ԍ�

**GGA�f�[�^**
```
{'gps_quality': '1', 'hdop': '2.8', 'altitude': '88.29', 'geoid_units': 'M', 'dgps_station_id': '', 'geoid_height': '36.37', 'dgps_age': '', 'altitude_units': 'M', 'num_satellites': '06', 'latitude': 0.0, 'longitude': 0.0, 'timestamp': '094023.00'}
```
- gps_quality : GPS�i��
- hdop : HDOP
- altitude : �W��
- geoid_units : �W�I�C�h�����P��
- dgps_station_id : DGPS��n��ID
- geoid_height : �W�I�C�h����
- dgps_age : DGPS�f�[�^�n
- altitude_units : �W���P��
- num_satellites : �q����
- latitude : �ܓx (�x�ŏo�͂����)
- longitude : �o�x�@(�x�ŏo�͂����)
- timestamp : �^�C���X�^���v (���f�[�^)

**RMC�f�[�^**
```
{'longitude': 0.0, 'latitude': 0.0, 'course_over_ground': '0.0', 'status': 'A', 'mag_var_direction': '', 'magnetic_variation': '0.0', 'mode_indicator': 'A', 'timestamp': '094023.00', 'speed_over_ground': '0.50', 'date': '160325'}
```
- longitude : �o�x (�x�ŏo�͂����)
- latitude : �ܓx (�x�ŏo�͂����)
- course_over_ground : �ړ������̊p�x
- status : �X�e�[�^�X
- mag_var_direction : ���C�Ίp����
- magnetic_variation : ���C�Ίp
- mode_indicator : ���[�h�C���W�P�[�^
- timestamp : �^�C���X�^���v (���f�[�^)
- speed_over_ground : �n�㑬�x
- date : ���t (���f�[�^)

**GLL�f�[�^**
```
{'longitude': 0.0, 'latitude': 0.0, 'timestamp': '094023.00', 'status': 'A', 'mode_indicator': 'A'}
```
- longitude : �o�x (�x�ŏo�͂����)
- latitude : �ܓx (�x�ŏo�͂����)
- timestamp : �^�C���X�^���v (���f�[�^)
- status : �X�e�[�^�X
- mode_indicator : ���[�h�C���W�P�[�^

**VTG�f�[�^**
```
{'reference_t': 'T', 'mode_indicator': 'A', 'speed_kmh': '0.92', 'course_over_ground_m': '0.0', 'reference_m': 'M', 'speed_knots': '0.50', 'units_knots': 'N', 'units_kmh': 'K', 'course_over_ground_t': '0.0'}
```
- reference_t : �^�k, ���k�̔���(T:�^�k M:���k)
- mode_indicator : ���[�h�C���W�P�[�^
- speed_kmh : �n�㑬�x(km/h)
- course_over_ground_m : ���k����Ƃ����i�H�̊p�x
- reference_m : �^�k, ���k�̔���(T:�^�k M:���k)
- speed_knots : �n�㑬�x(knots)
- units_knots : �P�ʂ�����
- units_kmh : �P�ʂ�����
- course_over_ground_t : �^�k����Ƃ����i�H�̊p�x
