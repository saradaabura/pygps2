# Gemini made this code.
# This version isn't stable
# Pico2 test code
# 2025-02-21
import time
import math
import sys
import gc

class pygps2:
    def __init__(self, op0=True, op1=True, op2=True, op3=True, op4=True):
        # オプション設定
        self.OBTAIN_IDENTIFLER_FROM_GSA = op0
        self.IN_BAND_DATA_INTO_GSV = op1
        self.DETECT_CONVERT_QZS = op2
        self.DETECT_CONVERT_SBAS = op3
        self.ENABLE_CHECKSUM = op4
        
        # オリジナルと同じプロパティ構造
        self.GGA = None
        self.GLL = None
        self.GSA = None
        self.GSV = {"GP": None, "GL": None, "GA": None, "GB": None, "GQ": None, "GN": None}
        self.RMC = None
        self.VTG = None
        self.GST = None
        self.DHV = None
        self.ZDA = None
        self.GNS = None
        self.TXT = None
        
        # 内部バッファ
        self.parsed_data = {k: [] for k in ['GGA','GLL','GSA','GSV','RMC','VTG','GST','DHV','ZDA','GNS','TXT','Other']}
        self._gsv_buffer = {"GP": [], "GL": [], "GA": [], "GB": [], "GQ": [], "GN": []}
        self._gsa_buffer = {"GP": [], "GL": [], "GA": [], "GB": [], "GQ": [], "GN": []}

    def convert_to_degrees(self, coord, direction):
        if not coord or not direction: return 0.0
        try:
            # MicroPythonではDecimalよりfloatの方が圧倒的に高速なためfloatを使用
            dot_idx = coord.find('.')
            dd = float(coord[:dot_idx-2])
            mm = float(coord[dot_idx-2:])
            deg = dd + (mm / 60.0)
            return -deg if direction in ('S', 'W') else deg
        except: return 0.0

    def verify_checksum(self, sentence):
        try:
            if '*' not in sentence: return False
            data, checksum = sentence.split('*')
            chk = 0
            for c in data[1:]: chk ^= ord(c)
            return f'{chk:02X}' == checksum.strip().upper()
        except: return False

    def parse_gga(self, f):
        return {
            'timestamp': f[1] if len(f) > 1 else '000000.0',
            'latitude': self.convert_to_degrees(f[2], f[3]) if len(f) > 3 else 0.0,
            'longitude': self.convert_to_degrees(f[4], f[5]) if len(f) > 5 else 0.0,
            'gps_quality': f[6] if len(f) > 6 else '0',
            'num_satellites': f[7] if len(f) > 7 else '0',
            'hdop': f[8] if len(f) > 8 else '0.0',
            'altitude': f[9] if len(f) > 9 else '0.0',
            'altitude_units': f[10] if len(f) > 10 else 'M',
            'geoid_height': f[11] if len(f) > 11 else '0.0',
            'geoid_units': f[12] if len(f) > 12 else 'M',
            'dgps_age': f[13] if len(f) > 13 else '',
            'dgps_station_id': f[14].split('*')[0] if len(f) > 14 else ''
        }

    def parse_rmc(self, f):
        data = {
            'timestamp': f[1] if len(f) > 1 else '000000.0',
            'status': f[2] if len(f) > 2 else 'V',
            'latitude': self.convert_to_degrees(f[3], f[4]) if len(f) > 4 else 0.0,
            'longitude': self.convert_to_degrees(f[5], f[6]) if len(f) > 6 else 0.0,
            'speed_over_ground': f[7] if len(f) > 7 else '0.0',
            'course_over_ground': f[8] if len(f) > 8 else '0.0',
            'date': f[9] if len(f) > 9 else '010100',
            'magnetic_variation': f[10] if len(f) > 10 else '0.0',
            'mag_var_direction': f[11] if len(f) > 11 else '',
            'mode_indicator': f[12].split('*')[0] if len(f) > 12 else ''
        }
        # 日時計算ロジックの復元
        try:
            h, m, s = int(data['timestamp'][0:2]), int(data['timestamp'][2:4]), int(data['timestamp'][4:6])
            d, mo, y = int(data['date'][0:2]), int(data['date'][2:4]), int(data['date'][4:6]) + 2000
            utc = time.mktime((y, mo, d, h, m, s, 0, 0))
            offset = math.floor(float(data['longitude']) / 15)
            local = time.localtime(utc + offset * 3600)
            data['utc_datetime'] = f'{y:04d}-{mo:02d}-{d:02d} {h:02d}:{m:02d}:{s:02d}'
            data['local_datetime'] = f'{local[0]:04d}-{local[1]:02d}-{local[2]:02d} {local[3]:02d}:{local[4]:02d}:{local[5]:02d}'
        except:
            data['utc_datetime'] = data['local_datetime'] = None
        return data

    def parse_gsa(self, f):
        sats = []
        for i in range(3, 15):
            val = f[i] if len(f) > i else ''
            if val:
                sats.append((val, f[18].split('*')[0]) if self.OBTAIN_IDENTIFLER_FROM_GSA and len(f) > 18 else val)
            else: sats.append('0')
        return {
            'fix_select': f[1] if len(f) > 1 else 'A',
            'fix_status': f[2] if len(f) > 2 else '1',
            'satellites_used': sats,
            'pdop': f[15] if len(f) > 15 else '0.0',
            'hdop': f[16] if len(f) > 16 else '0.0',
            'vdop': f[17].split('*')[0] if len(f) > 17 else '0.0'
        }

    def merge_gsa(self, gsa_list):
        if not gsa_list: return None
        merged = {'fix_select': gsa_list[0]['fix_select'], 'fix_status': gsa_list[0]['fix_status']}
        sats = []
        for g in gsa_list: sats.extend([s for s in g['satellites_used'] if s not in ('0', '')])
        merged['satellites_used'] = list(set(sats))
        def avg(key):
            vals = [float(g[key]) for g in gsa_list if float(g[key]) > 0]
            return str(sum(vals)/len(vals)) if vals else '0.0'
        merged['pdop'], merged['hdop'], merged['vdop'] = avg('pdop'), avg('hdop'), avg('vdop')
        return merged

    def parse_gsv(self, f, talker):
        data = {
            'system_type': talker,
            'num_messages': f[1] if len(f) > 1 else '1',
            'message_num': f[2] if len(f) > 2 else '1',
            'num_satellites': f[3] if len(f) > 3 else '0',
            'satellites_info': []
        }
        band = f[-1].split('*')[0] if self.IN_BAND_DATA_INTO_GSV else 0
        for i in range(4, len(f) - 3, 4):
            if i+3 >= len(f) or not f[i]: continue
            data['satellites_info'].append({
                'prn': f[i], 'type': talker, 'elevation': f[i+1],
                'azimuth': f[i+2], 'snr': f[i+3].split('*')[0], 'band': band
            })
        return data

    def merge_gsv(self, gsv_list):
        if not gsv_list: return None
        merged = {'num_messages': str(len(gsv_list)), 'message_num': '1'}
        merged['num_satellites'] = str(max([int(g['num_satellites']) for g in gsv_list] or [0]))
        sats = []
        for g in gsv_list: sats.extend(g['satellites_info'])
        # QZSS/SBAS検知ロジックの復元
        if self.DETECT_CONVERT_QZS or self.DETECT_CONVERT_SBAS:
            for s in sats:
                if s['type'] in ('GP', 'GN'):
                    prn = int(s['prn'])
                    if self.DETECT_CONVERT_QZS and 193 <= prn <= 210: s['type'] = 'QZS'
                    elif self.DETECT_CONVERT_SBAS and 33 <= prn <= 64:
                        s['type'] = 'SBAS'
                        s['prn'] = str(prn + 87)
        merged['satellites_info'] = sats
        return merged

    def analyze_sentence(self, sentence):
        s = sentence.strip()
        if not s.startswith('$'): return
        if self.ENABLE_CHECKSUM and not self.verify_checksum(s): return
        
        f = s.split(',')
        header = f[0]
        talker = header[1:3]
        msg_type = header[3:6]

        if msg_type == 'GGA': self.GGA = self.parse_gga(f)
        elif msg_type == 'GLL':
            self.GLL = {
                'latitude': self.convert_to_degrees(f[1], f[2]),
                'longitude': self.convert_to_degrees(f[3], f[4]),
                'timestamp': f[5] if len(f) > 5 else '000000.0',
                'status': f[6] if len(f) > 6 else 'V',
                'mode_indicator': f[7].split('*')[0] if len(f) > 7 else ''
            }
        elif msg_type == 'RMC': self.RMC = self.parse_rmc(f)
        elif msg_type == 'GSA':
            if talker == "BD": talker = "GB"
            self._gsa_buffer[talker] = [self.parse_gsa(f)] # 簡易化しつつ保持
            self.GSA = self.merge_gsa([v[0] for v in self._gsa_buffer.values() if v])
        elif msg_type == 'GSV':
            if talker == "BD": talker = "GB"
            gsv = self.parse_gsv(f, talker)
            if gsv['message_num'] == '1': self._gsv_buffer[talker] = []
            self._gsv_buffer[talker].append(gsv)
            if gsv['message_num'] == gsv['num_messages']:
                self.GSV[talker] = self.merge_gsv(self._gsv_buffer[talker])
        elif msg_type == 'VTG':
            self.VTG = {
                'course_over_ground_t': f[1], 'reference_t': f[2],
                'course_over_ground_m': f[3], 'reference_m': f[4],
                'speed_knots': f[5], 'units_knots': f[6],
                'speed_kmh': f[7], 'units_kmh': f[8],
                'mode_indicator': f[9].split('*')[0] if len(f) > 9 else ''
            }
        elif msg_type == 'ZDA':
            self.ZDA = {
                'timestamp': f[1], 'day': f[2], 'month': f[3], 'year': f[4],
                'timezone_offset_hour': f[5] if len(f) > 5 else None,
                'timezone_offset_minute': f[6].split('*')[0] if len(f) > 6 else None
            }
