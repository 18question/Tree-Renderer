import datetime

import psutil

from .abc_renderer import ABCTreeRenderer
from .colors import PAINT_OFF, Paint


class ProcessColors:

    def __init__(self, pid, name, field, separator, value, error):
        self.pid = pid
        self.name = name
        self.field = field
        self.separator = separator
        self.value = value
        self.error = error

    def replace(self, pid=None, name=None, field=None, separator=None, value=None, error=None):
        if pid is None:
            pid = self.pid
        if name is None:
            name = self.name
        if field is None:
            field = self.field
        if separator is None:
            separator = self.separator
        if value is None:
            value = self.value
        if error is None:
            error = self.error

        return ProcessColors(
            pid=pid,
            name=name,
            field=field,
            separator=separator,
            value=value,
            error=error,
        )


COLORS_PROCESS_DEFAULT = ProcessColors(
    pid=Paint("\033[1;38;2;51;204;255m"),
    name=PAINT_OFF,
    field=Paint("\033[38;2;84;179;62m"),
    separator=Paint("\033[1;38;2;237;134;74m"),
    value=PAINT_OFF,
    error=Paint("\033[38;2;242;73;90m"),
)

COLORS_PROCESS_16 = ProcessColors(
    pid=Paint("\033[1;34m"),
    name=PAINT_OFF,
    field=Paint("\033[32m"),
    separator=Paint("\033[1;33m"),
    value=PAINT_OFF,
    error=Paint("\033[31m"),
)

COLORS_PROCESS_OFF = ProcessColors(
    pid=PAINT_OFF,
    name=PAINT_OFF,
    field=PAINT_OFF,
    separator=PAINT_OFF,
    value=PAINT_OFF,
    error=PAINT_OFF,
)


class ProcessTreeRenderer(ABCTreeRenderer):
    colors = COLORS_PROCESS_DEFAULT

    def __init__(self, glyph_style=None, colors=None, details=True):
        super().__init__(glyph_style=glyph_style, colors=colors)
        self.details = details

    def get_children(self, node):
        try:
            return node.children()
        except psutil.Error:
            return ()

    def on_node_enter(self, node, line_prefix, is_root, is_last):
        colors = self.colors
        pid = colors.pid(str(node.pid))

        try:
            name = node.name()
        except psutil.Error:
            self.output_lines.append(line_prefix + pid + colors.error(":"))
        else:
            self.output_lines.append(line_prefix + pid + colors.separator(": ") + colors.name(name))

        if not self.details:
            return

        indent = "".join(self.indent_prefix_stack)
        separator = colors.separator(" = ")

        try:
            cmdline = " ".join(node.cmdline())
        except psutil.Error:
            self.output_lines.append(indent + colors.error("cmdline"))
        else:
            self.output_lines.append(indent + colors.field("cmdline") + separator + colors.value(cmdline))

        try:
            status = node.status()
        except psutil.Error:
            self.output_lines.append(indent + colors.error("status"))
        else:
            self.output_lines.append(indent + colors.field("status") + separator + colors.value(status))

        try:
            username = node.username()
        except psutil.Error:
            self.output_lines.append(indent + colors.error("username"))
        else:
            self.output_lines.append(indent + colors.field("username") + separator + colors.value(username))

        try:
            create_time = node.create_time()
        except psutil.Error:
            self.output_lines.append(indent + colors.error("create_time"))
        else:
            formatted = datetime.datetime.fromtimestamp(create_time).strftime("%Y-%m-%d %H:%M:%S")
            self.output_lines.append(indent + colors.field("create_time") + separator + colors.value(formatted))

    def on_node_exit(self, node, line_prefix, is_root, is_last):
        pass


def render(root_node, glyph_style=None, colors=None, details=True):
    tree_renderer = ProcessTreeRenderer(glyph_style=glyph_style, colors=colors, details=details)
    tree_renderer.render_tree(root_node)
    return tree_renderer


def render_from_pid(pid=None, glyph_style=None, colors=None, details=True):
    return render(psutil.Process(pid), glyph_style=glyph_style, colors=colors, details=details)
