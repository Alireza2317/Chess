import enum
from chess.engine.core import Coordinate, Color
from chess.engine.pieces.bishop import Bishop
from chess.engine.pieces.king import King
from chess.engine.pieces.knight import Knight
from chess.engine.pieces.pawn import Pawn
from chess.engine.pieces.queen import Queen
from chess.engine.pieces.rook import Rook
from chess.engine.piece import Piece, PieceType
from chess.game.game import Game

MoveDetail = tuple[Coordinate, Coordinate, PieceType | None]

class LoopDecision(enum.Enum):
	BREAK = enum.auto()
	CONTINUE = enum.auto()
	PROCEED = enum.auto()


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
	#Knight(g.white, Coordinate.from_str("g1"))
	Knight(g.black, Coordinate.from_str("b8"))
	Knight(g.black, Coordinate.from_str("g8"))

	Bishop(g.white, Coordinate.from_str("c1"))
	#Bishop(g.white, Coordinate.from_str("f1"))
	Bishop(g.black, Coordinate.from_str("c8"))
	Bishop(g.black, Coordinate.from_str("f8"))

	Pawn(g.white, Coordinate.from_str("a2"))
	Pawn(g.white, Coordinate.from_str("b2"))
	Pawn(g.white, Coordinate.from_str("c2"))
	Pawn(g.white, Coordinate.from_str("d2"))
	#Pawn(g.white, Coordinate.from_str("e2"))
	Pawn(g.white, Coordinate.from_str("c6"))
	Pawn(g.white, Coordinate.from_str("f2"))
	#Pawn(g.white, Coordinate.from_str("f3"))
	Pawn(g.white, Coordinate.from_str("g2"))
	#Pawn(g.white, Coordinate.from_str("g4"))
	Pawn(g.white, Coordinate.from_str("h2"))

	#Pawn(g.black, Coordinate.from_str("a7"))
	Pawn(g.black, Coordinate.from_str("a5"))
	Pawn(g.black, Coordinate.from_str("b7"))
	#Pawn(g.black, Coordinate.from_str("c7"))
	#Pawn(g.black, Coordinate.from_str("d7"))
	Pawn(g.black, Coordinate.from_str("e7"))
	#Pawn(g.black, Coordinate.from_str("e6"))
	Pawn(g.black, Coordinate.from_str("f7"))
	Pawn(g.black, Coordinate.from_str("g7"))
	Pawn(g.black, Coordinate.from_str("h7"))

	return g

def handle_input(
	game: Game
) -> LoopDecision | MoveDetail:
	move_input: str = input('Enter move: ')

	if move_input == 'undo':
		if not game.undo():
			print('Cannot undo!')
		return LoopDecision.CONTINUE
	elif move_input == 'redo':
		if not game.redo():
			print('Cannot redo!')
		return LoopDecision.CONTINUE

	elif move_input == 'exit':
		return LoopDecision.BREAK

	promotion: PieceType | None = None

	try:
		parts = move_input.split()
		if len(parts) not in (2, 3):
			raise ValueError('Invalid input.')

		if len(parts) == 3: # promotion piece
			promotion = map_promotion(parts[2].lower())

		start: Coordinate = Coordinate.from_str(parts[0])
		end: Coordinate = Coordinate.from_str(parts[1])
	except Exception:
		print('Invalid input!')
		return LoopDecision.CONTINUE

	piece: Piece | None = game.board[start].piece
	if not piece:
		print(f'No piece found on {start}!')
		return LoopDecision.CONTINUE

	return start, end, promotion

def map_promotion(promotion_type: str) -> PieceType:
	promotion_map: dict[str, PieceType] = {
		'q': PieceType.QUEEN,
		'r': PieceType.ROOK,
		'b': PieceType.BISHOP,
		'n': PieceType.KNIGHT,
	}

	promotion: PieceType | None = promotion_map.get(promotion_type)
	if not promotion:
		raise ValueError('Invalid promotion type! Options: [q, r, b, n]')

	return promotion

def check_promotion(
	game: Game, start: Coordinate, end: Coordinate, promotion: PieceType | None
) -> LoopDecision:

	piece: Piece | None = game.board[start].piece
	if not piece:
		return LoopDecision.CONTINUE

	if piece.type == PieceType.PAWN:
		promotion_rank: str = '8' if piece.owner.color == Color.WHITE else '1'
		if end.rank == promotion_rank:
			if promotion is None:
				print('A promotion PieceType should be provided!')
				return LoopDecision.CONTINUE
		else:
			if promotion is not None:
				print(
					'A promotion PieceType was provided, while this is not a promotion move!'
				)
				return LoopDecision.CONTINUE

	return LoopDecision.PROCEED

def play_cli(game: Game) -> None:
	game.white.update_legal_moves()
	game.black.update_legal_moves()

	while True:
		#clear_console()

		if game.current_player.is_in_check() and  game.current_player.king:
			king_coord: Coordinate = game.current_player.king.coordinate
			game.board.print(checked=king_coord)
		else:
			game.board.print()


		print(f'{game.turn.name.title()} to move!')

		input_result: LoopDecision | MoveDetail = handle_input(game)
		if input_result == LoopDecision.CONTINUE:
			continue
		elif input_result == LoopDecision.BREAK:
			break

		if not isinstance(input_result, LoopDecision):
			start, end, promotion = input_result

		decision: LoopDecision = check_promotion(game, start, end, promotion)
		if decision == LoopDecision.CONTINUE:
			continue

		#print('move was a success')

		success: bool = game.play_turn(start, end, promotion=promotion)
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
