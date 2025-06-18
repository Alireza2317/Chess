from chess.pieces.pawn import Pawn
from chess.pieces.king import King
from chess.pieces.knight import Knight
from chess.components import Board, Color, Coordinate


b = Board()

for file in 'abcdefgh':
	Pawn(Color.WHITE, b, Coordinate(f'{file}2'))
	Pawn(Color.BLACK, b, Coordinate(f'{file}7'))


print(b)