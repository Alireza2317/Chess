from __future__ import annotations
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
	def __init__(self, player: Player, coordinate: Coordinate) -> None:
		from chess_refactored.engine.player import Player

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

	def all_moves(self) -> list[Coordinate]:
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

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, Piece):
			raise TypeError(
				f'Cannot compare {self.__class__.__name__} with {type(other)}.'
			)

		same_owner: bool = self.owner == other.owner
		same_type: bool = self.piece_type == other.piece_type
		same_coord: bool = self.coordinate == other.coordinate

		return same_owner and same_type and same_coord