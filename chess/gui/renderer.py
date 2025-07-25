import pygame as pg
from chess.engine.core import Coordinate, Color
from chess.engine.piece import PieceType
from chess.engine.board import Board
from chess.gui.config import cfg, RGBColor
from chess.gui.utils.asset_handler import load_piece_images

class Renderer:
	def __init__(self, board: Board):
		self.board: Board = board
		self.screen = pg.display.set_mode(cfg.screen_dims)
		self.screen.fill(cfg.bg_color)
		self.board_screen: pg.Surface = pg.Surface(cfg.board_dims)
		self.images: dict[
			tuple[Color, PieceType], pg.Surface
		] = load_piece_images()

		self.small_font = pg.font.Font(
			pg.font.get_default_font(), cfg.small_font_size
		)

		self.medium_font = pg.font.Font(
			pg.font.get_default_font(), cfg.font_size
		)

	def draw_coordinates(self, black_view: bool = False) -> None:
		""" draws the chess coordinates on the side of the board. """
		FILES: str = Coordinate.FILES
		RANKS: str = Coordinate.RANKS[::-1]
		if black_view:
			FILES = Coordinate.FILES[::-1]
			RANKS = Coordinate.RANKS

		pg.draw.rect(
			self.screen,
			cfg.coordinates_bg_color,
			(
				cfg.board_dims[0]-1,
				cfg.board_dims[1]-1,
				cfg.coordinates_width+1,
				cfg.coordinates_width+1
			)
		)
		pg.draw.line(
			self.screen,
			cfg.coordinates_text_color,
			start_pos=(cfg.board_dims[0]-2, cfg.board_dims[1]-1),
			end_pos=(
				cfg.board_dims[0]+cfg.coordinates_width-1,
				cfg.board_dims[1]+cfg.coordinates_width,
			),
			width=2
		)

		for file_i, file in enumerate(FILES):
			file_text: pg.Surface = self.small_font.render(
				file, True, cfg.coordinates_text_color
			)

			# file backgrounds
			pg.draw.rect(
				self.screen,
				cfg.coordinates_bg_color,
				(
					file_i * cfg.square_size,
					cfg.board_dims[1],
					cfg.square_size-1,
					cfg.coordinates_width
				)
			)

			# file texts
			self.screen.blit(
				file_text,
				(
					file_i * cfg.square_size + cfg.square_size//2 - 5,
					cfg.board_dims[1] + cfg.coordinates_width//2 - 6
				)
			)

		for rank_i, rank in enumerate(RANKS):
			rank_text: pg.Surface = self.small_font.render(
				rank, True, cfg.coordinates_text_color
			)
			# rank backgrounds
			pg.draw.rect(
				self.screen,
				cfg.coordinates_bg_color,
				(
					cfg.board_dims[0],
					rank_i * cfg.square_size,
					cfg.coordinates_width,
					cfg.square_size-1,
				)
			)

			# rank texts
			self.screen.blit(
				rank_text,
				(
					cfg.board_dims[0] + cfg.coordinates_width//2 - 6,
					rank_i * cfg.square_size + cfg.square_size//2 - 5,
				)
			)

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
				self.board_screen,
				color,
				rect
			)

	def draw_pieces(self) -> None:
		for coord, square in self.board:
			piece = square.piece
			if not piece:
				continue

			file_i, rank_i = coord.regular
			image: pg.Surface = self.images[piece.owner.color, piece.type]
			self.board_screen.blit(
				image, (file_i * cfg.square_size, rank_i * cfg.square_size)
			)

	def _create_square_rect(self) -> pg.Surface:
		rect_surface = pg.Surface(
			(cfg.square_size, cfg.square_size),
			pg.SRCALPHA
		)

		return rect_surface

	def _highlight_coord(self, rect: pg.Surface) -> None:
		center: tuple[int, int] = (cfg.square_size//2, cfg.square_size//2)
		radius = cfg.highlight_move_radius
		pg.draw.circle(
			rect, cfg.valid_color, center, radius
		)

	def _highlight_capture(self, rect: pg.Surface) -> None:
		center: tuple[int, int] = (cfg.square_size//2, cfg.square_size//2)
		radius = cfg.highlight_capture_radius
		pg.draw.circle(
			rect, cfg.valid_color, center, radius, width=10
		)

	def _blit_rect_on_coord(self, rect: pg.Surface, coord: Coordinate) -> None:
		file_i, rank_i = coord.regular
		left = file_i * cfg.square_size
		top = rank_i * cfg.square_size

		self.board_screen.blit(
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
