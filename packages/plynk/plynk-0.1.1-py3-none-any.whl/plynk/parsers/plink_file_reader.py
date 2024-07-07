from pathlib import Path
from functools import lru_cache


import pandas as pd


from plynk.enums.plink_filetypes import PlinkFileType
from plynk.enums.plink_headers import DEFAULT_HEADERS, HAS_HEADERS_INCLUDED


class PlinkFileReader:
    def __init__(self, plink_prefix: str | Path, encoding: str = "utf-8"):
        self.plink_prefix = Path(plink_prefix).absolute()
        self.encoding = encoding

    @classmethod
    def find_files(cls, path: str | Path) -> list[Path]:
        path = Path(path)
        try:
            files_present = sorted(path.iterdir())
        except FileNotFoundError:
            path = path.parent  # Likely plink prefix supplied
            files_present = sorted(path.iterdir())
        return [Path(path, file).absolute() for file in files_present]

    @lru_cache
    def find_file_by_type(self, file_type: PlinkFileType):
        for path in self.find_files(self.plink_prefix):
            if path.suffix.lstrip(".") == file_type:
                return path
        raise FileNotFoundError(
            f"No file found for {file_type=} at '{self.plink_prefix}'"
        )

    def get_headers(
        self,
        file_type: PlinkFileType,
        dataset: pd.DataFrame,
        numerated_colname: str = "",
    ) -> list[str]:
        if default_headers := DEFAULT_HEADERS.get(file_type):
            numerated_headers = []
            numerated_cols = dataset.shape[1] - len(default_headers)
            if numerated_cols:
                numerated_headers = [
                    (f"{numerated_colname} {i+1}".strip())
                    for i in range(numerated_cols)
                ]
            return default_headers + numerated_headers
        else:
            raise TypeError(f"{file_type=} not supported")

    def load_data(
        self,
        file_type: PlinkFileType | str = None,
        numerated_colname: str = "",
        *args,
        **kwargs,
    ) -> pd.DataFrame:
        file_path = self.find_file_by_type(file_type)
        header = 0 if file_type in HAS_HEADERS_INCLUDED else None
        dataset = pd.read_csv(file_path, sep=r"\s+", header=header, *args, **kwargs)
        try:
            file_type = file_type or Path(file_path).suffix
            headers = self.get_headers(
                file_type=file_type,
                dataset=dataset,
                numerated_colname=numerated_colname,
            )
            dataset.columns = headers
        except TypeError:
            pass
        return dataset

    def read_file(self, file_path: str, sep: str = r"\s+", *args, **kwargs):
        "Wrapper for pandas' read_csv with compatible settings for plink"
        return pd.read_csv(file_path, sep=sep, *args, **kwargs)
