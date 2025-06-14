from typing import TypeAlias
from enum import Enum

class Player(Enum):
	WHITE = 'w'
	BLACK = 'b'



class King:
	def __init__(self, side: Player, board):
		self.side = side


class Queen:
	def __init__(self, side: Player):
		self.side = side

class Rook:
	def __init__(self, side: Player):
		self.side = side

class Bishop:
	def __init__(self, side: Player):
		self.side = side

class Knight:
	def __init__(self, side: Player):
		self.side = side

class Pawn:
	def __init__(self, side: Player):
		self.side = side



Piece: TypeAlias = King | Queen | Rook | Bishop | Knight | Pawn


class Coordinate:
	def __init__(self, coordinate: str):
		file: str = str(coordinate[0]).lower()
		rank: str = str(coordinate[1])

		if (len(coordinate) != 2) or (file not in 'abcdefgh') or (rank not in '12345678'):
			raise ValueError('Invalid chess coordinate!')


		self.file: str = file
		self.rank: str = rank


	@property
	def regular(self) -> tuple[int, int]:
		""" converts chess coordinates like 'a1' to regular matrix coordinates. """

		row: int = int(self.rank) - 1
		col: int = 'abcdefgh'.index(self.file)

		return row, col


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

		self.board[row][col] = piece


	def remove(self, chess_coordinate: Coordinate) -> None:
		""" removes the piece(if any) from the given coordinate. """
		self.put(None, chess_coordinate)



def main():
	print(Coordinate('g7').regular)

if __name__ == '__main__':
	main()