from pathlib import Path
import sys

from .abc_renderer import ABCTreeRenderer
from .colors import PAINT_OFF, Paint


class PathColors:

    def __init__(self, directory, file, symlink, junction, error):
        self.directory = directory
        self.file = file
        self.symlink = symlink
        self.junction = junction
        self.error = error

    def replace(self, directory=None, file=None, symlink=None, junction=None, error=None):
        if directory is None:
            directory = self.directory
        if file is None:
            file = self.file
        if symlink is None:
            symlink = self.symlink
        if junction is None:
            junction = self.junction
        if error is None:
            error = self.error

        return PathColors(
            directory=directory,
            file=file,
            symlink=symlink,
            junction=junction,
            error=error,
        )


COLORS_PATH_FULL = PathColors(
    directory=Paint("\033[34m"),
    file=PAINT_OFF,
    symlink=Paint("\033[36m"),
    junction=Paint("\033[33m"),
    error=Paint("\033[31m"),
)

COLORS_PATH_OFF = COLORS_PATH_FULL.replace(
    directory=PAINT_OFF,
    file=PAINT_OFF,
    symlink=PAINT_OFF,
    junction=PAINT_OFF,
    error=PAINT_OFF,
)


class PathTreeRenderer(ABCTreeRenderer):
    colors = COLORS_PATH_FULL

    def __init__(self, glyph_style=None, colors=None, recursive=True):
        super().__init__(glyph_style=glyph_style, colors=colors)
        self.recursive = recursive
        self.called = False

    def get_children(self, node):
        if not self.called:
            self.called = True
        elif not self.recursive:
            return ()

        try:
            if node.is_symlink():
                return ()
            if sys.version_info >= (3, 12) and node.is_junction():
                return ()
            if node.is_dir():
                return tuple(node.iterdir())
            else:
                return ()
        except OSError:
            return ()

    def on_node_enter(self, node, line_prefix, is_root, is_last):
        if is_root:
            label = str(node)
        else:
            label = node.name
            if not label:
                label = str(node)

        try:
            parts = []
            if node.is_symlink():
                parts.append(self.colors.symlink(label))
                try:
                    target = str(node.resolve())
                except OSError:
                    parts.append(self.colors.error(" ->"))
                else:
                    parts.append(" -> ")
                    if node.is_dir():
                        parts.append(self.colors.directory(target))
                    elif node.is_file():
                        parts.append(self.colors.file(target))
                    else:
                        parts.append(self.colors.error(target))
            elif sys.version_info >= (3, 12) and node.is_junction():
                parts.append(self.colors.junction(label))
                try:
                    target = str(node.resolve())
                except OSError:
                    parts.append(self.colors.error(" ->"))
                else:
                    parts.append(" -> ")
                    if node.is_dir():
                        parts.append(self.colors.directory(target))
                    else:
                        parts.append(self.colors.error(target))
            elif node.is_dir():
                parts.append(self.colors.directory(label))
            elif node.is_file():
                parts.append(self.colors.file(label))
            else:
                parts.append(self.colors.error(label))

        except OSError:
            self.output_lines.append(line_prefix + self.colors.error(label))
        else:
            self.output_lines.append(line_prefix + "".join(parts))

    def on_node_exit(self, node, line_prefix, is_root, is_last):
        pass


def render(*args, glyph_style=None, colors=None, recursive=True):
    tree_renderer = PathTreeRenderer(glyph_style=glyph_style, colors=colors, recursive=recursive)
    tree_renderer.render_tree(Path(*args).resolve())
    return tree_renderer
