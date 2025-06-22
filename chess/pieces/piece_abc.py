from abc import ABC, abstractmethod
from enum import Enum
from chess.components import Coordinate
from chess.game.player import Player

class PieceType(Enum):
	KING = 'k'
	QUEEN = 'q'
	ROOK = 'r'
	BISHOP = 'b'
	KNIGHT = 'n'
	PAWN = 'p'


class Piece(ABC):
	def __init__(self, player: Player, coordinate: Coordinate):
		if not isinstance(coordinate, Coordinate):
			raise TypeError(f'coordinate should be of type {type(Coordinate)}!')

		self.board = player.board
		self.color = player.color
		self.coordinate = coordinate
		self.has_moved: bool = False

		# put the piece on the board on init
		self.board.put(self, self.coordinate)
		# add the piece to player's pieces
		player.add_piece(self)

	@abstractmethod
	def attacking_coordinates(self) -> list[Coordinate]:
		pass

	def available_moves(self) -> list[Coordinate]:
		"""
		returns the moves that the piece can choose.
		regardless of checks.
		"""
		moves: list[Coordinate] = []

		for c in self.attacking_coordinates():
			p: Piece | None = self.board.get(c).piece
			if p:
				# if is a piece of our own, cannot move there
				if p.color == self.color: continue

			moves.append(c)

		return moves

	@property
	@abstractmethod
	def piece_type(self) -> PieceType:
		pass
