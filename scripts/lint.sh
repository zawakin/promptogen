#!/usr/bin/env bash

set -eu

cd "$(dirname "$0")/.."

TARGET_DIR="promptgen"

poetry run flake8 "${TARGET_DIR}"
poetry run mypy "${TARGET_DIR}"
poetry run black --check "${TARGET_DIR}"
poetry run isort --check-only "${TARGET_DIR}"
