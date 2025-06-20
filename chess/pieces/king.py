from chess.components import Piece, Coordinate, Color, Board, Square


class King(Piece):
	def __init__(self, color: Color, board: Board, coordinate: Coordinate):
		super().__init__(color, board, coordinate)

	def attacking_coordinates(self) -> list[Coordinate]:
		"""
		returns the coordinates that the king can attack
		regardless of checks
		"""
		moves: list[Coordinate] = []

		file_ord: int = ord(self.coordinate.file)
		rank_ord: int = ord(self.coordinate.rank)

		possible_moves = []
		for file_code in range(file_ord-1, file_ord+2):
			for rank_s in range(rank_ord-1, rank_ord+2):
				file: str = chr(file_code)
				rank: str = chr(rank_s)
				# exclude the king's current coordinate
				if f'{file}{rank}' == self.coordinate.cc: continue

				possible_moves.append(f'{file}{rank}')

		for m in possible_moves:
			if Coordinate.is_valid(m):
				moves.append(Coordinate(m))

		return moves

	def available_moves(self) -> list[Coordinate]:
		"""
		returns the moves that the king can choose
		regardless of checks.
		is a subset of attacking squares
		"""

		return super().available_moves(self.attacking_coordinates())

	def __repr__(self):
		return 'K' if self.color == Color.WHITE else 'k'

def main():
	board = Board()
	Piece(Color.WHITE, board, Coordinate('e3'))
	Piece(Color.WHITE, board, Coordinate('e5'))
	Piece(Color.WHITE, board, Coordinate('d3'))
	Piece(Color.WHITE, board, Coordinate('d4'))
	Piece(Color.WHITE, board, Coordinate('d5'))
	Piece(Color.WHITE, board, Coordinate('f3'))
	Piece(Color.WHITE, board, Coordinate('f4'))
	Piece(Color.WHITE, board, Coordinate('f5'))

	king = King(Color.BLACK, board, Coordinate('e4'))

	print(king.available_moves())

if __name__ == '__main__':
	main()