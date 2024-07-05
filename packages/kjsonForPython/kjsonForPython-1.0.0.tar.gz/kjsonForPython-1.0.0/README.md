# kjson-for-python

This module is a Python encoder and decoder for the KJson format.

## About KJson

KJson is an extended format based on [json](https://www.json.org/) developed by [kuankuan](https://npmjs.org/package/@kuankuan/assist-2024).

KJson originally focused on the transmission of data between programs in different programming languages and technologies, ensuring that data types other than those defined in the basic data types of json format can be transmitted normally.

With the evolution of the technology stack and programming languages used by the team, KJson has gradually spread to other programming languages.

## Installation

```bash
pip install kjsonForPython
```

## Usage

```python
from kjsonForPython import KJson

KJson.stringify(...)
KJson.parse('...')
```

## License

This project is open-source under the [MulanPSL-2.0](LICENSE) license
