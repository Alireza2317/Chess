from chess.components import Piece, Coordinate, Color, Board
from chess.pieces.pawn import Pawn

class Rook(Piece):
	def __init__(self, color: Color, board: Board, coordinate: Coordinate):
		super().__init__(color, board, coordinate)

	def attacking_coordinates(self) -> list[Coordinate]:
		"""
		returns all coordinates that are under the attack of the rook.
		"""
		moves: list[Coordinate] = []

		file_ord = ord(self.coordinate.file)
		rank_ord = ord(self.coordinate.rank)

		# going up or down
		for new_rank_ord in range(rank_ord+1, rank_ord+8):
			m = f'{chr(file_ord)}{chr(new_rank_ord)}'
			if not Coordinate.is_valid(m): break

			c = Coordinate(m)
			moves.append(c)

			# if reached a piece, the range of attack stops
			if self.board.get(c).piece: break

		# going up or down, opposite direction
		for new_rank_ord in range(rank_ord-1, rank_ord-8, -1):
			m = f'{chr(file_ord)}{chr(new_rank_ord)}'
			if not Coordinate.is_valid(m): break

			c = Coordinate(m)
			moves.append(c)

			# if reached a piece, the range of attack stops
			if self.board.get(c).piece: break

		# going right or left
		for new_file_ord in range(file_ord+1, file_ord+8):
			m = f'{chr(new_file_ord)}{chr(rank_ord)}'
			if not Coordinate.is_valid(m): break

			c = Coordinate(m)
			moves.append(c)

			# if reached a piece, the range of attack stops
			if self.board.get(c).piece: break

		# going right or left, opposite direction
		for new_file_ord in range(file_ord-1, file_ord-8, -1):
			m = f'{chr(new_file_ord)}{chr(rank_ord)}'
			if not Coordinate.is_valid(m): break

			c = Coordinate(m)
			moves.append(c)

			# if reached a piece, the range of attack stops
			if self.board.get(c).piece: break

		return moves

	def available_moves(self) -> list[Coordinate]:
		"""
		returns the moves that the rook can choose.
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

	def __repr__(self):
		return 'R' if self.color == Color.WHITE else 'r'

def main():
	b = Board()

	rook = Rook(Color.WHITE, b, Coordinate('e4'))
	#Pawn(Color.WHITE, b, Coordinate('g3'))
	Pawn(Color.BLACK, b, Coordinate('e7'))
	Pawn(Color.WHITE, b, Coordinate('h4'))
	#Pawn(Color.WHITE, b, Coordinate('h2'))

	print(b)
	print(rook.attacking_coordinates())
	print(rook.available_moves())

if __name__ == '__main__':
	main()