from examples.llm.openai_util import OpenAITextBasedLLM
import promptgen as pg
from promptgen.prompt_collection.prompts.text_condenser import TextCondenserPrompt

llm = OpenAITextBasedLLM(model="gpt-3.5-turbo-16k")

formatter = pg.KeyValuePromptFormatter()
prompt_runner = pg.TextBasedPromptRunner(llm=llm, formatter=formatter)


text_condenser_prompt = TextCondenserPrompt()


def setup_reasoning_prompt(prompt: pg.Prompt) -> pg.Prompt:
    reasoning_extractor = pg.LLMReasoningExtractor(
        text_based_llm=llm, reasoning_template="This is because ... So the answer is ..."
    )
    reasoning_transformer = pg.PromptWithReasoningTransformer(reasoning_extractor)
    prompt_with_reasoning = reasoning_transformer.transform_prompt(prompt)
    return prompt_with_reasoning


text_condenser_prompt_with_reasoning = setup_reasoning_prompt(text_condenser_prompt)


def condense_text(text: str, information: str) -> str:
    input_value = {
        "information": information,
        "text": text,
    }
    resp = prompt_runner.run_prompt(text_condenser_prompt_with_reasoning, input_value=input_value)
    return resp["result"]


with open("examples/output/long_text.txt", "r") as f:
    text = f.read()

for i in range(10):
    print(condense_text(text, input("information: ")))
