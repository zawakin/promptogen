import json


class MyEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_indent = 0
        self.current_indent_str = ""

    def encode(self, obj):
        if isinstance(obj, (list, tuple)):
            self.current_indent += self.indent
            self.current_indent_str = ''.join(' ' for _ in range(self.current_indent))
            if not obj:
                self.current_indent -= self.indent
                return "[]"
            else:
                items = [self.current_indent_str + self.encode(item) for item in obj]
                self.current_indent -= self.indent
                if len(','.join(items)) + self.current_indent < 160:
                    return "[ " + ', '.join(items) + " ]"
                else:
                    return "[\n" + ',\n'.join(items) + "\n" + self.current_indent_str + "]"
        elif isinstance(obj, dict):
            self.current_indent += self.indent
            self.current_indent_str = ''.join(' ' for _ in range(self.current_indent))
            if not obj:
                self.current_indent -= self.indent
                return "{}"
            else:
                items = [self.current_indent_str + self.encode(k) + ": " + self.encode(v) for k, v in obj.items()]
                self.current_indent -= self.indent
                if len(','.join(items)) + self.current_indent < 160:
                    return "{ " + ', '.join(items) + " }"
                else:
                    return "{\n" + ',\n'.join(items) + "\n" + self.current_indent_str + "}"
        else:
            return super().encode(obj)


value = {"key1": "value1", "key2": "value2", "key3": ["value3", "value4", "value5"]}
formatted = json.dumps(value, cls=MyEncoder, indent=2)
print(formatted)
