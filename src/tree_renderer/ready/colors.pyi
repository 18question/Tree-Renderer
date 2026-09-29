class Paint:
    code: str
    reset: str

    def __init__(self, code: str, reset: str = ...) -> None: ...

    def __call__(self, content: str) -> str: ...


PAINT_OFF: Paint
