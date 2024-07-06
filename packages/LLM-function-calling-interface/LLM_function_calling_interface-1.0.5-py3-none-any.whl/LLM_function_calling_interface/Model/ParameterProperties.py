class ParameterProperties:
    def __init__(self, **kwargs):
        self.type = kwargs.get('type')
        self.description = kwargs.get('description')
        self.items = kwargs.get('items')
        self.properties = kwargs.get('properties')
        self.required = kwargs.get('required')
        self.enum = kwargs.get('enum')
        self.validate()

    def validate(self):
        if self.type is None:
            raise ValueError('type is required')
        if not isinstance(self.type, str) or self.type not in ['string', 'number', 'integer', 'boolean', 'array',
                                                               'object']:
            raise ValueError('type must be one of string, number, integer, boolean, array, object')
        if self.description is None:
            raise ValueError('description is required')
        if not isinstance(self.description, str):
            raise ValueError('description must be a string')
        if self.type == 'array':
            if self.items is None:
                raise ValueError('items is required for array type')
            ParameterProperties(**self.items)
        if self.type == 'object':
            if self.properties is None:
                raise ValueError('properties is required for object type')
            if not isinstance(self.properties, dict):
                raise ValueError('properties must be a dictionary')
            for key, value in self.properties.items():
                if not isinstance(key, str):
                    raise ValueError('properties keys must be strings')
                ParameterProperties(**value)
            if self.required is None:
                raise ValueError('required is required for object type')
            if not isinstance(self.required, list):
                raise ValueError('required must be a list')
        if self.enum is not None:
            if self.type != 'string':
                raise ValueError('enum is only valid for string type')
            if not isinstance(self.enum, list):
                raise ValueError('enum must be a list')
            for item in self.enum:
                if not isinstance(item, str):
                    raise ValueError('enum values must be strings')
        if self.type != 'array' and self.items is not None:
            raise ValueError('items is only valid for array type')
        if self.type != 'object' and self.properties is not None:
            raise ValueError('properties is only valid for object type')
        return self
