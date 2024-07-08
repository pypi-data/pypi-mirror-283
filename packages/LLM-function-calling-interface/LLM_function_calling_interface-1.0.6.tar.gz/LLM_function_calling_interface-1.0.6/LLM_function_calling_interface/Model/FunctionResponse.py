from typing import Any, Optional


class FunctionResponse:
    def __init__(self, function_name: Optional[str] = None, response: Optional[Any] = None):
        self.function_name = function_name
        self.function_output = response

    def validate(cls):
        if cls.function_name is None:
            raise ValueError('function_name is required')
        if isinstance(cls.function_name, str):
            raise ValueError('function_name must be a string')
        return cls
