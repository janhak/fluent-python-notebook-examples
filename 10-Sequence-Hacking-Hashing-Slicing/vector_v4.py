import numbers
from array import array
import reprlib
import math
import functools
import operator


class Vector:
    typecode = 'd'
    shortcut_names = 'xyzt'

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, numbers.Integral):
            return self._components[index]
        else:
            raise TypeError(f'{cls.__name__} indices must be integers')

    def __getattr__(self, name):
        cls = type(self)
        if len(name) == 1:
            pos = cls.shortcut_names.find(name)
            if 0 <= pos < len(self._components):
                return self._components[pos]
        msg = f'{cls.__name__!r} object has no attribute {name!r}'
        raise AttributeError(msg)

    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            if name in cls.shortcut_names:
                error = f'readonly attribute {name!r}'
            elif name.islower():
                error = f"can't set attributes 'a' to 'z' in {cls.__name__!r}"
            else:
                error = ''
            if error:
                raise AttributeError(error)
        super().__setattr__(name, value)

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        class_name = type(self).__name__
        return f'{class_name}({components})'

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(self._components))

    def __abs__(self):
        return math.sqrt(sum(x ** x for x in self))

    def __bool__(self):
        return bool(abs(self))

    def __eq__(self, other):
        return (len(self) == len(other) and
                all(a == b for a, b in zip(self, other)))

    """
    The code below is correct and efficient but quite verbose
    if len(self) != len(other):
        return False
    for a, b in zip(self, other):
        if a != b:
            return False
    return True
    """

    def __hash__(self):
        hashes = (hash(x) for x in self._components)
        return functools.reduce(operator.xor, hashes, 0)
        # It is good practice to implement reduce with the initial value
        # To avoid TypeError: reduce() of empty sequence with no initial value
        # Calculating hash in this instance is an example of map -> reduce computation

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)