from __future__ import annotations
from typing import TYPE_CHECKING
from chess.engine.core import Coordinate, Color, Direction
from chess.engine.piece import Piece, PieceType

if TYPE_CHECKING:
	from chess.engine.player import Player


class King(Piece):
	def __init__(self, player: Player, coordinate: Coordinate) -> None:
		super().__init__(player, coordinate)

		self.attack_directions: set[Direction] = {
			Direction(file_offset, rank_offset)
			for file_offset in (-1, 0, 1)
			for rank_offset in (-1, 0, 1)
			if file_offset or rank_offset
		}

		self.has_moved: bool = False
		self.start_rank: str = '1' if self.owner.color == Color.WHITE else '8'

	@property
	def type(self) -> PieceType:
		return PieceType.KING

	def attacking_coordinates(self) -> set[Coordinate]:
		"""
		returns the coordinates that the king can attack
		regardless of checks
		"""
		moves: set[Coordinate] = set()

		for direction in self.attack_directions:
			coord: Coordinate | None = self.coordinate.shift(direction)
			if coord:
				moves.add(coord)

		return moves

	def all_moves(self) -> set[Coordinate]:
		"""
		returns the moves that the king can choose
		regardless of checks.
		is a subset of attacking squares
		"""
		return super().all_moves()
