# Version 3.85
import time
import math
import sys

try:
    from decimal import Decimal as DecimalCls
except ImportError:
    try:
        from decimal import DecimalNumber as DecimalCls
    except ImportError:
        # For micropython environments
        class DecimalCls:
            def __init__(self, v): self.v = float(v)
            def __add__(self, o): return DecimalCls(self.v + getattr(o, 'v', float(o)))
            def __sub__(self, o): return DecimalCls(self.v - getattr(o, 'v', float(o)))
            def __mul__(self, o): return DecimalCls(self.v * getattr(o, 'v', float(o)))
            def __truediv__(self, o): return DecimalCls(self.v / getattr(o, 'v', float(o)))
            def __neg__(self): return DecimalCls(-self.v)
            def __str__(self): return str(self.v)
            def __float__(self): return float(self.v)

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
            if k == 'GSA':
                setattr(self, k, self.parse_gsa(''))
            else:
                setattr(self, k, [])
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
        try:
            data, checksum = sentence.split('*', 1)
            chk = 0
            for c in data[1:]: chk ^= ord(c)
            return "{:02X}".format(chk) == checksum.strip().upper()
        except: return False

    def _safe_get(self, fields, idx, default=''):
        if idx < len(fields) and fields[idx]:
            val = fields[idx]
            return val.split('*')[0] if '*' in val else val
        return default

    def parse_nmea_sentences(self, nmea_data):
        for k in self.parsed_data: self.parsed_data[k].clear()
        for s in nmea_data.split('\r\n'):
            self._parse_single_sentence(s)

    def _parse_single_sentence(self, s):
        s = s.strip()
        if not s: return
        if self.ENABLE_CHECKSUM and not self.verify_checksum(s): return
        stype = s[3:6]
        if stype in self.parsed_data:
            self.parsed_data[stype].append(s)
        else:
            self.parsed_data['Other'].append(s)

    def parse_gga(self, sentence_list):
        if not sentence_list: return
        f = sentence_list[0].split(',')
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

    def parse_gll(self, sentence_list):
        if not sentence_list: return
        f = sentence_list[0].split(',')
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

    def parse_zda(self, sentence_list):
        if not sentence_list: return
        f = sentence_list[0].split(',')
        return {k: self._safe_get(f, i, None) for i, k in enumerate(['_','timestamp','day','month','year','timezone_offset_hour','timezone_offset_minute'])}

    def merge_gsa(self, gsa_list):
        if not gsa_list: return self.parse_gsa('')
        merged = {'fix_select': gsa_list[0].get('fix_select', 'A'), 'fix_status': gsa_list[0].get('fix_status', '1')}
        sats = []
        for g in gsa_list:
            for s in g.get('satellites_used', []):
                val = s[0] if isinstance(s, tuple) else s
                if val not in ('0', ''): sats.append(s)
        seen = []
        merged['satellites_used'] = [x for x in sats if not (x in seen or seen.append(x))]
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
                unique[key] = s.copy()
                unique[key]['snr'] = [float(s['snr'])]
                unique[key]['band'] = [int(s['band'])]
            else:
                unique[key]['snr'].append(float(s['snr']))
                unique[key]['band'].append(int(s['band']))
        
        mx_s = 0
        for g in gsv_list:
            n = int(g.get('num_satellites', 0))
            if n > mx_s: mx_s = n
            
        res = {'num_messages': str(len(gsv_list)), 'message_num': '1', 'num_satellites': str(mx_s), 'satellites_info': list(unique.values())}
        if self.DETECT_CONVERT_QZS: res['satellites_info'] = self.detect_system(res['satellites_info'], 'QZS')
        if self.DETECT_CONVERT_SBAS: res['satellites_info'] = self.detect_system(res['satellites_info'], 'SBAS')
        return res

    def parse_rmc(self, sentence_list):
        if not sentence_list: return
        f = sentence_list[0].split(',')
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
            day, mo, y = int(dt[0:2]), int(dt[2:4]), int(dt[4:6]) + 2000
            t_tup = (y, mo, day, h, m, s, 0, 0, 0) if self._is_cpython else (y, mo, day, h, m, s, 0, 0)
            utc = time.mktime(t_tup)
            offset = math.floor(float(data['longitude']) / 15)
            loc = time.localtime(utc + offset * 3600)
            data['utc_datetime'] = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(y,mo,day,h,m,s)
            data['local_datetime'] = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(loc[0],loc[1],loc[2],loc[3],loc[4],loc[5])
        except: data['utc_datetime'] = data['local_datetime'] = None
        return data

    def parse_vtg(self, sentence_list):
        if not sentence_list: return
        f = sentence_list[0].split(',')
        keys = ['course_over_ground_t', 'reference_t', 'course_over_ground_m', 'reference_m', 'speed_knots', 'units_knots', 'speed_kmh', 'units_kmh', 'mode_indicator']
        defaults = ['0.0', 'T', '0.0', 'M', '0.0', 'N', '0.0', 'K', '']
        return {k: self._safe_get(f, i+1, defaults[i]) for i, k in enumerate(keys)}

    def parse_gst(self, sentence_list):
        if not sentence_list: return
        f = sentence_list[0].split(',')
        return {'timestamp': self._safe_get(f, 1, '000000.0'), 'rms': self._safe_get(f, 2, '0.0'), 'std_lat': self._safe_get(f, 6, '0.0'), 'std_lon': self._safe_get(f, 7, '0.0'), 'std_alt': self._safe_get(f, 8, '0.0')}

    def parse_dhv(self, sentence_list):
        if not sentence_list: return
        f = sentence_list[0].split(',')
        return {k: self._safe_get(f, i+1, None) for i, k in enumerate(['timestamp', '3d_speed', 'ecef_x_speed', 'ecef_y_speed', 'ecef_z_speed', 'horizontal_ground_speed'])}

    def parse_gns(self, sentence_list):
        if not sentence_list: return
        f = sentence_list[0].split(',')
        keys = ['utc_time','latitude','longitude','mode_indicator','use_sv','hdop','msl','geoid_alt','age_of_differential_data','station_id']
        map_idx = [1, 2, 4, 6, 7, 8, 9, 11, 13, 14]
        res = {k: self._safe_get(f, map_idx[i], '0.0') for i, k in enumerate(keys)}
        res['latitude'] = self.convert_to_degrees(self._safe_get(f, 2), self._safe_get(f, 3))
        res['longitude'] = self.convert_to_degrees(self._safe_get(f, 4), self._safe_get(f, 5))
        return res

    def parse_txt(self, sentence_list):
        if not sentence_list: return
        f = sentence_list[0].split(',')
        return {k: self._safe_get(f, i+1, None) for i, k in enumerate(['several_lines', 'free', 'type', 'text'])}

    def detect_system(self, info, system='QZS'):
        output = []
        for temp_s in info:
            if temp_s['type'] in ('GP', 'GN'):
                prn = int(temp_s['prn'])
                if system == 'QZS' and 193 <= prn <= 210:
                    temp_s['type'] = 'QZS'
                elif system == 'SBAS' and 33 <= prn <= 64:
                    temp_s['type'] = 'SBAS'
                    temp_s['prn'] = prn + 87
            output.append(temp_s)
        return output

    def qzss_detect(self, info):
        return self.detect_system(info, 'QZS')

    def sbas_detect(self, info):
        return self.detect_system(info, 'SBAS')
    
    def tolist(self, data):
        return '\r\n'.join(['$' + s for s in str(data).split('$') if s]) + '\r\n'

    def analyze_sentence(self, sentence, just="gga gll rmc vtg gst dhv zda gns txt gsa gsv"):
        self._parse_single_sentence(sentence)
        pd = self.parsed_data
        if 'gga' in just:
            if pd['GGA']: self.GGA = self.parse_gga(pd['GGA'])
        if 'gll' in just:
            if pd['GLL']: self.GLL = self.parse_gll(pd['GLL'])
        if 'rmc' in just:
            if pd['RMC']: self.RMC = self.parse_rmc(pd['RMC'])
        if 'vtg' in just:
            if pd['VTG']: self.VTG = self.parse_vtg(pd['VTG'])
        if 'gst' in just:
            if pd['GST']: self.GST = self.parse_gst(pd['GST'])
        if 'dhv' in just:
            if pd['DHV']: self.DHV = self.parse_dhv(pd['DHV'])
        if 'zda' in just:
            if pd['ZDA']: self.ZDA = self.parse_zda(pd['ZDA'])
        if 'gns' in just:
            if pd['GNS']: self.GNS = self.parse_gns(pd['GNS'])
        if 'txt' in just:
            if pd['TXT']: self.TXT = self.parse_txt(pd['TXT'])
        if 'gsa' in just:
            if pd['GSA']:
                for s in pd['GSA']:
                    talker = s[1:3]
                    if talker in self._gsa_buffer:
                        self._gsa_buffer[talker].append(s)
                        self.GSA = self.merge_gsa([self.parse_gsa(x) for x in self._gsa_buffer[talker]])
        if 'gsv' in just:
            if pd['GSV']:
                for s in pd['GSV']:
                    t = s[1:3]
                    talker = "GB" if t == "BD" else t
                    if talker not in self._gsv_sets: continue
                    f = s.split(',')
                    try:
                        if int(f[2]) == int(f[1]):
                            self._gsv_sets[talker].append([self.parse_gsv(x) for x in self._gsv_buffer[talker] + [s]])
                            self._gsv_buffer[talker].clear()
                            all_gsv = [item for sub in self._gsv_sets[talker] for item in sub]
                            if all_gsv: self.GSV[talker] = self.merge_gsv(all_gsv)
                        else:
                            self._gsv_buffer[talker].append(s)
                    except: pass

    def analyze(self, data, enable_type=(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)):
        self.raw = ''
        keys = ['GGA', 'GLL', 'GSA', 'GSV', 'RMC', 'VTG', 'GST', 'DHV', 'ZDA', 'GNS', 'TXT']
        for key in keys:
            setattr(self, key, [])
            self.parsed_data[key] = []
        try:
            data = str(data)
            data = self.tolist(data)
            self.parse_nmea_sentences(data)
        except Exception as e:
            print(f"Error during parsing sentences: {e}")
        parsed_data = self.parsed_data
        for key in ['GGA', 'GLL', 'RMC', 'VTG', 'GST', 'DHV', 'ZDA', 'TXT', 'GNS']:
            try:
                parse_func = getattr(self, f'parse_{key.lower()}')
                setattr(self, key, parse_func(parsed_data.get(key, [])))
            except Exception as e:
                print(f"Error parsing {key}: {e}")
        if parsed_data.get('GSA', []) and enable_type[8]:
            try:
                gsa_list = [self.parse_gsa(s) for s in parsed_data['GSA']]
                self.GSA = self.merge_gsa(gsa_list) if gsa_list else self.parse_gsa('')
            except Exception as e:
                print(f"Error parsing/merging GSA: {e}")
        if parsed_data.get('GSV', []) and enable_type[9]:
            try:
                gsv_list = [self.parse_gsv(s) for s in parsed_data['GSV']]
                self.GSV = self.merge_gsv(gsv_list) if gsv_list else self.parse_gsv('')
            except Exception as e:
                print(f"Error parsing/merging GSV: {e}")
