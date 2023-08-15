# {
#     "name": "DictTranslator",
#     "description": "Translate the given dict into the given language.",
#     "input_parameters": [
#         {
#             "name": "value",
#             "description": "The dict that needs to be translated"
#         },
#         {
#             "name": "language",
#             "description": "The language into which the dict needs to be translated"
#         }
#     ],
#     "output_parameters": [
#         {
#             "name": "translated_value",
#             "description": "The translated dict"
#         }
#     ],
#     "template": {
#         "input": {
#             "value": {
#                 "key1": "value1",
#                 "key2": "value2"
#             },
#             "language": "English"
#         },
#         "output": {
#             "translated_value": {
#                 "key1": "translated_value1",
#                 "key2": "translated_value2"
#             }
#         }
#     },
#     "examples": [
#         {
#             "input": {
#                 "value": {
#                     "greeting": "Hello",
#                     "farewell": "Goodbye",
#                     "thanks": {
#                         "normal": "Thank you",
#                         "extreme": "Thank you very much"
#                     }
#                 },
#                 "language": "Japanese"
#             },
#             "output": {
#                 "translated_value": {
#                     "greeting": "こんにちは",
#                     "farewell": "さようなら",
#                     "thanks": {
#                         "normal": "ありがとう",
#                         "extreme": "どうもありがとうございます"
#                     }
#                 }
#             }
#         },
#         {
#             "input": {
#                 "value": {
#                     "greeting": "Hello",
#                     "farewell": "Goodbye",
#                     "thanks": {
#                         "normal": "Thank you",
#                         "extreme": "Thank you very much"
#                     }
#                 },
#                 "language": "Spanish"
#             },
#             "output": {
#                 "translated_value": {
#                     "greeting": "Hola",
#                     "farewell": "Adiós",
#                     "thanks": {
#                         "normal": "Gracias",
#                         "extreme": "Muchas gracias"
#                     }
#                 }
#             }
#         },
#         {
#             "input": {
#                 "value": {
#                     "greeting": "Hello",
#                     "farewell": "Goodbye",
#                     "thanks": {
#                         "normal": "Thank you",
#                         "extreme": "Thank you very much"
#                     }
#                 },
#                 "language": "French"
#             },
#             "output": {
#                 "translated_value": {
#                     "greeting": "Bonjour",
#                     "farewell": "Au revoir",
#                     "thanks": {
#                         "normal": "Merci",
#                         "extreme": "Merci beaucoup"
#                     }
#                 }
#             }
#         },
#         {
#             "input": {
#                 "value": {
#                     "greeting": "Hello",
#                     "farewell": "Goodbye",
#                     "thanks": {
#                         "normal": "Thank you",
#                         "extreme": "Thank you very much"
#                     }
#                 },
#                 "language": "German"
#             },
#             "output": {
#                 "translated_value": {
#                     "greeting": "Hallo",
#                     "farewell": "Auf Wiedersehen",
#                     "thanks": {
#                         "normal": "Danke",
#                         "extreme": "Vielen Dank"
#                     }
#                 }
#             }
#         }
#     ]
# }


from promptogen.model.prompt import Prompt


class DictTranslatorPrompt(Prompt):
    """Translate the given dict into the given language.
    f: (value: dict, language: str) -> (translated_value: dict)
    """

    def __init__(self):
        super().__init__(
            name="DictTranslator",
            description="Translate the given dict into the given language.",
            input_parameters=[
                {"name": "language", "description": "The language into which the dict needs to be translated"},
                {"name": "value", "description": "The dict that needs to be translated"},
            ],
            output_parameters=[{"name": "translated_value", "description": "The translated dict"}],
            template={
                "input": {
                    "language": "English",
                    "value": {"key1": "value1", "key2": "value2"},
                },
                "output": {"translated_value": {"key1": "translated_value1", "key2": "translated_value2"}},
            },
            examples=[
                {
                    "input": {
                        "language": "Japanese",
                        "value": {
                            "greeting": "Hello",
                            "farewell": "Goodbye",
                            "thanks": {"normal": "Thank you", "extreme": "Thank you very much"},
                        },
                    },
                    "output": {
                        "translated_value": {
                            "greeting": "こんにちは",
                            "farewell": "さようなら",
                            "thanks": {"normal": "ありがとう", "extreme": "どうもありがとうございます"},
                        }
                    },
                },
                {
                    "input": {
                        "language": "Spanish",
                        "value": {
                            "greeting": "Hello",
                            "farewell": "Goodbye",
                            "thanks": {"normal": "Thank you", "extreme": "Thank you very much"},
                        },
                    },
                    "output": {
                        "translated_value": {
                            "greeting": "Hola",
                            "farewell": "Adiós",
                            "thanks": {"normal": "Gracias", "extreme": "Muchas gracias"},
                        }
                    },
                },
                {
                    "input": {
                        "language": "French",
                        "value": {
                            "greeting": "Hello",
                            "farewell": "Goodbye",
                            "thanks": {"normal": "Thank you", "extreme": "Thank you very much"},
                        },
                    },
                    "output": {
                        "translated_value": {
                            "greeting": "Bonjour",
                            "farewell": "Au revoir",
                            "thanks": {"normal": "Merci", "extreme": "Merci beaucoup"},
                        }
                    },
                },
                {
                    "input": {
                        "language": "German",
                        "value": {
                            "greeting": "Hello",
                            "farewell": "Goodbye",
                            "thanks": {"normal": "Thank you", "extreme": "Thank you very much"},
                        },
                    },
                    "output": {
                        "translated_value": {
                            "greeting": "Hallo",
                            "farewell": "Auf Wiedersehen",
                            "thanks": {"normal": "Danke", "extreme": "Vielen Dank"},
                        }
                    },
                },
            ],
        )
