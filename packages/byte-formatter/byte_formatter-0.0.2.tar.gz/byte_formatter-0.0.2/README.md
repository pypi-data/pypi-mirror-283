# Byte-Formatter

Byte-Formatter is a Python project for formatting bytes into a human-readable format. It supports various units and styles, including binary, decimal, SI units, and Unix-style units.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Local Usage](#local-usage)
  - [Basic Usage](#basic-usage)
  - [Advanced Options](#advanced-options)
  - [Examples](#examples)
- [Features](#features)
- [License](#license)

## Installation

To install Byte-Formatter, you need to have Python 3.7 or higher and Poetry installed on your system. Follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/byte-formatter.git
   ```
2. Navigate to the project directory:
   ```bash
   cd byte-formatter
   ```
3. Install the dependencies using Poetry:
   ```bash
   poetry install
   ```

## Usage

### Local Usage

To use Byte-Formatter locally, you can run it through Poetry:

```bash
# Output: 12.3 KB
poetry run byte-formatter 12345
```

This command will format the number `12345` into a human-readable byte format based on the default settings.

### Basic Usage

To format a number into a human-readable byte format with default settings (decimal units and one decimal place):

```bash
# Output: 12.3 KB
byte-formatter 12345
```

### Advanced Options

You can customize the output using the following options:

- `-b, --binary`: Use binary (base-1024) units (KiB, MiB, etc.).
- `-p, --precision <number>`: Set the number of decimal places.
- `-s, --suffix <text>`: Append a custom suffix to the formatted size.
- `-t, --strip-trailing-zeros`: Remove trailing zeros from the formatted size.
- `-S, --si-units`: Use SI units (kB, MB, etc.) which are base-1000 but with different symbols.
- `-U, --uppercase-units`: Use uppercase unit symbols (KB, MB). This is the default setting.
- `-l, --lowercase-units`: Use lowercase unit symbols (kb, mb), overriding the default uppercase setting.
- `-v, --verbose`: Use verbose unit names (Bytes, Kilobytes, etc.).
- `-x, --unix-style`: Use single-letter Unix-style unit names (B, K, M, G, T, P).

### Examples

Format a size using binary units with two decimal places:

```bash
# Output: 12.06 KiB
poetry run byte-formatter 12345 -b -p 2
```

Format a size with verbose unit names and no trailing zeros:

```bash
# Output: 2.0 Kilobytes
poetry run byte-formatter 2048 -v -t
```

Use SI units with lowercase symbols and a custom suffix:

```bash
# Output: 5.0 MB of data
poetry run byte-formatter 5000000 -S -l -s " of data"
```

## Features

Byte-Formatter offers the following features:

- Support for binary (base-1024) and decimal (base-1000) units.
- Option to use SI units with different symbols.
- Verbose and Unix-style unit names.
- Customizable precision and option to strip trailing zeros.

## License

Byte-Formatter is licensed under the MIT License. See the LICENSE file for more details.
