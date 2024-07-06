import unittest
from unittest.mock import patch
from pathlib import Path
from datetime import datetime

from library.enums.plink_keywords import PlinkKeyword
from library.converters.plink import Plink
from library.tools.collections import EnumList

PLINK_MODULE = "library.converters.plink"


class TestPlink(unittest.TestCase):
    def setUp(self):
        self.plink = Plink()

    def test_initialization_with_custom_binary(self):
        custom_binary = "/custom/path/to/plink"
        plink = Plink(custom_binary)
        self.assertEqual(plink.PLINK_CMD, Path(custom_binary).absolute())

    def test_initialization_with_default_binary(self):
        self.assertEqual(self.plink.PLINK_CMD, "plink")

    @patch(f"{PLINK_MODULE}.Plink.run_cmd")
    def test_info_property(self, mock_run_cmd):
        mock_run_cmd.return_value = b"PLINK v1.90b3 64-bit (21 Jun 2015)"
        info = self.plink.info
        self.assertEqual(info["name"], "PLINK")
        self.assertEqual(info["version"], "v1.90b3")
        self.assertEqual(info["architecture"], "64-bit")
        self.assertEqual(info["release_date"], datetime(2015, 6, 21))
        mock_run_cmd.assert_called_once_with(["plink", "--version"])

    def test_to_plink_format(self):
        self.assertEqual(
            self.plink.to_plink_format(PlinkKeyword.FILE, "path/to/file"),
            Path("path/to/file").absolute(),
        )
        self.assertEqual(
            self.plink.to_plink_format(PlinkKeyword.OUT, "output/path"),
            Path("output/path").absolute(),
        )
        self.assertEqual(
            self.plink.to_plink_format(PlinkKeyword.VERSION, "v1.90b3"), "v1.90b3"
        )

    def test_make_cmd_with_args_and_kwargs(self):
        cmd = self.plink.make_cmd(PlinkKeyword.VERSION, file="data")
        expected_cmd = ["plink", "--version", "--file", str(Path("data").absolute())]
        self.assertEqual(cmd, expected_cmd)

    @patch("subprocess.run")
    def test_run_cmd_success(self, mock_subprocess_run):
        mock_subprocess_run.return_value.returncode = 0
        mock_subprocess_run.return_value.stdout = b"success"
        cmd = ["plink", "--version"]
        output = self.plink.run_cmd(cmd)
        self.assertEqual(output, b"success")
        mock_subprocess_run.assert_called_once_with(
            cmd, capture_output=True, text=False
        )

    @patch("subprocess.run")
    def test_run_cmd_failure(self, mock_subprocess_run):
        mock_subprocess_run.return_value.returncode = 1
        mock_subprocess_run.return_value.stderr = b"error"
        cmd = ["plink", "--version"]
        with self.assertRaises(RuntimeError) as context:
            self.plink.run_cmd(cmd, "Custom error: {}")
        self.assertEqual(str(context.exception), "Custom error: b'error'")
        mock_subprocess_run.assert_called_once_with(
            cmd, capture_output=True, text=False
        )

    @patch("subprocess.run")
    def test_run_cmd_file_not_found(self, mock_subprocess_run):
        mock_subprocess_run.side_effect = FileNotFoundError
        cmd = ["plink", "--version"]
        with self.assertRaises(RuntimeError) as context:
            self.plink.run_cmd(cmd)
        self.assertEqual(str(context.exception), "Plink is not installed.")
        mock_subprocess_run.assert_called_once_with(
            cmd, capture_output=True, text=False
        )

    @patch(f"{PLINK_MODULE}.Plink.run_cmd")
    def test_run(self, mock_run_cmd):
        self.plink.run(PlinkKeyword.VERSION)
        expected_cmd = ["plink", "--version"]
        mock_run_cmd.assert_called_once_with(expected_cmd)

    @patch("warnings.warn")
    def test_make_cmd_with_invalid_keyword(self, mock_warn):
        cmd = self.plink.make_cmd(PlinkKeyword.VERSION, invalid_arg="value")
        expected_cmd = ["plink", "--version", "--invalid-arg", "value"]
        self.assertEqual(cmd, expected_cmd)
        mock_warn.assert_called_once_with(
            "Unsafely converted command 'invalid_arg' to '--invalid-arg'. "
            "Please notify the developer to fix this."
        )

    def test_make_cmd_with_additional_keywords(self):
        test_cases = [
            (PlinkKeyword.CHR_SET, "24"),
            (PlinkKeyword.CHR, "1"),
            (PlinkKeyword.GENO, "0.01"),
            (PlinkKeyword.MIND, "0.1"),
            (PlinkKeyword.MAF, "0.05"),
            (PlinkKeyword.AUTOSOME, True),
            (PlinkKeyword.WE, True),
            (PlinkKeyword.MAKE_BED, True),
            (PlinkKeyword.COW, True),
            (PlinkKeyword.PCA, "10"),
        ]
        for keyword, value in test_cases:
            with self.subTest(keyword=keyword, value=value):
                cmd = self.plink.make_cmd(**{keyword.name.lower(): value})
                if isinstance(value, bool):
                    expected_cmd = ["plink", keyword.value]
                else:
                    expected_cmd = ["plink", keyword.value, str(value)]
                self.assertEqual(EnumList(cmd), EnumList(expected_cmd))

    @patch("subprocess.run")
    def test_run_cmd_with_additional_keywords(self, mock_subprocess_run):
        mock_subprocess_run.return_value.returncode = 0
        mock_subprocess_run.return_value.stdout = b"success"
        cmd = self.plink.make_cmd(
            file="datafile", chr="1", geno="0.01", mind="0.1", out="output_prefix"
        )
        expected_cmd = [
            "plink",
            "--file",
            str(Path("datafile").absolute()),
            "--chr",
            "1",
            "--geno",
            "0.01",
            "--mind",
            "0.1",
            "--out",
            str(Path("output_prefix").absolute()),
        ]
        self.assertEqual(cmd, expected_cmd)
        output = self.plink.run_cmd(cmd)
        self.assertEqual(output, b"success")
        mock_subprocess_run.assert_called_once_with(
            expected_cmd, capture_output=True, text=False
        )

    @patch(f"{PLINK_MODULE}.Plink.run_cmd")
    def test_run_with_additional_keywords(self, mock_run_cmd):
        self.plink.run(
            file="datafile", chr="1", geno="0.01", mind="0.1", out="output_prefix"
        )
        expected_cmd = [
            "plink",
            PlinkKeyword.FILE,
            str(Path("datafile").absolute()),
            PlinkKeyword.CHR,
            "1",
            PlinkKeyword.GENO,
            "0.01",
            PlinkKeyword.MIND,
            "0.1",
            PlinkKeyword.OUT,
            str(Path("output_prefix").absolute()),
        ]
        mock_run_cmd.assert_called_once_with(expected_cmd)
