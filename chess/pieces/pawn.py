from chess.components import Coordinate, Color, PieceType, Piece

class Pawn(Piece):
	from chess.game.player import Player
	def __init__(self, player: Player, coordinate: Coordinate):
		super().__init__(player, coordinate)

	@property
	def piece_type(self) -> PieceType:
		return PieceType.PAWN

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

		file = self.coordinate.file
		rank_ord = ord(self.coordinate.rank)

		if self.color == Color.WHITE:
			sign: int = +1
		elif self.color == Color.BLACK:
			sign: int = -1

		new_rank = chr(rank_ord + sign*1)
		m = f'{file}{new_rank}'
		if Coordinate.is_valid(m):
			c: Coordinate = Coordinate(m)

			# if there isn't a piece ahead(any color) -> can move forward
			if not self.board.get(c).piece:
				moves.append(c)

				# only if it's the first move, allow double forward move
				if not self.has_moved:
					new_rank = chr(rank_ord + sign*2)
					m = f'{file}{new_rank}'
					if Coordinate.is_valid(m):
						c: Coordinate = Coordinate(m)

						# if there isn't a piece ahead
						if not self.board.get(c).piece:
							moves.append(c)

		# capturing moves
		for move in self.attacking_coordinates():
			p = self.board.get(move).piece
			if p:
				if p.color != self.color:
					moves.append(move)

		return moves

	def __repr__(self):
		return 'P' if self.color == Color.WHITE else 'p'


def main():
	from chess.game.player import Player
	from chess.components import Board
	from chess.pieces.king import King

	board = Board()
	white = Player(board, Color.WHITE)
	black = Player(board, Color.BLACK)

	King(white, Coordinate('e1'))
	King(black, Coordinate('e8'))

	P = Pawn(white, Coordinate('e2'))
	P2 = Pawn(white, Coordinate('h2'))
	p = Pawn(black, Coordinate('e3'))
	Pawn(black, Coordinate('h4'))

	print(P.available_moves())
	print(P2.available_moves())
	board.move(P2, Coordinate('h3'))
	print(P2.available_moves())

	print(board)

if __name__ == '__main__':
	main()