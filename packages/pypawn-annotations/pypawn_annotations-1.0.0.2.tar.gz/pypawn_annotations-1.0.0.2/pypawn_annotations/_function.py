from re import sub
from store import AnnotationQualifier, AnnotationTags
from store import ANNOTATION_TAG_NAMES, ANNOTATION_QUALIFIER_NAMES
from store import HUNGARIAN_NOTATION_MAX_ITEM_LENGTH, HUNGARIAN_NOTATION_TUPLE
from store import FUNC_ARG_STRUCTURE, FUNC_MAX_STRUCTURE_PARAM, FUNC_READ_PATTERN
from store import FUNC_FLAG_TITLE, FUNC_FLAG_NAME, FUNC_FLAG_GENERAL_TAG, FUNC_FLAG_ARGS


def _remove_whitespace(string: str) -> str:
    """
    This function returning str if 'string' type == str, else 'string' object
    :param string:
    :return str:
    """
    if isinstance(string, str):
        return " ".join(string.split())
    return string


def _parse_function_general_tag(general_tag: str) -> tuple[AnnotationTags, str]:
    """
    :param general_tag:
    :return tuple[AnnotationTags, str]:
    """
    if general_tag in ANNOTATION_TAG_NAMES:
        return AnnotationTags[ANNOTATION_TAG_NAMES.index(general_tag)], general_tag
    else:
        return AnnotationTags.TAG_CUSTOM, general_tag


def _parse_function_args(args: list) -> list[dict]:
    """
    :param list: args
    :return list[dict]:
    """
    output: list[dict] = []

    if not isinstance(args, list):
        return output

    for arg in args:
        _sub = sub(pattern=r"\s+|,|;|\=.+", repl=" ", string=arg).split(" ")
        _sub = [item for item in _sub if item]

        if not len(_sub):
            break

        _function_args: dict = {
            "qualifier": AnnotationQualifier.QUALIFIER_NONE,
            "tag": (AnnotationTags.TAG_INT, ANNOTATION_TAG_NAMES[AnnotationTags.TAG_INT.value]),
            "name": "",
            "description": ""
        }

        for item in _sub:
            if item in ANNOTATION_QUALIFIER_NAMES:
                _function_args["qualifier"] = AnnotationQualifier(ANNOTATION_QUALIFIER_NAMES.index(item))
                continue
            elif item[-1] == ":":
                item = item[0:-1]
                if item in ANNOTATION_TAG_NAMES:
                    _index = ANNOTATION_TAG_NAMES.index(item)
                    _function_args["tag"] = (AnnotationTags(_index), ANNOTATION_TAG_NAMES[_index])
                else:
                    _function_args["tag"] = (AnnotationTags.TAG_CUSTOM, item)
                continue
            else:
                """
                    Hungarian notation
                """
                _offset_name: int = 1
                _offset_notation: int = 0

                if len(item) + _offset_name >= HUNGARIAN_NOTATION_MAX_ITEM_LENGTH:
                    for n in HUNGARIAN_NOTATION_TUPLE:
                        # validation prefix hungarian notation
                        _offset_notation = len(n)
                        if item[0:_offset_notation] != n:
                            continue
                        # validation item first symbol after prefix
                        _chars = item[_offset_notation:_offset_notation + _offset_name]
                        if not _chars.isalpha() or not _chars.isupper():
                            continue
                        # validation item tag after change
                        if _function_args["tag"][0] == AnnotationTags.TAG_CUSTOM:
                            continue
                        # change tag
                        _function_args["tag"] = (
                            AnnotationTags(HUNGARIAN_NOTATION_TUPLE.index(n)),
                            ANNOTATION_TAG_NAMES[HUNGARIAN_NOTATION_TUPLE.index(n)]
                        )
                        break

                _function_args["name"] = item
                _function_args["description"] = item
        output.append(_function_args)
    return output


class _Function(object):
    def __init__(self, string: str):
        self._string: str = string
        self._general_tag = None
        self._title = None
        self._name = None
        self._args = None

    @property
    def string(self) -> str: return self._string

    @property
    def general_tag(self) -> tuple: return self._general_tag

    @property
    def title(self) -> str: return self._title

    @property
    def name(self) -> str: return self._name

    @property
    def args(self) -> list: return self._args

    @title.setter
    def title(self, value: str):
        self._title = value

    @name.setter
    def name(self, value: str):
        if len(value) > 64:
            raise AttributeError("[Error] name length (max 64 symbols)")
        self._name = value

    @general_tag.setter
    def general_tag(self, value: tuple[AnnotationTags, str]):

        # Validation: value type
        if not isinstance(value, tuple):
            raise AttributeError("[Error] set value is not tuple")

        # Validation: value len
        if len(value) < 2:
            raise AttributeError("[Error] tuple len < 2")

        # Validation: value[0] contains AnnotationTags
        if value[0].value not in [e.value for e in AnnotationTags]:
            raise AttributeError(
                f"[Error] value is not annotation_tags type {value} != {[e.value for e in AnnotationTags]}")

        self._general_tag = value

    def add_arg(self, arg: dict):
        """
        Add parameters to function
        :parameters
            arg (dict): Dict of function parameters
                :key qualifier int: The qualifier of the function arg
                :key tag tuple: The tag of the function arg
                :key name str: The name of the function arg
                :key description str: The description of the function arg
        """

        # Validation: func name
        if self._name is None:
            raise AttributeError("[Error] Empty name function")

        # Validation: arg param
        if not arg:
            raise AttributeError("[Error] Empty parameters")

        # Validation: arg keys
        if frozenset(arg.keys()) != FUNC_ARG_STRUCTURE:
            raise AttributeError("[Error] param keys: ", FUNC_ARG_STRUCTURE)

        # Validation: qualifier
        if arg["qualifier"].value not in [e.value for e in AnnotationQualifier]:
            raise AttributeError(
                f"[Error] value is not annotation_qualifier type {arg['qualifier']} != {[e.value for e in AnnotationQualifier]}")

        # [0] Tag validation
        if not isinstance(arg["tag"], tuple):
            raise AttributeError("[Error] tag is not tuple")

        # [1] Tag validation
        if len(arg["tag"]) < 2:
            raise AttributeError("[Error] tag tuple len < 2")

        # [2] Tag validation
        if arg["tag"][0].value not in [e.value for e in AnnotationTags]:
            raise AttributeError(
                f"[Error] value is not annotation_tags type {arg['tag']} != {[e.value for e in AnnotationTags]}")

        # Validation: len name
        if len(arg["name"]) > 32:
            raise AttributeError("[Error] name length (max 32 symbols)")

        # Validation: arg list
        if self._args is None:
            self._args = list()

        self._args.append(arg)


class PawnFunction(_Function):
    def __init__(self, string: str):
        super().__init__(string=string)
        self._match: tuple = self._create()

    @property
    def match(self) -> tuple:
        return self._match

    def is_title_native(self) -> bool:
        return self.title == 'native'

    def is_title_forward(self) -> bool:
        return self.title == 'forward'

    def is_title_function(self) -> bool:
        return self.title == 'f' or self.title == 'func' or self.title == 'function'

    def _create(self) -> tuple:
        _match: object = FUNC_READ_PATTERN.match(string=self._string)

        if _match is None:
            return tuple()

        _match_groups: tuple = _match.groups()

        if isinstance(_match_groups, tuple) and len(_match_groups) == FUNC_MAX_STRUCTURE_PARAM:
            self.title = _remove_whitespace(_match.group(1))
            self.name = _remove_whitespace(_match.group(3))
            self.general_tag = _parse_function_general_tag(_match.group(2))

            for arg in _parse_function_args(_match.group(4).split(",")):
                self.add_arg(arg)

        return _match_groups

    def flags(self) -> int:
        bit_sum: int = 0

        if self.title is not None:
            bit_sum |= FUNC_FLAG_TITLE

        if self.name is not None:
            bit_sum |= FUNC_FLAG_NAME

        if self.general_tag is not None:
            bit_sum |= FUNC_FLAG_GENERAL_TAG

        if self.args is not None:
            bit_sum |= FUNC_FLAG_ARGS

        return bit_sum


if __name__ == "__main__":
    function = PawnFunction(string="func test_func(const CustomTag: iVar1, const szVar2[32]);")

    print("[0] string:", function.string)
    print("[1] title:", function.title)
    print("[2] general_tag:", function.general_tag)
    print("[3] name:", function.name)
    print("[4] args:", function.args)
    print("[5] is_title_tag_function:", function.is_title_function())
    print("[6] is_title_tag_forward:", function.is_title_forward())
    print("[7] is_title_tag_native:", function.is_title_native())
    print("[8] flags:", function.flags())
