from chess.components import Coordinate, Color, Piece, PieceType

class Knight(Piece):
	from chess.game.player import Player
	def __init__(self, player: Player, coordinate: Coordinate):
		super().__init__(player, coordinate)

	@property
	def piece_type(self) -> PieceType:
		return PieceType.KNIGHT

	def attacking_coordinates(self) -> list[Coordinate]:
		"""
		returns the coordinates that the knight can attack
		regardless of checks
		"""
		moves: list[Coordinate] = []

		file_ord: int = ord(self.coordinate.file)
		rank_ord: int = ord(self.coordinate.rank)

		for f_dir, r_dir in [(2, 1), (1, 2)]:
			for f_s, r_s in [(-1, 1), (1, -1), (1, 1), (-1, -1)]:
				file = chr(file_ord + f_dir*f_s)
				rank = chr(rank_ord + r_dir*r_s)
				m = f'{file}{rank}'
				if not Coordinate.is_valid(m): continue
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
