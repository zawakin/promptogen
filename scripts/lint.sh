#!/usr/bin/env bash

set -eu

cd "$(dirname "$0")/.."

TARGET_DIRS="${@:-promptogen examples}"
echo "Linting ${TARGET_DIRS}"

poetry run flake8 ${TARGET_DIRS}
poetry run mypy ${TARGET_DIRS}

# if `--fix` is passed, then fix the code
if [[ "$*" == *--fix* ]]; then
    poetry run black ${TARGET_DIRS}
    poetry run isort ${TARGET_DIRS}
    exit 0
fi

poetry run black --check ${TARGET_DIRS}
poetry run isort --check-only ${TARGET_DIRS}
