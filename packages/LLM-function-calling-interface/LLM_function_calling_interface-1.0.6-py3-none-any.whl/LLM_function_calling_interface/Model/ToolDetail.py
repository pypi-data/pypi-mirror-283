from ToolParameter import ToolParameter


class ToolDetail:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.parameters = kwargs.get('parameters')
        self.validate()

    def validate(self):
        if self.name is None:
            raise ValueError('name is required')
        if not isinstance(self.name, str):
            raise ValueError('name must be a string')
        if self.description is None:
            raise ValueError('description is required')
        if not isinstance(self.description, str):
            raise ValueError('description must be a string')
        if self.parameters is not None:
            ToolParameter(**self.parameters)
        return self
