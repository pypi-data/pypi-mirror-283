import unittest
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
import io

from library.converters.plink_bin_downloader import PlinkBinDownloader


MOCK_DOWNLOAD_HTML = b"""
<table>
  <tr>
    <td colspan="4"><b>Build</b></td>
  </tr>
  <tr>
    <td><b>Operating system</b></td>
    <td><b>Stable (beta 7.2, 11 Dec 2023)</b></td>
    <td>Development (11 Dec 2023)</td>
    <td>Old (v1.07)</td>
  </tr>
  <tr>
    <td>Linux 64-bit</td>
    <td><a href="https://s3.amazonaws.com/plink1-assets/plink_linux_x86_64_20231211.zip">download</a></td>
    <td><a href="https://s3.amazonaws.com/plink1-assets/dev/plink_linux_x86_64.zip">download</a></td>
    <td><a href="https://s3.amazonaws.com/plink1-assets/1.07/plink1_linux_x86_64.zip">download</a></td>
  </tr>
  <tr>
    <td>Linux 32-bit</td>
    <td><a href="https://s3.amazonaws.com/plink1-assets/plink_linux_i686_20231211.zip">download</a></td>
    <td><a href="https://s3.amazonaws.com/plink1-assets/dev/plink_linux_i686.zip">download</a></td>
    <td><a href="https://s3.amazonaws.com/plink1-assets/1.07/plink1_linux_i686.zip">download</a></td>
  </tr>
  <tr>
    <td>macOS (64-bit)</td>
    <td><a href="https://s3.amazonaws.com/plink1-assets/plink_mac_20231211.zip">download</a></td>
    <td><a href="https://s3.amazonaws.com/plink1-assets/dev/plink_mac.zip">download</a></td>
    <td><a href="https://s3.amazonaws.com/plink1-assets/1.07/plink1_mac.zip">download (32-bit)</a></td>
  </tr>
  <tr>
    <td>Windows 64-bit</td>
    <td><a href="https://s3.amazonaws.com/plink1-assets/plink_win64_20231211.zip">download</a></td>
    <td><a href="https://s3.amazonaws.com/plink1-assets/dev/plink_win64.zip">download</a></td>
    <td rowspan="2"><a href="https://s3.amazonaws.com/plink1-assets/1.07/plink1_win32.zip">download</a></td>
  </tr>
  <tr>
    <td>Windows 32-bit</td>
    <td><a href="https://s3.amazonaws.com/plink1-assets/plink_win32_20231211.zip">download</a></td>
    <td><a href="https://s3.amazonaws.com/plink1-assets/dev/plink_win32.zip">download</a></td>
  </tr>
</table>
"""  # noqa


class MockHTTPResponse(io.BytesIO):
    def __init__(self, content, status=200, reason="OK", headers=None):
        super().__init__(content)
        self.status = status
        self.reason = reason
        self.headers = headers or {}

    def read(self, amt=None):
        return super().read(amt)

    def getheader(self, name, default=None):
        return self.headers.get(name, default)

    def getheaders(self):
        return self.headers.items()

    def close(self):
        pass


class TestPlinkBinDownloader(unittest.TestCase):
    def setUp(self):
        self.target_folder = "test_folder"
        self.target_fname = "plink"
        self.downloader = PlinkBinDownloader(self.target_folder, self.target_fname)

    @patch("urllib.request.urlopen")
    def test_download_links(self, mock_urlopen):
        mock_urlopen.return_value = MockHTTPResponse(MOCK_DOWNLOAD_HTML)
        self.assertTrue(len(self.downloader.download_links) > 1)
        for link in self.downloader.download_links:
            self.assertTrue(link.startswith("https://"))
            self.assertTrue(link.endswith(".zip"))

    @patch("platform.architecture")
    @patch("platform.system")
    def test_platform_key(self, mock_system, mock_architecture):
        mock_system.return_value = "Windows"
        mock_architecture.return_value = ("64bit", "")
        self.assertEqual(self.downloader.platform_key, "win64")
        del self.downloader.platform_key

        mock_system.return_value = "Darwin"
        mock_architecture.return_value = ("64bit", "")
        self.assertEqual(self.downloader.platform_key, "mac")
        del self.downloader.platform_key

        mock_system.return_value = "Linux"
        mock_architecture.return_value = ("64bit", "")
        self.assertEqual(self.downloader.platform_key, "linux_x86_64")
        del self.downloader.platform_key

    def test_target_path(self):
        expected_path = Path(self.target_folder).absolute() / self.target_fname
        self.assertEqual(self.downloader.target_path, expected_path)

    @patch("urllib.request.urlopen")
    @patch("zipfile.ZipFile")
    @patch("builtins.open", new_callable=mock_open)
    def test_download_plink(self, mock_open, mock_zipfile, mock_urlopen):
        mock_urlopen.return_value = MockHTTPResponse(b"Fake zip content")

        mock_zip = MagicMock()
        mock_zip.namelist.return_value = ["plink"]
        mock_zipfile.return_value.__enter__.return_value = mock_zip

        mock_open().write.return_value = None

        self.downloader.download_links = ["https://example.com/plink_win64.zip"]
        self.downloader.platform_key = "win64"
        result_path = self.downloader.download_plink()

        self.assertEqual(result_path, self.downloader.target_path)
        self.assertEqual(mock_open.call_count, 2)

    @patch("pathlib.Path.iterdir")
    @patch("os.remove")
    def test_cleanup_folder(self, mock_remove, mock_listdir):
        mock_listdir.return_value = ["file1", "file2", self.target_fname]
        self.downloader.cleanup_folder()
        self.assertEqual(mock_remove.call_count, 2)

    @patch("pathlib.Path.mkdir")
    def test_make_dir(self, mock_mkdir):
        self.downloader.make_dir()
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

    @patch("pathlib.Path.chmod")
    @patch("pathlib.Path.stat")
    def test_allow_executing_plink(self, mock_stat, mock_chmod):
        mock_stat.return_value.st_mode = 0o644
        self.downloader.platform_key = "linux_x86_64"
        self.downloader.allow_executing_plink()
        mock_chmod.assert_called_once_with(0o755)

    @patch("pathlib.Path.exists")
    @patch.object(PlinkBinDownloader, "download_plink")
    @patch.object(PlinkBinDownloader, "make_dir")
    @patch.object(PlinkBinDownloader, "allow_executing_plink")
    def test_ensure_plink(
        self, mock_allow_exec, mock_make_dir, mock_download, mock_exists
    ):
        mock_exists.side_effect = [False, True]
        result_path = self.downloader.ensure_plink()

        mock_make_dir.assert_called_once()
        mock_download.assert_called_once()
        mock_allow_exec.assert_called_once()
        self.assertEqual(result_path, self.downloader.target_path)
