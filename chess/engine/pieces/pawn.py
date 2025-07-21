from __future__ import annotations
from typing import TYPE_CHECKING
from chess.engine.core import Color, Coordinate, Direction
from chess.engine.piece import Piece, PieceType

if TYPE_CHECKING:
	from chess.engine.player import Player

class Pawn(Piece):
	def __init__(self, player: Player, coordinate: Coordinate) -> None:
		super().__init__(player, coordinate)
		self._start_rank: str = '2' if self.owner.color == Color.WHITE else '7'
		self.en_passant_target_rank: str = (
			'6' if self.owner.color == Color.WHITE else '3'
		)
		self._direction: int = self.owner.color.value

		self.attack_directions: set[Direction] = {
			Direction(file_offset, self._direction)
			for file_offset in (-1, 1)
		}

	@property
	def type(self) -> PieceType:
		return PieceType.PAWN

	def attacking_coordinates(self) -> set[Coordinate]:
		""" returns all squares that are under attack by the pawn. """
		attacks: set[Coordinate] = set()

		for direction in self.attack_directions:
			if (diag := self.coordinate.shift(direction)):
				attacks.add(diag)

		return attacks

	def all_moves(self) -> set[Coordinate]:
		moves: set[Coordinate] = set()

		one_ahead: Coordinate | None = self.coordinate.shift(
			Direction(file_offset=0, rank_offset=self._direction)
		)
		if (
			one_ahead and
			not self.owner.board[one_ahead].piece
	  	):
			moves.add(one_ahead)

			# first move double-step
			if self.coordinate.rank == self._start_rank:
				two_ahead: Coordinate | None = self.coordinate.shift(
					Direction(file_offset=0, rank_offset=2 * self._direction)
				)
				if (
					two_ahead and
					not self.owner.board[two_ahead].piece
				):
					moves.add(two_ahead)

		# add the attacking squares, if there are enemy pieces there
		# this behavior is needed only for pawns
		for move in super().all_moves():
			# since .all_moves() returns only the squares that are
			# empty or occupied by enemy pieces
			if self.owner.board[move].piece:
				moves.add(move)

		return moves


if __name__ == '__main__':
	from chess.engine.core import Coordinate, Color
	from chess.engine.board import Board
	from chess.engine.player import Player

	board = Board()
	player = Player(board=board, color=Color.WHITE)
	p = Pawn(player, Coordinate.from_str('e3'))
	Pawn(player, Coordinate.from_str('d4'))
	board.place_piece(p, p.coordinate)

	print(p.all_moves())
	print(p.attacking_coordinates())
