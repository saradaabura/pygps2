#Version 3.5
import re
import time
import math
import sys
from decimal import *

class pygps2:
    def __init__(self, op0=True, op1=True, op2=True):
        # Options
        self.OBTAIN_IDENTIFLER_FROM_GSA = op0
        #Possibly useful for modules using two or more satellite systems

        self.IN_BAND_DATA_INTO_GSV = op1

        #dev
        self.DETECT_CONVERT_QZS = op2
        
        
        self.raw = ''
        self.GGA = []
        self.GLL = []
        self.GSA = []
        self.GSV = []
        self.RMC = []
        self.VTG = []
        self.GST = []
        self.DHV = []
        self.ZDA = []
        self.GNS = []
        self.TXT = []
        self.parsed_data = {'GGA': [], 'GLL': [], 'GSA': [], 'GSV': [], 'RMC': [], 'VTG': [], 'GST': [], 'DHV': [], 'ZDA': [], 'GNS': [], 'TXT': [], 'Other': []}
        self.patterns = {
        'GGA': re.compile(r'\$GNGGA,.*?\*..|\$GPGGA,.*?\*..|\$BDGGA,.*?\*..'),
        'GLL': re.compile(r'\$GNGLL,.*?\*..|\$GPGLL,.*?\*..|\$BDGLL,.*?\*..'),
        'GSA': re.compile(r'\$GNGSA,.*?\*..|\$GPGSA,.*?\*..|\$BDGSA,.*?\*..'),
        'GSV': re.compile(r'\$GPGSV,.*?\*..|\$BDGSV,.*?\*..|\$GQGSV,.*?\*..|\$GLGSV,.*?\*..|\$GAGSV,.*?\*..|\$GBGSV,.*?\*..'),
        'RMC': re.compile(r'\$GNRMC,.*?\*..|\$GPRMC,.*?\*..|\$BDRMC,.*?\*..'),
        'VTG': re.compile(r'\$GNVTG,.*?\*..|\$GPVTG,.*?\*..|\$BDVTG,.*?\*..'),
        'GST': re.compile(r'\$GNGST,.*?\*..|\$GPGST,.*?\*..|\$BDGST,.*?\*..'),
        'DHV': re.compile(r'\$GNDHV,.*?\*..|\$GPDHV,.*?\*..|\$BDDHV,.*?\*..'),
        'ZDA': re.compile(r'\$GNZDA,.*?\*..|\$GPZDA,.*?\*..|\$BDZDA,.*?\*..'),
        'GNS': re.compile(r'\$GNGNS,.*?\*..|\$GPGNS,.*?\*..'),
        'TXT': re.compile(r'\$GNTXT,.*?\*..|\$GPTXT,.*?\*..|\$BDTXT,.*?\*..')
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
        if sys.implementation.name == 'micropython':
            try:
                if not coord:
                    return str(DecimalNumber('0.0'))
                degree_len = 2 if direction in ('N', 'S') else 3 if direction in ('E', 'W') else 0
                if degree_len == 0:
                    return str(DecimalNumber('0.0'))
                degrees = DecimalNumber(coord[:degree_len])
                minutes = DecimalNumber(coord[degree_len:]) if len(coord) > degree_len else DecimalNumber('0.0')
                decimal_degrees = degrees + minutes / DecimalNumber('60.0')
                if direction in ('S', 'W'):
                    decimal_degrees = -decimal_degrees
                return str(decimal_degrees)
            except Exception as e:
                print(f'Error in coordinate conversion: {e}')
                return str(DecimalNumber('0.0'))

    def verify_checksum(self, sentence):
        if '*' not in sentence:
            return False
        data, checksum = sentence.split('*')
        calculated_checksum = 0
        for char in data[1:]:
            calculated_checksum ^= ord(char)
        return f'{calculated_checksum:02X}' == checksum.strip().upper()

    def parse_nmea_sentences(self, nmea_data):
        sentences = nmea_data.split('\r\n')
        parsed_data = {key: [] for key in self.patterns.keys()}
        parsed_data['Other'] = []
        for sentence in sentences:
            sentence = sentence.strip()
            if not self.verify_checksum(sentence):
                continue
            matched = False
            for key, self.pattern in self.patterns.items():
                if self.pattern.match(sentence):
                    self.parsed_data[key].append(sentence)
                    matched = True
                    break
            if not matched and sentence:
                self.parsed_data['Other'].append(sentence)
        del sentences

    def parse_gga(self, sentence):
        if sentence == []:
            return
        fields = sentence[0].split(',')
        data = {
            'timestamp': fields[1] if len(fields) > 1 and fields[1] else '000000.0',
            'latitude': self.convert_to_degrees(fields[2], fields[3]) if len(fields) > 3 and fields[2] and fields[3] else 0.0,
            'longitude': self.convert_to_degrees(fields[4], fields[5]) if len(fields) > 5 and fields[4] and fields[5] else 0.0,
            'gps_quality': fields[6] if len(fields) > 6 and fields[6] else '0',
            'num_satellites': fields[7] if len(fields) > 7 and fields[7] else '0',
            'hdop': fields[8] if len(fields) > 8 and fields[8] else '0.0',
            'altitude': fields[9] if len(fields) > 9 and fields[9] else '0.0',
            'altitude_units': fields[10] if len(fields) > 10 and fields[10] else 'M',
            'geoid_height': fields[11] if len(fields) > 11 and fields[11] else '0.0',
            'geoid_units': fields[12] if len(fields) > 12 and fields[12] else 'M',
            'dgps_age': fields[13] if len(fields) > 13 and fields[13] else '',
            'dgps_station_id': fields[14].split('*')[0] if len(fields) > 14 and fields[14] else ''
        }
        del fields
        return data

    def parse_gll(self, sentence):
        if sentence == []:
            return
        fields = sentence[0].split(',')
        data = {
            'latitude': self.convert_to_degrees(fields[1], fields[2]) if len(fields) > 2 and fields[1] and fields[2] else 0.0,
            'longitude': self.convert_to_degrees(fields[3], fields[4]) if len(fields) > 4 and fields[3] and fields[4] else 0.0,
            'timestamp': fields[5] if len(fields) > 5 and fields[5] else '000000.0',
            'status': fields[6] if len(fields) > 6 and fields[6] else 'V',
            'mode_indicator': fields[7].split('*')[0] if len(fields) > 7 and fields[7] else ''
        }
        del fields
        return data

    def parse_gsa(self, sentence):
        if sentence == []:
            return
        fields = sentence.split(',')
        satellites_used = []
        for i in range(3, 15):
            if len(fields) > i and fields[i]:
                if self.OBTAIN_IDENTIFLER_FROM_GSA == True:
                    satellites_used.append((fields[i], fields[18].split('*')[0]))
                else:
                    satellites_used.append((fields[i]))
            else:
                satellites_used.append('0')
        data = {
            'fix_select': fields[1] if len(fields) > 1 and fields[1] else 'A',
            'fix_status': fields[2] if len(fields) > 2 and fields[2] else '1',
            'satellites_used': satellites_used,
            'pdop': fields[15] if len(fields) > 15 and fields[15] else '0.0',
            'hdop': fields[16] if len(fields) > 16 and fields[16] else '0.0',
            'vdop': fields[17].split('*')[0] if len(fields) > 17 and fields[17] else '0.0'
        }
        del fields
        return data
    def parse_gsv(self, sentence):
        if sentence == []:
            return
        fields = sentence.split(',')
        system_type = sentence[1:3]
        data = {
            'system_type': system_type,
            'num_messages': fields[1] if len(fields) > 1 and fields[1] else '1',
            'message_num': fields[2] if len(fields) > 2 and fields[2] else '1',
            'num_satellites': fields[3] if len(fields) > 3 and fields[3] else '0',
            'satellites_info': []
        }
        index = 4
        while index + 3 < len(fields) - 1:
            prn = fields[index].strip() if len(fields) > index and fields[index] else '0'
            elevation = fields[index+1].strip() if len(fields) > index+1 and fields[index+1] else '0.0'
            azimuth = fields[index+2].strip() if len(fields) > index+2 and fields[index+2] else '0.0'
            snr_field = fields[index+3].strip() if len(fields) > index+3 and fields[index+3] else '0.0'
            snr = snr_field.split('*')[0] if '*' in snr_field else snr_field
            if self.IN_BAND_DATA_INTO_GSV == True:
                band = fields[len(fields) - 1].split('*')[0]
            else:
                band = 0
            data['satellites_info'].append({
                'prn': prn,
                'type': system_type,
                'elevation': elevation,
                'azimuth': azimuth,
                'snr': snr,
                'band': band
            })
            index += 4
        del fields
        return data

    def parse_zda(self, sentence):
        if sentence == []:
            return
        fields = sentence[0].split(',')
        data = {
            'timestamp': fields[1] if len(fields) > 1 else None,
            'day': fields[2] if len(fields) > 2 else None,
            'month': fields[3] if len(fields) > 3 else None,
            'year': fields[4] if len(fields) > 4 else None,
            'timezone_offset_hour': fields[5] if len(fields) > 5 else None,
            'timezone_offset_minute': fields[6].split('*')[0] if len(fields) > 6 and '*' in fields[6] else None
        }
        del fields
        return data

    def parse_gns(self, sentence):
        if sentence == []:
            return
        fields = sentence[0].split(',')
        data = {
            'utc_time': fields[1] if len(fields) > 1 and fields[1] else '000000.0',
            'latitude': self.convert_to_degrees(fields[2], fields[3]) if len(fields) > 3 and fields[2] and fields[3] else 0.0,
            'longitude': self.convert_to_degrees(fields[4], fields[5]) if len(fields) > 5 and fields[4] and fields[5] else 0.0,
            'mode_indicator': fields[6] if len(fields) > 6 and fields[6] else 'N',
            'use_sv': fields[7] if len(fields) > 7 and fields[7] else '0',
            'hdop': fields[8] if len(fields) > 8 and fields[8] else '0.0',
            'msl': fields[9] if len(fields) > 9 and fields[9] else '0.0',
            'geoid_alt': fields[11] if len(fields) > 11 and fields[11] else '0.0',
            'age_of_differential_data': fields[13] if len(fields) > 13 and fields[13] else '0.0',
            'station_id': fields[14] if len(fields) > 14 and fields[14] else '0000'
        }
        del fields
        return data

    def merge_gsa(self, gsa_list):
        if not gsa_list:
            return parse_gsa('')
        merged = {}
        merged['fix_select'] = gsa_list[0].get('fix_select', 'A')
        merged['fix_status'] = gsa_list[0].get('fix_status', '1')
        sats = []
        for gsa in gsa_list:
            sats.extend([s for s in gsa.get('satellites_used', []) if s != '0' and s != ''])
        merged['satellites_used'] = list(dict.fromkeys(sats))
        def average(lst):
            try:
                return str(sum(float(x) for x in lst) / len(lst))
            except Exception:
                return '0.0'
        pdops = [gsa.get('pdop', '0.0') for gsa in gsa_list if gsa.get('pdop', '0.0') != '0.0']
        hdops = [gsa.get('hdop', '0.0') for gsa in gsa_list if gsa.get('hdop', '0.0') != '0.0']
        vdops = [gsa.get('vdop', '0.0') for gsa in gsa_list if gsa.get('vdop', '0.0') != '0.0']
        merged['pdop'] = average(pdops) if pdops else '0.0'
        merged['hdop'] = average(hdops) if hdops else '0.0'
        merged['vdop'] = average(vdops) if vdops else '0.0'
        return merged

    def merge_gsv(self, gsv_list):
        if not gsv_list:
            return parse_gsv('')
        merged = {}
        merged['num_messages'] = str(len(gsv_list))
        merged['message_num'] = '1'
        nums = [gsv.get('num_satellites', '0') for gsv in gsv_list if gsv.get('num_satellites', '0')]
        try:
            merged['num_satellites'] = str(max(int(n) for n in nums))
        except Exception:
            merged['num_satellites'] = '0'
        sats = []
        for gsv in gsv_list:
            sats.extend(gsv.get('satellites_info', []))
        unique_satellites = {}
        for sat in sats:
            key = (sat['prn'], sat['type'], sat['elevation'], sat['azimuth'])
            if key not in unique_satellites:
                unique_satellites[key] = {k: sat[k] for k in ['prn', 'type', 'elevation', 'azimuth', 'snr']}
                unique_satellites[key]['band'] = [int(sat['band'])]
            else:
                unique_satellites[key]['band'].append(int(sat['band']))
        merged['satellites_info'] = list(unique_satellites.values())
        if self.DETECT_CONVERT_QZS == True:
            merged['satellites_info'] = self.qzss_detect(merged['satellites_info'])
        return merged
    
    def parse_rmc(self, sentence):
        if sentence == []:
            return
        fields = sentence[0].split(',')
        data = {
            'timestamp': fields[1] if len(fields) > 1 and fields[1] else '000000.0',
            'status': fields[2] if len(fields) > 2 and fields[2] else 'V',
            'latitude': self.convert_to_degrees(fields[3], fields[4]) if len(fields) > 4 and fields[3] and fields[4] else 0.0,
            'longitude': self.convert_to_degrees(fields[5], fields[6]) if len(fields) > 6 and fields[5] and fields[6] else 0.0,
            'speed_over_ground': fields[7] if len(fields) > 7 and fields[7] else '0.0',
            'course_over_ground': fields[8] if len(fields) > 8 and fields[8] else '0.0',
            'date': fields[9] if len(fields) > 9 and fields[9] else '010100',
            'magnetic_variation': fields[10] if len(fields) > 10 and fields[10] else '0.0',
            'mag_var_direction': fields[11] if len(fields) > 11 and fields[11] else '',
            'mode_indicator': fields[12].split('*')[0] if len(fields) > 12 and fields[12] else ''
        }
        if data['timestamp'] and data['date']:
            try:
                hours = int(data['timestamp'][0:2])
                minutes = int(data['timestamp'][2:4])
                seconds = int(data['timestamp'][4:6])
                day = int(data['date'][0:2])
                month = int(data['date'][2:4])
                year = int(data['date'][4:6]) + 2000
                if sys.implementation.name == 'cpython':
                    utc_seconds = time.mktime((year, month, day, hours, minutes, seconds, 0, 0, 0))
                if sys.implementation.name == 'micropython':
                    utc_seconds = time.mktime((year, month, day, hours, minutes, seconds, 0, 0))
                localtime = math.floor(float(str(data['longitude'])) / 15)
                local_seconds = utc_seconds + localtime * 3600
                local_time = time.localtime(local_seconds)
                data['utc_datetime'] = '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(
                    year, month, day, hours, minutes, seconds
                )
                data['local_datetime'] = '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(
                    local_time[0], local_time[1], local_time[2], local_time[3], local_time[4], local_time[5]
                )
            except Exception as e:
                print('Error parsing RMC data:', e)
                data['utc_datetime'] = None
                data['jst_datetime'] = None
        del fields
        return data

    def parse_vtg(self, sentence):
        if sentence == []:
            return
        fields = sentence[0].split(',')
        data = {
            'course_over_ground_t': fields[1] if len(fields) > 1 and fields[1] else '0.0',
            'reference_t': fields[2] if len(fields) > 2 and fields[2] else 'T',
            'course_over_ground_m': fields[3] if len(fields) > 3 and fields[3] else '0.0',
            'reference_m': fields[4] if len(fields) > 4 and fields[4] else 'M',
            'speed_knots': fields[5] if len(fields) > 5 and fields[5] else '0.0',
            'units_knots': fields[6] if len(fields) > 6 and fields[6] else 'N',
            'speed_kmh': fields[7] if len(fields) > 7 and fields[7] else '0.0',
            'units_kmh': fields[8] if len(fields) > 8 and fields[8] else 'K',
            'mode_indicator': fields[9].split('*')[0] if len(fields) > 9 and fields[9] else ''
        }
        del fields
        return data

    def parse_gst(self, sentence):
        if sentence == []:
            return
        fields = sentence[0].split(',')
        data = {
            'timestamp': fields[1] if len(fields) > 1 and fields[1] else '000000.0',
            'rms': fields[2] if len(fields) > 2 and fields[2] else '0.0',
            'std_lat': fields[6] if len(fields) > 6 and fields[6] else '0.0',
            'std_lon': fields[7] if len(fields) > 7 and fields[7] else '0.0',
            'std_alt': fields[8].split('*')[0] if len(fields) > 8 and fields[8] else '0.0'
        }
        del fields
        return data
    
    def parse_dhv(self, sentence):
        if sentence == []:
            return
        fields = sentence[0].split(',')
        data = {
            'timestamp': fields[1] if len(fields) > 1 else None,
            '3d_speed': fields[2] if len(fields) > 2 else None,
            'ecef_x_speed': fields[3] if len(fields) > 3 else None,
            'ecef_y_speed': fields[4] if len(fields) > 4 else None,
            'ecef_z_speed': fields[5] if len(fields) > 5 else None,
            'horizontal_ground_speed': fields[6].split('*')[0] if len(fields) > 6 and '*' in fields[6] else None
        }
        del fields
        return data

    def parse_zda(self, sentence):
        if sentence == []:
            return
        fields = sentence[0].split(',')
        data = {
            'timestamp': fields[1] if len(fields) > 1 else None,
            'day': fields[2] if len(fields) > 2 else None,
            'month': fields[3] if len(fields) > 3 else None,
            'year': fields[4] if len(fields) > 4 else None,
            'timezone_offset_hour': fields[5] if len(fields) > 5 else None,
            'timezone_offset_minute': fields[6].split('*')[0] if len(fields) > 6 and '*' in fields[6] else None
        }
        del fields
        return data

    def parse_gns(self, sentence):
        if sentence == []:
            return
        fields = sentence[0].split(',')
        data = {
            'utc_time': fields[1] if len(fields) > 1 and fields[1] else '000000.0',
            'latitude': self.convert_to_degrees(fields[2], fields[3]) if len(fields) > 3 and fields[2] and fields[3] else 0.0,
            'longitude': self.convert_to_degrees(fields[4], fields[5]) if len(fields) > 5 and fields[4] and fields[5] else 0.0,
            'mode_indicator': fields[6] if len(fields) > 6 and fields[6] else 'N',
            'use_sv': fields[7] if len(fields) > 7 and fields[7] else '0',
            'hdop': fields[8] if len(fields) > 8 and fields[8] else '0.0',
            'msl': fields[9] if len(fields) > 9 and fields[9] else '0.0',
            'geoid_alt': fields[11] if len(fields) > 11 and fields[11] else '0.0',
            'age_of_differential_data': fields[13] if len(fields) > 13 and fields[13] else '0.0',
            'station_id': fields[14] if len(fields) > 14 and fields[14] else '0000'
        }
        del fields
        return data

    def parse_txt(self, sentence):
        if sentence == []:
            return
        fields = sentence[0].split(',')
        data = {
            'several_lines': fields[1] if len(fields) > 1 else None,
            'free': fields[2] if len(fields) > 2 else None,
            'type': fields[3] if len(fields) > 3 else None,
            'text': fields[4].split('*')[0] if len(fields) > 4 and '*' in fields[4] else None
        }
        del fields
        return data

    def qzss_detect(self, info):
        n = len(info)
        nn = 0
        output = []
        while n > nn:
            temp_s = info[nn]
            if temp_s['type'] == 'GP' or temp_s['type'] == 'GN':
                if 193 <= int(temp_s['prn']) <= 210:
                    temp_s['type'] = 'QZS'
            output.append(temp_s)
            nn += 1
        return output
    def tolist(self, data):
            sentences = data.split('$')
            sentences = ['$' + sentence for sentence in sentences if sentence]
            data = '\r\n'.join(sentences) + '\r\n'
            return data
        
    def analyze(self, data, enable_type=(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)):
        self.raw = ''
        self.GGA = []
        self.GLL = []
        self.GSA = []
        self.GSV = []
        self.RMC = []
        self.VTG = []
        self.GST = []
        self.DHV = []
        self.ZDA = []
        self.GNS = []
        self.TXT = []
        self.parsed_data = {'GGA': [], 'GLL': [], 'GSA': [], 'GSV': [], 'RMC': [], 'VTG': [], 'GST': [], 'DHV': [], 'ZDA': [], 'GNS': [], 'TXT': [], 'Other': []}
        
        data = str(data)
        data = self.tolist(data)
        self.parse_nmea_sentences(data)
        parsed_data = self.parsed_data
        self.GGA = self.parse_gga(parsed_data.get('GGA', []))
        self.GLL = self.parse_gll(parsed_data.get('GLL', []))
        self.RMC = self.parse_rmc(parsed_data.get('RMC', []))
        self.VTG = self.parse_vtg(parsed_data.get('VTG', []))
        self.GST = self.parse_gst(parsed_data.get('GST', []))
        self.DHV = self.parse_dhv(parsed_data.get('DHV', []))
        self.ZDA = self.parse_zda(parsed_data.get('ZDA', []))
        self.TXT = self.parse_txt(parsed_data.get('TXT', []))
        self.GNS = self.parse_gns(parsed_data.get('GNS', []))
        if parsed_data['GSA'] != []:
            if enable_type[8] == 1:
                gsa_list = [self.parse_gsa(sentence) for sentence in parsed_data.get('GSA', [])]
                merged_gsa = self.merge_gsa(gsa_list) if gsa_list else self.parse_gsa('')
                self.GSA = merged_gsa
        if parsed_data['GSV'] != []:
            if enable_type[9] == 1:
                gsv_list = [self.parse_gsv(sentence) for sentence in parsed_data.get('GSV', [])]
                merged_gsv = self.merge_gsv(gsv_list) if gsv_list else self.parse_gsv('')
                self.GSV = merged_gsv
        del parsed_data
        del data
