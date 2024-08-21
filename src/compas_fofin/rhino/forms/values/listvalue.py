from .value import Value


class ListValue(Value):
    def __init__(self, value=None, list_value_type=None):
        if value is None:
            value = []
        super(ListValue, self).__init__(value, list)
        self._list_value_type = list_value_type
        self._check_list_value_type(value)

    def _check_list_value_type(self, value):
        for i, item in enumerate(value):
            assert isinstance(item, self.list_value_type), "List item {}:{} is not of type {}".format(
                i, item, self.list_value_type
            )

    def check(self, value):
        super(ListValue, self).check(value)
        self._check_list_value_type(value)

    @property
    def list_value_type(self):
        return self._list_value_type

    @property
    def data(self):
        return {
            "value": self.value,
            "value_type": "list",
            "options": self.options,
            "list_value_type": self.list_value_type.__name__,
        }

    @data.setter
    def data(self, data):
        self._value = data["value"]
        self._options = data["options"]
