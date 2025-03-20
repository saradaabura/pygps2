# version 2.7
**decimal関数を用いてissues#2を解消**
使用したライブラリ
- micropython-decimal-number
https://github.com/mpy-dev/micropython-decimal-number/tree/main
THANK YOU!
latはlonは処理する前にstr()で文字列に変換する必要がある。今後はこの処理を関数に組み込む予定。

float(str())にして演算を行うと、精度が落ちるためなるべく、strで保持するようにする。

# version 2.6

**パターンにないデータの処理**

2.5以前はpatternsにないデータは処理されなかったが、2.6以降は処理されるようになった。

処理されたデータはpygps2.parse_nmea_sentences()でOtherに分類される。pygps2.analyze_nmea_data()では処理されない。

# Version 2.5
**DHV ZDA TXT追加**
- 解析センテンスの追加
**FIXしていないときの時刻は2000/01/01になりました**
- timeのmktimeエラー回避のため
# Version 2.4
**RMC変更**
- RMCに経度から計算したローカル時刻を追加
日付の変更に対応

# Version 2.3
**GST解析関数追加**
- GSTセンテンスの解析関数を追加
# Version 2.2
**衛星のデュアルバンドによるカウント重複の解消**
GNSSのセンテンスから2回以上同じPRNが検出されてもカウントしないようにした。

まだ完全ではないが、一部のセンテンスに対しては対応している。

動作確認
- AT6668
- AT6558
# Version 2.1
**GSV解析関数変更**
- 衛星識別子を追加

GSVセンテンスの先頭2文字目から4文字目を取得

それを識別子として辞書の"type"に追加するようにした

```例
$BDGSV "type":"BD"
$GPGSV "type":"GP"
$GAGSV "type":"GA"
$GLGSV "type":"GL"
$GNGSV "type":"GN"
$GQGSV "type":"GQ"
$GBGSV "type":"GB"
```
SBASについては対応していない

$GPGSVの中にあるQZSS等のデータはGPとして処理される。

そのままの出力であるため、使用するモジュールによってプログラムを変更する必要がある。

# Version 2.0
作成