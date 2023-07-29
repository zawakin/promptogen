from promptgen.model.prompt import Example, ParameterInfo, Prompt
from promptgen.model.prompt_transformer import PromptTransformer
from promptgen.model.reasoning_extractor import ReasoningExtractor


class PromptWithReasoningTransformer(PromptTransformer):
    explanation_generator: ReasoningExtractor

    def __init__(self, explanation_generator: ReasoningExtractor):
        self.explanation_generator = explanation_generator

    def transform_prompt(self, prompt: Prompt) -> Prompt:
        new_examples = []
        for example in prompt.examples:
            reasoning = self.explanation_generator.generate_reasoning(prompt, example)
            reasoned_output = {"reasoning": reasoning.reasoning, **example.output}
            new_examples.append(example.update(output=reasoned_output))

        return prompt.update(
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
            examples=new_examples,
        )
