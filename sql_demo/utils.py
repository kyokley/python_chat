from enum import Enum


class StrEnum(str, Enum):
    @classmethod
    def from_string(cls, str_type):
        if str_type is not None:
            for enum_type in cls:
                if enum_type.value.lower() == str_type.strip().lower():
                    return enum_type
        raise Exception(f'{str_type} did not match any types')

    def __str__(self):
        return self.value
