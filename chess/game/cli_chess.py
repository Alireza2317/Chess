import enum
from chess.engine.core import Coordinate, Color
from chess.engine.piece import Piece, PieceType
from chess.game.game import Game
from chess.game.fen import fen_loader

MoveDetail = tuple[Coordinate, Coordinate, PieceType | None]

class LoopDecision(enum.Enum):
	BREAK = enum.auto()
	CONTINUE = enum.auto()
	PROCEED = enum.auto()


def clear_console() -> None:
	print("\033[H\033[J", end="")

def classic_setup() -> Game:
	return fen_loader('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b - - - -')

def custom_setup() -> Game:
	return fen_loader('rnbqkbnr/pppppp1p/8/5Pp1/8/8/PPPPP1PP/RNBQKBNR w KQkq g6 - -')

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
	game.update_legal_moves()

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

		success: bool = game.play_turn(start, end, promotion=promotion)
		if not success:
			print('Illegal move!')
			continue

		game.update_legal_moves()

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
	#game: Game = classic_setup()
	game: Game = custom_setup()
	play_cli(game)


if __name__ == '__main__':
	main()
