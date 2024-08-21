from .value import Value


class DictValue(Value):
    def __init__(self, value=None, dict_value_type=None):
        if value is None:
            value = {}
        super(DictValue, self).__init__(value, dict)
        self._dict_value_type = dict_value_type
        self._check_dict_value_type(value)

    def _check_dict_value_type(self, value):
        for k, v in value.items():
            assert isinstance(k, str), "Dict key {} is not of type {}".format(k, str)
            assert isinstance(v, self.dict_value_type), "Dict value {}:{} is not of type {}".format(
                k, v, self.dict_value_type
            )

    def check(self, value):
        super(DictValue, self).check(value)
        self._check_dict_value_type(value)

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, value):
        assert isinstance(value, self.dict_value_type), "New value {} is not of type {}".format(
            value, self.dict_value_type
        )
        self.value[key] = value

    @property
    def dict_value_type(self):
        return self._dict_value_type

    @property
    def data(self):
        return {
            "value": self.value,
            "value_type": "dict",
            "dict_value_type": self.dict_value_type.__name__,
        }

    @data.setter
    def data(self, data):
        self._value = data["value"]
        self._dict_value_type = eval(data["dict_value_type"])
