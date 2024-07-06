# cmd-parser

[![PyPI - Version](https://img.shields.io/pypi/v/cmd-parser.svg)](https://pypi.org/project/cmd-parser)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cmd-parser.svg)](https://pypi.org/project/cmd-parser)

The `cmd-parser` library provides a simple way to parse command-line style input strings into a structured dictionary format. This is useful for applications that need to interpret commands with arguments and parameters.

---

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

You can install the Command Parser Library using pip:

```console
pip install cmd-parser
```

## Usage

Here's a quick example of how to use the library:

```python
from cmd_parser.core import asdict, parse

command_string = '!command arg1 arg2 param1="value1 test" param2=value2'
parsed_command = parse(command_string)
print(asdict(parsed_command))
```

This will output:

```python
{
    'command': 'command',
    'args': ['arg1', 'arg2'],
    'kwargs': {
        'param1': 'value1 test',
        'param2': 'value2'
    }
}
```

## License

`cmd-parser` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
