import typing


class LLM(typing.Protocol):
    """Language model interface."""

    pass  # pragma: no cover


class TextLLM(typing.Protocol):
    """Language model interface that generates text from text."""

    def generate(self, input_text: str) -> str: ...


class FunctionBasedTextLLM:
    """Text-based language model wrapper.
    It wraps a function that generates text by the given text.
    """

    _gen: typing.Callable[[str], str]

    def __init__(self, generate_text_by_text: typing.Callable[[str], str]):
        """Initialize a TextBasedLLMWrapper.

        Args:
            generate_text_by_text: (input_text: str) -> (output_text: str)
                A function that generates text by the given text.
        """
        if not callable(generate_text_by_text):
            raise TypeError("generate_text_by_text must be callable")
        self._gen = generate_text_by_text

    def generate(self, input_text: str) -> str:
        """Generate text by the given text.

        Args:
            input_text: The input text. It must be a str.

        Returns:
            The generated text. It is a str."""
        return self._gen(input_text)
