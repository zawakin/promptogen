TARGET_DIR="promptgen"

flake8 "${TARGET_DIR}"
mypy "${TARGET_DIR}"
black "${TARGET_DIR}"
isort "${TARGET_DIR}"
