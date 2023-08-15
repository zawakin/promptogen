from promptogen.model import PromptInterceptor
from promptogen.model.llm import TextLLM
from promptogen.model.prompt import Prompt
from promptogen.model.value_formatter import Value
from promptogen.prompt_tool.translation.dict_translator import ValueTranslator


class ValueTranslatorInterceptor(PromptInterceptor):
    def __init__(self, *, llm: TextLLM, from_lang: str, to_lang: str):
        self.value_translator = ValueTranslator(llm=llm)
        self.from_lang = from_lang
        self.to_lang = to_lang

    def before_run(self, _: Prompt, input_value: Value) -> Value:
        return self.value_translator.translate_value(input_value, self.to_lang)

    def after_run(self, _: Prompt, output_value: Value) -> Value:
        return self.value_translator.translate_value(output_value, self.from_lang)
