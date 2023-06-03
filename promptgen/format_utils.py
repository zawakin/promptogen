from typing import Any

from promptgen.dataclass import DataClass


def with_code_block(language: str, s: str) -> str:
    """Wrap the string in a code block.

    Args:
        language (str): The language of the code block.
        s (str): The string to wrap.

    Returns:
        str: The string wrapped in a code block.
    """
    return f"```{language}\n{s}```"


def remove_code_block(language: str, s: str) -> str:
    """Remove the code block from the string.

    Args:
        language (str): The language of the code block.
        s (str): The string to remove the code block from.

    Returns:
        str: The string without the code block.
    """
    return s.replace(f"```{language}", "").replace("```", "").strip()


def convert_data_class_to_dict(obj: DataClass | dict) -> dict[str, Any]:
    if isinstance(obj, DataClass):
        return obj.dict()
    if isinstance(obj, dict):
        return {k: convert_data_class_to_dict(v) for k, v in obj.items()}
    return obj
