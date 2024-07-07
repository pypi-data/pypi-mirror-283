from functools import cached_property
import urllib.request
import zipfile
import io
import os
import platform
import re
from pathlib import Path


class PlinkBinDownloader:
    def __init__(self, target_folder: str = "binaries", target_fname: str = "plink"):
        self.target_folder = Path(target_folder).absolute()
        self.target_fname = target_fname
        self.base_url = "https://www.cog-genomics.org/plink2/"

    @cached_property
    def download_links(self) -> list:
        with urllib.request.urlopen(self.base_url) as response:
            html_content = response.read().decode("utf-8")

        # Regex to find all href links containing 'plink' and ending with '.zip'
        download_links = re.findall(
            r'href="(https?://[^"]*plink[^"]*\.zip)"', html_content
        )

        return download_links

    @cached_property
    def platform_key(self):
        system = platform.system().lower()
        arch, _ = platform.architecture()

        if system == "windows":
            if "64" in arch:
                return "win64"
            else:
                return "win32"
        elif system == "darwin":
            return "mac"
        elif system == "linux":
            if "64" in arch:
                return "linux_x86_64"
            else:
                return "linux_i686"
        else:
            raise ValueError(f"Unsupported platform '{system}'")

    @cached_property
    def target_path(self):
        return self.target_folder / self.target_fname

    def make_dir(self):
        self.target_folder.mkdir(parents=True, exist_ok=True)

    def download_plink(self) -> str | None:
        download_url = next(
            (link for link in self.download_links if self.platform_key in link), None
        )

        if not download_url:
            raise ValueError(
                f"No download link found for platform: {self.platform_key}"
            )

        # Download the zip file
        with urllib.request.urlopen(download_url) as response:
            zip_content = response.read()

        # Extract only the 'plink' binary
        plink_bin_name = "plink"
        with zipfile.ZipFile(io.BytesIO(zip_content)) as z:
            for file in z.namelist():
                if plink_bin_name in file and not file.endswith(os.sep):
                    with open(self.target_path, "wb") as f:
                        f.write(z.read(file))
                    return self.target_path

    def cleanup_folder(self):
        "Remove all files except the plink binary"
        for filename in self.target_folder.iterdir():
            if filename != self.target_fname:
                os.remove(self.target_folder / filename)

    def allow_executing_plink(self):
        if self.platform_key not in ("win32", "win64"):
            self.target_path.chmod(self.target_path.stat().st_mode | 0o111)

    def ensure_plink(self) -> str:
        if not self.target_path.exists():
            self.make_dir()
            self.download_plink()
            self.allow_executing_plink()
        return self.target_path
