from __future__ import annotations
from chess.engine.core import Coordinate, Direction
from chess.engine.piece import Piece, PieceType
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from chess.engine.player import Player

class Rook(Piece):
	def __init__(self, player: Player, coordinate: Coordinate) -> None:
		super().__init__(player, coordinate)

		self.attack_directions: set[Direction] = {
			Direction(file_offset=1, rank_offset=0), # right
			Direction(file_offset=-1, rank_offset=0), # left
			Direction(file_offset=0, rank_offset=1), # up
			Direction(file_offset=0, rank_offset=-1) # down
		}

		if self.coordinate.file not in ('a', 'h'):
			self.has_moved = True

	@property
	def type(self) -> PieceType:
		return PieceType.ROOK

	def attacking_coordinates(self) -> set[Coordinate]:
		return super().attacking_coordinates()

