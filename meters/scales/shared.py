import multiprocessing


##### Public classes #####
class Value:
    def __init__(self, value_type=int, default=0):
        self._value_type=value_type
        self._value = multiprocessing.Value({
                int:   "i",
                float: "d",
            }[value_type], self._value_type(default))

    def set(self, value):
        self._value.value = self._value_type(value)

    def __call__(self):
        return self._value.value

    def __iadd__(self, other):
        with self._value.get_lock():
            self._value.value += self._value_type(other)
        return self

    def __isub__(self, other):
        with self._value.get_lock():
            self._value.value -= self._value_type(other)
        return self

