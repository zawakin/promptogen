def with_code_block(language: str, s: str) -> str:
    return f"```{language}\n{s}```"


def remove_code_block(language: str, s: str) -> str:
    return s.replace(f"```{language}", "").replace("```", "").strip()
