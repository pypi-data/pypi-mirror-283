# API Testing Toolkit

[![PyPI - Version](https://img.shields.io/pypi/v/api-testing-toolkit.svg)](https://pypi.org/project/api-testing-toolkit)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/api-testing-toolkit.svg)](https://pypi.org/project/api-testing-toolkit)

-----

## Installation

Mac or Linux (inside `$HOME` or another directory of your choice)
```sh
python3 -m venv api-testing
source api-testing/bin/activate
pip install --upgrade pip
pip install api-testing-toolkit
```

Windows TBD

## Development

Clone this repository and do this (for mac or linux, nothing for windows yet).

```sh
python3 -m venv .env
source .env/bin/activate
pip install --upgrade pip
pip install --editable .
```

Set your IDE to that .env venv and use the same to pull up jupyter in your target directory. If you change the code,
you'll need to reset the jupyter kernel.

## Usage

This package is meant to be used with Jupyter Lab. Installing this package will also
install Jupyter Lab, so you only need to install the one package. You can either run
Jupyter via CLI with the venv activated or point the desktop version at the venv
(that's my recommendation).

The toolkit provides a few utility functions that can be ignored if you don't want to
use them. The important part is the pattern, not the details.

## License

`api-testing-toolkit` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
