from __future__ import annotations
from chess_refactored.engine.core import Color, Coordinate, Board
from chess_refactored.engine.piece import Piece, PieceType


class Player:
	def __init__(self, board: Board, color: Color) -> None:
		self.color = color
		self.board = board
		self.pieces: list[Piece] = []

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

		self.pieces.append(piece)
		self._set_king()

	def remove_piece(self, piece: Piece) -> None:
		if piece is self.king:
			raise ValueError('Cannot remove king from the game!')
		if piece in self.pieces:
			self.pieces.remove(piece)

	def is_in_check(self) -> bool:
		if not self.king:
			return False

		# TODO
		# FIXME
		return False

	def __repr__(self) -> str:
		return f'<{self.color.name.title()} {self.__class__.__name__}>'

def main() -> None:
	b = Board()
	p = Player(b, Color.WHITE)
	print(p.king)


if __name__ == '__main__':
	main()
