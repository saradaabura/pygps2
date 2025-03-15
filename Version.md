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
そのままの出力であるため、使用するモジュールによってプログラムを変更する必要がある。
# Version 2.0
作成