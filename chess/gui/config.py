from dataclasses import dataclass
from typing import TypeAlias

RGBColor: TypeAlias = tuple[int, int, int] | tuple[int, int, int, int]

@dataclass(frozen=True)
class ChessGUIConfig:
	square_size: int = 100
	coordinates_width: int = square_size//4
	screen_dims: tuple[int, int] = (11*square_size, 9*square_size)
	board_dims: tuple[int, int] = (8*square_size, 8*square_size)
	padding: int = 20
	fps: int = 60
	anim_duration: float = .18 # second
	animation: bool = True

	bg_color: RGBColor = (40, 40, 40)

	black_color: RGBColor = (168, 84, 13)
	white_color: RGBColor = (237, 165, 104)

	valid_color: RGBColor = (90, 90, 90, 130)
	selected_piece_color: RGBColor = (80, 80, 100, 130)
	in_check_color: RGBColor = (240, 51, 73, 150)

	coordinates_text_color: RGBColor = (0, 0, 0)
	coordinates_bg_color: RGBColor = (150, 150, 150)

	popup_color: RGBColor = (115, 115, 115)

	highlight_capture_radius: float = square_size*0.49
	highlight_move_radius: float = square_size*0.135

	pieces_theme: str = 'neo_wood'

	font_size: int = 20
	small_font_size: int = 16

cfg: ChessGUIConfig = ChessGUIConfig()