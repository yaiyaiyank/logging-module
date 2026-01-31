# loggingモジュール

自分のエコシステム用につくったログ記録モジュール<br>
役立ちそう ∧ 機密情報なし なのでパブリックで公開

# install
### 動作環境
* Python 3.13↑
### インストール方法 
uvなら
```bash
uv add git+https://github.com/yaiyaiyank/logging-module
```
pipなら
```bash
pip install git+https://github.com/yaiyaiyank/logging-module
```
### 備考
標準ライブラリのみで完結するので外部ライブラリ依存なし

# usage
## init
プロジェクト直下のsetting/\_\_init\_\_.pyにて
```python
from logging_module import Log

log = Log()
```
ログ用にフォルダーを設定するとそのフォルダー / 年 / 月 / 日.logに記録可能
```python
from logging_module import Log
from pathlib import Path

LOG_FOLDER = Path.cwd() / "logs"
log = Log(LOG_FOLDER)
```
file_levelとstream_levelを指定すればそのレベル以上のやつのみ記録
```python
from logging_module import Log
from pathlib import Path

LOG_FOLDER = Path.cwd() / "logs"
log = Log(LOG_FOLDER, file_level="info", stream_level="warning")
```
## write
```python
from setting import log

log.info("どわーｗ")

log.error("おお")

```
コンソールに
```
[INFO] - File: test.py - どわーｗ
[ERROR] - File: test.py - おお
```
みたいに出て、ログフォルダーを設定している場合は
```
2026-01-31 20:42:28,560 [INFO] - File: test.py - どわーｗ
2026-01-31 20:42:28,562 [ERROR] - File: test.py - おお
```
みたいに書き込む
## search
```python
# フォルダーにログ記録している前提

# そのテキストがある行を取得
log.search_text_row("番目でエラー", datetime.date(2025, 8, 3), datetime.date(2026, 11, 15))
# -> ['2025-08-03 12:36:46,799 [ERROR] - Class: Scraping - 145番目でエラー', '2025-08-03 12:36:50,397 [ERROR] - Class: Scraping - 208番目でエラー', ..., '2026-11-14 22:44:58,815 [ERROR] - Class: Scraping - 11番目でエラー']

# そのテキストがある行がある日付を取得
log.search_text_date("番目でエラー", datetime.date(2025, 8, 3), datetime.date(2026, 11, 15))
# -> [datetime.date(2025, 8, 3), datetime.date(2025, 8, 10), ..., datetime.date(2025, 11, 12)]
```