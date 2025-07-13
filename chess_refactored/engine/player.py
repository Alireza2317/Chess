from __future__ import annotations
from chess_refactored.engine.core import Color, Board
from chess_refactored.engine.piece import Piece, PieceType


class Player:
	def __init__(self, board: Board, color: Color) -> None:
		self.color = color
		self.board = board
		self.pieces: set[Piece] = set()
		self._set_king()

	def _set_king(self) -> None:
		self.king: Piece | None = None

		king_count: int = 0
		for piece in self.pieces:
			if piece.piece_type == PieceType.KING:
				self.king = piece
				king_count += 1
		if king_count > 1:
			raise ValueError('Player cannot have more than 1 king piece!')

	def add_piece(self, piece: Piece) -> None:
		if piece.owner is not self:
			raise ValueError("Piece's owner is another player! Cannot add!")

		self.pieces.add(piece)
		self._set_king()

	def remove_piece(self, piece: Piece) -> None:
		if piece is self.king:
			raise ValueError('Cannot remove king from the game!')

		self.pieces.remove(piece) #? or discard

		#? also remove it from the board
		self.board.remove_piece(piece.coordinate)

	def is_in_check(self) -> bool:
		if not self.king:
			return False

		for square in self.board.all_squares():
			piece: Piece | None = square.piece
			if piece and piece.owner is not self:
				if self.king.coordinate in piece.attacking_coordinates():
					return True

		return False

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, Player):
			raise TypeError(
				f'Cannot compare {self.__class__.__name__} with {type(other)}'
			)

		return (self is other)

	def __repr__(self) -> str:
		return f'<{self.color.name.title()} {self.__class__.__name__}>'

