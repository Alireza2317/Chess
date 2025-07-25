import pygame as pg
from chess.engine.core import Color
from chess.engine.piece import PieceType
from chess.gui.config import cfg

def load_piece_images() -> dict[tuple[Color, PieceType], pg.Surface]:
	images: dict[tuple[Color, PieceType], pg.Surface] = {}
	# Assume images are in 'assets/' folder named like 'wp.png', 'bk.png', etc.
	for color in ('w', 'b'):
		for piece in 'kqrbnp':
			name: str = f'{color}{piece}'
			path: str = f'assets/pieces/{cfg.pieces_theme}/{name}.png'
			key: tuple[Color, PieceType] = (
				Color.WHITE if color == 'w' else Color.BLACK,
				{
					'k': PieceType.KING,
					'q': PieceType.QUEEN,
					'r': PieceType.ROOK,
					'b': PieceType.BISHOP,
					'n': PieceType.KNIGHT,
					'p': PieceType.PAWN,
				}[piece]
			)
			images[key] = pg.transform.scale(
				pg.image.load(path), (cfg.square_size, cfg.square_size)
			)
	return images