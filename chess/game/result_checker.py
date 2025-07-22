from chess.engine.piece import Piece, PieceType
from chess.game.game import Game, GameStatus
from chess.game.fen import FENLoader

class GameResultChecker:
	def __init__(self, game: Game):
		self.game: Game = game

	def did_white_win(self) -> bool:
		return self.game.black.is_checkmated()

	def did_black_win(self) -> bool:
		return self.game.white.is_checkmated()

	def is_stalemate(self) -> bool:
		return self.game.white.is_stalemeted() or self.game.black.is_stalemeted()

	def is_insufficient_material(self) -> bool:
		# insufficient material:
		# k vs. k
		# k + b vs. k
		# k + n vs. k
		# k + 2n vs. k
		# k + n vs. k + n
		# k + n vs. k + b
		# k + b vs. k + b

		if len(self.game.board.all_pieces()) >= 5:
			return False

		if len(self.game.white.pieces) >= 4 or len(self.game.black.pieces) >= 4:
			return False

		pieces: set[Piece] =  self.game.board.all_pieces().copy()
		for piece in pieces:
			if piece.type in (
				PieceType.QUEEN,
				PieceType.PAWN,
				PieceType.ROOK,
			):
				return False

		for player in (self.game.white, self.game.black):
			bishop_count: int = 0
			for piece in player.pieces:
				if piece.type == PieceType.BISHOP:
					bishop_count += 1
			if bishop_count >= 2:
				return False
		return True

	def is_draw(self) -> bool:
		# excluding stalemate, since its handled seperately
		# 1. insufficient material
		# 2. 50-move rule
		# 3. threefold repetition
		return self.is_insufficient_material()

	@property
	def result(self) -> GameStatus:
		if self.did_white_win():
			return GameStatus.WHITE_WON
		elif self.did_black_win():
			return GameStatus.BLACK_WON
		elif self.is_stalemate():
			return GameStatus.STALEMATE
		elif self.is_draw():
			return GameStatus.DRAW

		return GameStatus.ONGOING

if __name__ == '__main__':
	g = FENLoader('8/8/8/8/8/7k/7q/7K w - - - -').game
	g.update_legal_moves()
	g.switch_turn()
	g.update_legal_moves()
	g.switch_turn()

	res = GameResultChecker(g)
	print(res.is_stalemate())
	print(res.did_white_win())
	print(res.did_black_win())