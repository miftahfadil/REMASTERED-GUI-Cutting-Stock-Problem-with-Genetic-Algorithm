from dataclasses import dataclass

from typing import Tuple


@dataclass
class Colors:
    black: str = "#0d1914"
    white: str = "#fbfbff"

    green1: str = "#6d9773"
    green2: str = "#0c3a2d"
    yellow1: str = "#ffb902"
    yellow2: str = "#bb8a52"

    red: str = '#ef233c'

@dataclass
class Fonts:
    TYPE_FACE: str = "Helvetica"

    h1: Tuple[str|int] = (TYPE_FACE, 18, 'bold')
    h2: Tuple[str|int] = (TYPE_FACE, 16, 'bold')
    h3: Tuple[str|int] = (TYPE_FACE, 12, 'bold')
    h4: Tuple[str|int] = (TYPE_FACE, 10, 'bold')
    h5: Tuple[str|int] = (TYPE_FACE, 8, 'bold')

    p1: Tuple[str|int] = (TYPE_FACE, 12)
    p2: Tuple[str|int] = (TYPE_FACE, 10)
    p3: Tuple[str|int] = (TYPE_FACE, 8)