import pygame as pg
from chess.engine.core import Coordinate, Color
from chess.engine.piece import PieceType
from chess.engine.board import Board
from gui.config import cfg, RGBColor # type: ignore

class Renderer:
	def __init__(self, board: Board, screen: pg.Surface):
		self.board: Board = board
		self.screen: pg.Surface = screen
		self.images: dict[
			tuple[Color, PieceType], pg.Surface
		] = self._load_piece_images()

	def _load_piece_images(self) -> dict[tuple[Color, PieceType], pg.Surface]:
		images: dict[tuple[Color, PieceType], pg.Surface] = {}
		# Assume images are in 'assets/' folder named like 'wP.png', 'bK.png', etc.
		for color in ('w', 'b'):
			for piece in 'kqrbnp':
				name: str = f'{color}{piece}'
				path: str = f'assets/{name}.png'
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

	def draw_board(self) -> None:
		for square in self.board.all_squares():
			file_i: int = Coordinate.FILES.index(square.coordinate.file)
			rank_i: int = Coordinate.RANKS.index(square.coordinate.rank)
			rect: tuple[int, int, int, int] = (
				file_i * cfg.square_size, rank_i * cfg.square_size,
				cfg.square_size, cfg.square_size
			)
			color: RGBColor
			if square.color == Color.WHITE:
				color = cfg.white_color
			else:
				color = cfg.black_color
			pg.draw.rect(
				self.screen,
				color,
				rect
			)

	def draw_pieces(self) -> None:
		for coord, square in self.board:
			piece = square.piece
			if not piece:
				continue

			file: int = Coordinate.FILES.index(coord.file)
			rank: int = 7 - Coordinate.RANKS.index(coord.rank)
			image: pg.Surface = self.images[piece.owner.color, piece.type]
			self.screen.blit(
				image, (file * cfg.square_size, rank * cfg.square_size)
			)

	def highlight_squares(self, coords: set[Coordinate]) -> None:
		for coord in coords:
			file: int = Coordinate.FILES.index(coord.file)
			rank: int = 7 - Coordinate.RANKS.index(coord.rank)
			rect = pg.Rect(
				file * cfg.square_size, rank * cfg.square_size,
				cfg.square_size, cfg.square_size
			)
			pg.draw.rect(self.screen, cfg.valid_color, rect, width=4)
