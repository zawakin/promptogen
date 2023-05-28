TARGET_DIR="promptgen"

poetry run flake8 "${TARGET_DIR}"
poetry run black "${TARGET_DIR}"
poetry run isort "${TARGET_DIR}"
