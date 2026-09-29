class Paint:

    def __init__(self, code, reset="\033[0m"):
        self.code = code
        self.reset = reset

    def __call__(self, content):
        return self.code + content + self.reset


PAINT_OFF = Paint("", "")
