from promptogen.model.prompt import IOExample, ParameterInfo, Prompt
from promptogen.model.prompt_transformer import PromptTransformer
from promptogen.model.reasoning_extractor import ReasoningExtractor


class PromptWithReasoningTransformer(PromptTransformer):
    """A prompt transformer that adds reasoning to the prompt."""

    reasoning_extractor: ReasoningExtractor

    def __init__(self, reasoning_extractor: ReasoningExtractor):
        """Initialize a PromptWithReasoningTransformer.

        Args:
            reasoning_extractor (ReasoningExtractor): The reasoning extractor to use.
        """
        self.reasoning_extractor = reasoning_extractor

    def transform_prompt(self, prompt: Prompt) -> Prompt:
        """Transform the given prompt.

        Args:
            prompt (Prompt): The prompt to transform.
        """
        new_examples = []
        for example in prompt.examples:
            reasoning = self.reasoning_extractor.generate_reasoning(prompt, example)
            reasoned_output = {"reasoning": reasoning.reasoning, **example.output}
            new_examples.append(example.update(output=reasoned_output))

        return prompt.update(
            output_parameters=[
                ParameterInfo(name="reasoning", description="Reasoning for the output"),
                *prompt.output_parameters,
            ],
            template=IOExample(
                input=prompt.template.input,
                output={
                    "reasoning": self.reasoning_extractor.get_reasoning_template(),
                    **prompt.template.output,
                },
            ),
            examples=new_examples,
        )
