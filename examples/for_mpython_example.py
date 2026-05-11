import machine, time, gc
from pygps2 import pygps2

# バッファを大きく確保
uart = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1), rxbuf=2048)
gnss = pygps2(op4=False)

while True:
    if uart.any():
        raw_bytes = uart.read() 
        try:
            raw_str = raw_bytes.decode('utf-8', 'ignore')
            gnss.analyze_sentences_block(raw_str)
        except:
            pass

    # 3. 解析結果の利用
    if gnss.RMC:
        print(gnss.RMC["latitude"], gnss.RMC["longitude"])
    gc.collect()
    time.sleep(1)