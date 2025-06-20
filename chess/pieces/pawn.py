from chess.components import Piece, Coordinate, Color, Board


class Pawn(Piece):
	def __init__(self, color: Color, board: Board, coordinate: Coordinate):
		super().__init__(color, board, coordinate)

	def attacking_coordinates(self) -> list[Coordinate]:
		""" returns the one/two attacking coordinates of the pawn. """
		moves: list[Coordinate] = []

		if self.color == Color.WHITE:
			new_rank = chr(ord(self.coordinate.rank)+1)
		elif self.color == Color.BLACK:
			new_rank = chr(ord(self.coordinate.rank)-1)

		file = self.coordinate.file
		possible_moves = [
			chr(ord(file)-1)+new_rank,
			chr(ord(file)+1)+new_rank,
		]

		for m in possible_moves:
			if Coordinate.is_valid(m):
				moves.append(Coordinate(m))

		return moves

	def available_moves(self) -> list[Coordinate]:
		"""
		returns all available moves for the pawn.
		regardless of checks.
		"""
		moves: list[Coordinate] = []

		moves.extend(
			super().available_moves(self.attacking_coordinates())
		)

		file = self.coordinate.file
		rank_ord = ord(self.coordinate.rank)

		if self.color == Color.WHITE:
			sign: int = +1
		elif self.color == Color.BLACK:
			sign: int = -1

		new_rank = chr(rank_ord + sign*1)
		c: Coordinate = Coordinate(f'{file}{new_rank}')

		# if there isn't a piece ahead(any color) -> can move forward
		if not self.board.get(c).piece:
			moves.append(c)

			# only if it's the first move, allow double forward move
			if not self.has_moved:
				new_rank = chr(rank_ord + sign*2)
				c = Coordinate(f'{file}{new_rank}')
				# if there isn't a piece ahead
				if not self.board.get(c).piece:
					moves.append(c)

		return moves

	def __repr__(self):
		return 'P' if self.color == Color.WHITE else 'p'


def main():
	b = Board()
	p = Pawn(Color.BLACK, b, Coordinate('e7'))
	Pawn(Color.WHITE, b, Coordinate('d6'))

	print(b)
	print(p.attacking_coordinates())
	print(p.available_moves())

if __name__ == '__main__':
	main()