from dataclasses import dataclass
from typing import TypeAlias

Color: TypeAlias = tuple[int, int, int]

@dataclass
class ChessGUIConfig:
	coordinates_width: int = 24
	dimensions: tuple[int, int] = (800, 800)
	square_size: int = 100
	padding: int = 20
	fps: int = 1

	bg_color: Color = (20, 20, 20)
	black_color: Color = (200, 100, 100)
	white_color: Color = (80, 50, 50)
	coordinates_text_color: Color = (0, 0, 0)
	coordinates_bg_color: Color = (150, 150, 150)
	pieces_theme: str = 'neo_wood'

	font_size: int = 14

gui_cfg = ChessGUIConfig()