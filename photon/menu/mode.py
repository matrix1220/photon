
from enum import Enum

class Mode(Enum):
    inline = 1
    outline = 2

class Inline:
    mode = Mode.inline

class Outline:
    mode = Mode.outline

# print(Outline.mode)