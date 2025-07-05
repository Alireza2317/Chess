from chess.components import Coordinate, Color, Piece, PieceType

class Rook(Piece):
	from chess.game.player import Player

	def __init__(self, player: Player, coordinate: Coordinate):
		super().__init__(player, coordinate)

	@property
	def piece_type(self) -> PieceType:
		return PieceType.ROOK

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
