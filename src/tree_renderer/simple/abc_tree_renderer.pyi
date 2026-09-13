from abc import ABC, abstractmethod
from typing import Any, Iterable

from .glyph_style import GlyphStyle


class ABCTreeRenderer(ABC):
    glyph_style: GlyphStyle
    indent_prefix_stack: list[str]

    def __init__(self, glyph_style: GlyphStyle | None = None) -> None: ...

    @abstractmethod
    def get_children(self, node: Any) -> Iterable: ...

    @abstractmethod
    def on_node_enter(self, node: Any, line_prefix: str) -> None: ...

    @abstractmethod
    def on_node_exit(self, node: Any, line_prefix: str) -> None: ...
