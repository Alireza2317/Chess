from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from enum import Enum
from chess.utils import colored_str

if TYPE_CHECKING:
	from chess.game.player import Player


class PieceType(Enum):
	KING = 'k'
	QUEEN = 'q'
	ROOK = 'r'
	BISHOP = 'b'
	KNIGHT = 'n'
	PAWN = 'p'


class Color(Enum):
	WHITE = 'w'
	BLACK = 'b'


class Coordinate:
	def __init__(self, coordinate: str):
		file: str = str(coordinate[0]).lower()
		rank: str = str(coordinate[1])

		if (
			(len(coordinate) != 2) or
			(file not in 'abcdefgh') or
			(rank not in '12345678')
		):
			raise ValueError('Invalid chess coordinate!')


		self.file: str = file
		self.rank: str = rank

		# cc: chess coordinate
		self.cc: str = coordinate

	@property
	def regular(self) -> tuple[int, int]:
		""" converts chess coordinates like 'a1' to regular matrix coordinates. """

		row: int = int(self.rank) - 1
		col: int = 'abcdefgh'.index(self.file)

		return row, col

	@staticmethod
	def is_valid(coordinate: str) -> bool:
		return (coordinate[0] in 'abcdefgh') and (coordinate[1] in '12345678')

	def __eq__(self, other: Coordinate):
		print(other, type(other))
		if not isinstance(other, Coordinate):
			raise TypeError(
				f'Cannot check equality between ' +
				f'{Coordinate.__name__} and {type(other)}!'
			)

		return (self.file == other.file) and (self.rank == other.rank)

	def __ne__(self, other: Coordinate):
		if not isinstance(other, Coordinate):
			raise TypeError(
				f'Cannot check equality between ' +
				f'{Coordinate.__name__} and {type(other)}!'
			)

		return (self.file != other.file) or (self.rank != other.rank)

	def __repr__(self):
		return self.cc


class Piece(ABC):
	def __init__(self, player: Player, coordinate: Coordinate):
		if not isinstance(coordinate, Coordinate):
			raise TypeError(
				f'coordinate should be of type {Coordinate.__name__}!'
			)

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

	def __repr__(self):
		return str(self.piece)


class Board:
	def __init__(self):
		# the arrangement of these lists is such that the first row is
		# equivalent to the rank 1, from a to h
		# and the last row is the rank 8
		self.board: list[list[Square]] = []

		for rank in '12345678':
			self.board.append(
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

		if self.board[row][col].piece is None:
			self.board[row][col].piece = piece
			piece.coordinate = coordinate
		else:
			raise ValueError(f'There is already a piece on {coordinate}')

	def remove(self, coordinate: Coordinate) -> None:
		""" removes the piece(if any) from the given coordinate. """
		row, col = coordinate.regular
		self.board[row][col].piece = None

	def move(self, piece: Piece, coordinate: Coordinate) -> None:
		"""
		puts the piece in given coordinate and
		removes it from its original coordinate
		"""
		self.board.remove(piece.coordinate)
		self.board.put(piece, coordinate)

	def get(self, coordinate: Coordinate) -> Square:
		""" returns the square in the given coordinate. """
		row, col = coordinate.regular
		return self.board[row][col]

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
			new_file = chr(file_ord + i*direction[0])
			new_rank = chr(rank_ord + i*direction[1])

			m = f'{new_file}{new_rank}'

			if not Coordinate.is_valid(m): return coords

			c = Coordinate(m)
			coords.append(c)

			# if reached a piece, the range of attack stops
			if self.get(c).piece: return coords

		return coords

	def __repr__(self):
		s: str = ''
		for row in reversed(self.board):
			for sq in row:
				if sq.piece:
					s += f'{sq.piece}'
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