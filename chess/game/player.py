from __future__ import annotations
from chess.components import Color, Board, Piece, Coordinate
from chess.pieces.king import King
from chess.pieces.rook import Rook

class Player:
	def __init__(self, board: Board, color: Color):
		if not isinstance(color, Color):
			raise TypeError(f'color should be of type {type(Color)}!')
		if not isinstance(board, Board):
			raise TypeError(f'board should be of type {type(Board)}!')
		
		self.board = board
		self.color = color
		self.pieces: list[Piece] = []
		self.move: bool = True

	def set_king(self) -> None:
		""" sets up self.king based on self.pieces. """
		k_count = 0
		for piece in self.pieces:
			if isinstance(piece, King):
				self.king = piece
				k_count += 1

		if k_count != 1:
			raise TypeError(
				f'pieces parameter should be a list of Piece objects!'+
				f'and it should have one and only one King object inside.'
			)

	def add_piece(self, piece: Piece) -> None:
		"""	adds the given piece to self.pieces & updates self.king. """
		if not isinstance(piece, Piece):
			raise TypeError(
				f'piece should be of type {type(Piece)}'
			)

		self.pieces.append(piece)
		self.set_king()

	def can_castle(self) -> bool:
		""" Checks wether the player can castle or not. """
		if self.king.has_moved: return False
		if self.is_in_check(): return False

		for p in self.pieces:
			if isinstance(p, Rook):
				if not p.has_moved:
					return True

		# no rooks, or rooks have moved
		return False

	def castle_moves(self) -> list[tuple[Coordinate, Coordinate]] | None:
		"""
		returns a list of one or two available castling moves in the format of:
			a tuple that holds two Coordinate objects,
			first one is the king's new coordinate
			second one is the respective rook's new coordinate
		"""
		if not self.can_castle(): return None

		king_rook_moves_pair: list[tuple[Coordinate, Coordinate]] = []

		for p in self.pieces:
			if isinstance(p, Rook):
				if p.has_moved: continue

				# short castle
				if p.coordinate.file == 'h':
					if self.color == Color.WHITE:
						king_c = Coordinate('g1')
						rook_c = Coordinate('f1')
					else:
						king_c = Coordinate('g8')
						rook_c = Coordinate('f8')

				# long castle
				elif p.coordinate.file == 'a':
					if self.color == Color.WHITE:
						king_c = Coordinate('c1')
						rook_c = Coordinate('d1')
					else:
						king_c = Coordinate('c8')
						rook_c = Coordinate('d8')

				king_rook_moves_pair.append(
						(king_c, rook_c)
					)

		return king_rook_moves_pair

	def is_in_check(self, enemy: Player) -> bool:
		""" returns wether the player is in check or not. """
		if not self.move: return False

		for piece in enemy.pieces:
			if self.king.coordinate in piece.attacking_coordinates():
				return True

		return False

	def is_checkmated(self) -> bool:
		""" returns wether the player is lost or not. """
		return (
			self.move and
			self.is_in_check() and
			not self.king.available_moves()
		)

	def is_stalemate(self) -> bool:
		""" returns wether the game is a stalemate(draw) or not. """
		return (
			self.move and
			not self.is_in_check() and
			not self.king.available_moves()
		)