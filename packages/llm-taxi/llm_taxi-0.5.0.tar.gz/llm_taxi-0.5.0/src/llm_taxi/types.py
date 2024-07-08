from typing import Literal, TypeVar, Union

from typing_extensions import override


class NotSupported:
    def __bool__(self) -> Literal[False]:
        return False

    @override
    def __repr__(self) -> str:
        return "NOT_SUPPORTED"


NOT_SUPPORTED = NotSupported()

_T = TypeVar("_T")
NotSupportedOr = Union[_T, NotSupported]
