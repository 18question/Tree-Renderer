from _typeshed import StrPath
from pathlib import Path
from typing import Iterable

from .abc_renderer import ABCTreeRenderer
from .colors import Paint
from .glyph_style import GlyphStyle


class PathColors:
    directory: Paint
    file: Paint
    symlink: Paint
    junction: Paint
    error: Paint

    def __init__(
            self,
            directory: Paint,
            file: Paint,
            symlink: Paint,
            junction: Paint,
            error: Paint,
    ) -> None: ...

    def replace(
            self,
            directory: Paint | None = None,
            file: Paint | None = None,
            symlink: Paint | None = None,
            junction: Paint | None = None,
            error: Paint | None = None,
    ) -> PathColors: ...


COLORS_PATH_FULL: PathColors
COLORS_PATH_OFF: PathColors


class PathTreeRenderer(ABCTreeRenderer):
    colors: PathColors
    recursive: bool
    called: bool

    def __init__(
            self,
            glyph_style: GlyphStyle | None = None,
            colors: PathColors | None = None,
            recursive: bool = True,
    ) -> None: ...

    def get_children(self, node: Path) -> Iterable[Path]: ...

    def on_node_enter(
            self,
            node: Path,
            line_prefix: str,
            is_root: bool,
            is_last: bool,
    ) -> None: ...

    def on_node_exit(
            self,
            node: Path,
            line_prefix: str,
            is_root: bool,
            is_last: bool,
    ) -> None: ...

    def render_tree(self, root_node: Path) -> None: ...

    def render_subtree(
            self,
            node: Path,
            is_root: bool,
            is_last: bool,
    ) -> None: ...


def render(
        *args: StrPath,
        glyph_style: GlyphStyle | None = None,
        colors: PathColors | None = None,
        recursive: bool = True,
) -> PathTreeRenderer: ...
