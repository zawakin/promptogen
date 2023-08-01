from abc import ABC, abstractmethod
from typing import Callable, Optional

from promptgen.model.dataclass import DataClass
from promptgen.model.llm import LLM, TextBasedLLM
from promptgen.model.prompt import Example, ParameterInfo, Prompt
from promptgen.model.prompt_transformer import PromptTransformer
from promptgen.model.reasoning_extractor import ExampleReasoning, ReasoningExtractor, ReasoningTemplate
from promptgen.model.value_formatter import Value
from promptgen.prompt_formatter.key_value_formatter import KeyValueFormatter
from promptgen.prompt_formatter.prompt_formatter import PromptFormatter, PromptFormatterConfig
from promptgen.prompt_formatter.text_formatter import TextValueFormatter

DEFAULT_REASONING_TEMPLATE = """This is because ... So the answer is ..."""

DETAILED_REASONING_TEMPLATE = """First, we clearly define the problem. The issue we are facing is "...". Next, we deeply analyze this problem, understanding its elements, background, and impact. From our analysis, the points we should focus on are "...".

Then, we formulate hypotheses for problem-solving. There are several possible solutions, but first, let's put forward our first hypothesis as "...". Also, let's consider "...", as our second hypothesis. The reasons why we think each of these hypotheses could be effective are "...".

After that, we will concretely verify these hypotheses. When we tried "...", the result was "...". The reason why we got this result is "...". When we verified "...", the result was "...". The reason why we got this result is "...".

Based on these verification results and reasons, we select the most appropriate solution. Our analysis concluded that "..." is the most effective means.

Therefore, our final conclusion is "...". We believe this resolves the problem initially posed as "..."."""


class SimpleReasoningTemplate(ReasoningTemplate):
    template: str = DEFAULT_REASONING_TEMPLATE


class DetailedReasoningTemplate(ReasoningTemplate):
    template: str = DETAILED_REASONING_TEMPLATE


class ReasoningGeneratorPromptTransformer(PromptTransformer):
    reasoning_template: ReasoningTemplate

    def __init__(self, *, reasoning_template: str):
        self.reasoning_template = ReasoningTemplate(template=reasoning_template)

    def transform_prompt(self, prompt: Prompt) -> Prompt:
        name = "PromptReasoningGenerator"
        description = f"Please detail the cause-and-effect relationship that begins with the inputs {prompt.input_signature()} and leads to the outputs {prompt.output_signature()}, outlining the reasoning process from the initial inputs to the final outputs."
        input_parameters = prompt.input_parameters + prompt.output_parameters
        output_parameters = [
            ParameterInfo(name="reasoning", description="Reasoning for the output"),
        ]
        template = Example(
            input={**prompt.template.input, **prompt.template.output},
            output={"reasoning": self.reasoning_template.template},
        )
        return Prompt(
            name=name,
            description=description,
            input_parameters=input_parameters,
            output_parameters=output_parameters,
            template=template,
            examples=[],
        )


class LLMReasoningExtractor(ReasoningExtractor):
    """Reasoning extractor that uses a text-based LLM."""

    text_based_llm: TextBasedLLM
    reasoning_template: str

    def __init__(
        self,
        *,
        text_based_llm: TextBasedLLM,
        reasoning_template: str,
    ):
        """Initialize a LLMReasoningExtractor.

        Args:
            text_based_llm: The text-based LLM to use. It must be an instance of a class that inherits from TextBasedLLM.
            reasoning_template(str):
                The reasoning template to use. Defaults to DEFAULT_REASONING_TEMPLATE.
        """
        self.text_based_llm = text_based_llm
        self.reasoning_template = reasoning_template

    def generate_reasoning(self, prompt: Prompt, example: Example) -> ExampleReasoning:
        """Generate reasoning for the given prompt and example.

        Args:
            prompt: The prompt to generate reasoning for.
            example: The example to generate reasoning for.

        Returns:
            (ExampleReasoning): The generated reasoning.
        """
        transformer = ReasoningGeneratorPromptTransformer(reasoning_template=self.reasoning_template)

        config = PromptFormatterConfig(
            show_formatter_description=False,
            show_parameter_info=False,
        )
        f = PromptFormatter(
            input_formatter=KeyValueFormatter(), output_formatter=TextValueFormatter("reasoning"), config=config
        )
        reasoning_prompt = transformer.transform_prompt(prompt)
        raw_req = f.format_prompt(reasoning_prompt, {**example.input, **example.output})
        raw_resp = self.text_based_llm.generate(raw_req)
        resp = f.parse(reasoning_prompt, raw_resp)
        return ExampleReasoning(reasoning=resp["reasoning"])

    def get_reasoning_template(self) -> str:
        return self.reasoning_template
