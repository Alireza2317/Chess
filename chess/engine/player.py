from __future__ import annotations
from chess.engine.core import Color, Coordinate
from chess.engine.board import Board
from chess.engine.piece import Piece, PieceType
from chess.engine.moves.move import Move
from chess.engine.moves.move_simulator import MoveSimulator


def create_move(piece: Piece, to_coord: Coordinate, board: Board) -> Move:
	from_coord: Coordinate = piece.coordinate
	captured_piece: Piece | None = board[to_coord].piece

	# check en passant
	#en_passant: bool = (
	#	piece.piece_type == PieceType.PAWN and
	#	to_coord.file != from_coord.file and # pawn capture
	#	captured_piece is None
	#)

	return Move(
		piece=piece,
		start=from_coord,
		end=to_coord,
		captured=captured_piece,
		promotion=None, # TODO
		en_passant=False, # TODO
		castling=False # TODO
	)

class Player:
	def __init__(self, board: Board, color: Color) -> None:
		self.color = color
		self.board = board
		self.pieces: set[Piece] = set()
		self._set_king()

	def set_opponent(self, player: Player) -> None:
		if not isinstance(player, Player):
			raise TypeError(f'Opponent should be of type {self.__class__.__name__}!')
		self.opponent: Player = player

		# enemy of my enemy is myself!
		self.opponent.opponent = self

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
				move: Move = create_move(piece, target, self.board)

				# simulate move
				with MoveSimulator(self, move):
					if not self.is_in_check():
						legal_moves.add(target)

			piece.legal_moves = legal_moves

		#self.add_castling_moves() # TODO

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

