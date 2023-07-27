from __future__ import annotations

import pytest
from promptgen.model.prompt import Example, ParameterInfo, Prompt, create_sample_prompt
from promptgen.model.value_formatter import Value

from promptgen.prompt_collection.prompt_collection import PromptCollection
from promptgen.prompt_transformer.reasoning_prompt_transformer import ExplanationGenerator, ExplanationGeneratorInterface, ReasoningPromptTransformer


@pytest.fixture
def prompt():
    return Prompt(
        name='test name',
        description='test description',
        input_parameters=[
            ParameterInfo(name="test input parameter name", description='test input parameter description'),
            ParameterInfo(name="test input parameter name 2", description='test input parameter description 2'),
        ],
        output_parameters=[
            ParameterInfo(name="test output parameter name", description='test output parameter description'),
            ParameterInfo(name="test output parameter name 2", description='test output parameter description 2'),
        ],
        template=Example(
            input={
                'test input parameter name': 'test input parameter value',
                'test input parameter name 2': 'test input parameter value 2'
            },
            output={
                'test output parameter name': 'test output parameter value',
                'test output parameter name 2': 'test output parameter value 2'
            },
        ),
        examples=[
            Example(
                input={
                    'test input parameter name': 'example test input parameter value',
                    'test input parameter name 2': 'example test input parameter value 2'
                },
                output={
                    'test output parameter name': 'example test output parameter value',
                    'test output parameter name 2': 'example test output parameter value 2'
                },
            ),
            Example(
                input={
                    'test input parameter name': 'example test input parameter value 3',
                    'test input parameter name 2': 'example test input parameter value 4'
                },
                output={
                    'test output parameter name': 'example test output parameter value 3',
                    'test output parameter name 2': 'example test output parameter value 4'
                },
            ),
        ])


def test_explanation_generator_make_reasoning_prompt(prompt: Prompt):
    generate_llm_response = lambda s: f'Generated response for "{s}"'
    explanation_generator = ExplanationGenerator(generate_llm_response=generate_llm_response)

    reasoning_prompt = explanation_generator.make_reasoning_prompt(prompt)

    assert reasoning_prompt.name == 'PromptExplanationGenerator'
    assert reasoning_prompt.description == 'Please detail the cause-and-effect relationship that begins with the inputs (test input parameter name: str, test input parameter name 2: str) and leads to the outputs (test output parameter name: str, test output parameter name 2: str), outlining the reasoning process from the initial inputs to the final outputs.'

    assert reasoning_prompt.input_parameters == prompt.input_parameters + prompt.output_parameters
    assert reasoning_prompt.output_parameters == [ParameterInfo(name='reasoning', description='Reasoning for the output')]
    assert len(reasoning_prompt.examples) == 0


def test_explanation_generator_generate(prompt: Prompt):
    generated_reasoning = 'Generated reasoning'
    explanation_template = 'Explanation Template'
    def generate_llm_response(s: str):
        assert s == f"""Please detail the cause-and-effect relationship that begins with the inputs (test input parameter name: str, test input parameter name 2: str) and leads to the outputs (test output parameter name: str, test output parameter name 2: str), outlining the reasoning process from the initial inputs to the final outputs.

Template:
Input:
test input parameter name: "test input parameter value"
test input parameter name 2: "test input parameter value 2"
test output parameter name: "test output parameter value"
test output parameter name 2: "test output parameter value 2"
Output:
Explanation Template
--------

Input:
test input parameter name: "input1"
test input parameter name 2: "input2"
test output parameter name: "output1"
test output parameter name 2: "output2"
Output:"""

        return generated_reasoning

    explanation_generator = ExplanationGenerator(generate_llm_response=generate_llm_response, explanation_template=explanation_template)

    input_value = {
        'test input parameter name': 'input1',
        'test input parameter name 2': 'input2'
    }
    output_value = {
        'test output parameter name': 'output1',
        'test output parameter name 2': 'output2'
    }
    resp = explanation_generator.generate(prompt, input_value, output_value)

    assert resp == {'reasoning': generated_reasoning}


def test_reasoning_prompt_transformer_transform_prompt(prompt: Prompt):
    generated_reasoning = 'Generated reasoning'
    explanation_template = 'Explanation Template'
    def generate_llm_response(s: str):
        return generated_reasoning

    explanation_generator = ExplanationGenerator(generate_llm_response=generate_llm_response, explanation_template=explanation_template)
    prompt_transformer = ReasoningPromptTransformer(explanation_generator=explanation_generator)

    prompt_with_reasoning = prompt_transformer.transform_prompt(prompt)
    assert prompt_with_reasoning == Prompt(
        name=prompt.name,
        description=prompt.description,
        input_parameters=prompt.input_parameters,
        output_parameters=[
            ParameterInfo(name='reasoning', description='Reasoning for the output'),
        ] + prompt.output_parameters,
        template=Example(
            input=prompt.template.input,
            output={
                'reasoning': explanation_template,
                **prompt.template.output,
            },
        ),
        examples=[
            prompt.examples[0].update(output={
                'reasoning': generated_reasoning,
                **prompt.examples[0].output,
            }),
            prompt.examples[1].update(output={
                'reasoning': generated_reasoning,
                **prompt.examples[1].output,
            }),
        ],
    )
