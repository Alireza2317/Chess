from dataclasses import dataclass
from typing import TypeAlias

RGBColor: TypeAlias = tuple[int, int, int]

@dataclass
class ChessGUIConfig:
	coordinates_width: int = 24
	dimensions: tuple[int, int] = (800, 800)
	square_size: int = 100
	padding: int = 20
	fps: int = 10

	bg_color: RGBColor = (20, 20, 20)
	#black_color: RGBColor = (200, 100, 100)
	#white_color: RGBColor = (80, 50, 50)
	black_color: RGBColor = (168, 84, 13)
	white_color: RGBColor = (237, 165, 104)
	#valid_color: RGBColor = (75, 212, 84)
	valid_color: RGBColor = (85, 195, 144)
	coordinates_text_color: RGBColor = (0, 0, 0)
	coordinates_bg_color: RGBColor = (150, 150, 150)
	pieces_theme: str = 'neo_wood'

	font_size: int = 20
	coordinates_font_size: int = 14

gui_cfg = ChessGUIConfig()