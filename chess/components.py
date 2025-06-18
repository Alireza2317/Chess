from __future__ import annotations
from enum import Enum


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


	def __repr__(self):
		return self.cc


class Piece:
	def __init__(self, color: Color, board: Board, coordinate: Coordinate):
		self.color = color
		self.board = board
		self.coordinate = coordinate
		self.has_moved: bool = False

		# put the piece on the board on init
		self.board.put(self, self.coordinate)


class Square:
	def __init__(self, coordinate: Coordinate | str, piece: Piece | None = None):
		if isinstance(coordinate, Coordinate):
			self.coordinate = coordinate
		elif isinstance(coordinate, str):
			self.coordinate = Coordinate(coordinate)
		else:
			raise ValueError('Invalid coordinate!')

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
					Square(f'{file}{rank}', piece=None)
					for file in 'abcdefgh'
				]
			)


	def put(self, piece: Piece | None, coordinate: Coordinate) -> None:
		"""
		takes a chess coordinate and puts the given piece
		in the appropriate square
		"""

		row, col = coordinate.regular

		if self.board[row][col].piece is None:
			self.board[row][col].piece = piece
		else:
			raise ValueError(f'There is already a piece on {coordinate}')

	def remove(self, coordinate: Coordinate) -> None:
		""" removes the piece(if any) from the given coordinate. """
		self.put(None, coordinate)

	def get(self, coordinate: Coordinate) -> Square:
		""" returns the square in the given coordinate. """
		row, col = coordinate.regular
		return self.board[row][col]


def main():
	b = Board()
	print(*b.board, sep='\n')

if __name__ == '__main__':
	main()