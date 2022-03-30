import unittest
from unittest.mock import patch, Mock, _ANY

import requests

from lc_parser import make_list, parse_page


class TestUnits(unittest.TestCase):

    def test_make_list(self):
        """
        Emulate BeautifulSoup Tag object that contains the table,
        check if it works as expected.
        """
        cell1 = Mock(); cell2 = Mock(); cell3 = Mock(); cell4 = Mock()  # noqa E702
        cell1.text = '1. Two Sum'
        cell2.text = '48.4%'
        cell3.text = ''         # should be skipped
        cell4.text = 'Easy'
        row1 = Mock()
        row1.contents = [cell1, cell2, cell3, cell4]
        row3 = row2 = row1
        table = Mock()
        table.contents = [row1, row2, row3]
        result, errors = make_list(table)
        self.assertIsInstance(result, list)
        self.assertEqual(errors, 0)
        self.assertEqual(len(result), 3)
        self.assertEqual(len(result[0]), 4)
        for row in result:
            with self.subTest(row=row):
                self.assertEqual(row, [1, 'Two Sum', 48.4, 'easy'])

    def test_parse_page_fromfile(self):
        """
        Get page html as str from fixture file, check parsing result
        """
        with open('tests/fixtures/page.txt', 'r', encoding='utf8') as file:
            html_as_str = file.read()
        result_mock = Mock()
        result_mock.text = html_as_str
        with patch.object(requests, 'get', return_value=result_mock) as mock:
            rows, errors = parse_page(
                'www.mocking-mock.com/mocks', page_no=42)
            mock.assert_called_once_with(
                'www.mocking-mock.com/mocks',
                params=_ANY(), allow_redirects=_ANY()
            )
        self.assertEqual(len(rows), 50)
        self.assertEqual(errors, 0)
        self.assertEqual(rows[0], [1, 'Two Sum', 48.4, 'easy'])
