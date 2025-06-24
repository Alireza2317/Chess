from chess.components import Board, Color, Coordinate
from chess.game.player import Player
from chess.pieces.king import King
from chess.pieces.queen import Queen
from chess.pieces.rook import Rook
from chess.pieces.bishop import Bishop
from chess.pieces.knight import Knight
from chess.pieces.pawn import Pawn

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

	def step(self) -> bool:
		print(self.board)

		self.white_p.update_valid_moves()
		
		if self.white_p.is_checkmated() or self.white_p.is_stalemate():
			print('Game over!')
			return True

		white_moves = []
		for piece in self.white_p.pieces:
			for move in piece.valid_moves:
				white_moves.append(
					(piece, move)
				)

		for i, (p, wm) in enumerate(white_moves):
			print(f'{i}: {p.piece_type} {wm}')

		move_idx = int(input("White's move: "))
		p = white_moves[move_idx][0]
		wm = white_moves[move_idx][1]
		self.white_p.move_piece(p, wm)

		print(self.board)

		self.black_p.update_valid_moves()

		if self.black_p.is_checkmated() or self.black_p.is_stalemate():
			print('Game over!')
			return True

		black_moves = []
		for piece in self.black_p.pieces:
			for move in piece.valid_moves:
				black_moves.append(
					(piece, move)
				)

		for i, (p, bm) in enumerate(black_moves):
			print(f'{i}: {p.piece_type} {bm}')

		move_idx = int(input("Black's move: "))
		p = black_moves[move_idx][0]
		bm = black_moves[move_idx][1]
		self.black_p.move_piece(p, bm)


		return False

def main():
	game = ChessGame()
	game.classic_setup()
	game.white_p.update_valid_moves()
	game.white_p.update_valid_moves()

	while True:
		game_over = game.step()
		if game_over: break


if __name__ == '__main__':
	main()

