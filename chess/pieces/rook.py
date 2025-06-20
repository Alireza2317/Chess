from chess.components import Piece, Coordinate, Color, Board


class Rook(Piece):
	def __init__(self, color: Color, board: Board, coordinate: Coordinate):
		super().__init__(color, board, coordinate)

	def attacking_coordinates(self) -> list[Coordinate]:
		"""
		returns all coordinates that are under the attack of the rook.
		"""
		moves: list[Coordinate] = []

		file_ord = self.coordinate.file
		rank_ord = self.coordinate.rank

		# going up or down
		for new_rank_ord in range(rank_ord+1, rank_ord+8):
			m = f'{chr(file_ord)}{chr(new_rank_ord)}'
			if not Coordinate.is_valid(m): continue

			# if reached a piece, the range of attack stops
			if self.board.get(Coordinate(m)).piece:
				moves.append(Coordinate(m))
				break

		# going up or down, opposite direction
		for new_rank_ord in range(rank_ord-1, rank_ord-8, -1):
			m = f'{chr(file_ord)}{chr(new_rank_ord)}'
			if not Coordinate.is_valid(m): continue

			# if reached a piece, the range of attack stops
			if self.board.get(Coordinate(m)).piece:
				moves.append(Coordinate(m))
				break

		# going right or left
		for new_file_ord in range(file_ord+1, file_ord+8):
			m = f'{chr(new_file_ord)}{chr(rank_ord)}'
			if not Coordinate.is_valid(m): continue

			# if reached a piece, the range of attack stops
			if self.board.get(Coordinate(m)).piece:
				moves.append(Coordinate(m))
				break

		# going right or left, opposite direction
		for new_file_ord in range(file_ord-1, file_ord-8, -1):
			m = f'{chr(new_file_ord)}{chr(rank_ord)}'
			if not Coordinate.is_valid(m): continue

			# if reached a piece, the range of attack stops
			if self.board.get(Coordinate(m)).piece:
				moves.append(Coordinate(m))
				break

		return moves

	def available_moves(self) -> list[Coordinate]:
		"""
		returns the moves that the rook can choose.
		regardless of checks.
		"""
		moves: list[Coordinate] = self.attacking_coordinates()

		for c in self.attacking_coordinates():
			p: Piece | None = self.board.get(c).piece
			if p:
				# if is a piece of our own, cannot move there
				if p.color == self.color:
					moves.remove(c)

	def __repr__(self):
		return 'R' if self.color == Color.WHITE else 'r'

def main():
	pass

if __name__ == '__main__':
	main()