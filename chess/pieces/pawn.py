from chess.components import Coordinate, Color, Piece, PieceType

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

		direction: int
		starting_rank: str
		if self.color == Color.WHITE:
			direction = +1
			starting_rank = '2'
		elif self.color == Color.BLACK:
			direction = -1
			starting_rank = '7'

		new_rank = chr(rank_ord + direction)
		m = f'{file}{new_rank}'
		if Coordinate.is_valid(m):
			c: Coordinate = Coordinate(m)

			# if there isn't a piece ahead(any color) -> can move forward
			if not self.board.get(c).piece:
				moves.append(c)

				# only if it's the first move, allow double forward move
				if self.coordinate.rank == starting_rank:
					new_rank = chr(rank_ord + direction*2)
					m = f'{file}{new_rank}'
					if Coordinate.is_valid(m):
						c = Coordinate(m)

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
