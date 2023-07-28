from abc import ABC, abstractmethod
from typing import Callable

from promptgen.model.prompt import Example, ParameterInfo, Prompt
from promptgen.model.value_formatter import Value
from promptgen.prompt_formatter.key_value_formatter import KeyValueFormatter
from promptgen.prompt_formatter.prompt_formatter import PromptFormatter, PromptFormatterConfig
from promptgen.prompt_formatter.text_formatter import TextValueFormatter

DEFAULT_EXPLANATION_TEMPLATE = """First, we clearly define the problem. The issue we are facing is "...". Next, we deeply analyze this problem, understanding its elements, background, and impact. From our analysis, the points we should focus on are "...".

Then, we formulate hypotheses for problem-solving. There are several possible solutions, but first, let's put forward our first hypothesis as "...". Also, let's consider "...", as our second hypothesis. The reasons why we think each of these hypotheses could be effective are "...".

After that, we will concretely verify these hypotheses. When we tried "...", the result was "...". The reason why we got this result is "...". When we verified "...", the result was "...". The reason why we got this result is "...".

Based on these verification results and reasons, we select the most appropriate solution. Our analysis concluded that "..." is the most effective means.

Therefore, our final conclusion is "...". We believe this resolves the problem initially posed as "..."."""


class ExplanationGeneratorInterface(ABC):
    @abstractmethod
    def generate(self, prompt: Prompt, input_value: Value, output_value: Value) -> str:
        pass  # pragma: no cover

    @abstractmethod
    def get_reasoning_template(self) -> str:
        pass  # pragma: no cover


class ExplanationGenerator(ExplanationGeneratorInterface):
    def __init__(
        self, *, generate_llm_response: Callable[[str], str], explanation_template: str = DEFAULT_EXPLANATION_TEMPLATE
    ):
        self.generate_llm_response = generate_llm_response
        self.reasoning_template = explanation_template

    def generate(self, prompt: Prompt, input_value: Value, output_value: Value) -> str:
        config = PromptFormatterConfig(
            show_formatter_description=False,
            show_parameter_info=False,
        )
        f = PromptFormatter(
            input_formatter=KeyValueFormatter(), output_formatter=TextValueFormatter("reasoning"), config=config
        )
        reasoning_prompt = self.make_reasoning_prompt(prompt)
        raw_req = f.format_prompt(reasoning_prompt, {**input_value, **output_value})
        raw_resp = self.generate_llm_response(raw_req)
        resp = f.parse(reasoning_prompt, raw_resp)
        return resp["reasoning"]

    def make_reasoning_prompt(self, prompt: Prompt) -> Prompt:
        name = "PromptExplanationGenerator"
        description = f"Please detail the cause-and-effect relationship that begins with the inputs {prompt.input_signature()} and leads to the outputs {prompt.output_signature()}, outlining the reasoning process from the initial inputs to the final outputs."
        input_parameters = prompt.input_parameters + prompt.output_parameters
        output_parameters = [
            ParameterInfo(name="reasoning", description="Reasoning for the output"),
        ]
        template = Example(
            input={**prompt.template.input, **prompt.template.output},
            output={"reasoning": self.reasoning_template},
        )
        return Prompt(
            name=name,
            description=description,
            input_parameters=input_parameters,
            output_parameters=output_parameters,
            template=template,
            examples=[],
        )

    def get_reasoning_template(self) -> str:
        return self.reasoning_template


class ReasoningPromptTransformer:
    explanation_generator: ExplanationGeneratorInterface

    def __init__(self, explanation_generator: ExplanationGeneratorInterface):
        self.explanation_generator = explanation_generator

    def transform_prompt(self, prompt: Prompt) -> Prompt:
        examples_with_reasoning = []
        for example in prompt.examples:
            reason = self.explanation_generator.generate(prompt, example.input, example.output)
            example_with_reasoning = Example(
                input=example.input,
                output={
                    "reasoning": reason,
                    **example.output,
                },
            )
            examples_with_reasoning.append(example_with_reasoning)

        return prompt.copy().update(
            output_parameters=[
                ParameterInfo(name="reasoning", description="Reasoning for the output"),
                *prompt.output_parameters,
            ],
            template=Example(
                input=prompt.template.input,
                output={
                    "reasoning": self.explanation_generator.get_reasoning_template(),
                    **prompt.template.output,
                },
            ),
            examples=examples_with_reasoning,
        )
