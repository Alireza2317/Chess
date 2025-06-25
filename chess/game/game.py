from enum import Enum
from chess.components import Board, Color, Coordinate, Piece
from chess.game.player import Player
from chess.pieces.king import King
from chess.pieces.queen import Queen
from chess.pieces.rook import Rook
from chess.pieces.bishop import Bishop
from chess.pieces.knight import Knight
from chess.pieces.pawn import Pawn

class GameEndState(Enum):
	BLACK_WON = 'b'
	WHITE_WON = 'w'
	DRAW = 'd'
	ONGOING = 'o'


class ChessGame:
	def __init__(self):
		self.board = Board()
		self.white_p: Player = Player(self.board, Color.WHITE)
		self.black_p: Player = Player(self.board, Color.BLACK)

		self.white_p.set_opponent(self.black_p)
		self.black_p.set_opponent(self.white_p)

	def classic_setup(self) -> None:
		for color in [Color.WHITE, Color.BLACK]:
			if color == Color.WHITE:
				player = self.white_p
				pawn_rank = '2'
				pieces_rank = '1'
			else:
				player = self.black_p
				pawn_rank = '7'
				pieces_rank = '8'

			King(player, Coordinate(f'e{pieces_rank}'))
			Queen(player, Coordinate(f'd{pieces_rank}'))
			for file in ('a', 'h'):
				Rook(player, Coordinate(f'{file}{pieces_rank}'))
			for file in ('c', 'f'):
				Bishop(player, Coordinate(f'{file}{pieces_rank}'))
			for file in ('b', 'g'):
				Knight(player, Coordinate(f'{file}{pieces_rank}'))
			# pawns
			for file_ord in range(ord('a'), ord('h')+1):
				file = chr(file_ord)
				Pawn(player, Coordinate(f'{file}{pawn_rank}'))

		self.white_p.update_valid_moves()
		self.black_p.update_valid_moves()

	def two_kings_setup(self) -> None:
		King(self.white_p, Coordinate('e1'))
		King(self.black_p, Coordinate('e8'))

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

	def get_player_valid_moves(self, player: Player) -> list[Coordinate]:
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
			valid_moves: list[Coordinate]
	):
		move_idx = int(input(f"{player.color.name.title()}'s move: "))
		piece = valid_moves[move_idx][0]
		move = valid_moves[move_idx][1]

		## if there is an enemy piece on the desired coordinate: capture
		#if self.board.get(move).piece:
		#	# remove from board
		#	self.board.remove(move)
		#	# remove from player's pieces
		#	player.remove_piece(piece)

		self.board.move(piece, move)

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

			valid_moves = self.get_player_valid_moves(player)
			self.apply_input_to_game(
				player,
				valid_moves
			)

		return False


def main():
	game = ChessGame()

	game.classic_setup()
	while True:
		game_over = game.step()
		if game_over: break


if __name__ == '__main__':
	main()

