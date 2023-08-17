### :material-lightbulb: PromptoGen Project Vision

**"Achieving efficient and extensible communication with Large Language Models (LLM)"**

PromptoGen aims to provide a seamless platform that bridges the gap between modern AI technology and user programs. The mission of this project is to simplify and enhance the communication between LLMs and programs, and to improve the quality and efficiency of this communication.

**Key Features:**

1. **Seamless Conversion between LLM I/O and Python Objects**: Facilitate natural and efficient communication with LLMs.
2. **Unique Abstraction Interface**: Offer users high customizability and extensibility.
3. **Eliminating Dependency on LLM Communication**: Strive to construct a robust system that can flexibly adapt to future evolutions and changes in LLMs.

### :material-thought-bubble: Challenges to Address

Other libraries often handle everything from LLM communication to text generation and parsing, leading to the following challenges:

1. :material-thought-bubble: **Difficulty in forming a prompt engineering ecosystem**
2. :material-thought-bubble: **Vulnerability to changes and evolutions in LLMs due to strong dependencies**
3. :material-thought-bubble: **Complex implementations with low customizability**

### :material-check-circle: Solution

PromptoGen functions as a language conversion tool for facilitating communication with Large Language Models (LLM). At its core is the `TextLLM` interface, ensuring independence from specific LLM implementations.

Its characteristics lie in the following processes:

1. **Usage of the `Prompt` data class**:
    - This data class is designed to define basic information and format of prompts for communication with LLMs.
    - Each `Prompt` includes the prompt's name, description, input/output parameter information, and specific usage examples.

2. **Ensuring independence through the `TextLLM` interface**:
    - Using the `TextLLM` interface, one can easily switch between different language models or their versions without depending on specific LLM implementations.

3. **Generation of prompt strings and output parsing with `PromptFormatter`**:
    - The `PromptFormatter` takes a `Prompt` and input values and converts them into a prompt string that can be sent to the LLM.
    - It also converts text outputs from the LLM, based on the corresponding `Prompt` information, into Python data structures (especially dictionaries) that are easier for programs to handle.

### :material-star-shooting: Benefits for Users

1. **Modularity**: Freedom to combine with other models and libraries
2. **Extensibility**: Ability to add custom formatters and parsers
3. **Independence**: Unaffected by new language models or libraries
4. **Maintainability**: Easy management and troubleshooting
5. **Development Efficiency**: Focus on development without worrying about communication with large language models
6. **Robustness**: Limited dependencies allow for strength and swift adaptation to evolutions or changes in LLMs.

### TextLLM: Abstracting Large Language Models

Through the key interface of PromptoGen, `pg.TextLLM`, text generation with Large Language Models (LLM) is performed. Understanding and properly using this interface is key to maximizing the benefits of the PromptoGen library.

#### Usage Example:

```python
import promptogen as pg

class YourTextLLM(pg.TextLLM):
    def __init__(self, model: str):
        self.model = model

    def generate(self, text: str) -> str:
        return generate_by_your_text_llm(text, self.model)

text_llm = YourTextLLM(model="your-model")
```

In the example above, the `YourTextLLM` class is defined to use any desired LLM. The connection to the actual LLM and the text generation logic are delegated to the `generate_by_your_text_llm` method.

#### Why is the `pg.TextLLM` interface important?

PromptoGen is designed to be independent of specific LLM implementations (e.g., `gpt-3.5-turbo`, `gpt-4`). This allows for easy switching between different LLM versions or other language models. To achieve this independence, the `pg.TextLLM` interface plays a central role. Users can inject their own LLM implementations into PromptoGen through this interface.

In this way, PromptoGen retains flexibility and extensibility through the `pg.TextLLM` interface.
