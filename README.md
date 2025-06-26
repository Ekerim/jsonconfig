# jsonconfig

A Python library for reading and writing JSON configuration files. Comments and control characters are removed during parsing and are not preserved.

## Features

- Read and write JSON files or strings with a simple API
- Removes comments and control characters during parsing (not preserved)
- Automatically converts numeric strings to `int` or `float` where possible
- Handles all valid JSON types (dict, list, str, int, float, bool, null)

## Installation

You can install directly from source:

```bash
pip install git+https://github.com/Ekerim/jsonconfig.git
```

## Usage

### Basic Example

```python
from jsonconfig import readconfig, writeconfig

# Write a configuration to a file
config = {"foo": 123, "bar": [1, 2, 3], "baz": {"nested": True}}
writeconfig("config.json", config)

# Read the configuration back from the file
loaded = readconfig("config.json")
print(loaded)  # Output: {'foo': 123, 'bar': [1, 2, 3], 'baz': {'nested': True}}
```

### Reading from a JSON string

```python
json_str = '{"foo": "42", "bar": ["1.5", "2"]}'
config = readconfig(json_str)
print(config)  # Output: {'foo': 42, 'bar': [1.5, 2]}
```

### Comments and Control Characters

```python
relaxed = '''
// This is a comment
{"foo": 1, "bar": 2, "baz": "a\x01b\x02c"} // another comment
'''
config = readconfig(relaxed)
print(config)  # Output: {'foo': 1, 'bar': 2, 'baz': 'abc'}
```

> Comments and control characters (such as non-printable ASCII) are removed during parsing and are not preserved in the resulting data.

### Customizing Output Formatting

You can control indentation and key sorting when writing JSON:

```python
writeconfig("pretty.json", config, indent=4, sort_keys=False)
```

## API

- `readconfig(source: str) -> Any`: Read and parse a JSON configuration from a file path or JSON string.
- `writeconfig(file: str, source: Union[str, dict, list], indent: int = 2, sort_keys: bool = True) -> None`: Write JSON data to a file, with optional formatting.

## License

This project is licensed under the GNU Lesser General Public License v3 (LGPLv3). See the [LICENSE](./LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## Contact

For questions or support, please contact [ekerim@gmail.com](mailto:ekerim@gmail.com).
