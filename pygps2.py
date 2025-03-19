#pygps2.py Version 2.6
#このプログラムの問題点 / Problems with this program
#1GSVデータを完全に解析することができない(一部解消) / Cannot completely analyze GSV data (partially resolved)
#2すべてのGPSモジュールには対応しない
#ToDo
#1GSVデータの解析を改善する / Improve GSV data analysis
#2他のGPSモジュールにも対応する / Support other GPS modules
#3特定のセンテンスのみを解析できるようにする / Allow analysis of specific sentences only

import re
import time
import math

sts = []

def convert_to_degrees(coord, direction):
    #経緯度変換 / Convert latitude and longitude
    try:
        if not coord:
            return 0.0
        degree_len = 2 if direction in ('N', 'S') else 3 if direction in ('E', 'W') else 0
        if degree_len == 0:
            return 0.0
        degrees = int(coord[:degree_len])
        minutes = float(coord[degree_len:]) if len(coord) > degree_len else 0.0
        decimal_degrees = degrees + minutes / 60.0
        if direction in ('S', 'W'):
            decimal_degrees = -decimal_degrees
        return decimal_degrees
    except Exception:
        return 0.0

#パターン定義 / Pattern definitions
patterns = {
    'GGA': re.compile(r'\$GNGGA,.*?\*..|\$GPGGA,.*?\*..|\$BDGGA,.*?\*..'),
    'GLL': re.compile(r'\$GNGLL,.*?\*..|\$GPGLL,.*?\*..|\$BDGLL,.*?\*..'),
    'GSA': re.compile(r'\$GNGSA,.*?\*..|\$GPGSA,.*?\*..|\$BDGSA,.*?\*..'),
    'GSV': re.compile(r'\$GPGSV,.*?\*..|\$BDGSV,.*?\*..|\$GQGSV,.*?\*..|\$GLGSV,.*?\*..|\$GAGSV,.*?\*..'),
    'RMC': re.compile(r'\$GNRMC,.*?\*..|\$GPRMC,.*?\*..|\$BDRMC,.*?\*..'),
    'VTG': re.compile(r'\$GNVTG,.*?\*..|\$GPVTG,.*?\*..|\$BDVTG,.*?\*..'),
    'GST': re.compile(r'\$GNGST,.*?\*..|\$GPGST,.*?\*..|\$BDGST,.*?\*..'),
    'DHV': re.compile(r'\$GNDHV,.*?\*..|\$GPDHV,.*?\*..|\$BDDHV,.*?\*..'),
    'ZDA': re.compile(r'\$GNZDA,.*?\*..|\$GPZDA,.*?\*..|\$BDZDA,.*?\*..'),
    'TXT': re.compile(r'\$GNTXT,.*?\*..|\$GPTXT,.*?\*..|\$BDTXT,.*?\*..')
}

def parse_nmea_sentences(nmea_data):
    sentences = nmea_data.split('\r\n')
    parsed_data = {key: [] for key in patterns.keys()}
    parsed_data['Other'] = []
    for sentence in sentences:
        sentence = sentence.strip()
        matched = False
        for key, pattern in patterns.items():
            if pattern.match(sentence):
                parsed_data[key].append(sentence)
                matched = True
                break
        if not matched and sentence:
            parsed_data['Other'].append(sentence)
    return parsed_data

# 各解析関数 / Parsing functions
def parse_gga(sentence):
    #GGA解析 / GGA parsing
    fields = sentence.split(',')
    data = {
        'timestamp': fields[1] if len(fields) > 1 and fields[1] else '000000.0',
        'latitude': convert_to_degrees(fields[2], fields[3]) if len(fields) > 3 and fields[2] and fields[3] else 0.0,
        'longitude': convert_to_degrees(fields[4], fields[5]) if len(fields) > 5 and fields[4] and fields[5] else 0.0,
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
    return data

def parse_gll(sentence):
    #GLL解析 / GLL parsing
    fields = sentence.split(',')
    data = {
        'latitude': convert_to_degrees(fields[1], fields[2]) if len(fields) > 2 and fields[1] and fields[2] else 0.0,
        'longitude': convert_to_degrees(fields[3], fields[4]) if len(fields) > 4 and fields[3] and fields[4] else 0.0,
        'timestamp': fields[5] if len(fields) > 5 and fields[5] else '000000.0',
        'status': fields[6] if len(fields) > 6 and fields[6] else 'V',
        'mode_indicator': fields[7].split('*')[0] if len(fields) > 7 and fields[7] else ''
    }
    return data

def parse_gsa(sentence):
    #GSA解析 / GSA parsing
    fields = sentence.split(',')
    satellites_used = []
    for i in range(3, 15):
        if len(fields) > i and fields[i]:
            satellites_used.append(fields[i])
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
    return data

def parse_gsv(sentence):
    #GSV解析 / GSV parsing
    fields = sentence.split(',')
    #センテンスから識別文字を取得し、衛星システムを判別
    #Get the identifier from the sentence and determine the satellite system
    system_type = sentence[1:3]
    global sts
    data = {
        'system_type': system_type,  # 衛星システムの種類
        'num_messages': fields[1] if len(fields) > 1 and fields[1] else '1',
        'message_num': fields[2] if len(fields) > 2 and fields[2] else '1',
        'num_satellites': fields[3] if len(fields) > 3 and fields[3] else '0',
        'satellites_info': []
    }
    #GSVセンテンスを解析,2周波による重複を検出 / Parse GSV sentence, detect duplicates due to dual frequency
    index = 4
    while index + 3 < len(fields) - 1:
        prn = fields[index].strip() if len(fields) > index and fields[index] else '0'
        satellite_id = (system_type, prn)  #衛星識別子 (システムコード, PRN)
        if satellite_id in sts:  #重複チェック
            index += 4  #次の衛星データブロックに移動
            continue
        sts.append((system_type, prn))
        #衛星情報を解析 / Parse satellite information
        elevation = fields[index+1].strip() if len(fields) > index+1 and fields[index+1] else '0.0'
        azimuth = fields[index+2].strip() if len(fields) > index+2 and fields[index+2] else '0.0'
        snr_field = fields[index+3].strip() if len(fields) > index+3 and fields[index+3] else '0.0'
        snr = snr_field.split('*')[0] if '*' in snr_field else snr_field
        data['satellites_info'].append({
            'prn': prn,
            'type': system_type,
            'elevation': elevation,
            'azimuth': azimuth,
            'snr': snr
        })
        index += 4  # 次の衛星データブロックへ
    return data

def parse_rmc(sentence):
    fields = sentence.split(',')
    data = {
        'timestamp': fields[1] if len(fields) > 1 and fields[1] else '000000.0',
        'status': fields[2] if len(fields) > 2 and fields[2] else 'V',
        'latitude': convert_to_degrees(fields[3], fields[4]) if len(fields) > 4 and fields[3] and fields[4] else 0.0,
        'longitude': convert_to_degrees(fields[5], fields[6]) if len(fields) > 6 and fields[5] and fields[6] else 0.0,
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
            utc_seconds = time.mktime((year, month, day, hours, minutes, seconds, 0, 0))
            localtime = math.floor(data['longitude'] / 15)
            local_seconds = utc_seconds + localtime * 3600
            local_time = time.localtime(local_seconds)
            data['utc_datetime'] = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
                year, month, day, hours, minutes, seconds
            )
            data['local_datetime'] = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
                local_time[0], local_time[1], local_time[2], local_time[3], local_time[4], local_time[5]
            )
        except Exception as e:
            print("Error parsing RMC data:", e)
            data['utc_datetime'] = None
            data['jst_datetime'] = None
    return data

def parse_vtg(sentence):
    #VTG解析 / VTG parsing
    fields = sentence.split(',')
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
    return data

def parse_gst(sentence):
    #GST解析 / GST parsing
    fields = sentence.split(',')
    data = {
        'timestamp': fields[1] if len(fields) > 1 and fields[1] else '000000.0',
        'rms': fields[2] if len(fields) > 2 and fields[2] else '0.0',
        'std_lat': fields[6] if len(fields) > 6 and fields[6] else '0.0',
        'std_lon': fields[7] if len(fields) > 7 and fields[7] else '0.0',
        'std_alt': fields[8].split('*')[0] if len(fields) > 8 and fields[8] else '0.0'
    }
    return data

def parse_dhv(sentence):
    #DHV解析 / DHV parsing
    fields = sentence.split(',')
    return {
        'timestamp': fields[1] if len(fields) > 1 else None,
        '3d_speed': fields[2] if len(fields) > 2 else None,
        'ecef_x_speed': fields[3] if len(fields) > 3 else None,
        'ecef_y_speed': fields[4] if len(fields) > 4 else None,
        'ecef_z_speed': fields[5] if len(fields) > 5 else None,
        'horizontal_ground_speed': fields[6].split('*')[0] if len(fields) > 6 and '*' in fields[6] else None
}

def parse_zda(sentence):
    #ZDA解析 / ZDA parsing
    fields = sentence.split(',')
    return {
        'timestamp': fields[1] if len(fields) > 1 else None,
        'day': fields[2] if len(fields) > 2 else None,
        'month': fields[3] if len(fields) > 3 else None,
        'year': fields[4] if len(fields) > 4 else None,
        'timezone_offset_hour': fields[5] if len(fields) > 5 else None,
        'timezone_offset_minute': fields[6].split('*')[0] if len(fields) > 6 and '*' in fields[6] else None
    }

def parse_txt(sentence):
    #TXT解析 / TXT parsing
    fields = sentence.split(',')
    return {
        'several_lines': fields[1] if len(fields) > 1 else None,
        'free': fields[2] if len(fields) > 2 else None,
        'type': fields[3] if len(fields) > 3 else None,
        'text': fields[4].split('*')[0] if len(fields) > 4 and '*' in fields[4] else None
    }
#メッセージ統合(GSA GSV) / Message integration (GSA GSV)

def merge_gsa(gsa_list):
    #GSA統合 / GSA integration
    if not gsa_list:
        return parse_gsa('')
    merged = {}
    merged['fix_select'] = gsa_list[0].get('fix_select', 'A')
    merged['fix_status'] = gsa_list[0].get('fix_status', '1')
    #衛星IDは '0' 以外の値をすべて結合 / Concatenate all satellite IDs other than '0'
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

def merge_gsv(gsv_list):
    #GSV統合 / GSV integration
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
    merged['satellites_info'] = sats
    return merged

def analyze_nmea_data(parsed_data):
    global sts#(SatelliTeS)
    analyzed_data = {}
    #GGA, GLL, RMC, VTG, GST, DHV, ZDA, TXT 各リスト化 / GGA, GLL, RMC, VTG, GST, DHV, ZDA, TXT list
    analyzed_data['GGA'] = [parse_gga(sentence) for sentence in parsed_data['GGA']] if parsed_data['GGA'] else [parse_gga('')]
    analyzed_data['GLL'] = [parse_gll(sentence) for sentence in parsed_data['GLL']] if parsed_data['GLL'] else [parse_gll('')]
    analyzed_data['RMC'] = [parse_rmc(sentence) for sentence in parsed_data['RMC']] if parsed_data['RMC'] else [parse_rmc('')]
    analyzed_data['VTG'] = [parse_vtg(sentence) for sentence in parsed_data['VTG']] if parsed_data['VTG'] else [parse_vtg('')]
    analyzed_data['GST'] = [parse_gst(sentence) for sentence in parsed_data['GST']] if parsed_data['GST'] else [parse_gst('')]
    analyzed_data['DHV'] = [parse_dhv(sentence) for sentence in parsed_data['DHV']] if parsed_data['DHV'] else [parse_dhv('')]
    analyzed_data['ZDA'] = [parse_zda(sentence) for sentence in parsed_data['ZDA']] if parsed_data['ZDA'] else [parse_zda('')]
    analyzed_data['TXT'] = [parse_txt(sentence) for sentence in parsed_data['TXT']] if parsed_data['TXT'] else [parse_txt('')]
    #GSA統合化 / GSA merge
    if parsed_data['GSA']:
        gsa_list = [parse_gsa(sentence) for sentence in parsed_data['GSA']]
        merged_gsa = merge_gsa(gsa_list)
        analyzed_data['GSA'] = [merged_gsa]
    else:
        analyzed_data['GSA'] = [parse_gsa('')]
    #GSV統合化 / GSV merge
    sts = []
    if parsed_data['GSV']:
        gsv_list = [parse_gsv(sentence) for sentence in parsed_data['GSV']]
        merged_gsv = merge_gsv(gsv_list)
        analyzed_data['GSV'] = [merged_gsv]
    else:
        analyzed_data['GSV'] = [parse_gsv('')]
    return analyzed_data
