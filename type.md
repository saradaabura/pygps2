# �o�̓f�[�^�Ɠ��e

**GSA�f�[�^**
```
{'vdop': '2.3', 'fix_status': '3', 'pdop': '2.7', 'fix_select': 'A', 'satellites_used': ['66', '27', '02', '01', '08', '03', '31', '17'], 'hdop': '1.4'}
```
- hdop : HDOP
- vdop : VDOP
- fix_status_ : Fix���(1:NoFix 2:2DFix 3:3Dfix)
- satellites_used : �g�p�q��PRN�ԍ�
- pdop : PDOP
- fix_select : �������[�h(A:�I�[�g M:�}�j���A��)

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
- latitude : �ܓx (�x�ŏo�͂����) str�^
- longitude : �o�x�@(�x�ŏo�͂����) str�^
- timestamp : �^�C���X�^���v (���f�[�^)

**RMC�f�[�^**
```
[{'mode_indicator': 'N', 'date': '170325', 'mag_var_direction': '', 'utc_datetime': '2025-03-17 07:57:01', 'local_datetime': '2025-03-17 16:57:01', 'status': 'V', 'magnetic_variation': '0.0', 'course_over_ground': '0.0', 'speed_over_ground': '0.0', 'latitude': 0.0, 'longitude': 0.0, 'timestamp': '075701.00'}]
```
- longitude : �o�x (�x�ŏo�͂����) str�^
- latitude : �ܓx (�x�ŏo�͂����) str�^
- course_over_ground : �ړ������̊p�x
- status : �X�e�[�^�X
- mag_var_direction : ���C�Ίp����
- magnetic_variation : ���C�Ίp
- mode_indicator : ���[�h�C���W�P�[�^
- timestamp : �^�C���X�^���v (���f�[�^)
- speed_over_ground : �n�㑬�x
- date : ���t (���f�[�^)
- local_datetime : �o�x����Z�o���ꂽ���[�J������
- utc_datetime : UTC����

**GLL�f�[�^**
```
{'longitude': 0.0, 'latitude': 0.0, 'timestamp': '094023.00', 'status': 'A', 'mode_indicator': 'A'}
```
- longitude : �o�x (�x�ŏo�͂����) str�^
- latitude : �ܓx (�x�ŏo�͂����) Sstr�^
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

**ZDA�f�[�^**
```
[{'message': '18', 'additional_field1': '2025', 'timestamp': '063801.00', 'status': '03', 'additional_field2': None}]
```
- message : ���b�Z�[�W��
- additional_field1 : �J�X�^��(���W���[���ɂ���ĈقȂ�)
- timestamp : �^�C���X�^���v (���f�[�^)
- status : �X�e�[�^�X
- additional_field2 : �J�X�^��(���W���[���ɂ���ĈقȂ�)

**TXT�f�[�^**
```
[{'message': '01', 'additional_field1': 'JS=0', 'timestamp': '01', 'status': '02', 'additional_field2': None}]
```
���s���ɂ킽���ďo�͂����
- message : ���b�Z�[�W��(�g�p�ł��Ȃ��ꍇ����)
- additional_field1 : �J�X�^��(���W���[���ɂ���ĈقȂ�)
- timestamp : ���W���[���ɂ���ĈقȂ�B(����ύX�\��)
- status : �X�e�[�^�X
- additional_field2 : �J�X�^��(���W���[���ɂ���ĈقȂ�)

**DHV�f�[�^**
```
{'ecef_x_speed': '-0.294', 'ecef_z_speed': '-0.315', '3d_speed': '0.43', 'ecef_y_speed': '0.033', 'horizontal_ground_speed': None, 'timestamp': '052745.00'}
```
- ecef_x_speed : x�������̑��x
- ecef_z_speed : z�������̑��x
- 3d_speed : 3�������x
- ecef_y_speed : y�������̑��x
- horizontal_ground_speed : �����n�㑬�x
- timestamp : �^�C���X�^���v(���f�[�^�Ƃ��Ă�UTC����)

**GST�f�[�^**
```
{'rms': '30.9', 'std_lon': '32.9', 'timestamp': '052745.00', 'std_lat': '39.6', 'std_alt': '37.5'}
```
- rms: ���ϓ��덷(Root Mean Square Error)
- std_lon: �o�x�����̕W���΍�(���[�g���P��)
- timestamp: �^�C���X�^���v(���f�[�^�Ƃ��Ă�UTC����)
- std_lat: �ܓx�����̕W���΍�(���[�g���P��)
- std_alt: ���x�����̕W���΍�(���[�g���P��)

# ���̓f�[�^�Ɠ��e

**analyze**
�g�p��
pygps2.analyze(data, [1, 1,1 ,1 ,1, 0, 0, 0, 1, 1])

data�ɂ͉��s������f�R�[�h�f�[�^�����

- 1�ڂ͕K�{
- 2�ڂ͉�͂���f�[�^�̎�ނ��w�肷�郊�X�g
  - 0 : ��͂��Ȃ�
  - 1 : ��͂���
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

## �ȉ���Ver3.1�ȑO��pygps2.py���g�p�����ۂ̓��̓f�[�^�Ɠ��e
**analyze_nmea_date**

�g�p��
pygps2.analyze_nmea_data(parsed_data, [1, 1,1 ,1 ,1, 0, 0, 0, 1, 1])

- parsed_data : parse_nmea_sentences�ŉ�͂��ꂽ�f�[�^
- [1,1,1,1,1,0,0,0,1,1] : ��͂���f�[�^�̎�ނ��w�肷�郊�X�g
�K�{�̍��ڂł͂Ȃ� �f�t�H���g�l�͂��ׂėL���ɂȂ��Ă���([1, 1, 1, 1, 1, 1, 1 , 1, 1, 1])
  - 0 : ��͂��Ȃ�
  - 1 : ��͂���
�ǂꂪ�ǂ��ɑΉ����Ă��邩�͈ȉ��̒ʂ�ł���
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

�@�\
�Z���e���X��͂��s���֐�

**parse_nmea_sentences**

�g�p��
pygps2.parse_nmea_sentences(data)

- data : ���s�Ȃǂ��܂񂾐��f�[�^

�@�\
���̃Z���e���X�����X�g��