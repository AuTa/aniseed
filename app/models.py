# coding: utf-8


class Field():
    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type

    def __str__(self):
        return '{0}:{1}'.format(self.name, self.column_type)


class StringField(Field):
    def __init__(self, name):
        super(StringField, self).__init__(name, 'varchar(100)')


class TextField(Field):
    def __init__(self, name):
        super(TextField, self).__init__(name, 'text')


class IntegerField(Field):
    def __init__(self, name):
        super(IntegerField, self).__init__(name, 'bigint')


class BoolField(Field):
    def __init__(self, name):
        super(BoolField, self).__init__(name, 'boolean')


class URLField(Field):
    def __init__(self, name):
        super(URLField, self).__init__(name, 'url')


class URLListField(Field):
    def __init__(self, name):
        super(URLListField, self).__init__(name, 'url_list')


class JsonModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'JsonModel':
            return type.__new__(cls, name, bases, attrs)
        mappings = dict()
        for key, value in attrs.items():
            if isinstance(value, Field):
                print('Found mapping: {0} ===> {1}'.format(key, value))
                mappings[key] = value
        for k in mappings.keys():
            attrs.pop(k)
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系
        attrs['__table__'] = name  # 假设表名和类名一致
        return type.__new__(cls, name, bases, attrs)


class JsonModel(dict, metaclass=JsonModelMetaclass):
    def __init__(self, **kwargs):
        super(JsonModel, self).__init__(**kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'JsonModel' object has no attribute '{0}'".format(key))

    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        for key, value in self.__mappings__.items():
            fields.append(value.name)
            params.append('?')
            args.append(getattr(self, key, None))


class Project(JsonModel):
    id = IntegerField('id')
    project_name = StringField('project_name')
    project_name_en = StringField('project_name_en')
    project_address = StringField('project_address')
    project_address_en = StringField('project_address_en')
    project_time = StringField('project_time')
    project_info = TextField('project_info')
    background_url = URLField('background_url')
    project_url = URLListField('project_url')
    background_color = BoolField('background_color')


project = Project(id=1, project_name='name')
print(project)

