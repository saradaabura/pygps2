import threading
import serial
import time
from pygps2 import pygps2

class GPSReader:
    def __init__(self, port="COM6", baud=460800):
        self.port = port
        self.baud = baud
        self.running = False
        self.thread = None
        self.gps = pygps2()
        self.lock = threading.Lock()

    def start(self):
        # background thread starts
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def stop(self):
        # thread stops
        self.running = False
        if self.thread:
            self.thread.join()

    def _loop(self):
        # thread is reading GPS data
        try:
            ser = serial.Serial(self.port, self.baud, timeout=1)
        except Exception as e:
            print("Serial open error:", e)
            return

        print(f"[GPSReader] Reading {self.port} @ {self.baud}")

        while self.running:
            try:
                line = ser.readline().decode(errors="ignore").strip()
                if not line:
                    continue
                with self.lock:
                    self.gps.analyze_sentence(line)

            except Exception as e:
                print("Error in GPS thread:", e)

        ser.close()
        print("[GPSReader] Stopped")

    def get(self, key):
        """最新データを取得（スレッドセーフ）"""
        with self.lock:
            return getattr(self.gps, key, None)
# MAIN PROGRAM
if __name__ == "__main__":
    gps_reader = GPSReader("COM6", 460800)
    gps_reader.start()

    try:
        while True:
            rmc = gps_reader.get("RMC")
            gsv = gps_reader.get("GSV")

            if rmc:
                print("Lat:", rmc["latitude"], "Lon:", rmc["longitude"])

            if gsv:
                print("GPS:", gsv["GP"]["num_satellites"] if gsv["GP"] else 0,
                      "BD:", gsv["GB"]["num_satellites"] if gsv["GB"] else 0,
                      "GA:", gsv["GA"]["num_satellites"] if gsv["GA"] else 0)

            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping...")
        gps_reader.stop()
