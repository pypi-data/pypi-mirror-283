# Data Extract-Load-Transform for Autosink Project

[🇬🇧](README.md) | [🇰🇷](README.kr.md) | [🇨🇳](README.zh-CN.md)

Parse the values in the data lake and load them into memory, then make it executable for the data labeler. It organizes the labeled data into a format that is easy for the feature store to store. The autosink-data-elt contains utility classes and data type definitions for reading and writing json files stored in the data lake. When the data extracted from the Raspberry Pi is stored in the data lake, it is loaded, labeled, and transformed into a form that can be stored in the feature store, so it is named ELT.

## Features

- [ ] Parse the values in the data lake and load them into memory, then organize them into a format that is easy for the data labeler to read.
- [ ] Call the data labeler.
- [ ] Store the labeled data in the feature store.

# Environment

The environment is based on MacOS and Linux.

## `Makefile`

The `Makefile` has the following functions.

### `make lint`

- To use the `.vscode` settings, install the `pylint` extension.
- Override the options specified in the `pyproject.toml` file to lint the code with the default settings of the linter.

### `make format`

- The formatter uses google's `yapf`.
- Override the options specified in the `pyproject.toml` file to format the code with the default settings of the `yapf` formatter.
- To use the `.vscode` settings, install the `yapf` extension.

### `make test`

- The test uses `unittest`.
- Supports both `test_*.py` and `*_test.py` patterns.
- The test file must be connected to `__init__.py` up to the location where the test file exists.

### `make publish`

- Write the `~/.pypirc` file as follows.
    ```
    [pypi]
    username = __token__
    password = pypi-어쩌고저쩌고 # Write your personal API token.
    ```
- This command uses `flit` to push the package to the PyPI public registry.
- The package uploaded with the name specified earlier as `