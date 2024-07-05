# PyICU Slugify

A CLDR-compliant slugify function using PyICU.

## Features

- CLDR-compliant slugification
- Support for multiple languages
- Based on the robust ICU library

## Installation

### Prerequisites

Before installing PyICU Slugify, you need to have the ICU libraries installed on your system. The installation process varies depending on your operating system.

#### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install libicu-dev
```

#### Other Linux Distributions

For other Linux distributions, you'll need to install the ICU development libraries. The package name may vary:

- Fedora/CentOS/RHEL:
  ```bash
  sudo dnf install libicu-devel
  ```

- Arch Linux:
  ```bash
  sudo pacman -S icu
  ```

- OpenSUSE:
  ```bash
  sudo zypper install libicu-devel
  ```

After installing the ICU libraries, you may need to set the `ICU_VERSION` environment variable:

```bash
export ICU_VERSION=$(pkg-config --modversion icu-i18n)
```

#### macOS

Using Homebrew:

```bash
brew install icu4c
export CFLAGS=-I/usr/local/opt/icu4c/include
export LDFLAGS=-L/usr/local/opt/icu4c/lib
```

#### Windows

1. Download the ICU binaries from the official ICU website (http://icu-project.org/download).
2. Extract the binaries to a directory (e.g., C:\icu).
3. Add the bin folder to your PATH environment variable.
4. Set the ICU_ROOT environment variable to the ICU directory.

### Installing PyICU Slugify

Once you have the ICU libraries installed, you can install PyICU Slugify using pip:

```bash
pip install pyicu-slugify
```

If you encounter any issues related to PyICU installation, you may need to specify the ICU library path:

```bash
pip install --global-option=build_ext --global-option="-I/path/to/icu/include" --global-option="-L/path/to/icu/lib" pyicu-slugify
```

Replace /path/to/icu/include and /path/to/icu/lib with the appropriate paths on your system.

## Usage

Here's a basic example of how to use PyICU Slugify:

```python
from pyicu_slugify import pyicu_slugify

# Basic usage
print(pyicu_slugify("Hello World!"))  # Output: hello-world

# Language-specific slugification
print(pyicu_slugify("Über den Wölken", "de"))  # Output: uber-den-wolken
```

## Supported Languages

PyICU Slugify supports all languages available in the ICU library. Some commonly used language codes include:

- 'de' for German
- 'fr' for French
- 'es' for Spanish
- 'zh' for Chinese

For a full list of supported language codes, refer to the CLDR language codes (https://unicode-org.github.io/cldr-staging/charts/37/supplemental/language_plural_rules.html).

## Troubleshooting

If you encounter issues during installation or usage, here are some common problems and solutions:

1. ICU libraries not found: Ensure that the ICU libraries are correctly installed and that the library path is correctly set in your environment variables.

2. Incompatible ICU version: Make sure the installed ICU version is compatible with the PyICU version. You may need to upgrade or downgrade either the ICU libraries or PyICU.

3. Compilation errors: On some systems, you may need to install additional development tools. For example:

   On Ubuntu/Debian:
   ```bash
   sudo apt-get install build-essential
   ```

   On Fedora/CentOS/RHEL:
   ```bash
   sudo dnf groupinstall "Development Tools"
   ```

   On macOS:
   ```bash
   xcode-select --install
   ```

4. Python version compatibility: Ensure you're using a compatible Python version. This package is tested with Python 3.7 and above.

If you continue to experience issues, please open an issue on the GitHub repository with details about your system and the error you're encountering.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.