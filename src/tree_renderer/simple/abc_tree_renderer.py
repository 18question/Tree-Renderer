from abc import ABC, abstractmethod

from .glyph_style import STYLE_UNICODE


class ABCTreeRenderer(ABC):
    glyph_style = STYLE_UNICODE

    def __init__(self, glyph_style=None):
        if glyph_style is None:
            self.glyph_style = self.__class__.glyph_style
        else:
            self.glyph_style = glyph_style
        self.indent_prefix_stack = []

    @abstractmethod
    def get_children(self, node):
        pass

    @abstractmethod
    def on_node_enter(self, node, line_prefix):
        pass

    @abstractmethod
    def on_node_exit(self, node, line_prefix):
        pass
