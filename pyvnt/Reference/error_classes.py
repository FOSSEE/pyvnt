'''
This File stores the error classes that is used to display various errors that can be triggered while using this library
'''


class DefaultOutofRangeError(Exception):
    def __init__(self, default: str):
        self.default = default

    def __str__(self):
        return f"'{self.default}' not in property range"

class LeafNodeError(Exception):
    def __init__(self, default: str):
        self.default = default

    def __str__(self):
        return f"{self.default} cannot have children nodes"

class IsDefaultError(Exception):
    def __init__(self, val: str):
        self.val = val

    def __str__(self):
        return f"'{self.val}' is set as default value. Cannot remove {self.val}"


class ValueOutofRangeError(Exception):
    def __init__(self, val: str):
        self.val = val

    def __str__(self):
        return f"'{self.val}' not in propery range"


class KeyRepeatError(Exception):
    def __init__(self, key: str):
        self.key = key

    def __str__(self):
        return f"{self.key} Already exists"


class NotStringType(TypeError):
    def __init__(self, item):
        self.item = item

    def __str__(self):
        return f"{self.item} not a string type"


class NotSetType(TypeError):
    def __init__(self, item):
        self.item = item

    def __str__(self):
        return f"{self.item} not a set type"


class InvalidRangeError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return f"Given range is invalid"

class InvalidTupleError(TypeError):
    def __init__(self, item):
        self.item = item

    def __str__(self):
        return f"{self.item} not an tuple type"
    
class SizeError(Exception):
    def __init__(self, size: int):
        self.size = size

    def __str__(self):
        return f"Size of values should be {self.size}"

class NoPlaceholdersError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return f"{self.msg}"

class NoValueError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return f"{self.msg}"

class KeyRepeatError(Exception):
    def __init__(self, key: str):
        self.key = key

    def __str__(self):
        return f"{self.key} Already exists"

class IncorrectLengthError(Exception):
    def __init__(self, length: int):
        self.length = length

    def __str__(self):
        return f"Length of values should be 7. Length of given list is {self.length}"


