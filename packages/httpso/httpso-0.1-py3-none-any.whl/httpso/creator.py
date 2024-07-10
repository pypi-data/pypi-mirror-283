class CDict:
    def __init__(self, dictionary):
        self._dict = dictionary

    def __getattr__(self, attr):
        if attr in self._dict:
            return self._dict[attr]
        raise AttributeError(f"'CDict' object has no attribute '{attr}'")

    def __setattr__(self, attr, value):
        if attr == "_dict":
            super().__setattr__(attr, value)
        else:
            self._dict[attr] = value

    def __delattr__(self, attr):
        if attr in self._dict:
            del self._dict[attr]
        else:
            raise AttributeError(f"'CDict' object has no attribute '{attr}'")

    def __str__(self):
        return str(self._dict)

    def to_dict(self):
        return self._dict