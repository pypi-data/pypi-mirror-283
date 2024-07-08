import Tool


class FunctionCall:
    def __init__(self, **kwargs):
        self.function_name = kwargs.get('name')
        self.arguments = kwargs.get('arguments')

    def validate(cls):
        if cls.function_name is None:
            raise ValueError('function_name is required')
        if not isinstance(cls.function_name, str):
            raise ValueError('function_name must be a string')
        return cls

    def validate_arguments(cls, tools: list[Tool]):
        if cls.function_name not in [tool['function']['name'] for tool in tools]:
            raise ValueError(f'function {cls.function_name} is not in the list of tools')
        if cls.arguments is not None and not isinstance(cls.arguments, dict):
            raise ValueError(f'function {cls.function_name} arguments must be a dictionary')
        tool = [tool for tool in tools if tool['function']['name'] == cls.function_name][0]
        if cls.arguments is None and tool['function']['parameters'] is not None:
            raise ValueError(f'function {cls.function_name} must have arguments')
        messasges_invalid = []
        if cls.arguments is not None and tool['function']['parameters'] is not None:
            required = tool['function']['parameters']['required'] or []
            for key in required:
                if key not in cls.arguments:
                    messasges_invalid.append(f'{key} is required')
            for key in cls.arguments:
                properties = tool['function']['parameters']['properties'] or {}
                if key not in properties:
                    messasges_invalid.append(f'{key} is not a valid argument')
                if properties[key]['type'] == 'object' and not isinstance(cls.arguments[key], dict):
                    messasges_invalid.append(f'{key} must be a dictionary')
                if properties[key]['type'] == 'array' and not isinstance(cls.arguments[key], list):
                    messasges_invalid.append(f'{key} must be a list')
                if properties[key]['type'] == 'string' and not isinstance(cls.arguments[key], str):
                    messasges_invalid.append(f'{key} must be a string')
                if properties[key]['type'] == 'number' and not isinstance(cls.arguments[key], int):
                    messasges_invalid.append(f'{key} must be a number')
                if properties[key]['type'] == 'enum' and cls.arguments[key] not in tool['function']['parameters'][key]['enum']:
                    messasges_invalid.append(f'{key} must be one of {tool["function"]["parameters"][key]["enum"]}')
                if properties[key]['type'] == 'boolean' and not isinstance(cls.arguments[key], bool):
                    messasges_invalid.append(f'{key} must be a boolean')
                    print(messasges_invalid)
        if len(messasges_invalid) > 0:
            print(messasges_invalid)
            raise ValueError(f'function {cls.function_name} arguments are invalid: {", ".join(messasges_invalid)}')
