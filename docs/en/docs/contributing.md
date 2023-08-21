# Contribution Guide

Bug reports, new feature proposals, pull requests, etc. are highly welcome!

## Setting Up the Environment

Python 3.8 or higher is used for the development of PromptoGen.

### Installing Poetry

https://python-poetry.org/docs/#installation

### Cloning the Repository and Installing Dependencies

```bash
$ git clone https://github.com/zawakin/promptogen.git
$ cd promptogen
$ poetry install --with docs
```

Then, `.venv` is created in the repository root directory.

It is recommended to use the virtual environment created by Poetry.
To activate the virtual environment, run the following command:

```bash
$ poetry shell
```

For more information, see https://python-poetry.org/docs/basic-usage/#activating-the-virtual-environment.

### Running Tests

```bash
$ ./scripts/test.sh
```

### Running Tests with Coverage

```bash
$ ./scripts/coverage.sh
```

### Running Lint

```bash
$ ./scripts/lint.sh
```

### Running Lint with Auto-fix

```bash
$ ./scripts/lint.sh --fix
```

## Building the Documentation (for Maintainers)

```bash
$ poetry run python ./scripts/docs.py build-all
```

## Previewing the Documentation

```bash
$ poetry run python ./scripts/docs.py live <lang>
```

For `<lang>`, specify either `ja` (Japanese) or `en` (English).
