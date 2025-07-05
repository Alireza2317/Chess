from __future__ import annotations
from chess.components import Color, Board, Coordinate, Piece, PieceType

class Player:
	def __init__(self, board: Board, color: Color):
		if not isinstance(color, Color):
			raise TypeError(f'color should be of type {Color.__name__}!')
		if not isinstance(board, Board):
			raise TypeError(f'board should be of type {Board.__name__}!')

		self.board = board
		self.color = color
		self.pieces: list[Piece] = []
		# it's white's turn at first
		self.is_turn: bool = (color == Color.WHITE)

	def set_king(self) -> None:
		""" sets up self.king based on self.pieces. """
		k_count = 0
		for piece in self.pieces:
			if piece.piece_type == PieceType.KING:
				self.king = piece
				k_count += 1

		if k_count != 1:
			raise TypeError(
				f'pieces parameter should be a list of Piece objects!\n'+
				f'and it should have one and only one King object inside.'
			)

	def set_opponent(self, opponent: Player) -> None:
		self.opponent = opponent

	def update_valid_moves(self) -> None:
		"""
		updates valid_moves property for each piece of the player
		this is a subset of each piece's available_moves()
		but considers potential checks and illegal moves in chess
		and sets up only the legal and valid moves
		"""
		for piece in self.pieces:
			original_coord = piece.coordinate
			has_moved = piece.has_moved
			valid_moves: list[Coordinate] = []

			for coord in piece.available_moves():
				enemy_piece: Piece | None = self.board.get(coord).piece

				self.board.remove(coord)
				if enemy_piece:
					# remove from opponent's pieces
					for op_piece in self.opponent.pieces:
						if op_piece.coordinate == coord:
							self.opponent.pieces.remove(op_piece)
							break

				self.board.move(piece, coord)

				if not self.is_in_check():
					valid_moves.append(coord)

				# reset
				self.board.move(piece, original_coord)

				# reset
				if enemy_piece:
					self.board.put(enemy_piece, enemy_piece.coordinate)
					self.opponent.add_piece(enemy_piece)

			# reset
			piece.has_moved = has_moved

			# update valid moves for each piece
			piece.valid_moves = valid_moves

		self.add_castle_moves_to_king()

	def add_piece(self, piece: Piece) -> None:
		"""	adds the given piece to self.pieces & updates self.king. """
		if not isinstance(piece, Piece):
			raise TypeError(
				f'piece should be of type {Piece.__name__}'
			)

		self.pieces.append(piece)
		self.set_king()

	def remove_piece(self, piece: Piece) -> None:
		if piece is None: return

		for i, p in enumerate(self.pieces):
			if p == piece:
				self.pieces.pop(i)

	def castle_moves(
		self
	) -> list[tuple[Piece, Coordinate, Piece, Coordinate]] | None:
		"""
		returns a list of one or two available castling moves in the format of:
			a tuple that holds 4 items,
			first one is the king
			second one is the king's new coordinate
			third one is the respective rook
			fourth one is the respective rook's new coordinate
		"""
		if self.king.has_moved: return None
		if self.is_in_check(): return None

		# the result
		king_rook_moves_pair: list[
			tuple[Piece, Coordinate, Piece, Coordinate]
		] = []

		valid_rooks: list[Piece] = []
		for piece in self.pieces:
			if piece.piece_type != PieceType.ROOK: continue

			# rook has moved
			if piece.has_moved: continue

			rook_attacks: list[Coordinate] = piece.attacking_coordinates()
			# there are pieces in the middle
			if self.king.coordinate not in rook_attacks: continue

			valid_rooks.append(piece)

		for rook in valid_rooks:
			rank: str = rook.coordinate.rank

			match rook.coordinate.file:
				# short castle
				case 'h':
					king_c = Coordinate(f'g{rank}')
					rook_c = Coordinate(f'f{rank}')

				# long castle
				case 'a':
					king_c = Coordinate(f'c{rank}')
					rook_c = Coordinate(f'd{rank}')

			king_rook_moves_pair.append(
					(self.king, king_c, rook, rook_c)
			)

		return king_rook_moves_pair

	def add_castle_moves_to_king(self) -> None:
		""" add the valid castling moves to self.king. """
		castling_moves = self.castle_moves()
		if not castling_moves: return

		for moves_pair in castling_moves:
			_, king_new_coord, *_ = moves_pair
			self.king.valid_moves.append(king_new_coord)

	def is_under_attack(self, coordinate: Coordinate) -> bool:
		""" returns wether the given square is under opponent's attack."""
		for op_piece in self.opponent.pieces:
			if coordinate in op_piece.attacking_coordinates():
				return True

		return False

	def is_in_check(self) -> bool:
		""" returns wether the player is in check or not. """
		if not self.is_turn: return False

		return self.is_under_attack(self.king.coordinate)

	def is_checkmated(self) -> bool:
		""" returns wether the player is lost or not. """
		return (
			self.is_turn and
			self.is_in_check() and
			not self.king.valid_moves
		)

	def is_stalemate(self) -> bool:
		""" returns wether the game is a stalemate(draw) or not. """
		all_valid_moves = []
		for p in self.pieces:
			all_valid_moves.extend(p.valid_moves)

		return (
			self.is_turn and
			not self.is_in_check() and
			not all_valid_moves
		)

	def __repr__(self):
		return f'<{self.color.name.title()} {Player.__name__}>'


def main():
	from chess.pieces.king import King
	from chess.pieces.rook import Rook
	from chess.pieces.knight import Knight

	b = Board()
	white = Player(b, Color.WHITE)
	black = Player(b, Color.BLACK)

	white.set_opponent(black)
	black.set_opponent(white)

	wk = King(white, Coordinate('e1'))
	bk = King(black, Coordinate('e8'))

	short_rook = Rook(white, Coordinate('h1'))
	long_rook = Rook(white, Coordinate('a1'))

	#Knight(white, Coordinate('g1'))
	#Knight(white, Coordinate('b1'))

	white.update_valid_moves()

	print(b)
	print(wk.valid_moves)

if __name__ == '__main__':
	main()