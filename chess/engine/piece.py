from __future__ import annotations
import enum
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from chess.engine.core import Color, Coordinate, Direction

if TYPE_CHECKING:
	from chess.engine.player import Player


class PieceType(enum.Enum):
	KING = 'k'
	QUEEN = 'q'
	ROOK = 'r'
	BISHOP = 'b'
	KNIGHT = 'n'
	PAWN = 'p'


class Piece(ABC):
	def __init__(self, player: Player, coordinate: Coordinate) -> None:
		from chess.engine.player import Player

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

		# put the piece on the board if square is not occupied
		if self.owner.board[coordinate].piece:
			raise ValueError(f'There is already a piece on {coordinate}!')
		self.owner.board.place_piece(self, coordinate)

		# add the piece to player's pieces
		self.owner.add_piece(self)

		# piece's legal moves, which will be updated later on
		self.legal_moves: set[Coordinate] = set()

		# piece's attack directions, solely for queen, rook and bishop
		self.attack_directions: set[Direction] = set()

	@property
	@abstractmethod
	def type(self) -> PieceType: ...

	def all_moves(self) -> set[Coordinate]:
		moves: set[Coordinate] = set()

		for c in self.attacking_coordinates():
			piece: Piece | None = self.owner.board[c].piece

			# if it's a piece of our own, cannot move there
			if piece and piece.owner == self.owner:
				continue

			moves.add(c)

		return moves

	@abstractmethod
	def attacking_coordinates(self) -> set[Coordinate]:
		moves: set[Coordinate] = set()

		for direction in self.attack_directions:
			for coordinate in self.coordinate.in_direction(direction):
				piece: Piece | None = self.owner.board[coordinate].piece

				moves.add(coordinate)

				# the range of attack stops, when met a piece in the way
				if piece:
					break
				
		return moves

	def __repr__(self) -> str:
		symbol: str = self.type.value.lower()
		return symbol.upper() if self.owner.color == Color.WHITE else symbol

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, Piece):
			raise TypeError(
				f'Cannot compare {self.__class__.__name__} with {type(other)}.'
			)

		same_owner: bool = self.owner == other.owner
		same_type: bool = self.type == other.type
		same_coord: bool = self.coordinate == other.coordinate

		return same_owner and same_type and same_coord

	def __hash__(self) -> int:
		return hash(f'{self.owner.color.name} {self} {self.coordinate}')