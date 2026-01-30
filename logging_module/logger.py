import datetime
import inspect
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL, FileHandler, Formatter, StreamHandler, getLogger
from pathlib import Path
from typing import Literal

level_dict = {"debug": DEBUG, "info": INFO, "warning": WARNING, "error": ERROR, "critical": CRITICAL}


class Log:
    def __init__(
        self,
        log_folder_path: Path | str | None = None,
        file_level: Literal["debug", "info", "warning", "error", "critical"] = "info",
        stream_level: Literal["debug", "info", "warning", "error", "critical"] = "debug",
    ):
        """ログ"""
        if not isinstance(log_folder_path, Path | str | None):
            raise TypeError(f"log_folder_pathは型: {type(log_folder_path)}に対応していません。")
        self._set_handlers(log_folder_path, file_level, stream_level)

    def debug(self, text: str, module_name: str | None = None):
        if module_name is None:
            module_name = self._get_caller_name()
        self.logger.debug(f"{module_name} - {text}")

    def info(self, text: str, module_name: str | None = None):
        if module_name is None:
            module_name = self._get_caller_name()
        self.logger.info(f"{module_name} - {text}")

    def warning(self, text: str, module_name: str | None = None):
        if module_name is None:
            module_name = self._get_caller_name()
        self.logger.warning(f"{module_name} - {text}")

    def error(self, text: str, module_name: str | None = None):
        if module_name is None:
            module_name = self._get_caller_name()
        self.logger.error(f"{module_name} - {text}")

    def critical(self, text: str, module_name: str | None = None):
        if module_name is None:
            module_name = self._get_caller_name()
        self.logger.critical(f"{module_name} - {text}")

    def _set_handlers(self, log_folder_path: Path | str | None, file_level: str, stream_level: str):
        self.logger = getLogger()

        # 重複防止
        if self.logger.hasHandlers():
            return
        # debug以上のログを記録
        self.logger.setLevel(DEBUG)
        # はんどらせってい
        if not log_folder_path is None:
            log_folder_path = Path(log_folder_path)
            self._set_file_handler(log_folder_path, file_level)
        self._set_stream_handler(stream_level)

    def _set_file_handler(self, log_folder_path: Path, file_level: str):
        # 日付を
        date = datetime.date.today()
        log_file = log_folder_path / f"{date.year:04}" / f"{date.month:02}" / f"{date.day:02}.log"
        # フォルダ生成
        log_file.parent.mkdir(parents=True, exist_ok=True)

        # FileHandler
        handler = FileHandler(log_file, encoding="utf-8")
        handler.setLevel(level_dict[file_level])
        handler.setFormatter(Formatter("%(asctime)s [%(levelname)s] - %(message)s"))
        self.logger.addHandler(handler)

    def _set_stream_handler(self, stream_level: str) -> str:
        handler = StreamHandler()
        handler.setLevel(level_dict[stream_level])
        handler.setFormatter(Formatter("[%(levelname)s] - %(message)s"))
        self.logger.addHandler(handler)

    @staticmethod
    def _get_caller_name() -> str:
        """logの呼び出し名を決める。呼び出した位置に依存"""
        # スタックフレームを取得
        stack = inspect.stack()

        # 呼び出し元の情報を取得
        frame = stack[2]  # [0]はこの_get_caller_nameメソッド, [1]はこのクラスの__init__メソッド, [2]はその呼び出し元
        caller_frame = frame.frame
        code_object = caller_frame.f_code

        # クラスのイニシャライザか関数かを判定
        if "self" in caller_frame.f_locals:
            # selfがある場合はクラスのメソッド
            cls_name = caller_frame.f_locals["self"].__class__.__name__
            if code_object.co_name == "__init__":
                return f"Class: {cls_name}"
            return f"method: {cls_name}.{code_object.co_name}"
        elif code_object.co_name == "<module>":
            # selfがない場合は通常の関数
            return f"File: {Path(code_object.co_filename).name}"
        else:
            return f"Function: {code_object.co_name}"


if __name__ == "__main__":
    log = Log()
    log.info("にょわああ")
