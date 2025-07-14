from chess.engine.core import Color, Coordinate
from chess.engine.board import Board
from chess.engine.player import Player
from chess.engine.pieces.pawn import Pawn
from chess.engine.pieces.bishop import Bishop
from chess.engine.pieces.knight import Knight
from chess.engine.pieces.rook import Rook
from chess.engine.pieces.queen import Queen
from chess.engine.pieces.king import King

def validate_board(board: Board, white: Player, black: Player) -> None:
	errors = []

	# 1. Check piece.coordinate matches board position
	seen_pieces = set()
	for coord, square in board:
		piece = square.piece
		if piece:
			if piece.coordinate != coord:
				errors.append(
					f"Mismatch: piece {piece} says it's at {piece.coordinate}, "
					f"but is on square {coord}"
				)
			if piece in seen_pieces:
				errors.append(f"Duplicate: piece {piece} found on multiple squares")
			seen_pieces.add(piece)

	# 2. Check players' pieces exist on board
	for player in [white, black]:
		for p in player.pieces:
			square = board.get_square(p.coordinate)
			if square.piece != p:
				errors.append(
					f"{player} has piece {p} at {p.coordinate}, "
					f"but board has {square.piece}"
				)

	# 3. Optionally, check each piece has a valid coordinate
	for piece in seen_pieces:
		if not isinstance(piece.coordinate, Coordinate):
			errors.append(f"Invalid coordinate: {piece} has {piece.coordinate}")

	if errors:
		raise AssertionError("Board consistency check failed:\n" + "\n".join(errors))
	else:
		print("✅ Board is consistent.")

if __name__ == "__main__":
	board = Board()
	white = Player(board, Color.WHITE)
	black = Player(board, Color.BLACK)

	King(white, Coordinate.from_str("e1"))
	King(black, Coordinate.from_str("e8"))

	Queen(white, Coordinate.from_str("d1"))
	Queen(black, Coordinate.from_str("d8"))

	Rook(white, Coordinate.from_str("a1"))
	Rook(white, Coordinate.from_str("h1"))
	Rook(black, Coordinate.from_str("a8"))
	Rook(black, Coordinate.from_str("h8"))

	Knight(white, Coordinate.from_str("b1"))
	Knight(white, Coordinate.from_str("g1"))
	Knight(black, Coordinate.from_str("b8"))
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
	Pawn(black, Coordinate.from_str("f7"))
	Pawn(black, Coordinate.from_str("g7"))
	Pawn(black, Coordinate.from_str("h7"))

	print(board)
	validate_board(board, white, black)
