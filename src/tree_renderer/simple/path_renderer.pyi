from _typeshed import StrPath
from pathlib import Path
from typing import Iterable

from .abc_renderer import ABCTreeRenderer
from .glyph_style import GlyphStyle


class PathTreeRenderer(ABCTreeRenderer):

    def get_children(self, node: Path) -> Iterable[Path]: ...

    def on_node_enter(self, node: Path, line_prefix: str) -> None: ...

    def on_node_exit(self, node: Path, line_prefix: str) -> None: ...

    def render_tree(self, root_node: Path) -> None: ...

    def render_subtree(self, node: Path, is_root: bool, is_last: bool) -> None: ...


def render(*args: StrPath, glyph_style: GlyphStyle | None = None) -> PathTreeRenderer: ...
