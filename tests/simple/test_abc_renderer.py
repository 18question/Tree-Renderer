from tree_renderer.simple.abc_renderer import ABCTreeRenderer


class SimpleTree:

    def __init__(self, name, children):
        self.name = name
        self.children = children


class SimpleTreeRenderer(ABCTreeRenderer):

    def get_children(self, node):
        return node.children

    def on_node_enter(self, node, line_prefix):
        self.output_lines.append(line_prefix + node.name)

    def on_node_exit(self, node, line_prefix):
        pass


def render(root_node):
    tree_renderer = SimpleTreeRenderer()
    tree_renderer.render_tree(root_node)
    return tree_renderer


def test_single_root():
    simple_tree = SimpleTree("Root", ())
    assert str(render(simple_tree)) == "Root"


def test_one_level():
    simple_tree = SimpleTree(
        "Root", (
            SimpleTree("A", ()),
            SimpleTree("B", ()),
        ),
    )
    assert str(render(simple_tree)) == "\n".join(
        (
            "Root",
            "├─ A",
            "└─ B",
        ),
    )


def test_nested():
    simple_tree = SimpleTree(
        "Root", (
            SimpleTree(
                "A", (
                    SimpleTree("A1", ()),
                ),
            ),
            SimpleTree(
                "B", (
                    SimpleTree("B1", ()),
                ),
            ),
        ),
    )
    assert str(render(simple_tree)) == "\n".join(
        (
            "Root",
            "├─ A",
            "│   └─ A1",
            "└─ B",
            "    └─ B1",
        ),
    )
