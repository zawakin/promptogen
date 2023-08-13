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
$ poetry env use 3.8 # Create a virtual environment
$ poetry install --with docs
```

### Running Tests

```bash
$ ./scripts/test.sh
```

## Building the Documentation

```bash
$ poetry run python ./scripts/docs.py build-all
```

## Previewing the Documentation

```bash
$ poetry run python ./scripts/docs.py live <lang>
```

For `<lang>`, specify either `ja` (Japanese) or `en` (English).
```
