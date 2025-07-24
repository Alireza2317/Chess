from dataclasses import dataclass
from typing import TypeAlias

RGBColor: TypeAlias = tuple[int, int, int] | tuple[int, int, int, int]

@dataclass(frozen=True)
class ChessGUIConfig:
	square_size: int = 100
	coordinates_width: int = square_size//4
	dimensions: tuple[int, int] = (8*square_size, 8*square_size)
	padding: int = 20
	fps: int = 60
	anim_duration: float = .18 # second
	animation: bool = True

	bg_color: RGBColor = (20, 20, 20)

	black_color: RGBColor = (168, 84, 13)
	white_color: RGBColor = (237, 165, 104)

	valid_color: RGBColor = (90, 90, 90, 130)
	selected_piece_color: RGBColor = (80, 80, 100, 130)
	in_check_color: RGBColor = (240, 51, 73, 50)

	coordinates_text_color: RGBColor = (0, 0, 0)
	coordinates_bg_color: RGBColor = (150, 150, 150)

	pieces_theme: str = 'neo_wood'

	font_size: int = 20
	coordinates_font_size: int = 14

cfg: ChessGUIConfig = ChessGUIConfig()