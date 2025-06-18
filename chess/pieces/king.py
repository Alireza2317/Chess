from chess.components import Piece, Coordinate, Color, Board


class King(Piece):
	def __init__(self, color: Color, board: Board, coordinate: Coordinate):
		super().__init__(color, board, coordinate)

	def attacking_squares(self) -> list[Coordinate]:
		"""
		returns the squares that the king can attack
		regardless of checks
		"""
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
				# exclude the king's current coordinate
				if c.cc == self.coordinate.cc: continue

				moves.append(c)

		return moves

	def available_moves(self) -> list[Coordinate]:
		"""
		returns the moves that the king can choose
		regardless of checks
		is a subset of attacking squares
		"""
		moves: list[Coordinate] = []

		for square in self.attacking_squares():
			# if there is a piece there
			piece: Piece | None = self.board.get(square)

			if piece:
				# check its color
				# if its a piece of our own, can't move there
				if piece.color == self.color: continue

			moves.append(square)

		return moves

	def __repr__(self):
		return 'K' if self.color == Color.WHITE else 'k'

def main():
	board = Board()
	Piece(Color.BLACK, board, Coordinate('h2'))
	Piece(Color.WHITE, board, Coordinate('g1'))
	Piece(Color.BLACK, board, Coordinate('g2'))

	king = King(Color.WHITE, board, Coordinate('h1'))

	print(king.available_moves())

if __name__ == '__main__':
	main()