import subprocess
from functools import cached_property
from pathlib import Path
from typing import Optional
from datetime import datetime
import warnings
from collections.abc import Iterable

from library.enums.plink_keywords import PlinkKeyword
from library.tools.collections import EnumTuple
from library.converters.plink_bin_downloader import PlinkBinDownloader
from library.parsers.plink_file_reader import PlinkFileReader


class Plink:
    plink_binary_path: Path | None
    plink_prefix: Path | None

    PLINK_CMD: str = "plink"

    def __init__(
        self,
        plink_binary_path: Optional[str | Path] = None,
        plink_prefix: Optional[str | Path] = None,
        encoding: str = "utf-8",
    ):
        self.plink_binary_path = (
            Path(plink_binary_path).absolute() if plink_binary_path else None
        )
        self.plink_prefix = Path(plink_prefix).absolute() if plink_prefix else None
        self.encoding = encoding
        if plink_binary_path:
            self.PLINK_CMD = self.plink_binary_path

    @cached_property
    def plink_downloader(self):
        if not self.plink_binary_path:
            name = self.__class__.__name__
            raise ValueError(
                "You did not specify a path to the plink binary.\n"
                f"Use `{name}(plink_binary_path='/target/path/to/plink')` "
                f"instead of `{name}()`."
            )
        return PlinkBinDownloader(
            target_folder=self.plink_binary_path.parent,
            target_fname=self.plink_binary_path.name,
        )

    @cached_property
    def file_reader(self):
        if not self.plink_prefix:
            name = self.__class__.__name__
            raise ValueError(
                "You did not set the plink prefix "
                "(location where the data is stored).\n"
                f"Use `{name}(plink_prefix='/target/path/to/plink/prefix')` "
                f"instead of `{name}()`."
            )
        return PlinkFileReader(plink_prefix=self.plink_prefix)

    def download_binaries(self):
        """
        Downloads Plink binary from website, extracts it and sets correct permissions.
        Returned path should correspond to the already set plink_binary_path.
        """
        plink_binary_path = self.plink_downloader.ensure_plink()
        if not plink_binary_path == self.plink_binary_path:
            warnings.warn(
                "Paths to plink binaries updated! "
                f"New path will be '{plink_binary_path}'.\n"
            )
            self.__init__(plink_binary_path=plink_binary_path)
        return plink_binary_path

    @cached_property
    def info(self):
        cmd = self.make_cmd(PlinkKeyword.VERSION)
        info_str = self.run_cmd(cmd).decode()
        parts = info_str.strip().split(" ")
        return {
            "name": parts[0],
            "version": parts[1],
            "architecture": parts[2],
            "release_date": datetime.strptime(
                " ".join((part.strip("()") for part in parts[3:])), "%d %b %Y"
            ),
        }

    @classmethod
    def to_plink_keyword(cls, key):
        def unsafe_convert_to_command(key: str) -> str:
            """
            Attempts to convert python kwarg to plink kwarg with generic/unsafe logic.

            my_example -> --my-example
            """
            if key.startswith("--"):
                return key  # Already properly converted
            converted_key = "-".join(key.lower().split("_"))
            converted_key = f"--{converted_key}"
            warnings.warn(
                f"Unsafely converted command '{key}' to '{converted_key}'. "
                "Please notify the developer to fix this.",
            )
            return converted_key

        if isinstance(key, PlinkKeyword):
            return key
        elif isinstance(key, Path):
            return key.absolute()
        elif isinstance(key, str):
            upper_key = key.upper()
            if hasattr(PlinkKeyword, upper_key):
                return getattr(PlinkKeyword, upper_key)
            else:
                return unsafe_convert_to_command(key)
        return key

    @classmethod
    def to_plink_format(cls, key: PlinkKeyword | str, value: str):
        path_keywords = EnumTuple(
            PlinkKeyword.FILE, PlinkKeyword.BFILE, PlinkKeyword.OUT
        )
        if key in path_keywords:
            abs_path = Path(value).absolute()
            return abs_path
        return value

    def make_cmd(self, *args, **kwargs):
        args = [a.absolute() if isinstance(a, Path) else a for a in args]
        cmd = [self.PLINK_CMD, *args]

        for key, value in kwargs.items():
            keyword = self.to_plink_keyword(key)

            if is_iterable := (
                isinstance(value, Iterable) and not isinstance(value, str)
            ):
                value = [self.to_plink_format(keyword, v) for v in value]
            else:
                value = self.to_plink_format(keyword, value)
            cmd.append(keyword)
            if is_iterable:
                cmd.extend(value)
            elif value is not True:
                cmd.append(str(value))
        return cmd

    @staticmethod
    def run_cmd(cmd: list[str], error_message: str = ""):
        try:
            result = subprocess.run(cmd, capture_output=True, text=False)
            if result.returncode != 0:
                raise RuntimeError(error_message.format(result.stderr) or result.stderr)
            return result.stdout
        except FileNotFoundError:
            raise RuntimeError("Plink is not installed.")

    def run(self, *args, **kwargs):
        cmd = self.make_cmd(*args, **kwargs)
        return self.run_cmd(cmd)
