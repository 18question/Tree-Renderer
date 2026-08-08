class GlyphStyle:
    __slots__ = ("indent_guide", "indent_blank", "branch_mid", "branch_end")

    def __init__(self, indent_guide, indent_blank, branch_mid, branch_end):
        self.indent_guide = indent_guide
        self.indent_blank = indent_blank
        self.branch_mid = branch_mid
        self.branch_end = branch_end


STYLE_UNICODE = GlyphStyle(
    indent_guide="│   ",
    indent_blank="    ",
    branch_mid="├─ ",
    branch_end="└─ ",
)
STYLE_UNICODE_INDENT_4 = GlyphStyle(
    indent_guide="│   ",
    indent_blank="    ",
    branch_mid="├── ",
    branch_end="└── ",
)
STYLE_UNICODE_CMD = GlyphStyle(
    indent_guide="│  ",
    indent_blank="    ",
    branch_mid="├─",
    branch_end="└─",
)
STYLE_ASCII_CMD = GlyphStyle(
    indent_guide="|   ",
    indent_blank="    ",
    branch_mid="+---",
    branch_end=r"\---",
)
STYLE_BLANK_INDENT_4 = GlyphStyle(
    indent_guide="    ",
    indent_blank="    ",
    branch_mid="    ",
    branch_end="    ",
)
