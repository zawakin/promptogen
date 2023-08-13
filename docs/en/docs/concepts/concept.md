# Concept

## Modularization

PromptoGen separates the process of converting between Python objects and text strings from the process of communicating with the LLM.

This modular design makes it easier for PromptoGen to adapt to changes without affecting its core functionalities, even if the LLM evolves or changes.

!!! note "What is Modularization"

    In software design, modularization refers to dividing the system into smaller, manageable, inter-operable independent components (modules). The main advantages of this approach are as follows:

    1. Independence: Each module independently handles a specific task. This ensures that modifying one module doesn't impact others, minimizing potential risks and issues when adding or updating functionalities.

    2. Reusability: Modules are typically designed to be reusable. This means the same module can be used in different parts of a system or in other systems, saving time and reducing code duplication.

    3. Maintenance: Since each module handles a specific task, understanding, updating, debugging, and testing become easier. Moreover, different teams or individuals can also develop and maintain each module.

## Keeping the Library Small

In PromptoGen, the focus is on converting between Python objects and text strings to keep the library small. By excluding logic that directly communicates with the LLM, the library remains lightweight and flexible, making it easier to integrate with other systems and adapt to future changes or evolution of the LLM.

!!! note "Benefits of a Small Library"

    The advantages of a small library include:

    1. Efficiency: A smaller codebase is easier to understand, debug, test, and maintain.
    2. Simplicity: A library with a single clear purpose is user-friendly and less likely to cause unexpected side effects or conflicts with other parts of a system.
    3. Speed: Generally, smaller libraries load and execute faster, saving overall time and computational resources.
