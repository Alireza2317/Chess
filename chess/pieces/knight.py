from chess.components import Piece, Coordinate, Color, Board, Square


class Knight(Piece):
	def __init__(self, color: Color, board: Board, coordinate: Coordinate):
		super().__init__(color, board, coordinate)

	def attacking_squares(self) -> list[Coordinate]:
		"""
		returns the squares that the knight can attack
		regardless of checks
		"""
		moves: list[Coordinate] = []

		file_ord: int = ord(self.coordinate.file)
		rank_ord: int = ord(self.coordinate.rank)

		possible_moves = [
			chr(file_ord-2) + chr(rank_ord-1),
			chr(file_ord-1) + chr(rank_ord-2),
			chr(file_ord-2) + chr(rank_ord+1),
			chr(file_ord-1) + chr(rank_ord+2),
			chr(file_ord+2) + chr(rank_ord-1),
			chr(file_ord+1) + chr(rank_ord-2),
			chr(file_ord+2) + chr(rank_ord+1),
			chr(file_ord+1) + chr(rank_ord+2)
		]
		for m in possible_moves:
			if Coordinate.is_valid(m):
				moves.append(Coordinate(m))

		return moves

	def available_moves(self) -> list[Coordinate]:
		"""
		returns the moves that the knight can choose
		regardless of checks.
		is a subset of attacking squares
		"""
		moves: list[Coordinate] = []

		for coord in self.attacking_squares():
			square: Square = self.board.get(coord)

			# if there is a piece there
			if square.piece:
				# check its color
				# if its a piece of our own, can't move there
				if square.piece.color == self.color: continue

			moves.append(coord)

		return moves


	def __repr__(self):
		return 'N' if self.color == Color.WHITE else 'n'


def main():
	board = Board()
	Piece(Color.WHITE, board, Coordinate('d2'))
	Piece(Color.WHITE, board, Coordinate('f2'))

	knight = Knight(Color.WHITE, board, Coordinate('e4'))

	print(knight.available_moves())



if __name__ == '__main__':
	main()