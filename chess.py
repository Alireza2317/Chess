from __future__ import annotations
from enum import Enum


class Side(Enum):
	WHITE = 'w'
	BLACK = 'b'


class Coordinate:
	def __init__(self, coordinate: str):
		file: str = str(coordinate[0]).lower()
		rank: str = str(coordinate[1])

		if (len(coordinate) != 2) or (file not in 'abcdefgh') or (rank not in '12345678'):
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
	def __init__(self, side: Side, board: Board, coordinate: Coordinate):
		self.side = side
		self.board = board
		self.coordinate = coordinate
		self.has_moved: bool = False

		# put the piece on the board on init
		self.board.put(self, self.coordinate)


class King(Piece):
	def __init__(self, side, board, coordinate):
		super().__init__(side, board, coordinate)

	def available_moves(self) -> list[Coordinate]:
		moves: list[Coordinate] = []

		file_ord: int = ord(self.coordinate.file)
		for file_code in range(file_ord-1, file_ord+2):
			file: str = chr(file_code)
			if file not in 'abcdefgh': continue

			rank_ord: int = ord(self.coordinate.rank)
			for rank_s in range(rank_ord-1, rank_ord+2):
				rank: str = chr(rank_s)
				if rank not in '12345678': continue

				c = Coordinate(f'{file}{rank}')

				# if there is a piece there
				piece: Piece | None = self.board.get(c)
				if piece:
					# check its side
					# if its a piece of our own, can't move there
					if piece.side == self.side: continue

				moves.append(c)

		return moves


class Queen(Piece):
	def __init__(self, side, board, coordinate):
		super().__init__(side, board, coordinate)

	def available_moves(self) -> list[Coordinate]:
		pass


class Rook(Piece):
	def __init__(self, side, board, coordinate):
		super().__init__(side, board, coordinate)

	def available_moves(self) -> list[Coordinate]:
		pass


class Bishop(Piece):
	def __init__(self, side, board, coordinate):
		super().__init__(side, board, coordinate)

	def available_moves(self) -> list[Coordinate]:
		pass


class Knight(Piece):
	def __init__(self, side, board, coordinate):
		super().__init__(side, board, coordinate)

	def available_moves(self) -> list[Coordinate]:
		pass


class Pawn(Piece):
	def __init__(self, side, board, coordinate):
		super().__init__(side, board, coordinate)

	def available_moves(self) -> list[Coordinate]:
		pass



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


def main():
	board = Board()
	Piece(Side.BLACK, board, Coordinate('h2'))
	Piece(Side.WHITE, board, Coordinate('g1'))
	Piece(Side.BLACK, board, Coordinate('g2'))

	king = King(Side.WHITE, board, Coordinate('h1'))

	print(king.available_moves())

if __name__ == '__main__':
	main()