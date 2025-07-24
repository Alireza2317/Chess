from chess.game.game import Game
from chess.game.fen import FENLoader

def classic_setup() -> Game:
	return FENLoader('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1').game