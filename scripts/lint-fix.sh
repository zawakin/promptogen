#!/usr/bin/env bash

set -eu

cd "$(dirname "$0")/.."

TARGET_DIR="promptgen"

poetry run flake8 "${TARGET_DIR}"
poetry run mypy "${TARGET_DIR}"
poetry run black "${TARGET_DIR}"
poetry run isort "${TARGET_DIR}"

TARGET_DIR="examples"

poetry run flake8 "${TARGET_DIR}"
poetry run mypy "${TARGET_DIR}"
poetry run black "${TARGET_DIR}"
poetry run isort "${TARGET_DIR}"
