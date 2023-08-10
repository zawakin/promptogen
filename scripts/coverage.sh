#!/usr/bin/env bash

set -eu

cd "$(dirname "$0")/.."

TEST_DIR="tests"

poetry run pytest -vv --cov=promptogen --cov-report=xml "$TEST_DIR"
