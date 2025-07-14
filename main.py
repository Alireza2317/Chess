from chess.engine.core import Color, Coordinate
from chess.engine.board import Board
from chess.engine.player import Player
from chess.engine.piece import Piece
from chess.engine.pieces.knight import Knight


if __name__ == '__main__':
	board: Board = Board()
	player1: Player = Player(board, Color.WHITE)

	q: Piece = Knight(player1, Coordinate.from_str('e4'))
	print(q.all_moves())
	print(board)