from chess.engine.core import Coordinate
from chess.engine.pieces.bishop import Bishop
from chess.engine.pieces.king import King
from chess.engine.pieces.knight import Knight
from chess.engine.pieces.pawn import Pawn
from chess.engine.pieces.queen import Queen
from chess.engine.pieces.rook import Rook
from chess.game.game import Game

def clear_console() -> None:
		print("\033[H\033[J", end="")

def classic_setup() -> Game:
	g: Game = Game()

	King(g.white, Coordinate.from_str("e1"))
	King(g.black, Coordinate.from_str("e8"))

	Queen(g.white, Coordinate.from_str("d1"))
	Queen(g.black, Coordinate.from_str("d8"))

	Rook(g.white, Coordinate.from_str("a1"))
	Rook(g.white, Coordinate.from_str("h1"))
	Rook(g.black, Coordinate.from_str("a8"))
	Rook(g.black, Coordinate.from_str("h8"))

	Knight(g.white, Coordinate.from_str("b1"))
	Knight(g.white, Coordinate.from_str("g1"))
	Knight(g.black, Coordinate.from_str("b8"))
	Knight(g.black, Coordinate.from_str("g8"))

	Bishop(g.white, Coordinate.from_str("c1"))
	Bishop(g.white, Coordinate.from_str("f1"))
	Bishop(g.black, Coordinate.from_str("c8"))
	Bishop(g.black, Coordinate.from_str("f8"))

	Pawn(g.white, Coordinate.from_str("a2"))
	Pawn(g.white, Coordinate.from_str("b2"))
	Pawn(g.white, Coordinate.from_str("c2"))
	Pawn(g.white, Coordinate.from_str("d2"))
	Pawn(g.white, Coordinate.from_str("e2"))
	Pawn(g.white, Coordinate.from_str("f2"))
	#Pawn(g.white, Coordinate.from_str("f3"))
	Pawn(g.white, Coordinate.from_str("g2"))
	#Pawn(g.white, Coordinate.from_str("g4"))
	Pawn(g.white, Coordinate.from_str("h2"))

	Pawn(g.black, Coordinate.from_str("a7"))
	Pawn(g.black, Coordinate.from_str("b7"))
	Pawn(g.black, Coordinate.from_str("c7"))
	Pawn(g.black, Coordinate.from_str("d7"))
	Pawn(g.black, Coordinate.from_str("e7"))
	#Pawn(g.black, Coordinate.from_str("e6"))
	Pawn(g.black, Coordinate.from_str("f7"))
	Pawn(g.black, Coordinate.from_str("g7"))
	Pawn(g.black, Coordinate.from_str("h7"))

	return g

def handle_input(game: Game) -> None:
	pass


def play_cli(game: Game) -> None:
	game.white.update_legal_moves()
	game.black.update_legal_moves()

	while True:
		clear_console()
		print(game.board)


		print(f'{game.turn.name.title()} to move!')
		move_input: str = input('Enter move: ')

		if move_input == 'undo':
			if not game.undo():
				print('Cannot undo!')
			continue

		if move_input == 'exit':
			break

		try:
			start_str, end_str = move_input.split()
			start = Coordinate.from_str(start_str)
			end = Coordinate.from_str(end_str)
		except Exception:
			print('Invalid input!')
			continue

		game.current_player.update_legal_moves()

		success: bool = game.move(start, end)
		if not success:
			print('Illegal move!')
			continue

		game.current_player.update_legal_moves()

		if game.white.is_checkmated():
			print(game.board)
			print('Black Won!')
			break
		elif game.black.is_checkmated():
			print(game.board)
			print('White Won!')
			break
		elif game.current_player.is_stalemeted():
			print(game.current_player.has_legal_moves())
			print('Stalemate!')
			break


def main() -> None:
	game: Game = classic_setup()
	play_cli(game)


if __name__ == '__main__':
	main()
