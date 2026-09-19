from pathlib import Path
import sys

from .abc_renderer import ABCTreeRenderer


class PathTreeRenderer(ABCTreeRenderer):

    def get_children(self, node):
        if node.is_symlink():
            return ()
        if sys.version_info >= (3, 12) and node.is_junction():
            return ()
        if node.is_dir():
            try:
                return tuple(node.iterdir())
            except OSError:
                return ()
        else:
            return ()

    def on_node_enter(self, node, line_prefix):
        self.output_lines.append(line_prefix + node.name)

    def on_node_exit(self, node, line_prefix):
        pass


def render(*args, glyph_style=None):
    tree_renderer = PathTreeRenderer(glyph_style=glyph_style)
    tree_renderer.render_tree(Path(*args).resolve())
    return tree_renderer
