from chess_refactored.engine.core import Color, Coordinate
from chess_refactored.engine.piece import Piece, PieceType

from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from chess_refactored.engine.player import Player

class Pawn(Piece):
	def __init__(self, player: Player, coordinate: Coordinate) -> None:
		super().__init__(player, coordinate)
		self._start_rank: str = '2' if self.owner.color == Color.WHITE else '7'
		self._direction: int = self.owner.color.value

	@property
	def piece_type(self) -> PieceType:
		return PieceType.PAWN

	def legal_moves(self) -> list[Coordinate]:
		moves: list[Coordinate] = []

		one_ahead: Coordinate | None = self.coordinate.shift(0, self._direction)
		if (
			one_ahead and
			not self.owner.board[one_ahead].piece
	  	):
			moves.append(one_ahead)

			# first move double-step
			if self.coordinate.rank == self._start_rank:
				two_ahead: Coordinate | None = self.coordinate.shift(0, 2*self._direction)
				if (
					two_ahead and
					not self.owner.board[two_ahead].piece
				):
					moves.append(two_ahead)

		# add the attacking squares
		moves.extend(super().legal_moves())

		return moves

	def attacking_squares(self) -> list[Coordinate]:
		""" returns all squares that are under attack by the pawn. """
		attacks: list[Coordinate] = []

		for file_offset in (-1, 1):
			if (diag := self.coordinate.shift(file_offset, self._direction)):
				attacks.append(diag)

		return attacks
