# Version History of pygps2

# Version 3.72(Only CPython)
- 軽量化(Copilot)
<img width="3047" height="1852" alt="time" src="https://github.com/user-attachments/assets/65b825b7-aeb0-4e14-b3c2-8b530ead760b" />


# Version 3.7(Only MicroPython)
- 3.7 CPyをMpyに移植した。
- いずれにせよ、MicroPythonではmicropython-decimal-numberが必要。
- BDGSVをGBGSVとして処理するようにした。(共通)

# Version 3.71(Only CPython)
- GSVセンテンスよりあとのセンテンスの解析ができないバグを修正した。

# Version 3.7(Only CPython)
- GSVセンテンスの解析方法を変更し、GSVを正しく解析するようにした。
- 1センテンスごとに解析するようにした。
- CPythonのみサポートしたバージョンである。
(どうでも良いことですが、新しいPCで開発を始めました。)

# Version 3.52
- GPGSV GNGSVセンテンス中に33から64のPRNが含まれる場合、typeの値が"SBAS"になるようになった。

GNGSVがGLONNASなどを含んで出力する場合、この設定は無効にする。
SBASを利用しないモジュールの場合、誤検出・軽量化のため無効にする。

この設定は .pygps2(op3=False)で無効にすることができる。

# Version 3.51
- 2つ以上のバンドを使用時に、それらのバンドのSNR比を取得できるようにした。

# Version 3.5
- class化され、複数のモジュールを同時に使用できるようになった。
- class化に伴い、設定(QZS検知etc...)も個別でできるようになった。

# Version 3.4
- GNSセンテンス解析関数を追加

# DEV 3.3
- GNやGPメッセージに含まれるQZSSのPRNを検出し分類させることができるようになった。
- CONFIG項目が増えた。

ただし、この機能はGQメッセージでは効果がない。よってGQメッセージが出力する受信機は設定を無効にすることをおすすめする。

- GN,GPの中で193~210(みちびき初号機から6号機)を検出した場合のみ、QZSをして出力される。

今後はSBASも同じようにするようにする予定。(GQの2,3,4,7表記も検討)


# Version 3.22
- GSAセンテンスの解析方法を変更
- 上記に伴って設定できるよう変数を追加
**NMEAのフィールドには準拠していない**

これにより、より正確なGSAデータを取得できるようになった。(衛星PRN,識別)
(以前はPRNのみ取得したうえ、同じPRNを除去していたため不正確だった)

# Version 3.2
**軽量化#2**
- 一度にすべてのセンテンスを入れなくても、解析できるようにした。
- 解析データの変数をinit処理させるようにした。

結果として、小さいメモリでも動作しやすくなった。

使用方法は変わってしまうので、サンプルコードとしてexamples/pico_example_32.pyを参照

# Version 3.1
**実行関数の変更**
- analyzeにデコードしたデータを直接いれることができるようにした。
これにより、簡略化されたプログラムを作成できるようになった。

### 詳細はexamples/pico_example_31.pyを参照

# Version 3.01
gcをなくした。
理由はgcを使用すると処理時間が長くなるため。実行は各自行ってほしい。
# Version 3.0
**メモリリークを少なくした**
- delを使用して関数の処理が終了したときに変数をなくすようにした。
- gcモジュールを使用してメモリの解放を行うようにした。
- ToDoにあった解析機能を切り替えできるようにした。
**これらはanalyze_nmea_dateを実行すると処理される**

リソースが少ないデバイスでも使用しやすくなった。

# Version 2.9
**チェックサムの機能を追加**
- 各センテンスをチェックサムにより検証する機能を追加
→parse_nmea_sentencesで処理される際、チェックサムを検証するようになった。

今後はチェックサム検証を有効にするかどうかを選択できるようにする予定。

# Version 2.8
**RMCや経緯度変換関数の変更**
### RMC
- cpython環境下でmktimeのエラー回避　cpythonではmicropythonと同じように使用可能
### 経緯度変換関数
- cpythonでDecimalを使用するように変更。

## どちらも条件分岐でmicropythonとcpythonで処理を変更するようにしている。
これにより、cpython環境でも安定して動作するようになった。
# Version 2.7
**decimal関数を用いてissues#2を解消**
使用したライブラリ
- micropython-decimal-number
https://github.com/mpy-dev/micropython-decimal-number/tree/main
THANK YOU!
latはlonは処理する前にstr()で文字列に変換する必要がある。今後はこの処理を関数に組み込む予定。

float(str())にして演算を行うと、精度が落ちるためなるべく、strで保持するようにする。

# Version 2.6

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
