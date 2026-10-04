from typing import Iterable

from psutil import Process

from .abc_renderer import ABCTreeRenderer
from .colors import Paint
from .glyph_style import GlyphStyle


class ProcessColors:
    pid: Paint
    name: Paint
    field: Paint
    separator: Paint
    value: Paint
    error: Paint

    def __init__(
            self,
            pid: Paint,
            name: Paint,
            field: Paint,
            separator: Paint,
            value: Paint,
            error: Paint,
    ) -> None: ...

    def replace(
            self,
            pid: Paint | None = None,
            name: Paint | None = None,
            field: Paint | None = None,
            separator: Paint | None = None,
            value: Paint | None = None,
            error: Paint | None = None,
    ) -> ProcessColors: ...


COLORS_PROCESS_DEFAULT: ProcessColors
COLORS_PROCESS_16: ProcessColors
COLORS_PROCESS_OFF: ProcessColors


class ProcessTreeRenderer(ABCTreeRenderer):
    colors: ProcessColors
    details: bool

    def __init__(
            self,
            glyph_style: GlyphStyle | None = None,
            colors: ProcessColors | None = None,
            details: bool = True,
    ) -> None: ...

    def get_children(self, node: Process) -> Iterable[Process]: ...

    def on_node_enter(
            self,
            node: Process,
            line_prefix: str,
            is_root: bool,
            is_last: bool,
    ) -> None: ...

    def on_node_exit(
            self,
            node: Process,
            line_prefix: str,
            is_root: bool,
            is_last: bool,
    ) -> None: ...

    def render_tree(self, root_node: Process) -> None: ...

    def render_subtree(
            self,
            node: Process,
            is_root: bool,
            is_last: bool,
    ) -> None: ...


def render(
        root_node: Process,
        glyph_style: GlyphStyle | None = None,
        colors: ProcessColors | None = None,
        details: bool = True,
) -> ProcessTreeRenderer: ...


def render_from_pid(
        pid: int | None = None,
        glyph_style: GlyphStyle | None = None,
        colors: ProcessColors | None = None,
        details: bool = True,
) -> ProcessTreeRenderer: ...
