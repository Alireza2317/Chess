import pygame as pg
from chess.engine.core import Coordinate, Color
from chess.engine.piece import PieceType
from chess.engine.board import Board
from chess.gui.config import cfg, RGBColor

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

	def draw_board(self) -> None:
		for square in self.board.all_squares():
			file_i, rank_i = square.coordinate.regular
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

	def _create_square_rect(self) -> pg.Surface:
		rect_surface = pg.Surface(
			(cfg.square_size, cfg.square_size),
			pg.SRCALPHA
		)

		return rect_surface

	def _highlight_coord(self, rect: pg.Surface) -> None:
		center: tuple[int, int] = (cfg.square_size//2, cfg.square_size//2)
		radius = cfg.square_size/6.5
		pg.draw.circle(
			rect, cfg.valid_color, center, radius
		)

	def _highlight_capture(self, rect: pg.Surface) -> None:
		center: tuple[int, int] = (cfg.square_size//2, cfg.square_size//2)
		radius = cfg.square_size*0.49
		pg.draw.circle(
			rect, cfg.valid_color, center, radius, width=10
		)

	def _blit_rect_on_coord(self, rect: pg.Surface, coord: Coordinate) -> None:
		file_i, rank_i = coord.regular
		left = file_i * cfg.square_size
		top = rank_i * cfg.square_size

		self.screen.blit(
			rect,
			pg.Rect((left, top), rect.get_size())
		)

	def highlight_squares(self, coords: set[Coordinate]) -> None:
		for coord in coords:
			rect_surface: pg.Surface = self._create_square_rect()

			# capture
			if self.board[coord].piece:
				self._highlight_capture(rect_surface)
			# regular move
			else:
				self._highlight_coord(rect_surface)

			self._blit_rect_on_coord(rect_surface, coord)
