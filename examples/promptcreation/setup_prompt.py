import promptgen as pg
from examples.llm.openai_util import generate_text_by_text_openai_api

formatter = pg.KeyValuePromptFormatter()
llm = pg.TextBasedLLMWrapper(generate_text_by_text=lambda s: generate_text_by_text_openai_api(s, "gpt-4"))
prompt_runner = pg.TextBasedPromptRunner(llm=llm, formatter=formatter)
collection = pg.PromptCollection(load_predefined=True)


resp = prompt_runner.run_prompt(
    collection["PromptCreator"],
    input_value={
        "description": "Answer the question for the given context.",
        "background": "(context: str, question: str, answer: str)",
    },
)
print(pg.Prompt.from_dict(resp["prompt"]))
