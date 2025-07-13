from chess_refactored.engine.core import Color, Coordinate, Board
from chess_refactored.engine.player import Player
from chess_refactored.engine.piece import Piece
from chess_refactored.engine.pieces.knight import Knight


if __name__ == '__main__':
	board: Board = Board()
	player1: Player = Player(board, Color.WHITE)

	q: Piece = Knight(player1, Coordinate.from_str('e4'))
	print(q.all_moves())
	print(board)