#!/usr/bin/env bash

set -eu

cd "$(dirname "$0")/.."

TEST_DIR="tests"

poetry run pytest -vv --cov=promptgen --cov-report=xml "$TEST_DIR"
