import enum
from chess.components import Board, Color, Coordinate, Piece, PieceType
from chess.game.player import Player
from chess.pieces.king import King
from chess.pieces.queen import Queen
from chess.pieces.rook import Rook
from chess.pieces.bishop import Bishop
from chess.pieces.knight import Knight
from chess.pieces.pawn import Pawn

class GameEndState(enum.Enum):
	BLACK_WON = enum.auto()
	WHITE_WON = enum.auto()
	DRAW = enum.auto()
	ONGOING = enum.auto()


class ChessGame:
	def __init__(self) -> None:
		self.board = Board()
		self.white_p: Player = Player(self.board, Color.WHITE)
		self.black_p: Player = Player(self.board, Color.BLACK)

		self.white_p.set_opponent(self.black_p)

		# it's white's turn at first
		self.turn: Color = Color.WHITE

		# default promotion piece is queen
		self.promotion_piece: PieceType = PieceType.QUEEN

		self.en_passant_target_square: Coordinate | None = None
		self.en_passant_pawns: list[Piece] = []

	@property
	def current_player(self) -> Player:
		if self.turn == Color.WHITE:
			return self.white_p
		else:
			return self.black_p

	def change_turns(self):
		""" changes the player's turns, from white to black or vice versa. """
		self.turn = ~self.turn

	def classic_setup(self) -> None:
		self.load_FEN('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

	def destroy_all_pieces(self):
		self.white_p.pieces = []
		self.black_p.pieces = []
		for row in self.board.board_matrix:
			for square in row:
				self.board.remove(square.coordinate)

	def load_FEN(self, FEN: str):
		"""
		this method will load the game based on the given FEN notation. 
		"""
		def reset_game():
			# reset game
			self.destroy_all_pieces()
			self.turn = Color.WHITE

		def place_pieces(fen_placements: str):
			# fen_placements is the first field of FEN
			p_placements_ranks: list[str] = fen_placements.split('/')

			for rank, rank_pieces in zip('87654321', p_placements_ranks):
				file = 'a'
				for piece in rank_pieces:
					# can be 'KQRBNPkqrbnp' or a number between 1 and 8
					# the number denotes the number of consecutive empty squares
					if piece in '87654321':
						new_f_ord = ord(file) + int(piece)
						file = chr(new_f_ord)
						continue

					if piece.isupper():
						player = self.white_p
					else:
						player = self.black_p

					coord = Coordinate(f'{file}{rank}')

					if piece in 'Kk':
						King(player, coord)
					elif piece in 'Qq':
						Queen(player, coord)
					elif piece in 'Rr':
						Rook(player, coord)
					elif piece in 'Bb':
						Bishop(player, coord)
					elif piece in 'Nn':
						Knight(player, coord)
					elif piece in 'Pp':
						Pawn(player, coord)

					# move to next file
					file = chr(ord(file) + 1)

		def handle_turn(fen_turn: str):
			if fen_turn == 'b':
				self.change_turns()

		def handle_castle_moves(fen_castle_field: str) -> None:
			# k means kingside, q means queenside
			to_disable: list[str] = ['K', 'Q', 'k', 'q']
			for cr in fen_castle_field:
				if cr in to_disable:
					to_disable.remove(cr)

			for move in to_disable:
				if move.isupper():
					player = self.white_p
				else:
					player = self.black_p

				if move in 'Kk':
					rook_file = 'h'
				if move in 'Qq':
					rook_file = 'a'

				for p in player.pieces:
					if p.piece_type != PieceType.ROOK: continue
					if p.coordinate.file != rook_file: continue
					p.has_moved = True

		fen_fields: list[str] = FEN.split()
		# 0: piece placements, from rank 8 to 1
		# 1: 'w' or 'b', current player's turn
		# 2: castling availablity, first white's then black's or -
		# 3: en passant target square
		# 4, 5 are not important really

		reset_game()

		place_pieces(fen_fields[0])

		self.white_p.set_king()
		self.black_p.set_king()

		handle_turn(fen_fields[1])

		# handling castle moves
		handle_castle_moves(fen_fields[2])

		# en passant
		#fen_fields[3]

	def check_state(self) -> GameEndState:
		if self.white_p.is_checkmated():
			print('Black won!')
			return GameEndState.BLACK_WON
		if self.black_p.is_checkmated():
			print('White won!')
			return GameEndState.WHITE_WON

		if self.white_p.is_stalemate() or self.black_p.is_stalemate():
			print('Stalemate(Draw)')
			return GameEndState.DRAW

		return GameEndState.ONGOING

	def handle_en_passant(self, piece: Piece, coordinate: Coordinate) -> None:
		# if this move was a pawn trying to escape, set the en passant square
		if piece.piece_type != PieceType.PAWN: return

		opponent_pawns: list[Piece] = self.current_player.opponent.potential_en_passant_pawns()
		if not opponent_pawns: return

		if coordinate.rank != opponent_pawns[0].coordinate.rank: return

		adjacent_files = []
		if (f:=chr(ord(coordinate.file)+1)) in 'abcdefgh':
			adjacent_files.append(f)
		if (f:=chr(ord(coordinate.file)-1)) in 'abcdefgh':
			adjacent_files.append(f)

		adjacent_coords = []
		for file in adjacent_files:
			adjacent_coords.append(Coordinate(f'{file}{coordinate.rank}'))

		en_passant_pawns: list[Piece] = []
		for op_pawn in opponent_pawns:
			if op_pawn.coordinate in adjacent_coords:
				en_passant_pawns.append(op_pawn)

		if not en_passant_pawns: return

		# this was a move, that enabled en passant on the next move
		# so
		new_rank: str
		if self.current_player.color == Color.WHITE:
			new_rank = chr(ord(piece.coordinate.rank)+1)
		else:
			new_rank = chr(ord(piece.coordinate.rank)-1)


		self.en_passant_target_square = Coordinate(
			f'{piece.coordinate.file}{new_rank}'
		)

		self.en_passant_pawns = en_passant_pawns
		self.can_en_passant = True

	def get_rook_castle_move(
		self, piece: Piece, coordinate: Coordinate
	) -> tuple[Piece, Coordinate] | None:
		"""
		returns rook's castle move if the move is a castle move.
		based on the given piece(king) and its new coordinate.
		else returns None.
		"""

		king = self.current_player.king
		if piece != king: return None

		castle_moves = self.current_player.castle_moves()
		if not castle_moves: return None

		for moves_pair in castle_moves:
			_, king_move, rook, rook_move = moves_pair

			if coordinate == king_move:
				return (rook, rook_move)

		return None

	def pawn_promotion(self, piece: Piece, coordinate: Coordinate) -> bool:
		""" checks pawn promotion and returns wether it happened or not. """
		if piece.piece_type != PieceType.PAWN: return False

		if coordinate.rank not in ('1', '8'): return False

		# remove pawn from board and player's pieces
		piece.player.remove_piece(piece)
		self.board.remove(coordinate)

		return True

	def set_promotion_piece(self):
		while True:
			p = input('Promote to [q, r, b, n]: ')
			if p in 'Qq':
				self.promotion_piece = PieceType.QUEEN
			elif p in 'Rr':
				self.promotion_piece = PieceType.ROOK
			elif p in 'Bb':
				self.promotion_piece = PieceType.BISHOP
			elif p in 'Nn':
				self.promotion_piece = PieceType.KNIGHT
			else: continue

			break

	def move(self, piece: Piece, coordinate: Coordinate):
		"""
		moves the given piece to the given coordinate.
		handles castling moves.
		handles captures of opponent pieces.
		"""
		if not (piece and coordinate):
			print('wrong inputs!')
			return

		can_en_passant: bool = False
		if self.en_passant_target_square:
			can_en_passant = True

		# make en passant happen in the next move, if possible
		self.handle_en_passant(piece, coordinate)

		if can_en_passant:
			# en passant is happeing if
			if piece in self.en_passant_pawns and coordinate == self.en_passant_target_square:
				# remove the enemy pawn
				if self.current_player.color == Color.WHITE:
					rank = chr(ord(coordinate.rank)-1)
				else:
					rank = chr(ord(coordinate.rank)+1)
				pawn_coord: Coordinate = Coordinate(f'{coordinate.file}{rank}')
				op_pawn: Piece = self.board.get(pawn_coord).piece
				self.board.remove(pawn_coord)
				self.current_player.opponent.remove_piece(op_pawn)

			# disable en passant, either way
			self.en_passant_target_square = None
			self.en_passant_pawns = []

		# if castling, move the rook too
		rook_castle_move = self.get_rook_castle_move(piece, coordinate)
		if rook_castle_move:
			rook, rook_move = rook_castle_move
			self.board.move(rook, rook_move)
			# the king
			self.board.move(piece, coordinate)
			self.change_turns()
			return

		# regular moves
		opponent_piece: Piece | None = self.board.get(coordinate).piece

		if opponent_piece:
			opponent: Player = opponent_piece.player

		# removes opponent's piece from board, if any
		# or just moves the piece
		self.board.move(piece, coordinate)

		# capturing
		if opponent_piece:
			# remove piece from opponent's(player) pieces
			opponent.remove_piece(opponent_piece)

		# pawn promotion
		if self.pawn_promotion(piece, coordinate):
			self.set_promotion_piece()

			match self.promotion_piece:
				case PieceType.QUEEN:
					Queen(piece.player, coordinate)
				case PieceType.ROOK:
					Rook(piece.player, coordinate)
				case PieceType.BISHOP:
					Bishop(piece.player, coordinate)
				case PieceType.KNIGHT:
					Knight(piece.player, coordinate)

		# switch turns
		self.change_turns()

	def print_player_valid_moves(
		self, player: Player
	) -> list[tuple[Piece, Coordinate]]:
		player_moves = []
		for piece in player.pieces:
			for move in piece.valid_moves:
				player_moves.append(
					(piece, move)
				)

		for i, (p, wm) in enumerate(player_moves):
			print(f'{i:02}: {p.piece_type.name.title(): >6} {wm}')

		return player_moves

	def apply_input_to_game(
			self,
			player: Player,
			valid_moves: list[tuple[Piece, Coordinate]]
	):
		move_idx = int(input(f"{player.color.name.title()}'s move: "))
		piece, move = valid_moves[move_idx]

		self.move(piece, move)

	def step(self) -> bool:
		"""
		one step in the game which contains one move from white and
		one move from black
		returns the game_over state(bool)
		"""
		for player in (self.white_p, self.black_p):
			print(self.board)

			player.update_valid_moves()

			state = self.check_state()
			if state != GameEndState.ONGOING: return True

			valid_moves = self.print_player_valid_moves(player)
			self.apply_input_to_game(player, valid_moves)

		return False


def main():
	game = ChessGame()

	game.classic_setup()
	game.white_p.update_valid_moves()
	game.black_p.update_valid_moves()

	while True:
		game_over = game.step()
		if game_over: break


if __name__ == '__main__':
	main()

