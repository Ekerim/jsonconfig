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

"""
jsonconfig.main

Provides functions for reading and writing JSON configuration files. Comments and control characters are removed during parsing and are not preserved. Also supports automatic type conversion for numeric strings.
"""
import os
import json
import logging
import re
from typing import Any, Union

logger = logging.getLogger(__name__)


class _Decoder(json.JSONDecoder):
    """
    Custom JSON decoder that attempts to convert string values to int or float when possible.
    """
    def decode(self, s: str, **kwargs) -> Any:
        """
        Decode a JSON document to a Python object, converting string values to int or float if possible.

        Args:
            s: The JSON string to decode.
            **kwargs: Additional keyword arguments for the base decoder.
        Returns:
            The decoded Python object, with string values converted to int or float where possible.
        """
        result = super().decode(s)
        return self._decode(result)

    def _decode(self, o: Any) -> Any:
        """
        Recursively convert string values in the decoded object to int or float if possible.

        Args:
            o: The object to process.
        Returns:
            The processed object with string values converted to int or float where possible.
        """
        # Check if a string value contain ...
        if isinstance(o, str):
            # ... an INT
            try:
                return int(o)
            except ValueError:
                # ... else i might contain a FLOAT
                try:
                    return float(o)
                except ValueError:
                    # ... No it is just a string.
                    return o
        elif isinstance(o, dict):
            return {k: self._decode(v) for k, v in o.items()}
        elif isinstance(o, list):
            return [self._decode(v) for v in o]
        else:
            return o


def _sanitize_json_string(json_string: str) -> str:
    """
    Remove comments and control characters from a JSON string.
    Does not check for JSON structure; relies on the decoder for validation.

    Args:
        json_string: The raw JSON string to sanitize.
    Returns:
        The sanitized JSON string.
    """
    # Remove comments
    json_string = re.sub(r'^\s*#.*|^\s*//.*|//.*', '', json_string, flags=re.MULTILINE)

    # Strip leading and trailing whitespace
    json_string = json_string.strip()

    # Remove control characters
    json_string = ''.join(ch for ch in json_string if ch >= ' ')

    return json_string


def readconfig(source: str) -> Any:
    """
    Read and parse a JSON configuration from a file path or a JSON string.
    Attempts to convert string values to int or float where possible.

    Args:
        source: Path to a JSON file or a JSON string.
    Returns:
        The parsed Python object (dict, list, or other JSON type).
    Raises:
        ValueError: If the JSON is invalid or unbalanced.
        json.JSONDecodeError: If the JSON cannot be parsed.
    """
    if os.path.isfile(source):
        logger.debug(f"Reading JSON file {source}")
        with open(source, "r") as jsonfile:
            json_content = jsonfile.read()
    else:
        logger.debug("Parsing JSON string")
        json_content = source

    # Sanitize and clean the JSON string
    json_content = _sanitize_json_string(json_content)

    return json.loads(json_content, cls=_Decoder)


def writeconfig(file: str, source: Union[str, dict, list], indent: int = 2, sort_keys: bool = True) -> None:
    """
    Write JSON data to a file, pretty-printed and optionally sorted by keys.

    Args:
        file: The path to the file to write.
        source: The data to write (dict, list, or JSON string).
        indent: Number of spaces for indentation in the output file (default: 2).
        sort_keys: Whether to sort the keys in the output file (default: True).
    Raises:
        ValueError: If the source is not a dict, list, or string.
        json.JSONDecodeError: If the source cannot be parsed as valid JSON.
    """
    logger.debug(f"Writing JSON file {file}")

    if isinstance(source, (dict, list)):
        # If source is a dict or list, convert to JSON string
        json_string = json.dumps(source)
    elif isinstance(source, str):
        json_string = source
    else:
        raise ValueError("Invalid source type. Expected string, dict, or list.")

    sanitized_source = _sanitize_json_string(json_string)
    json_data = json.loads(sanitized_source)

    with open(file, "w") as jsonfile:
        # PrettyPrint json to file.
        json.dump(json_data, jsonfile, indent=indent, sort_keys=sort_keys)
