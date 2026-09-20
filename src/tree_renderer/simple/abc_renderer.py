from abc import ABCMeta, abstractmethod

from .glyph_style import STYLE_UNICODE


class ABCTreeRenderer(metaclass=ABCMeta):
    glyph_style = STYLE_UNICODE

    def __init__(self, glyph_style=None):
        if glyph_style is None:
            self.glyph_style = self.__class__.glyph_style
        else:
            self.glyph_style = glyph_style
        self.indent_prefix_stack = []
        self.output_lines = []

    @abstractmethod
    def get_children(self, node):
        pass

    @abstractmethod
    def on_node_enter(self, node, line_prefix):
        pass

    @abstractmethod
    def on_node_exit(self, node, line_prefix):
        pass

    def render_tree(self, root_node):
        self.render_subtree(root_node, is_root=True, is_last=True)

    def render_subtree(self, node, is_root, is_last):
        # Process the line prefix.
        enter_line_prefix_list = self.indent_prefix_stack[:]
        if not is_root:
            if is_last:
                # Push onto the stack.
                self.indent_prefix_stack.append(self.glyph_style.indent_blank)
                enter_line_prefix_list.append(self.glyph_style.branch_end)
            else:
                # Push onto the stack.
                self.indent_prefix_stack.append(self.glyph_style.indent_guide)
                enter_line_prefix_list.append(self.glyph_style.branch_mid)
        enter_line_prefix = "".join(enter_line_prefix_list)
        exit_line_prefix = "".join(self.indent_prefix_stack)

        # Call the hook.
        self.on_node_enter(node, enter_line_prefix)

        # Iterate child nodes.
        child_iterator = iter(self.get_children(node))
        try:
            current_node = next(child_iterator)
        except StopIteration:
            # Length == 0
            pass
        else:
            # Length >= 1
            while True:
                try:
                    next_node = next(child_iterator)
                except StopIteration:
                    # Is last.
                    self.render_subtree(current_node, is_root=False, is_last=True)
                    break
                else:
                    # Is not last.
                    self.render_subtree(current_node, is_root=False, is_last=False)
                    current_node = next_node

        # Call the hook.
        self.on_node_exit(node, exit_line_prefix)

        # Pop from the stack.
        if not is_root:
            self.indent_prefix_stack.pop()

    def __str__(self):
        return "\n".join(self.output_lines)
