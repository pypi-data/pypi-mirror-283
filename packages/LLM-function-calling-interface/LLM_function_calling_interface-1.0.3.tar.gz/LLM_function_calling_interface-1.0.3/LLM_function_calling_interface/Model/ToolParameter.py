from ParameterProperties import ParameterProperties


class ToolParameter:
    def __init__(self, **kwargs):
        self.type = kwargs.get('type')
        self.properties = kwargs.get('properties')
        self.required = kwargs.get('required')
        self.validate()

    def validate(self):
        if self.type is None:
            raise ValueError('type is required')
        if not isinstance(self.type, str) or self.type != 'object':
            raise ValueError('type must be object')
        if self.properties is not None and not isinstance(self.properties, dict):
            raise ValueError('properties must be a dictionary')
        if self.properties is not None:
            for key, value in self.properties.items():
                if not isinstance(key, str):
                    raise ValueError('properties keys must be strings')
                ParameterProperties(**value)
        if self.required is not None and not isinstance(self.required, list):
            raise ValueError('required must be a list')
        return self
