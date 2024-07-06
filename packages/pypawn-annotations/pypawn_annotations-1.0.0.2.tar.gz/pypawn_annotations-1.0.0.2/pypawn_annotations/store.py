from enum import Enum
from re import compile


class AnnotationQualifier(Enum):
    QUALIFIER_NONE = 0
    QUALIFIER_CONST = 1


class AnnotationTags(Enum):
    TAG_INT = 0
    TAG_FLOAT = 1
    TAG_STR = 2
    TAG_BOOL = 3
    TAG_CUSTOM = 4


ANNOTATION_TAG_NAMES: tuple = (
    "int",
    "float",
    "str",
    "bool",
)

ANNOTATION_QUALIFIER_NAMES: tuple = (
    "",
    "const",
)

HUNGARIAN_NOTATION_TUPLE: tuple = (
    'i',
    'fl',
    'sz',
    'b'
)

FUNC_TITLES: tuple = (
    'func',
    'native',
    'forward'
)

FUNC_FLAG_TITLE = (1 << 0)
FUNC_FLAG_NAME = (1 << 1)
FUNC_FLAG_GENERAL_TAG = (1 << 2)
FUNC_FLAG_ARGS = (1 << 3)

FUNC_MAX_STRUCTURE_PARAM = 4
HUNGARIAN_NOTATION_MAX_ITEM_LENGTH = len(max(HUNGARIAN_NOTATION_TUPLE))
FUNC_READ_PATTERN = compile(r"^(\w+\s+)(.*:|\s{0})(.*?(?=\(\)*))\(([^)]*)\)")
FUNC_ARG_STRUCTURE: frozenset = frozenset({"qualifier", "tag", "name", "description"})

if __name__ == "__main__":
    print("[0]", [e for e in AnnotationQualifier])
    print("[1]", [e for e in AnnotationTags])
    print("[2]", ANNOTATION_TAG_NAMES)
    print("[3]", ANNOTATION_QUALIFIER_NAMES)
    print("[4]", HUNGARIAN_NOTATION_TUPLE)
    print("[5]", FUNC_MAX_STRUCTURE_PARAM)
    print("[6]", HUNGARIAN_NOTATION_MAX_ITEM_LENGTH)
    print("[7]", FUNC_ARG_STRUCTURE)
