from _typeshed import StrPath
from typing import Iterable, TypeAlias

from .abc_renderer import ABCTreeRenderer
from .glyph_style import GlyphStyle

JSONType: TypeAlias = bool | int | float | str | list["JSONType"] | dict[str, "JSONType"] | None
NodeType: TypeAlias = JSONType | tuple[str, JSONType]


class JSONTreeRenderer(ABCTreeRenderer):

    def get_children(self, node: NodeType) -> Iterable[NodeType]: ...

    def on_node_enter(self, node: NodeType, line_prefix: str) -> None: ...

    def on_node_exit(self, node: NodeType, line_prefix: str) -> None: ...


def render(root_node: JSONType, glyph_style: GlyphStyle | None = None) -> JSONTreeRenderer: ...


def render_from_path(path: StrPath, glyph_style: GlyphStyle | None = None) -> JSONTreeRenderer: ...
