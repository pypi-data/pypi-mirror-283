import glob
import json
import os

import pytest

import parser_functions
from parser_functions.combinators import Stream
from parser_functions.csv import CSV
from tests.helpers import assert_success

csvs = os.path.join(os.path.dirname(__file__), "data", "csvs")
jsons = os.path.join(os.path.dirname(__file__), "data", "jsons")

csv = CSV()


class TestCSV:
    def test_unquoted_field(self):
        assert_success(
            next(csv.unquoted_field(Stream.from_string('abc 123,'))), 'abc 123', 7
        )
        assert_success(next(csv.unquoted_field(Stream.from_string(',,'))), '', 0)

    def test_quoted_field(self):
        assert_success(
            next(csv.quoted_field(Stream.from_string('"  a,b,c ""bob"" \n alice"'))),
            '  a,b,c "bob" \n alice',
            25,
        )

    def test_field(self):
        assert_success(next(csv.field(Stream.from_string('abc 123,'))), 'abc 123', 7)
        assert_success(
            next(csv.field(Stream.from_string('"  a,b,c ""bob"" \n alice"'))),
            '  a,b,c "bob" \n alice',
            25,
        )

    def test_record(self):
        assert_success(
            next(csv.record(Stream.from_string("  test , a,  b,,c  \r\n"))),
            ["  test ", " a", "  b", "", "c  "],
            19,
        )

    def test_records_simple(self):
        assert_success(
            next(csv.records(Stream.from_string("a,b,c\n1,2,3\n8,9,10\n"))),
            [
                ["a", "b", "c"],
                ["1", "2", "3"],
                ["8", "9", "10"],
            ],
            19,
        )
        assert_success(
            next(csv.records(Stream.from_string("a,b,c\n1,2,3\n8,9,10"))),
            [
                ["a", "b", "c"],
                ["1", "2", "3"],
                ["8", "9", "10"],
            ],
            18,
        )

    @pytest.mark.parametrize(
        "name",
        [
            os.path.splitext(os.path.basename(p))[0]
            for p in glob.glob(os.path.join(csvs, "*.csv"))
        ],
    )
    def test_files(self, name):
        csv_path = os.path.join(csvs, name + ".csv")
        json_path = os.path.join(jsons, name + ".json")
        with open(csv_path, newline="", encoding='utf8') as f:
            received = parser_functions.csv.loads(f.read())
        with open(json_path, encoding='utf8') as f:
            expected = json.load(f)
        assert received == expected

    def test_loads_no_header_false(self):
        example = "a,b,c\n1,2,3\n3,4,5\nfoo,bar,baz\n"
        assert csv.loads(example, header=False) == [
            ['a', 'b', 'c'],
            ['1', '2', '3'],
            ['3', '4', '5'],
            ['foo', 'bar', 'baz'],
        ]

    def test_single_value(self):
        example = "a\nb\nc\n"
        assert csv.loads(example, header=False) == [['a'], ['b'], ['c']]

    def test_missmatched_header_size(self):
        example = "a,b,c\n1,2\n3,4,5,6\n7,8,9"
        with pytest.raises(ValueError):
            csv.loads(example)
