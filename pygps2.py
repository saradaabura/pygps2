# Version3.95
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
            def __add__(self, o): return DecimalCls(self.v + getattr(o, "v", float(o)))
            def __sub__(self, o): return DecimalCls(self.v - getattr(o, "v", float(o)))
            def __mul__(self, o): return DecimalCls(self.v * getattr(o, "v", float(o)))
            def __truediv__(self, o): return DecimalCls(self.v / getattr(o, "v", float(o)))
            def __neg__(self): return DecimalCls(-self.v)
            def __str__(self): return str(self.v)
            def __float__(self): return float(self.v)

class pygps2:
    def __init__(self, op0=True, op1=True, op2=True, op3=True, op4=True, op5=True, op6="GGA", op7=None):
        # オプション デフォではすべて有効
        self.OBTAIN_IDENTIFLER_FROM_GSA = op0
        self.IN_BAND_DATA_INTO_GSV = op1
        self.DETECT_CONVERT_QZS = op2
        self.DETECT_CONVERT_SBAS = op3
        self.ENABLE_CHECKSUM = op4
        self.USE_DECIMAL = op5
        self.FIRST_SENTENCE = op6
        self.UPDATE_CALLBACK = op7
        
        self.D = DecimalCls
        impl = sys.implementation.name
        self._is_cpython = (impl == "cpython")

        self.reset_data()

    def reset_data(self):
        self.raw = ""
        for k in ["GGA","GLL","GSA","GSV", "RMC","VTG","GST","DHV","ZDA","GNS","TXT"]:
            setattr(self, k, [])
        #self.GSV = {k: None for k in ["GP", "GL", "GA", "GB", "GQ", "GN"]}
        self.parsed_data = {k: [] for k in ["GGA","GLL","GSA","GSV","RMC","VTG","GST","DHV","ZDA","GNS","TXT","Other"]}
        self.parsed_data["GSV"] = {k: {} for k in ["GP","GL","GA","GB","BD","GQ","GN"]}
        
        self.temp_gsv = []
        self.temp_gsa = []

    def convert_to_degrees(self, coord, direction):
        if not coord or not direction: return "0.0"
        
        if self.USE_DECIMAL == True:
            try:
                d_len = 2 if direction in "NS" else 3
                deg = self.D(coord[:d_len])
                minutes = self.D(coord[d_len:])
                res = deg + minutes / self.D("60.0")
                if direction in "SW": res = -res
                return str(res)
            except: return "0.0"
        else:
            try:
                d_len = 2 if direction in "NS" else 3
                deg = float(coord[:d_len])
                minutes = float(coord[d_len:])
                res = deg + (minutes / 60.0)
                if direction in "SW":
                    res = -res
                return str(res)
            except: return "0.0"

    def verify_checksum(self, sentence):
        if "*" not in sentence: return False
        try:
            data, checksum = sentence.split("*", 1)
            chk = 0
            for c in data[1:]: chk ^= ord(c)
            return "{:02X}".format(chk) == checksum.strip().upper()
        except: return False

    def _safe_get(self, fields, idx, default=""):
        if idx < len(fields) and fields[idx]:
            val = fields[idx]
            return val.split("*")[0] if "*" in val else val
        return default

    # XXGGAセンテンス
    def parse_gga(self, f):
        if not f: return
        return {
            "timestamp": self._safe_get(f, 1, "000000.0"),
            "latitude": self.convert_to_degrees(self._safe_get(f, 2), self._safe_get(f, 3)),
            "longitude": self.convert_to_degrees(self._safe_get(f, 4), self._safe_get(f, 5)),
            "gps_quality": self._safe_get(f, 6, "0"),
            "num_satellites": self._safe_get(f, 7, "0"),
            "hdop": self._safe_get(f, 8, "0.0"),
            "altitude": self._safe_get(f, 9, "0.0"),
            "altitude_units": self._safe_get(f, 10, "M"),
            "geoid_height": self._safe_get(f, 11, "0.0"),
            "geoid_units": self._safe_get(f, 12, "M"),
            "dgps_age": self._safe_get(f, 13),
            "dgps_station_id": self._safe_get(f, 14)
        }

    # XXGLLセンテンス
    def parse_gll(self, f):
        if not f: return
        return {
            "latitude": self.convert_to_degrees(self._safe_get(f, 1), self._safe_get(f, 2)),
            "longitude": self.convert_to_degrees(self._safe_get(f, 3), self._safe_get(f, 4)),
            "timestamp": self._safe_get(f, 5, "000000.0"),
            "status": self._safe_get(f, 6, "V"),
            "mode_indicator": self._safe_get(f, 7)
        }

    # XXGSAセンテンス
    def parse_gsa(self, sentence):
        if not sentence: return {"fix_select":"A","fix_status":"1","satellites_used":["0"]*12,"self.parsed_dataop":"0.0","hdop":"0.0","vdop":"0.0"}
        f = sentence.split(",")
        sys_id = self._safe_get(f, 18)
        sats = [ (self._safe_get(f, i, "0"), sys_id) if self.OBTAIN_IDENTIFLER_FROM_GSA else self._safe_get(f, i, "0") for i in range(3, 15) ]
        return {
            "fix_select": self._safe_get(f, 1, "A"),
            "fix_status": self._safe_get(f, 2, "1"),
            "satellites_used": sats,
            "self.parsed_dataop": self._safe_get(f, 15, "0.0"),
            "hdop": self._safe_get(f, 16, "0.0"),
            "vdop": self._safe_get(f, 17, "0.0")
        }

    # XXGSVセンテンス
    def parse_gsv(self, sentence):
         if not sentence: return
         f = sentence.split(",")
         sys_type = sentence[1:3]
         band = self._safe_get(f, -1, "0") if self.IN_BAND_DATA_INTO_GSV else 0
         sats_info = []
         for i in range(4, len(f) - 3, 4):
             sats_info.append({
                 "prn": self._safe_get(f, i, "0"), "type": sys_type,
                 "elevation": self._safe_get(f, i+1, "0.0"), "azimuth": self._safe_get(f, i+2, "0.0"),
                 "snr": self._safe_get(f, i+3, "0.0"), "band": band
             })
         return {"system_type": sys_type, "num_messages": self._safe_get(f, 1, "1"), "message_num": self._safe_get(f, 2, "1"), "num_satellites": self._safe_get(f, 3, "0"), "satellites_info": sats_info}

    # XXZDAセンテンス
    def parse_zda(self, f):
        if not f: return
        return {k: self._safe_get(f, i, None) for i, k in enumerate(["_","timestamp","day","month","year","timezone_offset_hour","timezone_offset_minute"])}

    # XXGSAの結果をマージ analyze_sentenceから呼び出される。
    def merge_gsa(self, gsa_list):
        if not gsa_list: return self.parse_gsa("")
        merged = {"fix_select": gsa_list[0].get("fix_select", "A"), "fix_status": gsa_list[0].get("fix_status", "1")}
        sats = []
        for g in gsa_list:
            for s in g.get("satellites_used", []):
                val = s[0] if isinstance(s, tuple) else s
                if val not in ("0", ""): sats.append(s)
        seen = []
        merged["satellites_used"] = [x for x in sats if not (x in seen or seen.append(x))]
        for k in ["self.parsed_dataop", "hdop", "vdop"]:
            vals = [float(g.get(k, 0)) for g in gsa_list if float(g.get(k, 0)) > 0]
            merged[k] = str(sum(vals)/len(vals)) if vals else "0.0"
        return merged

    # XXGSVの結果をマージ analyze_sentenceから呼び出される。
    def merge_gsv(self, gsv_list):
        if not gsv_list: return self.parse_gsv("")
        unique = {}
        for s in [s for g in gsv_list for s in g.get("satellites_info", [])]:
            key = (s["prn"], s["type"], s["elevation"], s["azimuth"])
            if key not in unique:
                unique[key] = s.copy()
                unique[key]["snr"] = [float(s["snr"])]
                unique[key]["band"] = [int(s["band"])]
            else:
                unique[key]["snr"].append(float(s["snr"]))
                unique[key]["band"].append(int(s["band"]))
            
        res = {"num_messages": str(len(gsv_list)), "message_num": "1", "num_satellites": "0", "satellites_info": list(unique.values())}
        if self.DETECT_CONVERT_QZS: res["satellites_info"] = self.detect_system(res["satellites_info"], "QZS")
        if self.DETECT_CONVERT_SBAS: res["satellites_info"] = self.detect_system(res["satellites_info"], "SBAS")
        res["num_satellites"] = len(res["satellites_info"])
        return res

    # RMCセンテンス
    def parse_rmc(self, f):
        if not f: return
        data = {
            "timestamp": self._safe_get(f, 1, "000000.0"), "status": self._safe_get(f, 2, "V"),
            "latitude": self.convert_to_degrees(self._safe_get(f, 3), self._safe_get(f, 4)),
            "longitude": self.convert_to_degrees(self._safe_get(f, 5), self._safe_get(f, 6)),
            "speed_over_ground": self._safe_get(f, 7, "0.0"), "course_over_ground": self._safe_get(f, 8, "0.0"),
            "date": self._safe_get(f, 9, "010100"), "magnetic_variation": self._safe_get(f, 10, "0.0"),
            "mag_var_direction": self._safe_get(f, 11), "mode_indicator": self._safe_get(f, 12)
        }
        try:# 時差処理
            ts, dt = data["timestamp"], data["date"]
            h, m, s = int(ts[0:2]), int(ts[2:4]), int(ts[4:6])
            day, mo, y = int(dt[0:2]), int(dt[2:4]), int(dt[4:6]) + 2000
            t_tup = (y, mo, day, h, m, s, 0, 0, 0) if self._is_cpython else (y, mo, day, h, m, s, 0, 0)
            utc = time.mktime(t_tup)
            offset = math.floor(float(data["longitude"]) / 15)
            loc = time.localtime(utc + offset * 3600)
            data["utc_datetime"] = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(y,mo,day,h,m,s)
            data["local_datetime"] = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(loc[0],loc[1],loc[2],loc[3],loc[4],loc[5])
        except: data["utc_datetime"] = data["local_datetime"] = None
        return data

    # XXVTGセンテンス
    def parse_vtg(self, f):
        if not f: return
        keys = ["course_over_ground_t", "reference_t", "course_over_ground_m", "reference_m", "speed_knots", "units_knots", "speed_kmh", "units_kmh", "mode_indicator"]
        defaults = ["0.0", "T", "0.0", "M", "0.0", "N", "0.0", "K", ""]
        return {k: self._safe_get(f, i+1, defaults[i]) for i, k in enumerate(keys)}

    # XXGSTセンテンス
    def parse_gst(self, f):
        if not f: return
        return {"timestamp": self._safe_get(f, 1, "000000.0"), "rms": self._safe_get(f, 2, "0.0"), "std_lat": self._safe_get(f, 6, "0.0"), "std_lon": self._safe_get(f, 7, "0.0"), "std_alt": self._safe_get(f, 8, "0.0")}
   
   # XXDHVセンテンス
    def parse_dhv(self, f):
        if not f: return
        return {k: self._safe_get(f, i+1, None) for i, k in enumerate(["timestamp", "3d_speed", "ecef_x_speed", "ecef_y_speed", "ecef_z_speed", "horizontal_ground_speed"])}

    # XXGNSセンテンス
    def parse_gns(self, f):
        if not f: return
        keys = ["utc_time","latitude","longitude","mode_indicator","use_sv","hdop","msl","geoid_alt","age_of_differential_data","station_id"]
        map_idx = [1, 2, 4, 6, 7, 8, 9, 11, 13, 14]
        res = {k: self._safe_get(f, map_idx[i], "0.0") for i, k in enumerate(keys)}
        res["latitude"] = self.convert_to_degrees(self._safe_get(f, 2), self._safe_get(f, 3))
        res["longitude"] = self.convert_to_degrees(self._safe_get(f, 4), self._safe_get(f, 5))
        return res

    # XXTXTセンテンス
    def parse_txt(self, f):
        if not f: return
        return {k: self._safe_get(f, i+1, None) for i, k in enumerate(["several_lines", "free", "type", "text"])}
    # GP,GN GSVからQZSとSBASを検出し、タイプやPRNを変換する。QZSは193-210、SBASは33-64(補正後120-151)。
    def detect_system(self, info, system="QZS"):
        output = []
        for temp_s in info:
            if temp_s["type"] in ("GP", "GN"):
                prn = int(temp_s["prn"])
                if system == "QZS" and 193 <= prn <= 210:
                    temp_s["type"] = "QZS"
                elif system == "SBAS" and 33 <= prn <= 64:
                    temp_s["type"] = "SBAS"
                    temp_s["prn"] = prn + 87
            output.append(temp_s)
        return output
    
    def tolist(self, data):
        return "\r\n".join(["$" + s for s in str(data).split("$") if s]) + "\r\n"
    # analyze_sentenceからそれぞれのパーサーにわたす。
    # 各パーサーで結果(Return)を代入するようにしてもいいかもしれない。
    def analyze_sentence(self, sentence, en_gsa=True, en_gsv=True, en_txt=True):
        if self.ENABLE_CHECKSUM == True:
            if self.verify_checksum(sentence) == False:
                return
        # チェックサム検証
        temp = sentence.split(",")
        stype = temp[0][3:6] # sentence type
        sttype = temp[0][1:3] # satellite type
        if stype in self.parsed_data and stype != "GSV" and stype != "GSA":
            self.parsed_data[stype] = sentence
            if stype == self.FIRST_SENTENCE:
                self.temp_gsv = []
                self.temp_gsa = []
                # GSV/GSA用の一時変数をリセット
            if stype == "GGA":
                self.GGA = self.parse_gga(temp)
            if stype == "GLL":
                self.GLL = self.parse_gll(temp)
            if stype == "RMC":
                self.RMC = self.parse_rmc(temp)
            if stype == "VTG":
                self.VTG = self.parse_vtg(temp)
            if stype == "GST":
                self.GST = self.parse_gst(temp)
            if stype == "DHV":
                self.DHV = self.parse_dhv(temp)
            if stype == "ZDA":
                self.ZDA = self.parse_zda(temp)
            if stype == "GNS":
                self.GNS = self.parse_gns(temp)
            if stype == "TXT" and en_txt:
                self.TXT = self.parse_txt(temp)
        # 複数のセンテンスになりうるGSV GSAだけ特別処理
        elif stype == "GSV" and en_gsv:
            if "*" in temp[len(temp) - 1]:# this is not working...
                band = temp[len(temp) - 1]
                band = str(band.split("*")[0])
            else:
                band = "0"
            if temp[2] == "1":
                self.parsed_data["GSV"][sttype][band] = []
            self.parsed_data["GSV"][sttype][band].append(sentence)
            
            check_temp = self.parsed_data["GSV"][sttype][band][len(self.parsed_data["GSV"][sttype][band]) - 1]
            check_temp = check_temp.split(",")
            if check_temp[1] == check_temp[2]: # 最後のセンテンスになったら解析する(同BAND&同衛星であることを想定)
                sentences = self.parsed_data["GSV"][sttype][band]
                for s in sentences:
                    self.temp_gsv.append(self.parse_gsv(s))
                    self.GSV = self.merge_gsv(self.temp_gsv)
            
        elif stype == "GSA" and en_gsa:
            if "*" in temp[len(temp) - 1]:# this is not working...
                num = temp[len(temp) - 1]
                num = str(num.split("*")[0])
                if num == "1":
                    self.parsed_data["GSA"] = []
            self.parsed_data["GSA"].append(sentence)
            self.temp_gsa.append(self.parse_gsa(sentence))
            self.GSA = self.merge_gsa(self.temp_gsa)

        else:
            pass#今後検討
            #self.parsed_data["Other"].append(sentence)
            # 保持しなくていいかもしれない。
        if stype == self.FIRST_SENTENCE:
            print("呼び出し")
            if self.UPDATE_CALLBACK is not None:
                self.UPDATE_CALLBACK()
