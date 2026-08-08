class GlyphStyle:
    __slots__ = ("indent_guide", "indent_blank", "branch_mid", "branch_end")

    indent_guide: str
    indent_blank: str
    branch_mid: str
    branch_end: str

    def __init__(
            self,
            indent_guide: str,
            indent_blank: str,
            branch_mid: str,
            branch_end: str,
    ) -> None: ...


STYLE_UNICODE: GlyphStyle
STYLE_UNICODE_INDENT_4: GlyphStyle
STYLE_UNICODE_CMD: GlyphStyle
STYLE_ASCII_CMD: GlyphStyle
STYLE_BLANK_INDENT_4: GlyphStyle
