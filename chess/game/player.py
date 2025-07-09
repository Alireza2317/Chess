from __future__ import annotations
from chess.components import Color, Board, Coordinate, Piece, PieceType

class DummyKing: ...

CASTLE_PATHS: dict[str, tuple[str, str]] = {
	'a': ('c', 'd'),
	'h': ('g', 'f')
}


class Player:
	def __init__(self, board: Board, color: Color):
		if not isinstance(color, Color):
			raise TypeError(f'color should be of type {Color.__name__}!')
		if not isinstance(board, Board):
			raise TypeError(f'board should be of type {Board.__name__}!')

		self.board = board
		self.color = color
		self.pieces: list[Piece] = []

	@property
	def _start_rank(self) -> str:
		if self.color == Color.WHITE:
			return '1'
		else:
			return '8'

	def set_king(self) -> None:
		""" sets up self.king based on self.pieces. """
		k_count = 0
		for piece in self.pieces:
			if piece.piece_type == PieceType.KING:
				self.king = piece
				k_count += 1

		if k_count == 0:
			self.set_dummy_king()
			return

		if k_count > 1:
			raise TypeError(
				f'player should exactly one King object!'
			)

		if self.king.coordinate != Coordinate(f'e{self._start_rank}'):
			self.king.has_moved = True

	def set_dummy_king(self):
		""" setup a dummy king so that a game can be played without kings! """
		self.king = DummyKing()

	def rooks(self) -> list[Piece]:
		rooks: list[Piece] = []

		for piece in self.pieces:
			if piece.piece_type == PieceType.ROOK:
				rooks.append(piece)

		classic_coords: list[Coordinate] = [
			Coordinate(f'{file}{self._start_rank}') for file in CASTLE_PATHS
		]

		for rook in rooks:
			if rook.coordinate not in classic_coords:
				rook.has_moved = True

		return rooks

	def set_opponent(self, opponent: Player) -> None:
		self.opponent = opponent

		# enemy of my enemy is myself!
		opponent.opponent = self

	def update_valid_moves(self) -> None:
		"""
		updates valid_moves property for each piece of the player
		this is a subset of each piece's available_moves()
		but considers potential checks and illegal moves in chess
		and sets up only the legal and valid moves
		"""
		for piece in self.pieces:
			valid_moves: list[Coordinate] = []

			# save to restore later
			original_coord = piece.coordinate

			for coord in piece.available_moves():
				enemy_piece: Piece | None = self.board.get(coord).piece

				if enemy_piece:
					self.board.remove(coord)
					# and remove from opponent's pieces
					self.opponent.remove_piece(enemy_piece)

				self.board.move(piece, coord, examine_mode=True)

				if not self.is_in_check():
					valid_moves.append(coord)

				# reset
				self.board.move(piece, original_coord, examine_mode=True)
				if enemy_piece:
					self.board.put(enemy_piece, enemy_piece.coordinate)
					self.opponent.add_piece(enemy_piece)

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

	def remove_piece(self, piece: Piece) -> None:
		if piece is None: return
		self.pieces.remove(piece)

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
		returns None or [] if player has no legal castle moves
		"""
		if isinstance(self.king, DummyKing): return None
		if self.king.has_moved: return None
		if self.is_in_check(): return None

		# the result
		king_rook_moves_pair: list[
			tuple[Piece, Coordinate, Piece, Coordinate]
		] = []

		valid_rooks: list[Piece] = []
		for rook in self.rooks():
			if rook.has_moved: continue
			rook_attacks: list[Coordinate] = rook.attacking_coordinates()
			# there are pieces in the middle
			if self.king.coordinate not in rook_attacks: continue

			valid_rooks.append(rook)

		for rook in valid_rooks:
			files: tuple[str, str] | None = CASTLE_PATHS.get(
				rook.coordinate.file, None
			)
			if not files: continue

			for file in files:
				# check squares in the middle for enemy attacks
				c = Coordinate(f'{file}{self._start_rank}')
				if self.is_under_attack(c): break
			else: # if successful and no break = no enemy attacks
				king_file, rook_file = files
				king_c = Coordinate(f'{king_file}{self._start_rank}')
				rook_c = Coordinate(f'{rook_file}{self._start_rank}')

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

	def potential_en_passant_pawns(self) -> list[Piece]:
		potential_pawns: list[Piece]= []

		for piece in self.pieces:
			if piece.piece_type != PieceType.PAWN: continue

			if self.color == Color.WHITE:
				if piece.coordinate.rank == '5':
					potential_pawns.append(piece)
			else:
				if piece.coordinate.rank == '4':
					potential_pawns.append(piece)
		return potential_pawns

	def is_under_attack(self, coordinate: Coordinate) -> bool:
		""" returns wether the given square is under opponent's attack."""
		for op_piece in self.opponent.pieces:
			if coordinate in op_piece.attacking_coordinates():
				return True

		return False

	def is_in_check(self) -> bool:
		""" returns wether the player is in check or not. """
		if isinstance(self.king, DummyKing): return False

		return self.is_under_attack(self.king.coordinate)

	def is_checkmated(self) -> bool:
		""" returns wether the player is lost or not. """
		if not self.is_in_check(): return False

		for piece in self.pieces:
			if piece.valid_moves:
				return False

		return True

	def is_stalemate(self) -> bool:
		""" returns wether the game is a stalemate(draw) or not. """
		if self.is_in_check(): return False

		for p in self.pieces:
			if p.valid_moves: return False

		return True

	def __repr__(self):
		return f'<{self.color.name.title()} {self.__class__.__name__}>'
