from chess_refactored.engine.core import Color, Coordinate, Board
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from chess_refactored.engine.piece import Piece

class Player:
	def __init__(self) -> None:
		self.pieces: list[Piece] = []
		self.color = Color.WHITE
		self.board = Board()