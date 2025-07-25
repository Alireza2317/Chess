import pygame as pg
from chess.engine.core import Coordinate, Color
from chess.engine.piece import PieceType
from chess.engine.board import Board
from chess.gui.config import cfg, RGBColor

class Renderer:
	def __init__(self, board: Board):
		self.board: Board = board
		self.screen = pg.display.set_mode((900, 900))
		self.screen.fill((0,0,0))
		self.board_screen: pg.Surface = pg.Surface(cfg.dimensions)
		self.images: dict[
			tuple[Color, PieceType], pg.Surface
		] = self._load_piece_images()

		self.small_font = pg.font.Font(
			pg.font.get_default_font(), cfg.coordinates_font_size
		)

		self.medium_font = pg.font.Font(
			pg.font.get_default_font(), cfg.font_size
		)

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

	def draw_coordinates(self) -> None:
		""" draws the chess coordinates on the side of the board. """
		pg.draw.rect(
			self.screen,
			cfg.coordinates_bg_color,
			(
				cfg.dimensions[0]-1,
				cfg.dimensions[1]-1,
				cfg.coordinates_width+1,
				cfg.coordinates_width+1
			)
		)
		pg.draw.line(
			self.screen,
			cfg.coordinates_text_color,
			start_pos=(cfg.dimensions[0]-2, cfg.dimensions[1]-1),
			end_pos=(
				cfg.dimensions[0]+cfg.coordinates_width-1,
				cfg.dimensions[1]+cfg.coordinates_width,
			),
			width=2
		)

		for file_i, file in enumerate(Coordinate.FILES):
			file_text: pg.Surface = self.small_font.render(
				file, True, cfg.coordinates_text_color
			)

			# file backgrounds
			pg.draw.rect(
				self.screen,
				cfg.coordinates_bg_color,
				(
					file_i * cfg.square_size,
					cfg.dimensions[1],
					cfg.square_size-1,
					cfg.coordinates_width
				)
			)

			# file texts
			self.screen.blit(
				file_text,
				(
					file_i * cfg.square_size + cfg.square_size//2 - 5,
					cfg.dimensions[1] + cfg.coordinates_width//2 - 6
				)
			)

		for rank_i, rank in enumerate(reversed(Coordinate.RANKS)):
			rank_text: pg.Surface = self.small_font.render(
				rank, True, cfg.coordinates_text_color
			)
			# rank backgrounds
			pg.draw.rect(
				self.screen,
				cfg.coordinates_bg_color,
				(
					cfg.dimensions[0],
					rank_i * cfg.square_size,
					cfg.coordinates_width,
					cfg.square_size-1,
				)
			)

			# rank texts
			self.screen.blit(
				rank_text,
				(
					cfg.dimensions[0] + cfg.coordinates_width//2 - 6,
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

			file: int = Coordinate.FILES.index(coord.file)
			rank: int = 7 - Coordinate.RANKS.index(coord.rank)
			image: pg.Surface = self.images[piece.owner.color, piece.type]
			self.board_screen.blit(
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
