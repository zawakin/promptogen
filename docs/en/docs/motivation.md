# Motivation

The idea for this library originated from **issues perceived while reading and utilizing various LLM-related open-source software**.

### Current Challenges with LLM Libraries (Communities)

Recently, not only OpenAI's `GPT-3.5-turbo` and `gpt-4`, a multitude of LLMs have become available.

Specifically, as of August 27, 2023, the number of LLMs supported by [LangChain](https://github.com/langchain-ai/langchain) is 52 ([langchain/llms](https://github.com/langchain-ai/langchain/tree/1960ac8d25c142f23a10a8203e6ccd14c8ca6be7/libs/langchain/langchain/llms)).

Given the trend, the number of accessible LLMs will likely increase exponentially.

Generally, LLM-related libraries evolve by adding newly released LLMs to their implementations. Most libraries employ abstract classes to avoid dependencies on specific LLMs, which seems like a correct approach. However, **each library conducts its abstraction, leading development efforts to be library-specific**. Moreover, the quality of the code can be inconsistent, with some being challenging to maintain.

If this continues, every time a new LLM-related library emerges, redundant implementations might repeat, potentially complicating inter-library collaborations.

Current libraries are designed to function independently, offering convenience. Yet, this leads to difficulties in integrating functionalities across libraries, potentially compromising extensibility and customizability. This inefficiency implies that **the community's resources may be wasted**.

From the concern that **"Python libraries might not keep pace with LLM advancements,"** there arose a need to consider a direction that ensures smooth collaboration between libraries.

### What Kind of Library Would Be Ideal?

Considering the aforementioned challenges, we envisioned a new library, setting the following three principles:

#### Principle 1: **Offer a simple interface that LLM-related libraries can confidently rely on**

By abstracting LLMs, at their core, they can be described as entities that accept input and produce text. For text-only input LLMs, a basic interface that takes text input and generates text is sufficient. While there may be nuanced settings for each LLM, these should be hidden as implementation details.

#### Principle 2: **Keep the library simple with limited functionalities**

A simple structure enhances user experience, enabling intuitive operations.

#### Principle 3: **Minimize dependencies**

[FastAPI](https://github.com/tiangolo/fastapi) is a good example of a library with few dependencies. We wanted to emulate that approach. Having fewer dependencies means the library is more robust against drastic changes in other libraries.

### In Summary

The library **PromptoGen** is built upon the above principles.

Our vision is like that **if libraries wishing to use LLMs depend on this library's interface, they can essentially support each LLM**.

Libraries relying on this interface can collaborate more easily, fostering an ecosystem where "reinventing the wheel" becomes less frequent, reducing unnecessary development resources.

Of course, this library isn't the sole solution, but we hope it serves as **a topic of discussion for the community**.
