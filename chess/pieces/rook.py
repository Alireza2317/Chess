from chess.components import Piece, Coordinate, Color, Board
from chess.game.player import Player
from chess.pieces.pawn import Pawn

class Rook(Piece):
	def __init__(self, player: Player, coordinate: Coordinate):
		super().__init__(player, coordinate)

	def attacking_coordinates(self) -> list[Coordinate]:
		"""
		returns all coordinates that are under the attack of the rook.
		"""
		moves: list[Coordinate] = []

		# directions in comments are from white's perspective
		attacking_directions: list[tuple[int, int]] = [
			(0, 1), # up
			(0, -1), # down
			(1, 0), # right
			(-1, 0), # left
		]

		for direction in attacking_directions:
			moves.extend(
				self.board.get_coordinates(self.coordinate, direction)
			)

		return moves

	def available_moves(self) -> list[Coordinate]:
		"""
		returns the moves that the rook can choose.
		regardless of checks.
		"""

		return super().available_moves()

	def __repr__(self):
		return 'R' if self.color == Color.WHITE else 'r'

def main():
	b = Board()

	rook = Rook(b, Color.WHITE, Coordinate('e4'))
	Pawn(b, Color.BLACK, Coordinate('e7'))
	Pawn(b, Color.WHITE, Coordinate('h4'))

	print(b)
	print(rook.attacking_coordinates())
	print(rook.available_moves())

if __name__ == '__main__':
	main()