from chess.components import Piece, Coordinate, Color, Board
from chess.pieces.pawn import Pawn

class Queen(Piece):
	def __init__(self, color: Color, board: Board, coordinate: Coordinate):
		super().__init__(color, board, coordinate)

	def attacking_coordinates(self) -> list[Coordinate]:
		"""
		returns all coordinates that are under the attack of the queen.
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


		# going up
		for i in range(1, 8):
			m = f'{chr(file_ord)}{chr(rank_ord+i)}'
			if not Coordinate.is_valid(m): break

			c = Coordinate(m)
			moves.append(c)

			# if reached a piece, the range of attack stops
			if self.board.get(c).piece: break

		# going down
		for i in range(1, 8):
			m = f'{chr(file_ord)}{chr(rank_ord-i)}'
			if not Coordinate.is_valid(m): break

			c = Coordinate(m)
			moves.append(c)

			# if reached a piece, the range of attack stops
			if self.board.get(c).piece: break

		# going right
		for i in range(1, 8):
			m = f'{chr(file_ord+i)}{chr(rank_ord)}'
			if not Coordinate.is_valid(m): break

			c = Coordinate(m)
			moves.append(c)

			# if reached a piece, the range of attack stops
			if self.board.get(c).piece: break

		# going left
		for i in range(1, 8):
			m = f'{chr(file_ord-i)}{chr(rank_ord)}'
			if not Coordinate.is_valid(m): break

			c = Coordinate(m)
			moves.append(c)

			# if reached a piece, the range of attack stops
			if self.board.get(c).piece: break

		return moves


	def available_moves(self) -> list[Coordinate]:
		"""
		returns the moves that the queen can choose.
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
		return 'Q' if self.color == Color.WHITE else 'q'

def main():
	b = Board()

	q = Queen(Color.WHITE, b, Coordinate('e4'))
	#Pawn(Color.WHITE, b, Coordinate('f3'))

	print(b)
	print(q.attacking_coordinates())
	print(q.available_moves())

if __name__ == '__main__':
	main()