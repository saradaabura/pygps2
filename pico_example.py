# Raspberry pi Pico 1/2��p / Only for Raspberry Pi Pico 1/2
#version3.1�ȍ~��pico_example_31.py���Q�� / Refer to pico_example_31.py for version 3.1 or later
from machine import UART, Pin
import pygps2
import time
gps = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
while True:
    raw = gps.read(8192) #GPS���Ԃ��f�[�^�̗ʂ̉����ĕύX (Pico 1���ƃ������s���ɂȂ邩������܂���)
                         #Change depending on the amount of data returned by the GPS (Pico 1 may run out of memory)
    if raw is not None:
        try:#�f�R�[�h�����@���r���[�ȃf�[�^�ɑ΂���G���[��h������
            #Decode processing to prevent errors for incomplete data
            raw = raw.replace(b'\r', b'').replace(b'\n', b'')
            raw = raw.replace(b'/', b'')
            data = raw.decode("utf-8", "ignore")
        except Exception as e:
            print(f"error: {e}")
            print(raw)
            continue
        sentences = data.split('$')
        sentences = ['$' + sentence for sentence in sentences if sentence]
        data = '\r\n'.join(sentences) + '\r\n'#NMEA�f�[�^�̍Ō�ɉ��s��ǉ� / Add a line feed at the end of the NMEA data
        parsed_data = pygps2.parse_nmea_sentences(data)
        analyzed_data = pygps2.analyze_nmea_data(parsed_data)
        print(analyzed_data)#�e�X�g�\�� / Test display
    time.sleep(0.01)