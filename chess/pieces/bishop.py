from chess.components import Coordinate, Color, Piece, PieceType

class Bishop(Piece):
	from chess.game.player import Player
	def __init__(self, player: Player, coordinate: Coordinate):
		super().__init__(player, coordinate)

	@property
	def piece_type(self) -> PieceType:
		return PieceType.BISHOP

	def attacking_coordinates(self) -> list[Coordinate]:
		"""
		returns all coordinates that are under the attack of the bishop.
		"""
		moves: list[Coordinate] = []

		# directions in comments are from white's perspective
		attacking_directions: list[tuple[int, int]] = [
			(1, 1), # up&right
			(-1, -1), # down&left
			(1, -1), # up&left
			(-1, 1), # down&right
		]

		for direction in attacking_directions:
			moves.extend(
				self.board.get_coordinates(self.coordinate, direction)
			)

		return moves

	def available_moves(self) -> list[Coordinate]:
		"""
		returns the moves that the bishop can choose.
		regardless of checks.
		"""

		return super().available_moves()

	def __repr__(self):
		return 'B' if self.color == Color.WHITE else 'b'

def main():
	from chess.components import Board
	from chess.pieces.pawn import Pawn
	from chess.pieces.king import King
	from chess.game.player import Player

	b = Board()
	p = Player(b, Color.WHITE)
	king = King(p, Coordinate('e1'))
	bish = Bishop(p, Coordinate('a8'))
	Pawn(p, Coordinate('c6'))

	print(b)
	print(bish.attacking_coordinates())
	print(bish.available_moves())

if __name__ == '__main__':
	main()