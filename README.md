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

プロジェクト直下のsetting/\_\_init\_\_.pyにて
```python
from logging_module import Log

log = Log()

```

```python
from setting import log

log.info("うおｗ")

log.error("おお")

```

ちなみに、FileHandlerはINFO以上、StreamHandlerはDEBUG以上です。Logクラスの引数で調整できます。