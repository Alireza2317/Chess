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

	def can_castle(self) -> bool:
		""" Checks wether the player can castle or not. """
		if self.king.has_moved: return False
		if self.is_in_check(): return False

		for piece in self.pieces:
			if piece.piece_type == PieceType.ROOK:
				if not piece.has_moved:
					# if there are no pieces in the middle
					if self.king.coordinate in piece.attacking_coordinates():
						return True

		# no rooks, or rooks have moved, or some pieces are in the middle
		return False

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
		if not self.can_castle(): return None

		# the result
		king_rook_moves_pair: list[tuple[Piece, Coordinate, Piece, Coordinate]] = []

		for piece in self.pieces:
			if piece.piece_type == PieceType.ROOK:
				if piece.has_moved: continue

				# short castle
				if piece.coordinate.file == 'h':
					if self.color == Color.WHITE:
						king_c = Coordinate('g1')
						rook_c = Coordinate('f1')
					else:
						king_c = Coordinate('g8')
						rook_c = Coordinate('f8')

				# long castle
				elif piece.coordinate.file == 'a':
					if self.color == Color.WHITE:
						king_c = Coordinate('c1')
						rook_c = Coordinate('d1')
					else:
						king_c = Coordinate('c8')
						rook_c = Coordinate('d8')

				king_rook_moves_pair.append(
						(self.king, king_c, piece, rook_c)
					)

		return king_rook_moves_pair

	def add_castle_moves_to_king(self):
		""" add the available castling moves to self.king. """
		king_moves: list[Coordinate] = []
		castling_moves = self.castle_moves()
		if castling_moves:
			for moves_pair in castling_moves:
				_, king_new_coord, *_ = moves_pair
				king_moves.append(king_new_coord)

		for move in king_moves:
			self.king.valid_moves.append(move)

	def is_in_check(self) -> bool:
		""" returns wether the player is in check or not. """
		if not self.is_turn: return False

		for piece in self.opponent.pieces:
			if self.king.coordinate in piece.attacking_coordinates():
				return True

		return False

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