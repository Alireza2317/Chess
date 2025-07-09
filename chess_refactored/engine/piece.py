import enum
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from chess_refactored.engine.core import Color, Coordinate

if TYPE_CHECKING:
	from chess_refactored.engine.player import Player


class PieceType(enum.Enum):
	KING = 'k'
	QUEEN = 'q'
	ROOK = 'r'
	BISHOP = 'b'
	KNIGHT = 'n'
	PAWN = 'p'


class Piece(ABC):
	from chess_refactored.engine.player import Player
	def __init__(self, player: Player, coordinate: Coordinate) -> None:
		if not isinstance(coordinate, Coordinate):
			raise TypeError(
				f'coordinate should be of type {Coordinate.__name__}!'
			)

		if not isinstance(player, Player):
			raise TypeError(
				f'player should be of type {Player.__name__}!'
			)

		self.owner: Player = player
		self.coordinate: Coordinate = coordinate

		# add the piece to player's pieces
		self.owner.pieces.append(self)
		# put the piece on the board
		self.owner.board.place_piece(self, coordinate)

	@property
	@abstractmethod
	def piece_type(self) -> PieceType: ...

	def legal_moves(self) -> list[Coordinate]:
		moves: list[Coordinate] = []

		for c in self.attacking_coordinates():
			piece: Piece | None = self.owner.board[c].piece

			# if it's a piece of our own, cannot move there
			if piece and piece.owner == self.owner:
				continue

			moves.append(c)

		return moves

	@abstractmethod
	def attacking_coordinates(self) -> list[Coordinate]: ...

	def __repr__(self) -> str:
		symbol: str = self.piece_type.value.lower()
		return symbol.upper() if self.owner.color == Color.WHITE else symbol


