from pathlib import Path
import datetime
import inspect
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL, FileHandler, Formatter, StreamHandler, getLogger
from typing import Literal
import traceback

from logging_module import Searcher

level_dict = {"debug": DEBUG, "info": INFO, "warning": WARNING, "error": ERROR, "critical": CRITICAL}


class Log:
    def __init__(
        self,
        log_folder_path: Path | str | None = None,
        file_level: Literal["debug", "info", "warning", "error", "critical"] = "debug",
        stream_level: Literal["debug", "info", "warning", "error", "critical"] = "info",
    ):
        """ログ"""
        self.log_folder_path = log_folder_path

        if not isinstance(self.log_folder_path, Path | str | None):
            raise TypeError(f"log_folder_pathは型: {type(self.log_folder_path)}に対応していません。")
        self._set_handlers(file_level, stream_level)

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

    def exception(self, text: str | None = None, module_name: str | None = None):
        """tracebackのテキストある版"""
        if module_name is None:
            module_name = self._get_caller_name()
        self.logger.exception(f"{module_name} - {text}")

    def traceback(self, module_name: str | None = None):
        """tracebackのテキストない版"""
        if module_name is None:
            module_name = self._get_caller_name()
        self.logger.error(f"{module_name} - {traceback.format_exc()}")

    def _set_handlers(self, file_level: str, stream_level: str):
        self.logger = getLogger("logging_module")

        # 重複防止
        if self.logger.hasHandlers():
            return
        # debug以上のログを記録
        self.logger.setLevel(DEBUG)
        # はんどらせってい
        if not self.log_folder_path is None:
            self.log_folder_path = Path(self.log_folder_path)
            self._set_file_handler(self.log_folder_path, file_level)
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

    def search_text_date(
        self, search_text: str, start_date: datetime.date | None = None, end_date: datetime.date | None = None
    ) -> list[datetime.date]:
        """
        Args:
            search_text (str): 検索する文字列。この文字列に部分一致するログのある日付を取得
            start_date (datetime.date): 開始日(自身を含む)。datetime.date(2025, 9, 14)なら2025-09-14以上の日付で検索。
            end_date (datetime.date): 終了日(自身を含まない)。datetime.date(2025, 11, 12)なら2029-11-12未満の日付で検索。
        """
        searcher = Searcher(self.log_folder_path)
        day_file_list = searcher.get_day_file_list(start_date, end_date)
        date_list = searcher.get_date_list(search_text, day_file_list)
        return date_list

    def search_text_row(
        self, search_text: str, start_date: datetime.date | None = None, end_date: datetime.date | None = None
    ) -> list[datetime.date]:
        """
        Args:
            search_text (str): 検索する文字列。この文字列に部分一致するログの行を取得
            start_date (datetime.date): 開始日(自身を含む)。datetime.date(2025, 9, 14)なら2025-09-14以上の日付で検索。
            end_date (datetime.date): 終了日(自身を含まない)。datetime.date(2025, 11, 12)なら2029-11-12未満の日付で検索。
        """
        searcher = Searcher(self.log_folder_path)
        day_file_list = searcher.get_day_file_list(start_date, end_date)
        text_row_list = searcher.get_text_row_list(search_text, day_file_list)
        return text_row_list


if __name__ == "__main__":
    log = Log()
    log.info("にょわああ")
