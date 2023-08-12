import promptogen as pg

summarizer = pg.Prompt(
    name="Text Summarizer and Keyword Extractor",
    description="Summarize text and extract keywords.",
    input_parameters=[
        pg.ParameterInfo(name="text", description="Text to summarize"),
    ],
    output_parameters=[
        pg.ParameterInfo(name="summary", description="Summary of text"),
        pg.ParameterInfo(name="keywords", description="Keywords extracted from text"),
    ],
    template=pg.IOExample(
        input={'text': "This is a sample text to summarize."},
        output={
            'summary': "This is a summary of the text.",
            'keywords': ["sample", "text", "summarize"],
        },
    ),
    examples=[
        pg.IOExample(
            input={
                'text': "One sunny afternoon, a group of friends decided to gather at the nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."},
            output={
                'summary': "A group of friends enjoyed an afternoon playing sports and making memories at a local park.",
                'keywords': ["friends", "park", "sports", "memories"],
            },
        )
    ],
)

print(summarizer)
# Text Summarizer and Keyword Extractor: (text: str) -> (summary: str, keywords: list)

# Description
# -----------
# Summarize text and extract keywords.

# Input Parameters
# ----------------
# - text (str): Text to summarize

# Output Parameters
# -----------------
# - summary (str): Summary of text
# - keywords (list): Keywords extracted from text

# Examples Count
# --------------
# 1
print(summarizer.model_dump_json(indent=4))
# {
#     "name": "Text Summarizer and Keyword Extractor",
#     "description": "Summarize text and extract keywords.",
#     "input_parameters": [
#         {
#             "name": "text",
#             "description": "Text to summarize"
#         }
#     ],
#     "output_parameters": [
#         {
#             "name": "summary",
#             "description": "Summary of text"
#         },
#         {
#             "name": "keywords",
#             "description": "Keywords extracted from text"
#         }
#     ],
#     "template": {
#         "input": {
#             "text": "This is a sample text to summarize."
#         },
#         "output": {
#             "summary": "This is a summary of the text.",
#             "keywords": [
#                 "sample",
#                 "text",
#                 "summarize"
#             ]
#         }
#     },
#     "examples": [
#         {
#             "input": {
#                 "text": "One sunny afternoon, a group of friends decided to gather at the nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."
#             },
#             "output": {
#                 "summary": "A group of friends enjoyed an afternoon playing sports and making memories at a local park.",
#                 "keywords": [
#                     "friends",
#                     "park",
#                     "sports",
#                     "memories"
#                 ]
#             }
#         }
#     ]
# }

from promptogen.prompt_formatter import KeyValueFormatter, JsonValueFormatter
from promptogen.model.value_formatter import ValueFormatter

value = {
    'summary': "This is a summary of the text.",
    'keywords': ["sample", "text", "summarize"],
}

value_formatter: ValueFormatter = KeyValueFormatter()
print(value_formatter.format(value))
# summary: "This is a summary of the text."
# keywords: [
#  "sample",
#  "text",
#  "summarize"
# ]

parsed_value = value_formatter.parse([
    ("summary", str),
    ("keywords", list),
], value_formatter.format(value))
print(parsed_value)
# {'summary': 'This is a summary of the text.', 'keywords': ['sample', 'text', 'summarize']}

value_formatter = JsonValueFormatter()
print(value_formatter.format(value))
# ```json
# {
#  "summary": "This is a summary of the text.",
#  "keywords": [
#   "sample",
#   "text",
#   "summarize"
#  ]
# }```
parsed_value = value_formatter.parse([
    ("summary", str),
    ("keywords", list),
], value_formatter.format(value))
print(parsed_value)
# {'summary': 'This is a summary of the text.', 'keywords': ['sample', 'text', 'summarize']}

formatter: pg.PromptFormatter = pg.KeyValuePromptFormatter()
print(formatter.format_prompt_without_input(summarizer))
# Summarize text and extract keywords.

# Input Parameters:
#   - text: Text to summarize

# Output Parameters:
#   - summary: Summary of text
#   - keywords: Keywords extracted from text

# Template:
# Input:
# text: "This is a sample text to summarize."
# Output:
# summary: """This is a summary of the text."""
# keywords: [
#  "sample",
#  "text",
#  "summarize"
# ]

# Example 1:
# Input:
# text: "One sunny afternoon, a group of friends decided to gather at the nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."
# Output:
# summary: """A group of friends enjoyed an afternoon playing sports and making memories at a local park."""
# keywords: [
#  "friends",
#  "park",
#  "sports",
#  "memories"
# ]

formatter = pg.JsonPromptFormatter()
print(formatter.format_prompt_without_input(summarizer))
# Summarize text and extract keywords.

# Output a JSON-formatted string without outputting any other strings.
# Be careful with the order of brackets in the json.

# Input Parameters:
#   - text: Text to summarize

# Output Parameters:
#   - summary: Summary of text
#   - keywords: Keywords extracted from text

# Template:
# Input:
# ```json
# {
#  "text": "This is a sample text to summarize."
# }```
# Output:
# ```json
# {
#  "summary": "This is a summary of the text.",
#  "keywords": [
#   "sample",
#   "text",
#   "summarize"
#  ]
# }```

# Example 1:
# Input:
# ```json
# {
#  "text": "One sunny afternoon, a group of friends decided to gather at the nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."
# }```
# Output:
# ```json
# {
#  "summary": "A group of friends enjoyed an afternoon playing sports and making memories at a local park.",
#  "keywords": [
#   "friends",
#   "park",
#   "sports",
#   "memories"
#  ]
# }```

formatter = pg.PromptFormatter(
    input_formatter=KeyValueFormatter(),
    output_formatter=JsonValueFormatter(),
)
print(formatter.format_prompt_without_input(summarizer))
# Summarize text and extract keywords.

# Output a JSON-formatted string without outputting any other strings.
# Be careful with the order of brackets in the json.

# Input Parameters:
#   - text: Text to summarize

# Output Parameters:
#   - summary: Summary of text
#   - keywords: Keywords extracted from text

# Template:
# Input:
# text: "This is a sample text to summarize."
# Output:
# ```json
# {
#  "summary": "This is a summary of the text.",
#  "keywords": [
#   "sample",
#   "text",
#   "summarize"
#  ]
# }```

# Example 1:
# Input:
# text: "One sunny afternoon, a group of friends decided to gather at the nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."
# Output:
# ```json
# {
#  "summary": "A group of friends enjoyed an afternoon playing sports and making memories at a local park.",
#  "keywords": [
#   "friends",
#   "park",
#   "sports",
#   "memories"
#  ]
# }```

formatter = pg.KeyValuePromptFormatter()

input_value = {
    'text': "In the realm of software engineering, developers often collaborate on projects using version control systems like Git. They work together to create and maintain well-structured, efficient code, and tackle issues that arise from implementation complexities, evolving user requirements, and system optimization.",
}
print(formatter.format_prompt(summarizer, input_value))
# Summarize text and extract keywords.

# Input Parameters:
#   - text: Text to summarize

# Output Parameters:
#   - summary: Summary of text
#   - keywords: Keywords extracted from text

# Template:
# Input:
# text: "This is a sample text to summarize."
# Output:
# summary: """This is a summary of the text."""
# keywords: [
#  "sample",
#  "text",
#  "summarize"
# ]

# Example 1:
# Input:
# text: "One sunny afternoon, a group of friends decided to gather at the nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."
# Output:
# summary: """A group of friends enjoyed an afternoon playing sports and making memories at a local park."""
# keywords: [
#  "friends",
#  "park",
#  "sports",
#  "memories"
# ]

# --------

# Input:
# text: "In the realm of software engineering, developers often collaborate on projects using version control systems like Git. They work together to create and maintain well-structured, efficient code, and tackle issues that arise from implementation complexities, evolving user requirements, and system optimization."
# Output:

formatter = pg.JsonPromptFormatter()

input_value = {
    'text': "In the realm of software engineering, developers often collaborate on projects using version control systems like Git. They work together to create and maintain well-structured, efficient code, and tackle issues that arise from implementation complexities, evolving user requirements, and system optimization.",
}
print(formatter.format_prompt(summarizer, input_value))
