# pygps2
# Japanese ���{��
Raspberry Pi Pico 1/2������GPS��̓��C�u�����ł��B
# �@�\
- GSV�̃f�[�^����͂ł��A�q���̏����擾�ł��܂��B(�s���S)
- GGA�̃f�[�^����͂ł��A�ܓx�A�o�x�A���x�AUTC�����A���ʐ��x�ADGPS�����擾�ł��܂��B(�s���S)
- RMC�̃f�[�^����͂ł��AUTC�����A�ܓx�A�o�x�A���x�A�i�s�����A���t�A���C�Ίp�A���C�Ίp�������擾�ł��܂��B
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
�ڍׂȎg����
1.�f�R�[�h�����f�[�^����s��pygps2.parse_nmea_sentences�ɓ��͂���B
2.return�ŕԂ����f�[�^��pygps2.analyze_nmea_data�ɓ��͂���B
3.return�Ŗ߂�̂ŕϐ��ɑ������B

�����Ȃ��ꍇ�͏�L��main.py���g���Ă݂Ă��������B
UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))�͐ڑ�����Ă���s���ɍ��킹�ĕύX���Ă��������B