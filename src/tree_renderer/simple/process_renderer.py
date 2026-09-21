import psutil

from .abc_renderer import ABCTreeRenderer


class ProcessTreeRenderer(ABCTreeRenderer):

    def get_children(self, node):
        try:
            return node.children()
        except psutil.Error:
            return ()

    def on_node_enter(self, node, line_prefix):
        try:
            name = node.name()
        except psutil.Error as e:
            name = type(e).__name__ + ": " + str(e)
        self.output_lines.append(line_prefix + str(node.pid) + ": " + str(name))

    def on_node_exit(self, node, line_prefix):
        pass


def render(root_node, glyph_style=None):
    tree_renderer = ProcessTreeRenderer(glyph_style=glyph_style)
    tree_renderer.render_tree(root_node)
    return tree_renderer


def render_from_pid(pid=None, glyph_style=None):
    return render(psutil.Process(pid), glyph_style=glyph_style)
