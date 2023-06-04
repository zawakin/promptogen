TARGET_DIR="promptgen"

flake8 "${TARGET_DIR}"
mypy "${TARGET_DIR}"
black --check "${TARGET_DIR}"
isort --check-only "${TARGET_DIR}"
