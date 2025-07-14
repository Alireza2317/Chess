from __future__ import annotations
from chess.engine.core import Coordinate, Direction
from chess.engine.piece import Piece, PieceType
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from chess.engine.player import Player

class Queen(Piece):
	def __init__(self, player: Player, coordinate: Coordinate) -> None:
		super().__init__(player, coordinate)

		self.attack_directions: set[Direction] = {
			Direction(file_offset=0, rank_offset=1), # up
			Direction(file_offset=0, rank_offset=-1), # down
			Direction(file_offset=1, rank_offset=0), # right
			Direction(file_offset=-1, rank_offset=0), # left
			Direction(file_offset=1, rank_offset=1), # up & right
			Direction(file_offset=-1, rank_offset=1), # up & left
			Direction(file_offset=1, rank_offset=-1), # down & right
			Direction(file_offset=-1, rank_offset=-1) # down & left
		}

	@property
	def type(self) -> PieceType:
		return PieceType.QUEEN

	def attacking_coordinates(self) -> set[Coordinate]:
		return super().attacking_coordinates()
