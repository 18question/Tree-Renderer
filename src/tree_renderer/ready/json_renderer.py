import json

from .abc_renderer import ABCTreeRenderer
from .colors import PAINT_OFF, Paint
from .glyph_style import STYLE_BLANK_INDENT_4


class JSONColors:

    def __init__(
            self,
            keyword,
            number_literal,
            string_literal,
            key,
            comma,
            colon,
            list_brackets,
            dict_braces,
    ):
        self.keyword = keyword
        self.number_literal = number_literal
        self.string_literal = string_literal
        self.key = key
        self.comma = comma
        self.colon = colon
        self.list_brackets = list_brackets
        self.dict_braces = dict_braces

    def replace(
            self,
            keyword=None,
            number_literal=None,
            string_literal=None,
            key=None,
            comma=None,
            colon=None,
            list_brackets=None,
            dict_braces=None,
    ):
        if keyword is None:
            keyword = self.keyword
        if number_literal is None:
            number_literal = self.number_literal
        if string_literal is None:
            string_literal = self.string_literal
        if key is None:
            key = self.key
        if comma is None:
            comma = self.comma
        if colon is None:
            colon = self.colon
        if list_brackets is None:
            list_brackets = self.list_brackets
        if dict_braces is None:
            dict_braces = self.dict_braces

        return JSONColors(
            keyword=keyword,
            number_literal=number_literal,
            string_literal=string_literal,
            key=key,
            comma=comma,
            colon=colon,
            list_brackets=list_brackets,
            dict_braces=dict_braces,
        )


COLORS_JSON_DEFAULT = JSONColors(
    keyword=Paint("\033[38;2;237;134;74m"),
    number_literal=Paint("\033[1;38;2;51;204;255m"),
    string_literal=Paint("\033[38;2;84;179;62m"),
    key=Paint("\033[38;2;237;148;255m"),
    comma=Paint("\033[1;38;2;237;134;74m"),
    colon=Paint("\033[1;38;2;237;134;74m"),
    list_brackets=PAINT_OFF,
    dict_braces=PAINT_OFF,
)

COLORS_JSON_16 = JSONColors(
    keyword=Paint("\033[33m"),
    number_literal=Paint("\033[1;34m"),
    string_literal=Paint("\033[32m"),
    key=Paint("\033[35m"),
    comma=Paint("\033[1;33m"),
    colon=Paint("\033[1;33m"),
    list_brackets=PAINT_OFF,
    dict_braces=PAINT_OFF,
)

COLORS_JSON_OFF = JSONColors(
    keyword=PAINT_OFF,
    number_literal=PAINT_OFF,
    string_literal=PAINT_OFF,
    key=PAINT_OFF,
    comma=PAINT_OFF,
    colon=PAINT_OFF,
    list_brackets=PAINT_OFF,
    dict_braces=PAINT_OFF,
)


class JSONTreeRenderer(ABCTreeRenderer):
    glyph_style = STYLE_BLANK_INDENT_4
    colors = COLORS_JSON_DEFAULT
    fold_threshold = 0

    def __init__(self, glyph_style=None, colors=None, fold_threshold=None):
        super().__init__(glyph_style=glyph_style, colors=colors)
        if fold_threshold is None:
            self.fold_threshold = self.__class__.fold_threshold
        else:
            self.fold_threshold = fold_threshold

    def should_fold(self, value):
        if isinstance(value, list):
            if len(value) > self.fold_threshold:
                return False
            if any(isinstance(item, (list, dict)) for item in value):
                return False
        if isinstance(value, dict):
            if len(value) > self.fold_threshold:
                return False
            if any(isinstance(item, (list, dict)) for item in value.values()):
                return False
        return True

    def format(self, value):
        # The bool check must come before the number check: `bool` is a subclass of `int`.
        if value is None:
            return self.colors.keyword("null")
        if isinstance(value, bool):
            return self.colors.keyword("true" if value else "false")
        if isinstance(value, (int, float)):
            return self.colors.number_literal(repr(value))
        if isinstance(value, str):
            # JSON requires double quotes.
            return self.colors.string_literal(json.dumps(value, ensure_ascii=False))
        if isinstance(value, list):
            return "".join(
                (
                    self.colors.list_brackets("["),
                    # Recurses to render nested containers inline.
                    self.colors.comma(", ").join(self.format(item) for item in value),
                    self.colors.list_brackets("]"),
                ),
            )
        if isinstance(value, dict):
            return "".join(
                (
                    self.colors.dict_braces("{"),
                    self.colors.comma(", ").join(
                        "".join(
                            (
                                # JSON requires double quotes.
                                self.colors.key(json.dumps(key, ensure_ascii=False)),
                                self.colors.colon(": "),
                                # Recurses to render nested containers inline.
                                self.format(item),
                            ),
                        ) for key, item in value.items()
                    ),
                    self.colors.dict_braces("}"),
                ),
            )
        raise TypeError("Object of type " + type(value).__name__ + " is not JSON serializable")

    def get_children(self, node):
        if isinstance(node, tuple):
            value = node[1]
        else:
            value = node

        if self.should_fold(value):
            return ()

        if isinstance(value, list):
            return value
        elif isinstance(value, dict):
            return value.items()
        else:
            # Unreachable: the `should_fold` check above returns for non-containers.
            return ()

    def on_node_enter(self, node, line_prefix, is_root, is_last):
        if isinstance(node, tuple):
            key, value = node
            # JSON requires double quotes.
            head = line_prefix + self.colors.key(json.dumps(key, ensure_ascii=False)) + self.colors.colon(": ")
        else:
            value = node
            head = line_prefix

        if self.should_fold(value):
            # JSON forbids trailing commas.
            if is_root or is_last:
                self.output_lines.append(head + self.format(value))
            else:
                self.output_lines.append(head + self.format(value) + self.colors.comma(","))
            return

        if isinstance(value, list):
            self.output_lines.append(head + self.colors.list_brackets("["))
        elif isinstance(value, dict):
            self.output_lines.append(head + self.colors.dict_braces("{"))
        else:
            # Unreachable: the `should_fold` check above returns for non-containers.
            return

    def on_node_exit(self, node, line_prefix, is_root, is_last):
        if isinstance(node, tuple):
            value = node[1]
        else:
            value = node

        if self.should_fold(value):
            return

        if isinstance(value, list):
            content = self.colors.list_brackets("]")
        elif isinstance(value, dict):
            content = self.colors.dict_braces("}")
        else:
            # Unreachable: the `should_fold` check above returns for non-containers.
            return

        # JSON forbids trailing commas.
        if is_root or is_last:
            self.output_lines.append(line_prefix + content)
        else:
            self.output_lines.append(line_prefix + content + self.colors.comma(","))


def render(root_node, glyph_style=None, colors=None, fold_threshold=None):
    tree_renderer = JSONTreeRenderer(glyph_style=glyph_style, colors=colors, fold_threshold=fold_threshold)
    tree_renderer.render_tree(root_node)
    return tree_renderer


def render_from_path(path, glyph_style=None, colors=None, fold_threshold=None):
    with open(path, mode="r", encoding="utf-8") as fp:
        root_node = json.load(fp)
    return render(root_node, glyph_style=glyph_style, colors=colors, fold_threshold=fold_threshold)
