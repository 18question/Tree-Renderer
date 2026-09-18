from abc import ABCMeta, abstractmethod
from typing import Any, Iterable

from .glyph_style import GlyphStyle


class ABCTreeRenderer(metaclass=ABCMeta):
    glyph_style: GlyphStyle
    indent_prefix_stack: list[str]
    output_lines: list[str]

    def __init__(self, glyph_style: GlyphStyle | None = None) -> None: ...

    @abstractmethod
    def get_children(self, node: Any) -> Iterable: ...

    @abstractmethod
    def on_node_enter(self, node: Any, line_prefix: str) -> None: ...

    @abstractmethod
    def on_node_exit(self, node: Any, line_prefix: str) -> None: ...

    def render_tree(self, root_node: Any) -> None: ...

    def render_subtree(self, node: Any, is_root: bool, is_last: bool) -> None: ...

    def __str__(self) -> str: ...
