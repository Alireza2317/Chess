import pygame as pg
from chess.engine.core import Color
from chess.engine.piece import PieceType
from chess.gui.config import cfg

class PromotionSelector:
	def __init__(
		self,
		screen: pg.Surface,
		color: Color,
		piece_images: dict[tuple[Color, PieceType], pg.Surface]
	):
		self.screen: pg.Surface = screen
		self.color: Color = color
		self.images: dict[tuple[Color, PieceType], pg.Surface] = piece_images

		self.options: list[PieceType] = [
			PieceType.QUEEN,
			PieceType.ROOK,
			PieceType.BISHOP,
			PieceType.KNIGHT,
		]

		self.option_rects: list[pg.Rect] = []

	def show(self) -> PieceType | None:
		selected: PieceType | None = None

		# Layout
		WIDTH: int = int((len(self.options)+1) * cfg.square_size)
		HEIGHT: int = cfg.square_size
		x: int = cfg.board_dims[0]//2 - WIDTH//2
		y: int = cfg.board_dims[1]//2 - HEIGHT//2

		background: pg.Surface = pg.Surface((WIDTH, HEIGHT))
		background.fill(cfg.popup_color)
		border_rect = background.get_rect(topleft=(x,y)) #?

		self.option_rects.clear()
		for i, ptype in enumerate(self.options):
			image: pg.Surface = self.images[self.color, ptype]
			rect: pg.Rect = pg.Rect(
				x + i*(WIDTH//len(self.options)) + cfg.square_size//8,
				y,
				cfg.square_size,
				cfg.square_size
			)
			self.option_rects.append(rect)
			background.blit(
				image, (i*(WIDTH//len(self.options)) + cfg.square_size//8, 0)
			)


		self.screen.blit(background, border_rect.topleft)
		pg.display.update()

		while selected is None:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit()
					exit()
				elif event.type == pg.MOUSEBUTTONDOWN:
					if event.button == 1:
						for i, rect in enumerate(self.option_rects):
							if rect.collidepoint(pg.mouse.get_pos()):
								selected = self.options[i]

		return selected