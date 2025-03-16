# Version 2.3
**GST解析関数追加**
- GSTセンテンスの解析関数を追加
# Version 2.2
**衛星のデュアルバンドによるカウント重複の解消**
GNSSのセンテンスから2回以上同じPRNが検出されてもカウントしないようにした。
まだ完全ではないが、一部のセンテンスに対しては対応している。
動作確認
AT6668
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