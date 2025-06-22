from chess.components import Piece, Coordinate, Color, Board
from chess.game.player import Player

class Knight(Piece):
	def __init__(self, player: Player, coordinate: Coordinate):
		super().__init__(player, coordinate)

	def attacking_coordinates(self) -> list[Coordinate]:
		"""
		returns the coordinates that the knight can attack
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
		"""

		return super().available_moves()

	def __repr__(self):
		return 'N' if self.color == Color.WHITE else 'n'


def main():
	board = Board()
	Piece(board, Color.WHITE, Coordinate('d2'))
	Piece(board, Color.WHITE, Coordinate('f2'))

	knight = Knight(board, Color.WHITE, Coordinate('e4'))

	print(knight.available_moves())



if __name__ == '__main__':
	main()