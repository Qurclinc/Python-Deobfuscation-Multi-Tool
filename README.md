# Python Deobfuscation Multi-Tool

## Disclaimer

**This tool is created for educational purposes only. The author is not responsible for any misuse of this software.**

## Overview

Python Deobfuscation Multi-Tool is a command-line utility designed to analyze and deobfuscate obfuscated Python scripts and projects. It supports various obfuscation methods, including Kramer, Zlib+Base64, and Marshal (More may be added later).

## Features

- Detects and deobfuscates different types of Python obfuscation.

- Supports both single file and full project deobfuscation.

- Automatically iterates through multiple layers of obfuscation.

- Cross-Platform.

# Installation

## Prerequisites

- Python 3.7+

- pip (Python package manager)

## Install Dependencies

`
pip install -r requirements.txt
`

# Usage

## Deobfuscate a Single File

`
python main.py --source_file <path/to/obfuscated.py> --destination_file <path/to/deobfuscated.py>
`

**Example:**

`
python main.py -i obfuscated.py -o deobfuscated.py
`

## Deobfuscate an Entire Project

`
python main.py --root <path/to/obfuscated_project>
`

**Example:**

`
python main.py -r /path/to/project
`

## License

This project is licensed under the MIT License.

## Contribution

Feel free to fork the project and submit pull requests for improvements or additional deobfuscation methods.

## Contact

For questions or issues, open an issue on GitHub or contact me via telegram @user0635.