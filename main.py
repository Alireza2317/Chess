from chess.engine.core import Color, Coordinate
from chess.engine.board import Board
from chess.engine.player import Player
from chess.engine.pieces.knight import Knight
from chess.engine.pieces.pawn import Pawn
from chess.engine.pieces.bishop import Bishop
from chess.engine.pieces.rook import Rook
from chess.engine.pieces.king import King
from chess.engine.pieces.queen import Queen



if __name__ == '__main__':
	board: Board = Board()
	white: Player = Player(board, Color.WHITE)
	black: Player = Player(board, Color.BLACK)

	white.set_opponent(black)

	King(white, Coordinate.from_str("e1"))
	King(black, Coordinate.from_str("e8"))

	wq=Queen(white, Coordinate.from_str("d1"))
	Queen(black, Coordinate.from_str("d8"))

	Rook(white, Coordinate.from_str("a1"))
	Rook(white, Coordinate.from_str("h1"))
	Rook(black, Coordinate.from_str("a8"))
	Rook(black, Coordinate.from_str("h8"))

	wnb=Knight(white, Coordinate.from_str("b1"))
	Knight(white, Coordinate.from_str("g1"))
	bnb=Knight(black, Coordinate.from_str("b8"))
	Knight(black, Coordinate.from_str("g8"))

	Bishop(white, Coordinate.from_str("c1"))
	Bishop(white, Coordinate.from_str("f1"))
	Bishop(black, Coordinate.from_str("c8"))
	Bishop(black, Coordinate.from_str("f8"))

	Pawn(white, Coordinate.from_str("a2"))
	Pawn(white, Coordinate.from_str("b2"))
	Pawn(white, Coordinate.from_str("c2"))
	Pawn(white, Coordinate.from_str("d2"))
	Pawn(white, Coordinate.from_str("e2"))
	Pawn(white, Coordinate.from_str("f2"))
	Pawn(white, Coordinate.from_str("g2"))
	Pawn(white, Coordinate.from_str("h2"))

	Pawn(black, Coordinate.from_str("a7"))
	Pawn(black, Coordinate.from_str("b7"))
	Pawn(black, Coordinate.from_str("c7"))
	Pawn(black, Coordinate.from_str("d7"))
	Pawn(black, Coordinate.from_str("e7"))
	p=Pawn(black, Coordinate.from_str("f7"))
	Pawn(black, Coordinate.from_str("g7"))
	Pawn(black, Coordinate.from_str("h7"))

	b=Bishop(white, Coordinate.from_str("g6"))
	#black.update_legal_moves()
	white.update_legal_moves()

	print(b.attacking_coordinates())
	print(b.all_moves())
	print(b.legal_moves)

	print(board)