# pygps2
# �o�[�W�������

2.0 �쐬

2.1 GSV��͂ɑ΂��A�q���̎�ނ��擾�ł���悤�ɕύX

2.2 �q���̃f���A���o���h�ɂ��J�E���g�d���̉���

2.3 GST��͊֐��ǉ�

2.4 RMC�Ɍo�x����v�Z�������[�J��������ǉ�

# Japanese ���{��
Raspberry Pi Pico 1/2������GPS��̓��C�u�����ł��B
# �@�\
- GSV�̃f�[�^����͂ł��A�q���̏����擾�ł��܂��B(�s���S)
- GGA�̃f�[�^����͂ł��A�ܓx�A�o�x�A���x�AUTC�����A���ʐ��x�ADGPS�����擾�ł��܂��B(�s���S)
- RMC�̃f�[�^����͂ł��AUTC�����A�ܓx�A�o�x�A���x�A�i�s�����A���t�A���C�Ίp�A���C�Ίp�������擾�ł��܂��B
- RMC�֐��ł�Localtime�̏o�͂ł��܂�
# �g����
```python:main.py
from machine import UART, Pin
import pygps2
import time
gps = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
while True:
    raw = gps.read(8192)
    if raw is not None:
        try:
            raw = raw.replace(b'\r', b'').replace(b'\n', b'')
            raw = raw.replace(b'/', b'')
            data = raw.decode("utf-8", "ignore")
        except Exception as e:
            print(f"error: {e}")
            print(raw)
            continue
        sentences = data.split('$')
        sentences = ['$' + sentence for sentence in sentences if sentence]
        data = '\r\n'.join(sentences) + '\r\n'
        parsed_data = pygps2.parse_nmea_sentences(data)
        analyzed_data = pygps2.analyze_nmea_data(parsed_data)
        print(analyzed_data)
    time.sleep(0.01) # CPU timing �e������ / Adjust to your CPU timing
```
# �ڍׂȎg����
1.�f�R�[�h�����f�[�^����s��pygps2.parse_nmea_sentences�ɓ��͂���B

2.return�ŕԂ����f�[�^��pygps2.analyze_nmea_data�ɓ��͂���B

3.return�Ŗ߂�̂ŕϐ��ɑ������B

�����Ȃ��ꍇ�͏�L��main.py���g���Ă݂Ă��������B

UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))�͐ڑ�����Ă���s���ɍ��킹�ĕύX���Ă��������B
# �T���v��
�o�͂����f�[�^�̗�(analyze_nmea_data���Ԃ�)
```python
{'GSA': [{'hdop': '0.6', 'vdop': '0.8', 'mode2': '3', 'satellites_used': {'snr': '26', 'prn': '14', 'elevation': '24', 'azimuth': '181'}, {'snr': '34', 'prn': '24', 'elevation': '48', 'azimuth': '052'}, {'snr': '23', 'prn': '25', 'elevation': '62', 'azimuth': '296'}, {'snr': '42', 'prn': '33', 'elevation': '43', 'azimuth': '203'}, {'snr': '10', 'prn': '35', 'elevation': '08', 'azimuth': '043'}, {'snr': '37', 'prn': '38', 'elevation': '14', 'azimuth': '213'}, {'snr': '23', 'prn': '40', 'elevation': '14', 'azimuth': '187'}, {'snr': '38', 'prn': '44', 'elevation': '22', 'azimuth': '086'}, {'snr': '38', 'prn': '59', 'elevation': '46', 'azimuth': '181'}, {'snr': '43', 'prn': '33', 'elevation': '43', 'azimuth': '203'}, {'snr': '25', 'prn': '35', 'elevation': '08', 'azimuth': '043'}, {'snr': '39', 'prn': '44', 'elevation': '22', 'azimuth': '086'}, {'snr': '42', 'prn': '02', 'elevation': '66', 'azimuth': '174'}, {'snr': '38', 'prn': '04', 'elevation': '51', 'azimuth': '201'}, {'snr': '36', 'prn': '07', 'elevation': '44', 'azimuth': '202'}], 'message_num': '1'}], 'GGA': [{'gps_quality': '1', 'hdop': '0.6', 'altitude': '62.75', 'geoid_units': 'M', 'dgps_station_id': '', 'geoid_height': '36.37', 'dgps_age': '', 'altitude_units': 'M', 'num_satellites': '30', 'latitude': 0.0, 'longitude': 0.0, 'timestamp': '211311.00'}], 'RMC': [{'longitude': 0.0, 'latitude': 0.0, 'course_over_ground': '0.0', 'status': 'A', 'mag_var_direction': '', 'magnetic_variation': '0.0', 'mode_indicator': 'A', 'timestamp': '211311.00', 'speed_over_ground': '0.27', 'date': '120325'}], 'GLL': [{'longitude': 0.0, 'latitude': 0.0, 'timestamp': '211311.00', 'status': 'A', 'mode_indicator': 'A'}], 'VTG': [{'reference_t': 'T', 'mode_indicator': 'A', 'speed_kmh': '0.50', 'course_over_ground_m': '0.0', 'reference_m': 'M', 'speed_knots': '0.27', 'units_knots': 'N', 'units_kmh': 'K', 'course_over_ground_t': '0.0'}]}
```
# ����m�F�ς݊�
- Raspberry Pi Pico 2
- MicroPython v1.24.1 on 2024-11-29; Raspberry Pi Pico2 with RP2350
- GPS���W���[��: AT6668 (M5Stack GPS���W���[��v1.1)
- GPS���W���[��: AT6558 (Air530Z)
���W���[���ɂ���Ă͓��삵�Ȃ���������܂���B���̏ꍇ�o�̓f�[�^���ڂ���issue�𗧂ĂĂ��������B
# English �p��
I use Google Translate, so there may be some strange sentences.

A GPS analysis library for Raspberry Pi Pico 1/2.
# Functions
- Can analyze GSV data and obtain satellite information. (Incomplete)
- Can analyze GGA data and obtain latitude, longitude, altitude, UTC time, positioning accuracy, and DGPS information. (Incomplete)
- Can analyze RMC data and obtain UTC time, latitude, longitude, speed, heading, date, magnetic declination, and magnetic declination direction.
# How to use
```python:main.py
from machine import UART, Pin
import pygps2
import time
gps = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
while True:
 raw = gps.read(8192)
 if raw is not None:
 try:
 raw = raw.replace(b'\r', b'').replace(b'\n', b'')
 raw = raw.replace(b'/', b'')
 data = raw.decode("utf-8", "ignore")
 except Exception as e:
 print(f"error: {e}")
 print(raw)
 continue
 sentences = data.split('$')
 sentences = ['$' + sentence for sentence in sentences if sentence]
 data = '\r\n'.join(sentences) + '\r\n' parsed_data = pygps2.parse_nmea_sentences(data)
analyzed_data = pygps2.analyze_nmea_data(parsed_data)
print(analyzed_data)
time.sleep(0.01) # CPU timing Adjust to your CPU timing
```
# Detailed usage
1. Enter the decoded data in one line into pygps2.parse_nmea_sentences.
1. 
2. Enter the data returned by return into pygps2.analyze_nmea_data.
1. 
3. Assign the data to a variable when it returns with return.

If it doesn't work, try using the main.py above.

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