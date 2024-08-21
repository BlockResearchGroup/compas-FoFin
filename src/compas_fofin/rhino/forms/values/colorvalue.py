from compas.colors import Color

from .value import Value


class ColorValue(Value):
    def __init__(self, value=Color.black()):
        value = Color(*value)
        super(ColorValue, self).__init__(value, Color)

    def cast(self, value):
        try:
            return Color(*value)
        except ValueError:
            raise ValueError("Cannot cast {} to {}".format(value, self.value_type))

    @property
    def data(self):
        return {
            "value": self.value,
            "value_type": "compas.colors.Color",
            "options": self.options,
        }

    @data.setter
    def data(self, data):
        self._value = data["value"]
        self._options = data["options"]
