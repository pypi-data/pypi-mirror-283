from ToolDetail import ToolDetail


class Tool:
    def __init__(self, **kwargs):
        self.type = kwargs.get('type')
        self.function = kwargs.get('function')
        self.validate()

    def validate(self):
        if self.type is None:
            raise ValueError('type is required')
        if self.type not in ['function']:
            raise ValueError('type must be one of function')
        if self.function is None:
            raise ValueError('function is required')
        ToolDetail(**self.function)
        return self
