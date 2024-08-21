from .value import Value
from .dictvalue import DictValue


class Settings(DictValue):
    def __init__(self, settings=None):
        if settings is None:
            settings = {}
        super(Settings, self).__init__(settings, Value)

    def __getitem__(self, key):
        return self.value[key].value

    def __setitem__(self, key, value):
        self.value[key].value = value

    def items(self):
        return self.value.items()

    def keys(self):
        return self.value.keys()

    def get(self, key, valueobject=False):
        if valueobject:
            return self.value[key]
        else:
            return self.value[key].value

    def update(self, settings):
        for k, v in settings.items():
            self.value[k] = v

    @property
    def grouped_items(self):
        def group(settings):
            groups = {}
            for key, value in settings.items():
                parts = key.split(".")
                if len(parts) > 1:
                    if parts[0] not in groups:
                        groups[parts[0]] = {}
                    subkey = ".".join(parts[1:])
                    groups[parts[0]][subkey] = value
                else:
                    groups[key] = value

            for key, value in groups.items():
                if isinstance(value, dict):
                    groups[key] = group(value)

            return groups

        return group(self.value)
