# Version 3.7
# Supports only CPython
import re
import time
import math
import sys
from decimal import *

class pygps2:
    def __init__(self, op0=True, op1=True, op2=True, op3=True, op4=True):
        # Options
        self.OBTAIN_IDENTIFLER_FROM_GSA = op0
        self.IN_BAND_DATA_INTO_GSV = op1
        self.DETECT_CONVERT_QZS = op2
        self.DETECT_CONVERT_SBAS = op3
        self.ENABLE_CHECKSUM = op4

        self.raw = ''
        self.GGA = []
        self.GLL = []
        self.GSA = []
        # GSV has been changed to a dictionary per talker.
        self.GSV = {
            "GP": None,
            "GL": None,
            "GA": None,
            "GB": None,
            "GQ": None,
            "GN": None,
        }
        self.RMC = []
        self.VTG = []
        self.GST = []
        self.DHV = []
        self.ZDA = []
        self.GNS = []
        self.TXT = []
        self.parsed_data = {
            'GGA': [], 'GLL': [], 'GSA': [], 'GSV': [],
            'RMC': [], 'VTG': [], 'GST': [], 'DHV': [],
            'ZDA': [], 'GNS': [], 'TXT': [], 'Other': []
        }
        self.patterns = {
            'GGA': re.compile(r'\$GNGGA,.*?\*..|\$GPGGA,.*?\*..|\$BDGGA,.*?\*..'),
            'GLL': re.compile(r'\$GNGLL,.*?\*..|\$GPGLL,.*?\*..|\$BDGLL,.*?\*..'),
            'GSA': re.compile(r'\$GNGSA,.*?\*..|\$GPGSA,.*?\*..|\$BDGSA,.*?\*..'),
            'GSV': re.compile(r'\$GPGSV,.*?\*..|\$GBGSV,.*?\*..|\$GQGSV,.*?\*..|\$GLGSV,.*?\*..|\$GAGSV,.*?\*..\$BDGSV,.*?\*..|'),
            'RMC': re.compile(r'\$GNRMC,.*?\*..|\$GPRMC,.*?\*..|\$BDRMC,.*?\*..'),
            'VTG': re.compile(r'\$GNVTG,.*?\*..|\$GPVTG,.*?\*..|\$BDVTG,.*?\*..'),
            'GST': re.compile(r'\$GNGST,.*?\*..|\$GPGST,.*?\*..|\$BDGST,.*?\*..'),
            'DHV': re.compile(r'\$GNDHV,.*?\*..|\$GPDHV,.*?\*..|\$BDDHV,.*?\*..'),
            'ZDA': re.compile(r'\$GNZDA,.*?\*..|\$GPZDA,.*?\*..|\$BDZDA,.*?\*..'),
            'GNS': re.compile(r'\$GNGNS,.*?\*..|\$GPGNS,.*?\*..'),
            'TXT': re.compile(r'\$GNTXT,.*?\*..|\$GPTXT,.*?\*..|\$BDTXT,.*?\*..')
        }
        # buffer for GSV sentences by talker (e.g., "GP", "GL", etc.) to collect multi-part messages
        self._gsv_buffer = {
            "GP": [], "GL": [], "GA": [], "GB": [], "GQ": [], "GN": []
        }
        self._gsv_sets = {
            "GP": [], "GL": [], "GA": [], "GB": [], "GQ": [], "GN": []
        }
        self._gsa_buffer = {
            "GP": [], "GL": [], "GA": [], "GB": [], "GQ": [], "GN": []
        }

    def convert_to_degrees(self, coord, direction):
        if sys.implementation.name == 'cpython':
            try:
                if not coord:
                    return str(Decimal('0.0'))
                degree_len = 2 if direction in ('N', 'S') else 3 if direction in ('E', 'W') else 0
                if degree_len == 0:
                    return str(Decimal('0.0'))
                degrees = Decimal(coord[:degree_len])
                minutes = Decimal(coord[degree_len:]) if len(coord) > degree_len else Decimal('0.0')
                decimal_degrees = degrees + minutes / Decimal('60.0')
                if direction in ('S', 'W'):
                    decimal_degrees = -decimal_degrees
                return str(decimal_degrees)
            except Exception as e:
                print(f'Error in coordinate conversion: {e}')
                return str(Decimal('0.0'))

    def verify_checksum(self, sentence):
        if '*' not in sentence:
            return False
        data, checksum = sentence.split('*')
        chk = 0
        for c in data[1:]:
            chk ^= ord(c)
        return f'{chk:02X}' == checksum.strip().upper()

    def parse_nmea_sentences(self, nmea_data):
        for k in self.parsed_data:
            self.parsed_data[k] = []
        for s in nmea_data.split('\r\n'):
            s = s.strip()
            if not s:
                continue
            if self.ENABLE_CHECKSUM and not self.verify_checksum(s):
                continue
            for k, p in self.patterns.items():
                if p.match(s):
                    self.parsed_data[k].append(s)
                    break
            else:
                if s:
                    self.parsed_data['Other'].append(s)

    def parse_gga(self, sentence):
        if not sentence:
            return
        f = sentence[0].split(',')
        return {
            'timestamp': f[1] if len(f) > 1 and f[1] else '000000.0',
            'latitude': self.convert_to_degrees(f[2], f[3]) if len(f) > 3 and f[2] and f[3] else 0.0,
            'longitude': self.convert_to_degrees(f[4], f[5]) if len(f) > 5 and f[4] and f[5] else 0.0,
            'gps_quality': f[6] if len(f) > 6 and f[6] else '0',
            'num_satellites': f[7] if len(f) > 7 and f[7] else '0',
            'hdop': f[8] if len(f) > 8 and f[8] else '0.0',
            'altitude': f[9] if len(f) > 9 and f[9] else '0.0',
            'altitude_units': f[10] if len(f) > 10 and f[10] else 'M',
            'geoid_height': f[11] if len(f) > 11 and f[11] else '0.0',
            'geoid_units': f[12] if len(f) > 12 and f[12] else 'M',
            'dgps_age': f[13] if len(f) > 13 and f[13] else '',
            'dgps_station_id': f[14].split('*')[0] if len(f) > 14 and f[14] else ''
        }

    def parse_gll(self, sentence):
        if not sentence:
            return
        f = sentence[0].split(',')
        return {
            'latitude': self.convert_to_degrees(f[1], f[2]) if len(f) > 2 and f[1] and f[2] else 0.0,
            'longitude': self.convert_to_degrees(f[3], f[4]) if len(f) > 4 and f[3] and f[4] else 0.0,
            'timestamp': f[5] if len(f) > 5 and f[5] else '000000.0',
            'status': f[6] if len(f) > 6 and f[6] else 'V',
            'mode_indicator': f[7].split('*')[0] if len(f) > 7 and f[7] else ''
        }

    def parse_gsa(self, sentence):
        if not sentence:
            return
        f = sentence.split(',')
        sats = []
        for i in range(3, 15):
            if len(f) > i and f[i]:
                if self.OBTAIN_IDENTIFLER_FROM_GSA:
                    sats.append((f[i], f[18].split('*')[0]))
                else:
                    sats.append(f[i])
            else:
                sats.append('0')
        return {
            'fix_select': f[1] if len(f) > 1 and f[1] else 'A',
            'fix_status': f[2] if len(f) > 2 and f[2] else '1',
            'satellites_used': sats,
            'pdop': f[15] if len(f) > 15 and f[15] else '0.0',
            'hdop': f[16] if len(f) > 16 and f[16] else '0.0',
            'vdop': f[17].split('*')[0] if len(f) > 17 and f[17] else '0.0'
        }

    def parse_gsv(self, sentence):
        if not sentence:
            return
        f = sentence.split(',')
        sys_type = sentence[1:3]
        data = {
            'system_type': sys_type,
            'num_messages': f[1] if len(f) > 1 and f[1] else '1',
            'message_num': f[2] if len(f) > 2 and f[2] else '1',
            'num_satellites': f[3] if len(f) > 3 and f[3] else '0',
            'satellites_info': []
        }
        band = f[-1].split('*')[0] if self.IN_BAND_DATA_INTO_GSV else 0
        for i in range(4, len(f) - 4, 4):
            prn = f[i].strip() if f[i] else '0'
            elev = f[i+1].strip() if f[i+1] else '0.0'
            azim = f[i+2].strip() if f[i+2] else '0.0'
            snr_raw = f[i+3].strip() if f[i+3] else '0.0'
            snr = snr_raw.split('*')[0] if '*' in snr_raw else snr_raw
            data['satellites_info'].append({
                'prn': prn,
                'type': sys_type,
                'elevation': elev,
                'azimuth': azim,
                'snr': snr,
                'band': band
            })
        return data

    def parse_zda(self, sentence):
        if not sentence:
            return
        f = sentence[0].split(',')
        return {
            'timestamp': f[1] if len(f) > 1 else None,
            'day': f[2] if len(f) > 2 else None,
            'month': f[3] if len(f) > 3 else None,
            'year': f[4] if len(f) > 4 else None,
            'timezone_offset_hour': f[5] if len(f) > 5 else None,
            'timezone_offset_minute': f[6].split('*')[0] if len(f) > 6 and '*' in f[6] else None
        }

    def merge_gsa(self, gsa_list):
        if not gsa_list:
            return self.parse_gsa('')
        merged = {
            'fix_select': gsa_list[0].get('fix_select', 'A'),
            'fix_status': gsa_list[0].get('fix_status', '1')
        }
        sats = [s for gsa in gsa_list for s in gsa.get('satellites_used', []) if s not in ('0', '')]
        merged['satellites_used'] = list(dict.fromkeys(sats))

        def avg(lst):
            try:
                return str(sum(map(float, lst)) / len(lst))
            except:
                return '0.0'

        merged['pdop'] = avg([g.get('pdop', '0.0') for g in gsa_list if g.get('pdop', '0.0') != '0.0']) or '0.0'
        merged['hdop'] = avg([g.get('hdop', '0.0') for g in gsa_list if g.get('hdop', '0.0') != '0.0']) or '0.0'
        merged['vdop'] = avg([g.get('vdop', '0.0') for g in gsa_list if g.get('vdop', '0.0') != '0.0']) or '0.0'
        return merged

    def merge_gsv(self, gsv_list):
        if not gsv_list:
            return self.parse_gsv('')
        merged = {
            'num_messages': str(len(gsv_list)),
            'message_num': '1'
        }
        try:
            merged['num_satellites'] = str(max(int(g.get('num_satellites', '0')) for g in gsv_list))
        except:
            merged['num_satellites'] = '0'

        sats = [s for g in gsv_list for s in g.get('satellites_info', [])]
        unique = {}
        for s in sats:
            key = (s['prn'], s['type'], s['elevation'], s['azimuth'])
            if key not in unique:
                unique[key] = {k: s[k] for k in ['prn', 'type', 'elevation', 'azimuth', 'snr']}
                unique[key]['band'] = [int(s['band'])]
                unique[key]['snr'] = [float(s['snr'])]
            else:
                unique[key]['band'].append(int(s['band']))
                unique[key]['snr'].append(float(s['snr']))
        merged['satellites_info'] = list(unique.values())

        if self.DETECT_CONVERT_QZS:
            merged['satellites_info'] = self.qzss_detect(merged['satellites_info'])
        if self.DETECT_CONVERT_SBAS:
            merged['satellites_info'] = self.sbas_detect(merged['satellites_info'])
        return merged

    def parse_rmc(self, sentence):
        if not sentence:
            return
        f = sentence[0].split(',')
        data = {
            'timestamp': f[1] if len(f) > 1 and f[1] else '000000.0',
            'status': f[2] if len(f) > 2 and f[2] else 'V',
            'latitude': self.convert_to_degrees(f[3], f[4]) if len(f) > 4 and f[3] and f[4] else 0.0,
            'longitude': self.convert_to_degrees(f[5], f[6]) if len(f) > 6 and f[5] and f[6] else 0.0,
            'speed_over_ground': f[7] if len(f) > 7 and f[7] else '0.0',
            'course_over_ground': f[8] if len(f) > 8 and f[8] else '0.0',
            'date': f[9] if len(f) > 9 and f[9] else '010100',
            'magnetic_variation': f[10] if len(f) > 10 and f[10] else '0.0',
            'mag_var_direction': f[11] if len(f) > 11 and f[11] else '',
            'mode_indicator': f[12].split('*')[0] if len(f) > 12 and f[12] else ''
        }
        if data['timestamp'] and data['date']:
            try:
                h, m, s = int(data['timestamp'][0:2]), int(data['timestamp'][2:4]), int(data['timestamp'][4:6])
                d, mo, y = int(data['date'][0:2]), int(data['date'][2:4]), int(data['date'][4:6]) + 2000
                if sys.implementation.name == 'cpython':
                    utc = time.mktime((y, mo, d, h, m, s, 0, 0, 0))
                else:
                    utc = time.mktime((y, mo, d, h, m, s, 0, 0))
                offset = math.floor(float(str(data['longitude'])) / 15)
                local = time.localtime(utc + offset * 3600)
                data['utc_datetime'] = f'{y:04d}-{mo:02d}-{d:02d} {h:02d}:{m:02d}:{s:02d}'
                data['local_datetime'] = f'{local[0]:04d}-{local[1]:02d}-{local[2]:02d} {local[3]:02d}:{local[4]:02d}:{local[5]:02d}'
            except Exception as e:
                print('Error parsing RMC data:', e)
                data['utc_datetime'] = None
                data['jst_datetime'] = None
        return data

    def parse_vtg(self, sentence):
        if not sentence:
            return
        f = sentence[0].split(',')
        return {
            'course_over_ground_t': f[1] if len(f) > 1 and f[1] else '0.0',
            'reference_t': f[2] if len(f) > 2 and f[2] else 'T',
            'course_over_ground_m': f[3] if len(f) > 3 and f[3] else '0.0',
            'reference_m': f[4] if len(f) > 4 and f[4] else 'M',
            'speed_knots': f[5] if len(f) > 5 and f[5] else '0.0',
            'units_knots': f[6] if len(f) > 6 and f[6] else 'N',
            'speed_kmh': f[7] if len(f) > 7 and f[7] else '0.0',
            'units_kmh': f[8] if len(f) > 8 and f[8] else 'K',
            'mode_indicator': f[9].split('*')[0] if len(f) > 9 and f[9] else ''
        }

    def parse_gst(self, sentence):
        if not sentence:
            return
        f = sentence[0].split(',')
        return {
            'timestamp': f[1] if len(f) > 1 and f[1] else '000000.0',
            'rms': f[2] if len(f) > 2 and f[2] else '0.0',
            'std_lat': f[6] if len(f) > 6 and f[6] else '0.0',
            'std_lon': f[7] if len(f) > 7 and f[7] else '0.0',
            'std_alt': f[8].split('*')[0] if len(f) > 8 and f[8] else '0.0'
        }

    def parse_dhv(self, sentence):
        if not sentence:
            return
        f = sentence[0].split(',')
        return {
            'timestamp': f[1] if len(f) > 1 else None,
            '3d_speed': f[2] if len(f) > 2 else None,
            'ecef_x_speed': f[3] if len(f) > 3 else None,
            'ecef_y_speed': f[4] if len(f) > 4 else None,
            'ecef_z_speed': f[5] if len(f) > 5 else None,
            'horizontal_ground_speed': f[6].split('*')[0] if len(f) > 6 and '*' in f[6] else None
        }

    def parse_gns(self, sentence):
        if not sentence:
            return
        f = sentence[0].split(',')
        return {
            'utc_time': f[1] if len(f) > 1 and f[1] else '000000.0',
            'latitude': self.convert_to_degrees(f[2], f[3]) if len(f) > 3 and f[2] and f[3] else 0.0,
            'longitude': self.convert_to_degrees(f[4], f[5]) if len(f) > 5 and f[4] and f[5] else 0.0,
            'mode_indicator': f[6] if len(f) > 6 and f[6] else 'N',
            'use_sv': f[7] if len(f) > 7 and f[7] else '0',
            'hdop': f[8] if len(f) > 8 and f[8] else '0.0',
            'msl': f[9] if len(f) > 9 and f[9] else '0.0',
            'geoid_alt': f[11] if len(f) > 11 and f[11] else '0.0',
            'age_of_differential_data': f[13] if len(f) > 13 and f[13] else '0.0',
            'station_id': f[14] if len(f) > 14 and f[14] else '0000'
        }

    def parse_txt(self, sentence):
        if not sentence:
            return
        f = sentence[0].split(',')
        return {
            'several_lines': f[1] if len(f) > 1 else None,
            'free': f[2] if len(f) > 2 else None,
            'type': f[3] if len(f) > 3 else None,
            'text': f[4].split('*')[0] if len(f) > 4 and '*' in f[4] else None
        }

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

    def analyze(self, data, enable_type=(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)):
        self.raw = ''
        keys = ['GGA', 'GLL', 'GSA', 'GSV', 'RMC', 'VTG', 'GST', 'DHV', 'ZDA', 'GNS', 'TXT']
        for key in keys:
            if key == 'GSV':
                self.GSV = {"GP": None, "GL": None, "GA": None, "GB": None, "GQ": None, "GN": None}
            else:
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
                # merge
                merged = self.merge_gsv(gsv_list) if gsv_list else self.parse_gsv('')
                self.GSV["GN"] = merged
            except Exception as e:
                print(f"Error parsing/merging GSV: {e}")
    # Stream Analyze: Handle sentences one by one and update internal state incrementally.
    def _handle_gsv_sentence(self, sentence):
        talker = sentence[1:3]  # "GP", "GB", "GL", "GA", "GN", etc.
        f = sentence.split(',')
        try:
            total = int(f[1])
            num = int(f[2])
        except Exception:
            return

        if talker not in self._gsv_buffer:
            self._gsv_buffer[talker] = []
        if talker not in self._gsv_sets:
            self._gsv_sets[talker] = []

        self._gsv_buffer[talker].append(sentence)
        # Once a complete set is assembled, analyze it and add it to the setlist, merging it if necessary.
        if num == total:
            try:
                gsv_list = [self.parse_gsv(s) for s in self._gsv_buffer[talker]]
                # このセットを talker ごとのセットリストに追加
                self._gsv_sets[talker].append(gsv_list)
            except Exception as e:
                print("Error in GSV set parse:", e)
            self._gsv_buffer[talker] = []
            # Make one merged GSV from all sets for this talker
            try:
                all_gsv = []
                for gsv_set in self._gsv_sets[talker]:
                    all_gsv.extend(gsv_set)
                if all_gsv:
                    merged = self.merge_gsv(all_gsv)
                    self.GSV[talker] = merged
            except Exception as e:
                print("Error in GSV merge:", e)

    def _handle_gsa_sentence(self, sentence):
        talker = sentence[1:3]
        if talker not in self._gsa_buffer:
            self._gsa_buffer[talker] = []
        self._gsa_buffer[talker].append(sentence)
        try:
            gsa_list = [self.parse_gsa(s) for s in self._gsa_buffer[talker]]
            self.GSA = self.merge_gsa(gsa_list)
        except Exception as e:
            print("Error in GSA merge:", e)

    def analyze_sentence(self, sentence):
        """
        For Stream Analyze
        """
        try:
            self.parse_nmea_sentences(sentence)
        except Exception as e:
            print(f"Error during parsing single sentence: {e}")
            return

        pd = self.parsed_data

        if pd['GGA']:
            try:
                self.GGA = self.parse_gga(pd['GGA'])
            except Exception as e:
                print("Error parsing GGA:", e)

        if pd['GLL']:
            try:
                self.GLL = self.parse_gll(pd['GLL'])
            except Exception as e:
                print("Error parsing GLL:", e)

        if pd['RMC']:
            try:
                self.RMC = self.parse_rmc(pd['RMC'])
            except Exception as e:
                print("Error parsing RMC:", e)

        if pd['VTG']:
            try:
                self.VTG = self.parse_vtg(pd['VTG'])
            except Exception as e:
                print("Error parsing VTG:", e)

        if pd['GST']:
            try:
                self.GST = self.parse_gst(pd['GST'])
            except Exception as e:
                print("Error parsing GST:", e)

        if pd['DHV']:
            try:
                self.DHV = self.parse_dhv(pd['DHV'])
            except Exception as e:
                print("Error parsing DHV:", e)

        if pd['ZDA']:
            try:
                self.ZDA = self.parse_zda(pd['ZDA'])
            except Exception as e:
                print("Error parsing ZDA:", e)

        if pd['GNS']:
            try:
                self.GNS = self.parse_gns(pd['GNS'])
            except Exception as e:
                print("Error parsing GNS:", e)

        if pd['TXT']:
            try:
                self.TXT = self.parse_txt(pd['TXT'])
            except Exception as e:
                print("Error parsing TXT:", e)

        if pd['GSA']:
            for s in pd['GSA']:
                self._handle_gsa_sentence(s)

        if pd['GSV']:
            for s in pd['GSV']:
                self._handle_gsv_sentence(s)
