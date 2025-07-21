from __future__ import annotations
from typing import TYPE_CHECKING
from chess.engine.core import Coordinate
from chess.engine.pieces.king import King
from chess.engine.pieces.queen import Queen
from chess.engine.pieces.rook import Rook
from chess.engine.pieces.bishop import Bishop
from chess.engine.pieces.knight import Knight
from chess.engine.pieces.pawn import Pawn
from chess.game.game import Game
if TYPE_CHECKING:
	from chess.engine.player import Player

def fen_loader(fen: str) -> Game:
	fields: list[str] = fen.split()
	if len(fields) != 6:
		raise ValueError('Invalid FEN string!')

	pieces, turn, castle, ept, halfmove, fullmove = fields

	game: Game = Game()

	setup_pieces(game, pieces)

	handle_turn(game, turn)

	return game

def setup_pieces(game: Game, fen_pieces_part: str) -> None:
	# fen_pieces_part is the first field of FEN
	p_placements_ranks: list[str] = fen_pieces_part.split('/')
	if len(p_placements_ranks) != 8:
		raise ValueError('Invalid FEN string!')

	for rank, rank_pieces in zip(Coordinate.RANKS[::-1], p_placements_ranks):
		file_idx: int = 0
		file: str = Coordinate.FILES[file_idx]
		for piece in rank_pieces:
			# can be 'KQRBNPkqrbnp' or a number between 1 and 8
			# the number denotes the number of consecutive empty squares
			if piece.isdigit():
				file_idx += int(piece)
				continue

			player: Player
			if piece.isupper():
				player = game.white
			else:
				player = game.black

			file = Coordinate.FILES[file_idx]
			coord = Coordinate(file, rank)

			piece_map: dict[str, type] = {
				'k': King,
				'q': Queen,
				'r': Rook,
				'b': Bishop,
				'n': Knight,
				'p': Pawn,
			}

			piece_t: type = piece_map[piece.lower()]
			piece_t(player, coord)

			file_idx += 1

def handle_turn(game: Game, fen_turn: str) -> None:
	if len(fen_turn) != 1 or fen_turn not in 'wb':
		raise ValueError('Invalid FEN string!')

	if fen_turn == 'b':
		game.switch_turn()
