from __future__ import annotations
from chess_refactored.engine.core import Coordinate, Direction
from chess_refactored.engine.piece import Piece, PieceType
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from chess_refactored.engine.player import Player

class Knight(Piece):
	def __init__(self, player: Player, coordinate: Coordinate) -> None:
		super().__init__(player, coordinate)

	@property
	def piece_type(self) -> PieceType:
		return PieceType.KNIGHT

	def attacking_coordinates(self) -> set[Coordinate]:
		moves: set[Coordinate] = set()

		for file_offset, rank_offset in ((1, 2), (2, 1)):
			for file_dir, rank_dir in ((1, 1), (1, -1), (-1, -1), (-1, 1)):
				direction: Direction = Direction(
					file_dir * file_offset, rank_dir * rank_offset
				)
				coord: Coordinate | None = self.coordinate.shift(direction)
				if coord:
					moves.add(coord)

		return moves