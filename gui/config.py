from dataclasses import dataclass
from typing import TypeAlias

Color: TypeAlias = tuple[int, int, int]

@dataclass
class ChessGUIConfig:
	dimensions: tuple[int, int] = (824, 824)
	square_size: int = 100
	padding: int = 20
	fps: int = 10

	bg_color: Color = (20, 20, 20)
	black_color: Color = (200, 100, 100)
	white_color: Color = (80, 50, 50)
	pieces_theme: str = 'neo_wood'

	font_size: int = 14

gui_cfg = ChessGUIConfig()