from .value import Value


class BoolValue(Value):
    def __init__(self, value=True):
        super(BoolValue, self).__init__(value, bool)
