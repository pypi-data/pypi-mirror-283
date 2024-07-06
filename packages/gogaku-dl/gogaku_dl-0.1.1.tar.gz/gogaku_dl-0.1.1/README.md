# はじめに

このプログラムは、NHKラジオの「らじる★らじる」で公開されている番組の
HLSのアドレスを取得するためのパッケージを提供します。

HLSのアドレスが入手できれば、
[第48回『らじる★らじる』の聴き逃がしサービス（4）](https://gihyo.jp/article/2023/04/zoku-gansiki-0048?summary)を参照に
コンテンツのダウンロードが可能となります。

# API 

## 使用方法

### 「らじる★らじる」の英語番組のタイトル一覧の習得例

```python
(nhk) taku@okisuke:~/study/nhk/gogaku_dl$ ipython
Python 3.12.4 | packaged by conda-forge | (main, Jun 17 2024, 10:23:07) [GCC 12.3.0]
Type 'copyright', 'credits' or 'license' for more information
IPython 8.26.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from gogaku_dl import english

In [2]: english.get_program_titles()
Out[2]: 
['小学生の基礎英語',
 '中学生の基礎英語レベル1',
 '中学生の基礎英語レベル2',
 '中高生の基礎英語in English',
 'ラジオ英会話',
 'ボキャブライダー',
 'エンジョイ・シンプル・イングリッシュ',
 '英会話タイムトライアル',
 'ニュースで学ぶ「現代英語」',
 'ラジオビジネス英語']

In [3]: 

```
### 「らじる★らじる」の英語番組のHLSの取得例

`get_english_hls`関数でHLSを取得することができます。
`get_english_hls`の引数には、`get_program_titles`で取得したいずれかの値を指定します。

「エンジョイ・シンンプル・イングリシュ」のHLSの取得例を示します。

```python
(nhk) taku@okisuke:~/study/nhk/gogaku_dl$ ipython
Python 3.12.4 | packaged by conda-forge | (main, Jun 17 2024, 10:23:07) [GCC 12.3.0]
Type 'copyright', 'credits' or 'license' for more information
IPython 8.26.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from gogaku_dl import english

In [2]: english.get_english_hls('エンジョイ・シンプル・イングリッシュ')
Out[2]: 
{'title': 'エンジョイ・シンプル・イングリッシュ',
 'detail_url': 'https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=3064&corner_site_id=01',
 'episodes': [{'エンジョイ・シンプル・イングリッシュ「箱根への道」': {'onair': '6月24日(月)午前9:10放送',
    'hls': 'https://vod-stream.nhk.jp/radioondemand/r/3064/s/stream_3064_fee6e512960579b4ded0ba5db73d54ec/index.m3u8'}},
  {'エンジョイ・シンプル・イングリッシュ「詰め放題＆腕相撲」': {'onair': '6月25日(火)午前9:10放送',
    'hls': 'https://vod-stream.nhk.jp/radioondemand/r/3064/s/stream_3064_31d8db87f7b54acbd4cc746ef76f4297/index.m3u8'}},
  {'エンジョイ・シンプル・イングリッシュ「通信カラオケ」': {'onair': '6月26日(水)午前9:10放送',
    'hls': 'https://vod-stream.nhk.jp/radioondemand/r/3064/s/stream_3064_19af8a39defb5ea74ca89f2a6c4728e7/index.m3u8'}},
  {'エンジョイ・シンプル・イングリッシュ「かにと母親」': {'onair': '6月27日(木)午前9:10放送',
    'hls': 'https://vod-stream.nhk.jp/radioondemand/r/3064/s/stream_3064_1889cf1c4ab7913625f8eb972d9f41bf/index.m3u8'}},
  {'エンジョイ・シンプル・イングリッシュ「あやしい旅行者－最終話－」': {'onair': '6月28日(金)午前9:10放送',
    'hls': 'https://vod-stream.nhk.jp/radioondemand/r/3064/s/stream_3064_7231a97605445389cedfeed0c5aa3d2d/index.m3u8'}}],
 'fiscal_year': 2024}

In [3]: 


```

# APIを使用した実装例

「エンジョイン・シンプル・イングリシュ」をmp3にダウンロードする実装例
を`examples/rec_enjoy_simple_english.py`として格納しました。

実行例を以下に示します。

https://github.com/takushi1969/gogaku_dl/assets/3589129/bf56750c-3b2b-47b7-a925-a9e1f15bce87






