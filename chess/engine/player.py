from __future__ import annotations
from chess.engine.core import Color, Coordinate
from chess.engine.board import Board
from chess.engine.piece import Piece, PieceType
from chess.engine.moves.move import Move
from chess.engine.moves.simulator import MoveSimulator
from chess.engine.moves.executer import MoveExecuter
from chess.engine.moves.factory import create_move

class Player:
	def __init__(self, board: Board, color: Color) -> None:
		self.color = color
		self.board = board
		self.pieces: set[Piece] = set()
		self.executer: MoveExecuter = MoveExecuter(self)
		self.king: Piece | None = None

	def set_opponent(self, player: Player) -> None:
		if not isinstance(player, Player):
			raise TypeError(f'Opponent should be of type {self.__class__.__name__}!')
		self.opponent: Player = player

		# enemy of my enemy is myself!
		self.opponent.opponent = self

	def add_piece(self, piece: Piece) -> None:
		if piece.owner is not self:
			raise ValueError("Piece's owner is another player! Cannot add!")

		if piece.type == PieceType.KING:
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

	def update_legal_moves(self) -> None:
		"""
		Update each piece's valid_moves list.
		A valid move:
		- Is within the board
		- Does not leave the player in check
		"""
		for piece in self.pieces:
			legal_moves: set[Coordinate] = set()

			for target in piece.all_moves():
				move: Move = create_move(piece, target, simulation=True)

				# simulate move
				with MoveSimulator(self, move):
					if not self.is_in_check():
						legal_moves.add(target)

			piece.legal_moves = legal_moves

		self._add_castling_moves() # TODO

	def _add_castling_moves(self) -> None:
		pass

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

