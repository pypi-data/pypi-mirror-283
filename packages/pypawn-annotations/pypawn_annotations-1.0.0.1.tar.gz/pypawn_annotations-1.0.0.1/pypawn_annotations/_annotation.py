from ._function import PawnFunction
from .store import AnnotationQualifier, AnnotationTags
from .store import ANNOTATION_TAG_NAMES, ANNOTATION_QUALIFIER_NAMES
from .store import FUNC_FLAG_TITLE, FUNC_FLAG_NAME, FUNC_FLAG_GENERAL_TAG, FUNC_FLAG_ARGS

WHITESPACE = 4


def _compute_dynamic_whitespace(func_args: list) -> int:
    if func_args is None or not len(func_args):
        return 0

    _max_len_name = max(
        [len(arg["name"]) for arg in func_args]
    )

    _max_len_qualifier = max(
        [len(ANNOTATION_QUALIFIER_NAMES[arg["qualifier"].value]) for arg in func_args]
    )

    _max_len_tag = max(
        [len(arg["tag"][1]) for arg in func_args]
    )

    return _max_len_name + _max_len_qualifier + _max_len_tag


class Annotation:
    def __init__(self, description: str, function: PawnFunction):
        self._function: PawnFunction = function
        self._description: str = description

    @property
    def description(self):
        return self._description

    @property
    def function(self):
        return self._function

    def show(self) -> str:
        """
        Show annotation
        :return str: This is annotation
        """

        function: PawnFunction = self._function
        function_flags: int = function.flags()

        if function_flags == (FUNC_FLAG_TITLE | FUNC_FLAG_NAME | FUNC_FLAG_GENERAL_TAG | FUNC_FLAG_ARGS):
            dynamic_whitespace: int = _compute_dynamic_whitespace(self._function.args) + WHITESPACE

            buffer: str = "/* "

            for line in self._description.split("\n"):
                buffer += f"\n * {line}"

            buffer += "\n * "

            for param in function.args:
                # func: name
                name: str = param['name']

                # func: qualifier
                qualifier: str = ANNOTATION_QUALIFIER_NAMES[param['qualifier'].value]

                # func: tag
                tag: str = param['tag'][1]

                # qualifier & tag
                qualifier_and_tag: str = f"{qualifier} {tag}" if len(qualifier) else f"{tag}"

                # finally whitespace
                whitespace: int = dynamic_whitespace - (len(name) + len(qualifier_and_tag))

                # param buffer
                buffer += f"\n * @param {qualifier_and_tag}:{name}{' ' * whitespace}{param['description']}"

            buffer += f"\n * @return {' ' * dynamic_whitespace}{function.general_tag[1]} \n */"
            return buffer

        if function_flags:
            buffer: str = "/* "

            for line in self._description.split("\n"):
                buffer += f"\n * {line}"

            buffer += "\n * "
            buffer += f"\n */"
            return buffer
        return ''


if __name__ == "__main__":
    func: PawnFunction = PawnFunction(string='func test_func()')

    func.general_tag = (AnnotationTags.TAG_INT, ANNOTATION_TAG_NAMES[AnnotationTags.TAG_INT.value])

    func.add_arg(
        {
            "qualifier": AnnotationQualifier.QUALIFIER_NONE,
            "tag": (
                AnnotationTags.TAG_INT,
                ANNOTATION_TAG_NAMES[AnnotationTags.TAG_INT.value]
            ),
            "name": "test_arg:1",
            "description": "test_description:1"
        }
    )

    func.add_arg(
        {
            "qualifier": AnnotationQualifier.QUALIFIER_CONST,
            "tag": (
                AnnotationTags.TAG_INT,
                ANNOTATION_TAG_NAMES[AnnotationTags.TAG_INT.value]
            ),
            "name": "test_arg:2",
            "description": "test_description:2"
        }
    )

    func.add_arg(
        {
            "qualifier": AnnotationQualifier.QUALIFIER_NONE,
            "tag": (
                AnnotationTags.TAG_INT,
                ANNOTATION_TAG_NAMES[AnnotationTags.TAG_INT.value]
            ),
            "name": "test_arg:2",
            "description": "test_description:2"
        },
    )

    annotation = Annotation(
        description="Annotation:1",
        function=func
    )

    print(annotation.show())
