from chess.game.game import Game
from chess.game.fen import FENLoader

def classic_setup() -> Game:
	return FENLoader('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1').game

def custom_setup() -> Game:
	return FENLoader('rnbqkbnr/pPpppp1p/8/8/8/8/P1PPPPpP/RNBQKBNR w KQkq - 0 1').game
