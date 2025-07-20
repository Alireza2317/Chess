from __future__ import annotations
from chess.engine.core import Color
from chess.engine.board import Board
from chess.engine.piece import Piece
from chess.engine.pieces.king import King
from chess.engine.pieces.rook import Rook
from chess.engine.castle import CastleSide, CastleInfo
from chess.engine.moves.executer import MoveExecuter


class Player:
	def __init__(self, board: Board, color: Color) -> None:
		self.color = color
		self.board = board
		self.pieces: set[Piece] = set()
		self.executer: MoveExecuter = MoveExecuter(self)
		self.king: King | None = None
		self.castle_info: CastleInfo = CastleInfo(self.color)

	def set_opponent(self, player: Player) -> None:
		if not isinstance(player, Player):
			raise TypeError(f'Opponent should be of type {self.__class__.__name__}!')
		self.opponent: Player = player

		# enemy of my enemy is myself!
		self.opponent.opponent = self

	def add_piece(self, piece: Piece) -> None:
		if piece.owner is not self:
			raise ValueError("Piece's owner is another player! Cannot add!")

		if isinstance(piece, King):
			if self.king:
				raise ValueError('Player cannot have more than 1 king piece!')
			self.king = piece

		self.pieces.add(piece)

		# also put the piece on the board
		if self.board[piece.coordinate].piece:
			# square is occupied
			raise ValueError(f'There is already a piece on {piece.coordinate}!')

		self.board.place_piece(piece, piece.coordinate)

	def remove_piece(self, piece: Piece) -> None:
		if piece is self.king:
			raise ValueError('Cannot remove king from the game!')

		if piece not in self.pieces:
			raise KeyError(
				f'{self} has no {piece} on {piece.coordinate}! Abort piece removal.'
		 	)

		self.pieces.remove(piece)

		# also remove it from the board
		self.board.remove_piece(piece.coordinate)

	def _can_castle(self, rook: Piece | None, side: CastleSide) -> bool:
		"""Checks wether the player has a legal castle move or not."""
		if not self.king or self.king.has_moved or self.is_in_check():
			return False

		# is it really a rook?
		if not isinstance(rook, Rook):
			return False

		# is the rook ours? has it moved?
		if rook.owner != self or rook.has_moved:
			return False

		self.castle_info.update_info(side)

		if self.king.coordinate.rank != self.castle_info.rank:
			return False

		if rook.coordinate != self.castle_info.rook_start:
			return False

		# check if all squares between king and rook are empty
		if self.king.coordinate not in rook.attacking_coordinates():
			# rook cannot see the king
			return False

		# check opponent attacks on the squares that the king needs to pass
		for coord in self.castle_info.king_path:
			for op_piece in self.opponent.pieces:
				if coord in op_piece.attacking_coordinates():
					return False

		return True

	def _add_castling_moves(self) -> None:
		if not self.king or self.king.has_moved or self.is_in_check():
			return

		for side in (CastleSide.KINGSIDE, CastleSide.QUEENSIDE):
			self.castle_info.update_info(side)
			rook: Piece | None = self.board[self.castle_info.rook_start].piece

			if self._can_castle(rook, side):
				self.king.legal_moves.add(self.castle_info.king_end)

	def has_legal_moves(self) -> bool:
		for piece in self.pieces:
			if piece.legal_moves:
				return True

		return False

	def is_in_check(self) -> bool:
		if not self.king:
			return False

		for opponent_piece in self.opponent.pieces:
			if self.king.coordinate in opponent_piece.attacking_coordinates():
				return True
		return False

	def is_checkmated(self) -> bool:
		if not self.king:
			return False

		return self.is_in_check() and not self.has_legal_moves()

	def is_stalemeted(self) -> bool:
		return not self.is_in_check() and not self.has_legal_moves()

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, Player):
			raise TypeError(
				f'Cannot compare {self.__class__.__name__} with {type(other)}'
			)

		return (self is other)

	def __repr__(self) -> str:
		return f'<{self.color.name.title()} {self.__class__.__name__}>'

