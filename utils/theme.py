from dataclasses import dataclass

from typing import Tuple


@dataclass
class Colors:
    black: str = ""
    white: str = ""

    green1: str = ""
    green2: str = ""
    yellow1: str = ""
    yellow2: str = ""

@dataclass
class Fonts:
    TYPE_FACE: str = "Helvetica"

    h1: Tuple[str|int] = (TYPE_FACE, 16, 'Bold')