from _typeshed import StrPath
from typing import Iterable, TypeAlias

from .abc_renderer import ABCTreeRenderer
from .colors import Paint
from .glyph_style import GlyphStyle

JSONType: TypeAlias = bool | int | float | str | list["JSONType"] | dict[str, "JSONType"] | None
NodeType: TypeAlias = JSONType | tuple[str, JSONType]


class JSONColors:
    keyword: Paint
    number_literal: Paint
    string_literal: Paint
    key: Paint
    comma: Paint
    colon: Paint
    list_brackets: Paint
    dict_braces: Paint

    def __init__(
            self,
            keyword: Paint,
            number_literal: Paint,
            string_literal: Paint,
            key: Paint,
            comma: Paint,
            colon: Paint,
            list_brackets: Paint,
            dict_braces: Paint,
    ) -> None: ...

    def replace(
            self,
            keyword: Paint | None = None,
            number_literal: Paint | None = None,
            string_literal: Paint | None = None,
            key: Paint | None = None,
            comma: Paint | None = None,
            colon: Paint | None = None,
            list_brackets: Paint | None = None,
            dict_braces: Paint | None = None,
    ) -> JSONColors: ...


COLORS_JSON_DEFAULT: JSONColors
COLORS_JSON_16: JSONColors
COLORS_JSON_OFF: JSONColors


class JSONTreeRenderer(ABCTreeRenderer):
    colors: JSONColors
    fold_threshold: int

    def __init__(
            self,
            glyph_style: GlyphStyle | None = None,
            colors: JSONColors | None = None,
            fold_threshold: int | None = None,
    ) -> None: ...

    def should_fold(self, value: JSONType) -> bool: ...

    def format(self, value: JSONType) -> str: ...

    def get_children(self, node: NodeType) -> Iterable[NodeType]: ...

    def on_node_enter(
            self,
            node: NodeType,
            line_prefix: str,
            is_root: bool,
            is_last: bool,
    ) -> None: ...

    def on_node_exit(
            self,
            node: NodeType,
            line_prefix: str,
            is_root: bool,
            is_last: bool,
    ) -> None: ...

    def render_tree(self, root_node: JSONType) -> None: ...

    def render_subtree(
            self,
            node: NodeType,
            is_root: bool,
            is_last: bool,
    ) -> None: ...


def render(
        root_node: JSONType,
        glyph_style: GlyphStyle | None = None,
        colors: JSONColors | None = None,
        fold_threshold: int | None = None,
) -> JSONTreeRenderer: ...


def render_from_path(
        path: StrPath,
        glyph_style: GlyphStyle | None = None,
        colors: JSONColors | None = None,
        fold_threshold: int | None = None,
) -> JSONTreeRenderer: ...
