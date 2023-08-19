#!/usr/bin/env bash

set -eu

cd "$(dirname "$0")/.."

FIX=false
TARGET_DIRS=""

for arg in "$@"; do
    if [ "$arg" == "--fix" ]; then
        FIX=true
    else
        if [ -z "$TARGET_DIRS" ]; then
            TARGET_DIRS="$arg"
        else
            TARGET_DIRS="$TARGET_DIRS $arg"
        fi
    fi
done

if [ -z "$TARGET_DIRS" ]; then
    TARGET_DIRS="promptogen examples"
fi

echo "Linting ${TARGET_DIRS}"

poetry run flake8 ${TARGET_DIRS}
poetry run mypy ${TARGET_DIRS}

if $FIX; then
    poetry run black ${TARGET_DIRS}
    poetry run isort ${TARGET_DIRS}
    exit 0
fi

poetry run black --check ${TARGET_DIRS}
poetry run isort --check-only ${TARGET_DIRS}
