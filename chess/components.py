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


class Board:
	def __init__(self):
		# the arrangement of these lists is such that the first row is
		# equivalent to the rank 1, from a to h
		# and the last row is the rank 8
		self.board: list[list[Piece | None]] = [
			[None for _ in range(8)]
			for _ in range(8)
		]

	def put(self, piece: Piece | None, chess_coordinate: Coordinate) -> None:
		"""
		takes a chess coordinate and puts the given piece
		in the appropriate location
		"""

		row, col = chess_coordinate.regular

		if self.board[row][col] is None:
			self.board[row][col] = piece
		else:
			raise ValueError(f'There is already a piece on {chess_coordinate}')

	def remove(self, chess_coordinate: Coordinate) -> None:
		""" removes the piece(if any) from the given coordinate. """
		self.put(None, chess_coordinate)

	def get(self, chess_coordinate: Coordinate) -> Piece | None:
		""" returns the piece in the given coordinate. """
		row, col = chess_coordinate.regular
		return self.board[row][col]


