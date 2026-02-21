# Version 3.8 (Optimized)
import time
import math
import sys
from decimal import Decimal

try:
    from decimal import DecimalNumber as DecimalCls
except ImportError:
    DecimalCls = Decimal

class pygps2:
    def __init__(self, op0=True, op1=True, op2=True, op3=True, op4=True):
        self.OBTAIN_IDENTIFLER_FROM_GSA = op0
        self.IN_BAND_DATA_INTO_GSV = op1
        self.DETECT_CONVERT_QZS = op2
        self.DETECT_CONVERT_SBAS = op3
        self.ENABLE_CHECKSUM = op4
        
        self.D = DecimalCls
        impl = sys.implementation.name
        self._is_cpython = (impl == "cpython")

        self.reset_data()
        self._gsv_buffer = {k: [] for k in ["GP", "GL", "GA", "GB", "GQ", "GN"]}
        self._gsv_sets = {k: [] for k in ["GP", "GL", "GA", "GB", "GQ", "GN"]}
        self._gsa_buffer = {k: [] for k in ["GP", "GL", "GA", "GB", "GQ", "GN"]}

    def reset_data(self):
        self.raw = ''
        for k in ['GGA','GLL','GSA','RMC','VTG','GST','DHV','ZDA','GNS','TXT']:
            setattr(self, k, [] if k != 'GSA' else self.parse_gsa(''))
        self.GSV = {k: None for k in ["GP", "GL", "GA", "GB", "GQ", "GN"]}
        self.parsed_data = {k: [] for k in ['GGA','GLL','GSA','GSV','RMC','VTG','GST','DHV','ZDA','GNS','TXT','Other']}

    def convert_to_degrees(self, coord, direction):
        if not coord or not direction: return '0.0'
        try:
            d_len = 2 if direction in 'NS' else 3
            deg = self.D(coord[:d_len])
            minutes = self.D(coord[d_len:])
            res = deg + minutes / self.D('60.0')
            if direction in 'SW': res = -res
            return str(res)
        except: return '0.0'

    def verify_checksum(self, sentence):
        if '*' not in sentence: return False
        data, checksum = sentence.split('*', 1)
        chk = 0
        for c in data[1:]: chk ^= ord(c)
        return f'{chk:02X}' == checksum.strip().upper()

    def _safe_get(self, fields, idx, default=''):
        if idx < len(fields) and fields[idx]:
            return fields[idx].split('*')[0] if '*' in fields[idx] else fields[idx]
        return default

    def parse_nmea_sentences(self, nmea_data):
        for k in self.parsed_data: self.parsed_data[k].clear()
        for s in nmea_data.split('\r\n'):
            self._parse_single_sentence(s)

    def _parse_single_sentence(self, s):
        s = s.strip()
        if not s or (self.ENABLE_CHECKSUM and not self.verify_checksum(s)): return
        stype = s[3:6]
        if stype in self.parsed_data:
            self.parsed_data[stype].append(s)
        else:
            self.parsed_data['Other'].append(s)

    def parse_gga(self, sentence):
        if not sentence: return
        f = sentence[0].split(',')
        return {
            'timestamp': self._safe_get(f, 1, '000000.0'),
            'latitude': self.convert_to_degrees(self._safe_get(f, 2), self._safe_get(f, 3)),
            'longitude': self.convert_to_degrees(self._safe_get(f, 4), self._safe_get(f, 5)),
            'gps_quality': self._safe_get(f, 6, '0'),
            'num_satellites': self._safe_get(f, 7, '0'),
            'hdop': self._safe_get(f, 8, '0.0'),
            'altitude': self._safe_get(f, 9, '0.0'),
            'altitude_units': self._safe_get(f, 10, 'M'),
            'geoid_height': self._safe_get(f, 11, '0.0'),
            'geoid_units': self._safe_get(f, 12, 'M'),
            'dgps_age': self._safe_get(f, 13),
            'dgps_station_id': self._safe_get(f, 14)
        }

    def parse_gll(self, sentence):
        if not sentence: return
        f = sentence[0].split(',')
        return {
            'latitude': self.convert_to_degrees(self._safe_get(f, 1), self._safe_get(f, 2)),
            'longitude': self.convert_to_degrees(self._safe_get(f, 3), self._safe_get(f, 4)),
            'timestamp': self._safe_get(f, 5, '000000.0'),
            'status': self._safe_get(f, 6, 'V'),
            'mode_indicator': self._safe_get(f, 7)
        }

    def parse_gsa(self, sentence):
        if not sentence: return {'fix_select':'A','fix_status':'1','satellites_used':['0']*12,'pdop':'0.0','hdop':'0.0','vdop':'0.0'}
        f = sentence.split(',')
        sys_id = self._safe_get(f, 18)
        sats = [ (self._safe_get(f, i, '0'), sys_id) if self.OBTAIN_IDENTIFLER_FROM_GSA else self._safe_get(f, i, '0') for i in range(3, 15) ]
        return {
            'fix_select': self._safe_get(f, 1, 'A'),
            'fix_status': self._safe_get(f, 2, '1'),
            'satellites_used': sats,
            'pdop': self._safe_get(f, 15, '0.0'),
            'hdop': self._safe_get(f, 16, '0.0'),
            'vdop': self._safe_get(f, 17, '0.0')
        }

    def parse_gsv(self, sentence):
        if not sentence: return
        f = sentence.split(',')
        sys_type = sentence[1:3]
        band = self._safe_get(f, -1, '0') if self.IN_BAND_DATA_INTO_GSV else 0
        sats_info = []
        for i in range(4, len(f) - 3, 4):
            sats_info.append({
                'prn': self._safe_get(f, i, '0'), 'type': sys_type,
                'elevation': self._safe_get(f, i+1, '0.0'), 'azimuth': self._safe_get(f, i+2, '0.0'),
                'snr': self._safe_get(f, i+3, '0.0'), 'band': band
            })
        return {'system_type': sys_type, 'num_messages': self._safe_get(f, 1, '1'), 'message_num': self._safe_get(f, 2, '1'), 'num_satellites': self._safe_get(f, 3, '0'), 'satellites_info': sats_info}

    def parse_zda(self, sentence):
        if not sentence: return
        f = sentence[0].split(',')
        return {k: self._safe_get(f, i, None) for i, k in enumerate(['_','timestamp','day','month','year','timezone_offset_hour','timezone_offset_minute'])}

    def merge_gsa(self, gsa_list):
        if not gsa_list: return self.parse_gsa('')
        merged = {'fix_select': gsa_list[0].get('fix_select', 'A'), 'fix_status': gsa_list[0].get('fix_status', '1')}
        sats = []
        for g in gsa_list: sats.extend([s for s in g.get('satellites_used', []) if (s[0] if isinstance(s, tuple) else s) not in ('0', '')])
        merged['satellites_used'] = list(dict.fromkeys(sats))
        for k in ['pdop', 'hdop', 'vdop']:
            vals = [float(g.get(k, 0)) for g in gsa_list if float(g.get(k, 0)) > 0]
            merged[k] = str(sum(vals)/len(vals)) if vals else '0.0'
        return merged

    def merge_gsv(self, gsv_list):
        if not gsv_list: return self.parse_gsv('')
        unique = {}
        for s in [s for g in gsv_list for s in g.get('satellites_info', [])]:
            key = (s['prn'], s['type'], s['elevation'], s['azimuth'])
            if key not in unique:
                unique[key] = {**s, 'snr': [float(s['snr'])], 'band': [int(s['band'])]}
            else:
                unique[key]['snr'].append(float(s['snr']))
                unique[key]['band'].append(int(s['band']))
        res = {'num_messages': str(len(gsv_list)), 'message_num': '1', 'num_satellites': str(max([int(g.get('num_satellites', 0)) for g in gsv_list] + [0])), 'satellites_info': list(unique.values())}
        if self.DETECT_CONVERT_QZS: res['satellites_info'] = self.detect_system(res['satellites_info'], 'QZS')
        if self.DETECT_CONVERT_SBAS: res['satellites_info'] = self.detect_system(res['satellites_info'], 'SBAS')
        return res

    def parse_rmc(self, sentence):
        if not sentence: return
        f = sentence[0].split(',')
        data = {
            'timestamp': self._safe_get(f, 1, '000000.0'), 'status': self._safe_get(f, 2, 'V'),
            'latitude': self.convert_to_degrees(self._safe_get(f, 3), self._safe_get(f, 4)),
            'longitude': self.convert_to_degrees(self._safe_get(f, 5), self._safe_get(f, 6)),
            'speed_over_ground': self._safe_get(f, 7, '0.0'), 'course_over_ground': self._safe_get(f, 8, '0.0'),
            'date': self._safe_get(f, 9, '010100'), 'magnetic_variation': self._safe_get(f, 10, '0.0'),
            'mag_var_direction': self._safe_get(f, 11), 'mode_indicator': self._safe_get(f, 12)
        }
        try:
            ts, dt = data['timestamp'], data['date']
            h, m, s = int(ts[0:2]), int(ts[2:4]), int(ts[4:6])
            d, mo, y = int(dt[0:2]), int(dt[2:4]), int(dt[4:6]) + 2000
            utc = time.mktime((y, mo, d, h, m, s, 0, 0, 0 if self._is_cpython else 0))
            offset = math.floor(float(data['longitude']) / 15)
            loc = time.localtime(utc + offset * 3600)
            data['utc_datetime'] = f'{y:04d}-{mo:02d}-{d:02d} {h:02d}:{m:02d}:{s:02d}'
            data['local_datetime'] = f'{loc[0]:04d}-{loc[1]:02d}-{loc[2]:02d} {loc[3]:02d}:{loc[4]:02d}:{loc[5]:02d}'
        except: data['utc_datetime'] = data['local_datetime'] = None
        return data

    def parse_vtg(self, sentence):
        if not sentence: return
        f = sentence[0].split(',')
        keys = ['course_over_ground_t', 'reference_t', 'course_over_ground_m', 'reference_m', 'speed_knots', 'units_knots', 'speed_kmh', 'units_kmh', 'mode_indicator']
        defaults = ['0.0', 'T', '0.0', 'M', '0.0', 'N', '0.0', 'K', '']
        return {k: self._safe_get(f, i+1, defaults[i]) for i, k in enumerate(keys)}

    def parse_gst(self, sentence):
        if not sentence: return
        f = sentence[0].split(',')
        return {'timestamp': self._safe_get(f, 1, '000000.0'), 'rms': self._safe_get(f, 2, '0.0'), 'std_lat': self._safe_get(f, 6, '0.0'), 'std_lon': self._safe_get(f, 7, '0.0'), 'std_alt': self._safe_get(f, 8, '0.0')}

    def parse_dhv(self, sentence):
        if not sentence: return
        f = sentence[0].split(',')
        return {k: self._safe_get(f, i+1, None) for i, k in enumerate(['timestamp', '3d_speed', 'ecef_x_speed', 'ecef_y_speed', 'ecef_z_speed', 'horizontal_ground_speed'])}

    def parse_gns(self, sentence):
        if not sentence: return
        f = sentence[0].split(',')
        keys = ['utc_time','latitude','longitude','mode_indicator','use_sv','hdop','msl','geoid_alt','age_of_differential_data','station_id']
        map_idx = [1, 2, 4, 6, 7, 8, 9, 11, 13, 14]
        res = {k: self._safe_get(f, map_idx[i], '0.0') for i, k in enumerate(keys)}
        res['latitude'] = self.convert_to_degrees(self._safe_get(f, 2), self._safe_get(f, 3))
        res['longitude'] = self.convert_to_degrees(self._safe_get(f, 4), self._safe_get(f, 5))
        return res

    def parse_txt(self, sentence):
        if not sentence: return
        f = sentence[0].split(',')
        return {k: self._safe_get(f, i+1, None) for i, k in enumerate(['several_lines', 'free', 'type', 'text'])}

    def detect_system(self, info, system='QZS'):
        for s in info:
            if s['type'] in ('GP', 'GN'):
                prn = int(s['prn'])
                if system == 'QZS' and 193 <= prn <= 210: s['type'] = 'QZS'
                elif system == 'SBAS' and 33 <= prn <= 64: s['type'] = 'SBAS'; s['prn'] = str(prn + 87)
        return info

    def analyze(self, data, enable_type=(1,1,1,1,1,1,1,1,1,1,1)):
        self.reset_data()
        try:
            formatted = '\r\n'.join(['$' + s for s in str(data).split('$') if s]) + '\r\n'
            self.parse_nmea_sentences(formatted)
        except: return
        pd = self.parsed_data
        for k in ['GGA','GLL','RMC','VTG','GST','DHV','ZDA','TXT','GNS']:
            try: setattr(self, k, getattr(self, f'parse_{k.lower()}')(pd.get(k, [])))
            except: pass
        if pd.get('GSA') and enable_type[8]:
            self.GSA = self.merge_gsa([self.parse_gsa(s) for s in pd['GSA']])
        if pd.get('GSV') and enable_type[9]:
            self.GSV["GN"] = self.merge_gsv([self.parse_gsv(s) for s in pd['GSV']])

    def analyze_sentence(self, sentence):
        self._parse_single_sentence(sentence)
        pd = self.parsed_data
        for k in ['GGA','GLL','RMC','VTG','GST','DHV','ZDA','GNS','TXT']:
            if pd[k]: setattr(self, k, getattr(self, f'parse_{k.lower()}')(pd[k]))
        if pd['GSA']:
            for s in pd['GSA']:
                talker = s[1:3]
                self._gsa_buffer[talker].append(s)
                self.GSA = self.merge_gsa([self.parse_gsa(x) for x in self._gsa_buffer[talker]])
        if pd['GSV']:
            for s in pd['GSV']:
                talker = "GB" if (t:=s[1:3]) == "BD" else t
                f = s.split(',')
                try:
                    if int(f[2]) == int(f[1]):
                        self._gsv_sets[talker].append([self.parse_gsv(x) for x in self._gsv_buffer[talker] + [s]])
                        self._gsv_buffer[talker].clear()
                        all_gsv = [item for sub in self._gsv_sets[talker] for item in sub]
                        if all_gsv: self.GSV[talker] = self.merge_gsv(all_gsv)
                    else: self._gsv_buffer[talker].append(s)
                except: pass
