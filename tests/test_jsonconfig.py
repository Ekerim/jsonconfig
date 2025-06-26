# Copyright (c) 2025 Fredrik Larsson
# 
# This file is part of the jsonconfig library.
# 
# The jsonconfig library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# The jsonconfig library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this library. If not, see <https://www.gnu.org/licenses/>.

import unittest
import tempfile
import os
from jsonconfig import readconfig, writeconfig
import json

class TestJsonConfig(unittest.TestCase):
    def test_write_and_read_json_file(self):
        data = {"foo": 123, "bar": [1, 2, 3], "baz": {"nested": True}}
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, 'test.json')
            writeconfig(file_path, data)
            result = readconfig(file_path)
            self.assertEqual(result, data)

    def test_write_and_read_json_string(self):
        data = [1, 2, 3, {"a": "b"}]
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, 'test.json')
            writeconfig(file_path, data)
            with open(file_path) as f:
                json_str = f.read()
            result = readconfig(json_str)
            self.assertEqual(result, data)

    def test_read_malformed_json_raises(self):
        malformed = '{"foo": 123, "bar": [1, 2, 3]'
        with self.assertRaises(json.JSONDecodeError):
            readconfig(malformed)

    def test_json_loads_accepts_all_types(self):
        test_cases = [
            '"a string"',
            '123',
            '3.14',
            'true',
            'false',
            'null',
            '[1, 2, 3]',
            '{"a": 1}'
        ]
        for case in test_cases:
            try:
                result = readconfig(case)
            except Exception as e:
                self.fail(f"readconfig failed for input {case}: {e}")

    def test_comments_and_ctrl_characters_removed(self):
        json_with_comments = '''
        // This is a comment
        {"foo": 1, "bar": 2} // another comment
        '''
        result = readconfig(json_with_comments)
        self.assertEqual(result, {"foo": 1, "bar": 2})

        json_with_ctrl = '{"foo": "bar\x01\x02"}'
        result = readconfig(json_with_ctrl)
        self.assertEqual(result, {"foo": "bar"})

    def test_writeconfig_invalid_type_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, 'test.json')
            with self.assertRaises(ValueError):
                writeconfig(file_path, {1, 2, 3})  # set is not valid

    def test_round_trip_nested_structures(self):
        data = {"a": [1, {"b": [2, 3, {"c": "d"}]}]}
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, 'test.json')
            writeconfig(file_path, data)
            result = readconfig(file_path)
            self.assertEqual(result, data)

    def test_empty_structures(self):
        for data in [{}, []]:
            with tempfile.TemporaryDirectory() as tmpdir:
                file_path = os.path.join(tmpdir, 'test.json')
                writeconfig(file_path, data)
                result = readconfig(file_path)
                self.assertEqual(result, data)

    def test_unicode_and_special_characters(self):
        data = {"emoji": "😀", "accented": "café", "newline": "line1\nline2"}
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, 'test.json')
            writeconfig(file_path, data)
            result = readconfig(file_path)
            self.assertEqual(result, data)

if __name__ == "__main__":
    unittest.main()
