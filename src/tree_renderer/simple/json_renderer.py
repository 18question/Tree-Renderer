import json

from .abc_renderer import ABCTreeRenderer
from .glyph_style import STYLE_BLANK_INDENT_4


class JSONTreeRenderer(ABCTreeRenderer):
    glyph_style = STYLE_BLANK_INDENT_4

    def get_children(self, node):
        if isinstance(node, tuple):
            value = node[1]
            if isinstance(value, list):
                return value
            elif isinstance(value, dict):
                return value.items()
            else:
                return ()
        elif isinstance(node, list):
            return node
        elif isinstance(node, dict):
            return node.items()
        else:
            return ()

    def on_node_enter(self, node, line_prefix):
        if isinstance(node, tuple):
            key = node[0]
            value = node[1]
            if isinstance(value, list):
                self.output_lines.append(line_prefix + repr(key) + ": [")
            elif isinstance(value, dict):
                self.output_lines.append(line_prefix + repr(key) + ": {")
            else:
                self.output_lines.append(line_prefix + repr(key) + ": " + repr(value))
        elif isinstance(node, list):
            self.output_lines.append(line_prefix + "[")
        elif isinstance(node, dict):
            self.output_lines.append(line_prefix + "{")
        else:
            self.output_lines.append(line_prefix + repr(node))

    def on_node_exit(self, node, line_prefix):
        if isinstance(node, tuple):
            value = node[1]
            if isinstance(value, list):
                self.output_lines.append(line_prefix + "]")
            elif isinstance(value, dict):
                self.output_lines.append(line_prefix + "}")
            else:
                pass
        elif isinstance(node, list):
            self.output_lines.append(line_prefix + "]")
        elif isinstance(node, dict):
            self.output_lines.append(line_prefix + "}")
        else:
            pass


def render(root_node, glyph_style=None):
    tree_renderer = JSONTreeRenderer(glyph_style=glyph_style)
    tree_renderer.render_tree(root_node)
    return tree_renderer


def render_from_path(path, glyph_style=None):
    with open(path, mode="r", encoding="utf-8") as fp:
        root_node = json.load(fp)
    return render(root_node, glyph_style=glyph_style)
