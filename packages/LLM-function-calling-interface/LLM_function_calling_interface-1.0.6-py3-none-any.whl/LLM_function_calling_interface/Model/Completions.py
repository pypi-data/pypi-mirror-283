from Tool import Tool


def validate_instruction(value):
    if value is not None and not isinstance(value, str):
        raise ValueError('instruction must be a string')
    return value


def validate_generate_function(value):
    if value is None:
        raise ValueError('generate_function is required')
    if not callable(value):
        raise ValueError('generate_function must be a callable')
    return value


def validate_tools(value):
    if value is not None and not isinstance(value, list):
        raise ValueError('tools must be a list')
    if value is not None:
        for tool in value:
            Tool(**tool)
    return value


class CompletionModel:
    def __init__(self, **kwargs):
        self.instruction = kwargs.get('instruction') or None
        self.generate_function = kwargs.get('generate_function')
        self.tools = kwargs.get('tools') or None
        self.validate()

    def validate(self):
        validate_instruction(self.instruction)
        validate_generate_function(self.generate_function)
        validate_tools(self.tools)
