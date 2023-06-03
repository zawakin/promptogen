from __future__ import annotations


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
