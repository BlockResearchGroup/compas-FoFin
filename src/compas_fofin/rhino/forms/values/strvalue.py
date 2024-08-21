from .value import Value


class StrValue(Value):
    def __init__(self, value="", options=None):
        super(StrValue, self).__init__(value, str, options=options)
