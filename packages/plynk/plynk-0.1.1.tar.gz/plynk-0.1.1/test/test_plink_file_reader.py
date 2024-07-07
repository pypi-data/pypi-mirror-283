import unittest
from unittest.mock import patch
from pathlib import Path
import pandas as pd
from plynk.enums.plink_filetypes import PlinkFileType
from plynk.enums.plink_headers import DEFAULT_HEADERS
from plynk.parsers.plink_file_reader import PlinkFileReader


class TestPlinkFileReader(unittest.TestCase):
    def setUp(self):
        self.plink_prefix = "/test/path"
        self.reader = PlinkFileReader(self.plink_prefix)

    @patch("os.listdir")
    def test_find_files(self, mock_listdir):
        mock_listdir.return_value = ["file1.ped", "file2.map", "file3.log"]
        expected_files = [
            Path(self.plink_prefix, "file1.ped").absolute(),
            Path(self.plink_prefix, "file2.map").absolute(),
            Path(self.plink_prefix, "file3.log").absolute(),
        ]
        files = self.reader.find_files(self.plink_prefix)
        self.assertEqual(files, expected_files)

    @patch.object(PlinkFileReader, "find_files")
    def test_find_file_by_type(self, mock_find_files):
        mock_find_files.return_value = [
            Path(self.plink_prefix, "test.ped").absolute(),
            Path(self.plink_prefix, "test.map").absolute(),
        ]
        file_path = self.reader.find_file_by_type(PlinkFileType.PED)
        self.assertEqual(file_path, Path(self.plink_prefix, "test.ped").absolute())

    @patch.object(PlinkFileReader, "find_files")
    def test_find_file_by_type_not_found(self, mock_find_files):
        mock_find_files.return_value = [Path(self.plink_prefix, "test.map").absolute()]
        with self.assertRaises(FileNotFoundError):
            self.reader.find_file_by_type(PlinkFileType.PED)

    def test_get_headers(self):
        dataset = pd.DataFrame(
            columns=[
                "Family ID",
                "Individual ID",
                "Marker 1",
                "Paternal ID",
                "Maternal ID",
                "Sex",
                "Phenotype",
            ]
        )
        headers = self.reader.get_headers(PlinkFileType.PED, dataset, "Marker")
        expected_headers = DEFAULT_HEADERS[PlinkFileType.PED] + ["Marker 1"]
        self.assertEqual(sorted(headers), sorted(expected_headers))

    def test_get_headers_unsupported_type(self):
        dataset = pd.DataFrame(columns=["col1", "col2"])
        with self.assertRaises(TypeError):
            self.reader.get_headers("unsupported_type", dataset)

    @patch.object(PlinkFileReader, "find_file_by_type")
    @patch("pandas.read_csv")  # TODO: Use non-proprietary template data!
    def test_load_data_with_headers(self, mock_read_csv, mock_find_file_by_type):
        mock_find_file_by_type.return_value = Path(
            self.plink_prefix, "test.het"
        ).absolute()
        mock_read_csv.return_value = pd.DataFrame(
            [[1, 2, 3, 4, 5, 6]],
            columns=["FID", "IID", "O(HOM)", "E(HOM)", "N(NM)", "F"],
        )

        dataset = self.reader.load_data(PlinkFileType.HET)
        expected_headers = DEFAULT_HEADERS[PlinkFileType.HET]
        self.assertEqual(list(dataset.columns), expected_headers)

    @patch.object(PlinkFileReader, "find_file_by_type")
    @patch("pandas.read_csv")  # TODO: Use non-proprietary template data!
    def test_load_data_without_headers(self, mock_read_csv, mock_find_file_by_type):
        mock_find_file_by_type.return_value = Path(
            self.plink_prefix, "test.ped"
        ).absolute()
        mock_read_csv.return_value = pd.DataFrame(
            [[1, 2, 3, 4, 5, 6, "A"]], columns=[0, 1, 2, 3, 4, 5, 6]
        )

        dataset = self.reader.load_data(PlinkFileType.PED, numerated_colname="Marker")
        expected_headers = DEFAULT_HEADERS[PlinkFileType.PED] + ["Marker 1"]
        self.assertEqual(list(dataset.columns), expected_headers)

    @patch("pandas.read_csv")  # TODO: Use non-proprietary template data!
    def test_read_file(self, mock_read_csv):
        file_path = Path(self.plink_prefix, "test.ped").absolute()
        self.reader.read_file(file_path, sep=",")
        mock_read_csv.assert_called_once_with(file_path, sep=",")

    @patch.object(PlinkFileReader, "find_file_by_type")
    @patch("pandas.read_csv")  # TODO: Use non-proprietary template data!
    def test_load_data_non_default_encoding(
        self, mock_read_csv, mock_find_file_by_type
    ):
        mock_find_file_by_type.return_value = Path(
            self.plink_prefix, "test.ped"
        ).absolute()
        mock_read_csv.return_value = pd.DataFrame(
            [[1, 2, 3, 4, 5, 6]], columns=[0, 1, 2, 3, 4, 5]
        )
        reader = PlinkFileReader(self.plink_prefix, encoding="latin-1")

        _ = reader.load_data(PlinkFileType.PED)
        mock_read_csv.assert_called_with(
            Path(self.plink_prefix, "test.ped").absolute(), sep=r"\s+", header=None
        )

    @patch.object(PlinkFileReader, "find_file_by_type")
    @patch("pandas.read_csv")  # TODO: Use non-proprietary template data!
    def test_load_data_with_included_headers(
        self, mock_read_csv, mock_find_file_by_type
    ):
        mock_find_file_by_type.return_value = Path(
            self.plink_prefix, "test.het"
        ).absolute()
        # Mocking the data to include headers
        mock_read_csv.return_value = pd.DataFrame(
            [[1, 2, 3, 4, 5, 6]],
            columns=["FID", "IID", "O(HOM)", "E(HOM)", "N(NM)", "F"],
        )

        dataset = self.reader.load_data(PlinkFileType.HET)
        expected_headers = DEFAULT_HEADERS[PlinkFileType.HET]
        self.assertEqual(list(dataset.columns), expected_headers)
        mock_read_csv.assert_called_with(
            Path(self.plink_prefix, "test.het").absolute(), sep=r"\s+", header=0
        )

    @patch.object(PlinkFileReader, "find_file_by_type")
    @patch("pandas.read_csv")  # TODO: Use non-proprietary template data!
    def test_load_data_without_included_headers(
        self, mock_read_csv, mock_find_file_by_type
    ):
        mock_find_file_by_type.return_value = Path(
            self.plink_prefix, "test.ped"
        ).absolute()
        mock_read_csv.return_value = pd.DataFrame(
            [[1, 2, 3, 4, 5, 6, "A"]], columns=[0, 1, 2, 3, 4, 5, 6]
        )

        dataset = self.reader.load_data(PlinkFileType.PED, numerated_colname="Marker")
        expected_headers = DEFAULT_HEADERS[PlinkFileType.PED] + ["Marker 1"]
        self.assertEqual(list(dataset.columns), expected_headers)
        mock_read_csv.assert_called_with(
            Path(self.plink_prefix, "test.ped").absolute(), sep=r"\s+", header=None
        )
