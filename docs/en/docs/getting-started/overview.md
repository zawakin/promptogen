## :material-book-multiple: About PromptoGen

### :material-lightbulb: Project Vision of PromptoGen

**"Achieving efficient and expandable communication with Large Language Models (LLM)"**

1. **Seamless Conversion between LLM I/O and Python Objects**: Facilitate natural and efficient communication with LLMs.
2. **Unique Abstraction Interface**: Offer users high customizability and extensibility.
3. **Eliminating Dependency on LLM Communication**: Aim to build a robust system capable of flexibly adapting to future evolutions and changes in LLMs.

### :material-thought-bubble: Problems with Existing Libraries

Many other LLM-related libraries frequently handle everything, from the intricate details of LLM communication to text generation and parsing. This approach leads to several challenges:

1. :material-thought-bubble: **Difficulty in forming a prompt-engineering ecosystem.**
2. :material-thought-bubble: **High dependence on LLM, making it vulnerable to LLM changes and evolution.**
3. :material-thought-bubble: **Complex implementation with low customizability.**

### :material-check-circle: Solutions

To address these challenges, PromptoGen offers the following classes and interfaces:

1. :material-check-circle: **`Prompt` Data Class**: **Fostering a prompt engineering ecosystem** 
    - Defines basic LLM communication information (name, description, input/output info, template, examples).
2. :material-check-circle: **`TextLLM` Interface**: **Ensuring independence from LLM implementations**
    - Communication with LLM is through the `TextLLM` interface.
3. :material-check-circle: **`PromptFormatter` Interface**: **Enhancing customizability**
    - Users can define any formatter.
    - Generates prompt strings from `Prompt` and input.
    - Converts LLM text output to Python data structures.

PromptoGen relies solely on the data class library `Pydantic`, ensuring a robust design that remains resilient to LLM advancements.

By utilizing PromptoGen, **there's no longer a need to implement the processes that commonly convert between strings and Python objects without relying on LLM**.

### :material-star-shooting: Benefits for Users

- :material-puzzle: **Modularity**: Freedom to combine.
- :material-plus: **Extensibility**: Ability to add custom formatters and parsers.
- :material-shield-half-full: **Independence**: Unaffected by new models or libraries.
- :material-wrench: **Maintainability**: Simplified management and troubleshooting.
- :material-clock: **Development Efficiency**: No need to change the implementation for each LLM

### :material-alert: Limitations of PromptoGen

PromptoGen is designed prioritizing efficiency, simplicity, and reliability. Based on this philosophy, the tool deliberately does not support the following functionalities or characteristics:

1. **Direct Communication with LLM**:  
   PromptoGen doesn't directly support LLM communication. Instead, it emphasizes supporting interfaces and data conversion to enable efficient and natural communication.

2. **Integration of a Version Manager for Prompt Management**:  
   To avoid added complexities, the tool doesn't provide features for managing prompt versions.

3. **Optimization for Specific LLM Implementations**:  
   PromptoGen is designed to remain independent of any particular LLM implementation. This ensures it can flexibly adapt to future LLM changes or developments, serving its role as an autonomous library.

----

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
