from typing import Iterable

from psutil import Process

from .abc_renderer import ABCTreeRenderer
from .glyph_style import GlyphStyle


class ProcessTreeRenderer(ABCTreeRenderer):

    def get_children(self, node: Process) -> Iterable[Process]: ...

    def on_node_enter(self, node: Process, line_prefix: str) -> None: ...

    def on_node_exit(self, node: Process, line_prefix: str) -> None: ...

    def render_tree(self, root_node: Process) -> None: ...

    def render_subtree(self, node: Process, is_root: bool, is_last: bool) -> None: ...


def render(root_node: Process, glyph_style: GlyphStyle | None = None) -> ProcessTreeRenderer: ...


def render_from_pid(pid: int | None = None, glyph_style: GlyphStyle | None = None) -> ProcessTreeRenderer: ...
