from __future__ import annotations
from chess_refactored.engine.core import Coordinate, Direction
from chess_refactored.engine.piece import Piece, PieceType
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from chess_refactored.engine.player import Player

class Queen(Piece):
	def __init__(self, player: Player, coordinate: Coordinate) -> None:
		super().__init__(player, coordinate)

	@property
	def piece_type(self) -> PieceType:
		return PieceType.QUEEN

	def attacking_coordinates(self) -> set[Coordinate]:
		moves: set[Coordinate] = set()

		directions: tuple[Direction, ...] = (
			Direction(file_offset=0, rank_offset=1), # up
			Direction(file_offset=0, rank_offset=-1), # down
			Direction(file_offset=1, rank_offset=0), # right
			Direction(file_offset=-1, rank_offset=0), # left
			Direction(file_offset=1, rank_offset=1), # up & right
			Direction(file_offset=-1, rank_offset=1), # up & left
			Direction(file_offset=1, rank_offset=-1), # down & right
			Direction(file_offset=-1, rank_offset=-1) # down & left
		)

		for direction in directions:
			moves.update(self.coordinate.in_direction(direction))

		return moves