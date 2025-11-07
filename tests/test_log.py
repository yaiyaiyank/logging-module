# yt-dlpとかjpholidayがこの位置にunittest書いてたのでそうする予定

# TODO sys.pathに追加せずにライブラリのテストをするのはどうやっているんだろう？
import sys
from pathlib import Path

sys.path.append(Path.cwd().__str__())

from logging_module import Log

if __name__ == "__main__":
    log = Log(stream_level="debug")
    log.info("waa")
