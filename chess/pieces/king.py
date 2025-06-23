from chess.components import Coordinate, Color, PieceType, Piece

class King(Piece):
	from chess.game.player import Player
	def __init__(self, player: Player, coordinate: Coordinate):
		super().__init__(player, coordinate)

	@property
	def piece_type(self) -> PieceType:
		return PieceType.KING

	def attacking_coordinates(self) -> list[Coordinate]:
		"""
		returns the coordinates that the king can attack
		regardless of checks
		"""
		moves: list[Coordinate] = []

		file_ord: int = ord(self.coordinate.file)
		rank_ord: int = ord(self.coordinate.rank)

		possible_moves = []
		for file_code in range(file_ord-1, file_ord+2):
			for rank_s in range(rank_ord-1, rank_ord+2):
				file: str = chr(file_code)
				rank: str = chr(rank_s)
				c = Coordinate(f'{file}{rank}')
				# exclude the king's current coordinate
				if c == self.coordinate: continue

				possible_moves.append(f'{file}{rank}')

		for m in possible_moves:
			if Coordinate.is_valid(m):
				moves.append(Coordinate(m))

		return moves

	def available_moves(self) -> list[Coordinate]:
		"""
		returns the moves that the king can choose
		regardless of checks.
		is a subset of attacking squares
		"""

		return super().available_moves()

	def __repr__(self):
		return 'K' if self.color == Color.WHITE else 'k'

def main():
	pass

if __name__ == '__main__':
	main()