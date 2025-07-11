from chess_refactored.engine.core import Coordinate
from chess_refactored.engine.piece import Piece, PieceType

class King(Piece):
	from chess_refactored.engine.player import Player
	def __init__(self, player: Player, coordinate: Coordinate) -> None:
		super().__init__(player, coordinate)

	@property
	def piece_type(self) -> PieceType:
		return PieceType.KING

	def attacking_coordinates(self) -> list[Coordinate]:
		"""
		returns the coordinates that the king can attack
		regardless of checks
		"""
		moves: list[Coordinate] = []

		for file_offset in (-1, 0, 1):
			for rank_offset in (-1, 0, 1):
				c: Coordinate | None = self.coordinate.shift(file_offset, rank_offset)
				if not c:
					continue
				# exclude the king's current coordinate
				if c == self.coordinate:
					continue

				moves.append(c)

		return moves

	def all_moves(self) -> list[Coordinate]:
		"""
		returns the moves that the king can choose
		regardless of checks.
		is a subset of attacking squares
		"""

		return super().all_moves()
