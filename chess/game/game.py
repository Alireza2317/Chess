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


def main():
	game = ChessGame()
	game.classic_setup()

if __name__ == '__main__':
	main()

