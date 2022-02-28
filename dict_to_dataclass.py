from inspect import get_annotations
from dataclasses import is_dataclass
from dataclass import Id

non_recursive_classes =  [Id]

def check(_type):
    if is_dataclass(_type) or (isinstance(_type, list) and is_dataclass(_type[0])):
        return True
    else:
        return False


def recur(cls, data):
    if not any([check(_type) for field, _type in get_annotations(cls).items()]):
        return cls(**data)

    for field, _type in get_annotations(cls).items():
        if type(_type).__name__ == 'EnumType':
            data[field] = _type(data.get(field))

        elif check(_type) and is_dataclass(_type):
            if _type in [non_recursive_classes]:
                data[field] = _type(data.get(field))

        elif check(_type) and isinstance(_type, list):
            data[field] = [recur(_type[0], x) for x in data[field]]

    return cls(**data)
