from chess.engine.core import Coordinate
from chess.gui.renderer import HighlightMode
from chess.game.game import Game

def build_highlight_map(
	game: Game, coords: set[Coordinate]
) -> dict[Coordinate, HighlightMode]:
	result: dict[Coordinate, HighlightMode] = {}

	for coord in coords:
		if game.board[coord].piece:
			result[coord] = HighlightMode.CAPTURE
		else:
			result[coord] = HighlightMode.VALID_MOVE

	return result