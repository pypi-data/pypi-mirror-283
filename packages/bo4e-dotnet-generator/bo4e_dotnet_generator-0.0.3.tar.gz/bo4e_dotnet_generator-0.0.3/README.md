# Generate C# Code from BO4E JSON Schemas

This tool generates C# dotnet classes based on [BO4E-JSON-Schemas](https://github.com/bo4e/BO4E-Schemas).
For fetching last json schemas it uses [`BO4E-Schema-Tool`](https://github.com/bo4e/BO4E-Schema-Tool) tool.
it takes advantage of QuickType npm package to generate C# classes from JSON schemas.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python Versions (officially) supported](https://img.shields.io/pypi/pyversions/bo4e-dotnet-generator.svg)
![Pypi status badge](https://img.shields.io/pypi/v/bo4e-dotnet-generator)
![Unittests status badge](https://github.com/Hochfrequenz/bo4e-dotnet-generator.py/workflows/Unittests/badge.svg)
![Coverage status badge](https://github.com/Hochfrequenz/bo4e-dotnet-generator.py/workflows/Coverage/badge.svg)
![Linting status badge](https://github.com/Hochfrequenz/bo4e-dotnet-generator.py/workflows/Linting/badge.svg)
![Black status badge](https://github.com/Hochfrequenz/bo4e-dotnet-generator.py/workflows/Formatting/badge.svg)

## How to use this Tool (as a user)
```bash
pip install bo4e-dotnet-generator
```

## How to use this Repository on Your Machine (as a developer)

Please follow the instructions in our
[Python Template Repository](https://github.com/Hochfrequenz/python_template_repository#how-to-use-this-repository-on-your-machine).
And for further information, see the [Tox Repository](https://github.com/tox-dev/tox).

### Quicktype Executable Path

This script checks the `APPDATA` environment variable to find the `Quicktype.cmd` npm package in the AppData path on Windows.
