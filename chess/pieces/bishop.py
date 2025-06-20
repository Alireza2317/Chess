from chess.components import Piece, Coordinate, Color, Board
from chess.pieces.pawn import Pawn

class Bishop(Piece):
	def __init__(self, color: Color, board: Board, coordinate: Coordinate):
		super().__init__(color, board, coordinate)

	def attacking_coordinates(self) -> list[Coordinate]:
		"""
		returns all coordinates that are under the attack of the bishop.
		"""
		moves: list[Coordinate] = []

		file_ord = ord(self.coordinate.file)
		rank_ord = ord(self.coordinate.rank)

		# directions, from white's perspective
		# going down and right diagonally
		for i in range(1, 8):
			new_file = chr(file_ord+i)
			new_rank = chr(rank_ord-i)
			m = f'{new_file}{new_rank}'

			if not Coordinate.is_valid(m): break

			c = Coordinate(m)
			moves.append(c)

			# range of attack stops if there's a piece in the way
			if self.board.get(c).piece: break

		# going up and left diagonally
		for i in range(1, 8):
			new_file = chr(file_ord-i)
			new_rank = chr(rank_ord+i)
			m = f'{new_file}{new_rank}'

			if not Coordinate.is_valid(m): break

			c = Coordinate(m)
			moves.append(c)

			# range of attack stops if there's a piece in the way
			if self.board.get(c).piece: break

		# going up and right diagonally
		for i in range(1, 8):
			new_file = chr(file_ord+i)
			new_rank = chr(rank_ord+i)
			m = f'{new_file}{new_rank}'

			if not Coordinate.is_valid(m): break

			c = Coordinate(m)
			moves.append(c)

			# range of attack stops if there's a piece in the way
			if self.board.get(c).piece: break

		# going down and left diagonally
		for i in range(1, 8):
			new_file = chr(file_ord-i)
			new_rank = chr(rank_ord-i)
			m = f'{new_file}{new_rank}'

			if not Coordinate.is_valid(m): break

			c = Coordinate(m)
			moves.append(c)

			# range of attack stops if there's a piece in the way
			if self.board.get(c).piece: break

		return moves


	def available_moves(self) -> list[Coordinate]:
		"""
		returns the moves that the bishop can choose.
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
		return 'B' if self.color == Color.WHITE else 'b'

def main():
	b = Board()

	bish = Bishop(Color.WHITE, b, Coordinate('a8'))
	Pawn(Color.WHITE, b, Coordinate('c6'))

	print(b)
	print(bish.attacking_coordinates())
	print(bish.available_moves())

if __name__ == '__main__':
	main()