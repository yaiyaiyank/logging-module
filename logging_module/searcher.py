from pathlib import Path
from dataclasses import dataclass
import datetime


def day_file_to_date(day_file: Path) -> datetime.date:
    return datetime.date(int(day_file.parent.parent.name), int(day_file.parent.name), int(day_file.stem))


class Searcher:
    def __init__(self, log_folder_path: Path | str | None):
        if log_folder_path is None or not Path(log_folder_path).exists():
            raise FileNotFoundError("ログファイルが設定されていないぁ、または存在していません。")
        self.log_folder_path = Path(log_folder_path)

    def get_text_row_list(self, search_text: str, day_file_list: list[Path]) -> list[Path]:
        text_row_list = []
        for day_file in day_file_list:
            text_list = day_file.read_text(encoding="utf-8").split("\n")
            # 含まれている行をすべて登録
            for text in text_list:
                if search_text in text:
                    text_row_list.append(text)

        return text_row_list

    def get_date_list(self, search_text: str, day_file_list: list[Path]) -> list[datetime.date]:
        date_list = []
        for day_file in day_file_list:
            text_list = day_file.read_text(encoding="utf-8").split("\n")
            # 1つでも含まれてればその日を登録
            for text in text_list:
                if search_text in text:
                    date_list.append(day_file_to_date(day_file))
                    break

        return date_list

    def get_day_file_list(
        self, start_date: datetime.date | None = None, end_date: datetime.date | None = None
    ) -> list[Path]:
        if not (isinstance(start_date, datetime.date | None) and isinstance(end_date, datetime.date | None)):
            raise TypeError

        day_file_list = list(self.log_folder_path.glob("**/*.log"))

        day_file_list.sort(key=day_file_to_date)

        if not start_date is None:
            day_file_list = [day_file for day_file in day_file_list if day_file_to_date(day_file) >= start_date]

        if not end_date is None:
            day_file_list = [day_file for day_file in day_file_list if day_file_to_date(day_file) < end_date]

        return day_file_list
