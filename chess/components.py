from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import enum
from chess.utils import colored_str

if TYPE_CHECKING:
	from chess.game.player import Player


class PieceType(enum.Enum):
	KING = 'k'
	QUEEN = 'q'
	ROOK = 'r'
	BISHOP = 'b'
	KNIGHT = 'n'
	PAWN = 'p'


class Color(enum.Enum):
	WHITE = 0
	BLACK = -1

	def __invert__(self):
		return self.__class__(~self.value)

class Coordinate:
	def __init__(self, coordinate: str):
		if not self.is_valid(coordinate):
			raise ValueError('Invalid chess coordinate.')

		self.file: str = coordinate[0].lower()
		self.rank: str = coordinate[1]

	@staticmethod
	def is_valid(coordinate: str) -> bool:
		if not isinstance(coordinate, str):
			raise ValueError('coordinate should be a str!')
		return (
			len(coordinate) == 2 and
			(coordinate[0] in 'abcdefgh') and
			(coordinate[1] in '12345678')
		)

	@property
	def regular(self) -> tuple[int, int]:
		""" 
		converts chess coordinates like 'a1' 
		to regular matrix coordinates.
		"""
		row: int = '12345678'.index(self.rank)
		col: int = 'abcdefgh'.index(self.file)

		return row, col

	def __eq__(self, other: object):
		if not isinstance(other, Coordinate):
			raise NotImplementedError(
				f'Cannot check equality between ' +
				f'{self.__class__.__name__} and {type(other)}!'
			)

		return repr(self) == repr(other)

	def __ne__(self, other: object):
		return not self.__eq__(other)

	def __repr__(self):
		return f'<{self.file}{self.rank}>'


class Piece(ABC):
	def __init__(self, player: Player, coordinate: Coordinate):
		if not isinstance(coordinate, Coordinate):
			raise TypeError(
				f'coordinate should be of type {Coordinate.__name__}!'
			)
		self.player = player
		self.board = player.board
		self.color = player.color
		self.coordinate = coordinate
		self.valid_moves: list[Coordinate]
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

	def __eq__(self, other: object):
		if other is None: return False
		if not isinstance(other, Piece):
			raise NotImplementedError(
				f'cannot compare {self.__class__.__name__} with {type(other)}!'
			)

		same_color: bool = (self.color == other.color)
		same_type: bool = (self.piece_type == other.piece_type)
		same_coordinate: bool = (self.coordinate == other.coordinate)
		return same_color and same_type and same_coordinate

	def __ne__(self, other: object):
		return not self.__eq__(other)


class Square:
	def __init__(self, coordinate: Coordinate, piece: Piece | None = None):
		if not isinstance(coordinate, Coordinate):
			raise TypeError(
				f'Invalid coordinate! should be of type {Coordinate.__name__}'
			)
		if not isinstance(piece, (Piece, type(None))):
			raise TypeError(
				f'Invalid piece! should be a Piece object, or None.'
			)

		self.coordinate = coordinate
		self.piece: Piece | None = piece

		# set the color based on the coordinate
		self.set_color()

	def set_color(self):
		if (
			(self.coordinate.file in 'aceg' and int(self.coordinate.rank)%2 == 1)
			or
			self.coordinate.file in 'bdfh' and int(self.coordinate.rank)%2 == 0
		):
			self.color = Color.BLACK
		else:
			self.color = Color.WHITE

	def __eq__(self, other: object):
		if not isinstance(other, Square):
			raise NotImplementedError(
				f'cannot compare {self.__class__.__name__} with {type(other)}!'
			)

		same_coordinate: bool = (self.coordinate == other.coordinate)
		same_piece: bool = (self.piece == other.piece)
		return same_coordinate and same_piece

	def __ne__(self, other: object):
		return not self.__eq__(other)

	def __repr__(self):
		return f'{self.__class__.__name__}({self.coordinate}, {self.piece})'


class Board:
	def __init__(self) -> None:
		# the arrangement of these lists is such that the first row is
		# equivalent to the rank 1, from a to h
		# and the last row is the rank 8
		self.board_matrix: list[list[Square]] = []

		for rank in '12345678':
			self.board_matrix.append(
				[
					Square(Coordinate(f'{file}{rank}'), piece=None)
					for file in 'abcdefgh'
				]
			)

	def put(self, piece: Piece, coordinate: Coordinate) -> None:
		"""
		takes a chess coordinate and puts the given piece
		in the appropriate square
		"""
		row, col = coordinate.regular
		self.board_matrix[row][col].piece = piece
		piece.coordinate = coordinate

	def remove(self, coordinate: Coordinate) -> None:
		""" removes the piece(if any) from the given coordinate. """
		row, col = coordinate.regular
		self.board_matrix[row][col].piece = None

	def move(self, piece: Piece, coordinate: Coordinate) -> None:
		"""
		puts the piece in given coordinate and
		removes it from its original coordinate
		"""
		self.remove(piece.coordinate)
		self.put(piece, coordinate)
		piece.has_moved = True

	def get(self, coordinate: Coordinate) -> Square:
		""" returns the square in the given coordinate. """
		row, col = coordinate.regular
		return self.board_matrix[row][col]

	def get_coordinates(
		self,
		current_coordinate: Coordinate,
		direction: tuple[int, int]) -> list[Coordinate]:
		"""
		returns all coordinates in the given direction
		stops when exits board or reaches a piece of any color(inclusive).
		direction is a tuple of 2 numbers, it contains a direction-like vector
		that corresponds to (file_direction, rank_direction)
		like (0, 1), which means going up
		"""

		file_ord = ord(current_coordinate.file)
		rank_ord = ord(current_coordinate.rank)

		coords: list[Coordinate] = []

		for i in range(1, 8):
			f_dir, r_dir = direction
			new_file = chr(file_ord + i*f_dir)
			new_rank = chr(rank_ord + i*r_dir)

			m = f'{new_file}{new_rank}'

			if not Coordinate.is_valid(m): return coords

			c = Coordinate(m)
			coords.append(c)

			# if reached a piece, the range of attack stops
			if self.get(c).piece: return coords

		return coords

	def __repr__(self) -> str:
		s: str = ''
		for row in reversed(self.board_matrix):
			for sq in row:
				if sq.piece:
					if sq.piece.color == Color.WHITE:
						s += colored_str(f'{sq.piece}', 'b')
					elif sq.piece.color == Color.BLACK:
						s += colored_str(f'{sq.piece}', 'y')
				else:
					if sq.color == Color.WHITE:
						s += '□'
					else:
						s += '■'
				s += '  '
			s += f'{colored_str(sq.coordinate.rank, color="g")}\n'

		s += colored_str('  '.join('abcdefgh'), 'g')

		return s


def main():
	pass

if __name__ == '__main__':
	main()