from dataclasses import dataclass
from colorsys import rgb_to_hls
from colorsys import hls_to_rgb
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

def darken_hex_color(hex_color: str, reduction: float = 0.2) -> str:
    """
    Mengurangi kecerahan (lightness) dari warna heksadesimal.
    
    Args:
        hex_color (str): Warna dalam format heksadesimal (misalnya "#RRGGBB").
        reduction (float): Proporsi penurunan kecerahan (default: 0.2, yaitu 20%).
    
    Returns:
        str: Warna hasil yang lebih gelap dalam format heksadesimal.
    """
    # Validasi input
    if not (hex_color.startswith("#") and len(hex_color) == 7):
        raise ValueError("Format warna harus berupa '#RRGGBB'.")
    
    # Konversi warna dari heksadesimal ke nilai RGB
    r = int(hex_color[1:3], 16) / 255.0
    g = int(hex_color[3:5], 16) / 255.0
    b = int(hex_color[5:7], 16) / 255.0

    # Konversi RGB ke HLS
    h, l, s = rgb_to_hls(r, g, b)

    # Kurangi kecerahan (lightness)
    l = max(0, l * (1 - reduction))

    # Konversi kembali dari HLS ke RGB
    r, g, b = hls_to_rgb(h, l, s)

    # Konversi RGB ke heksadesimal
    darkened_hex = "#{:02X}{:02X}{:02X}".format(
        int(r * 255), int(g * 255), int(b * 255)
    )
    
    return darkened_hex
