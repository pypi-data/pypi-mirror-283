from typing import Any


class Message:
    def __init__(self, role: str, content: Any):
        self.role = role
        self.content = content
        self.validate()

    def validate(cls):
        if cls.role is None:
            raise ValueError('role is required')
        if isinstance(cls.role, str) and cls.role not in ['user', 'assistant', 'function_call', 'function_response']:
            raise ValueError('role must be a string and one of user, assistant, function_call, function_response')
        if cls.content is None:
            raise ValueError('content is required')
        if cls.role == 'user' and not isinstance(cls.content, str):
            raise ValueError('content must be a string')
        if cls.role == 'assistant' and not isinstance(cls.content, str):
            raise ValueError('content must be a string')
        if cls.role == 'function_call' and not isinstance(cls.content, dict):
            raise ValueError('content must be a dictionary')
        if cls.role == 'function_response' and not isinstance(cls.content, dict):
            raise ValueError('content must be a dictionary')
        return cls
