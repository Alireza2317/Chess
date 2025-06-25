import sys
import pygame as pg
from gui.config import gui_cfg
from chess.components import Board, Coordinate, Color, Piece, PieceType
#from chess.pieces.king import King
#from chess.pieces.queen import Queen
#from chess.pieces.rook import Rook
#from chess.pieces.bishop import Bishop
#from chess.pieces.knight import Knight
#from chess.pieces.pawn import Pawn
from chess.game.game import ChessGame

class ChessGUI(ChessGame):
	def __init__(self):
		super().__init__()

		self.init_gui_elements()

		self.classic_setup()

	def init_gui_elements(self):
		pg.init()
		pg.display.set_caption('Chess')

		self.screen = pg.display.set_mode(gui_cfg.dimensions)
		self.clock = pg.time.Clock()
		self.font = pg.font.Font(
			pg.font.get_default_font(), gui_cfg.font_size
		)

	def handle_events(self):
		# get user input in event loop
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()

			if event.type == pg.KEYDOWN:
				print('keydown')
				if event.key == pg.K_q:
					pg.quit()
					sys.exit()

	def _draw_image_at(
		self,
		surface: pg.Surface,
		filepath: str,
		xy: tuple[int, int]
	):
		"""
		puts the given image on the given surface and position.
		"""
		image = pg.image.load(filepath)

		scaled_image = pg.transform.scale(
			image,
			(gui_cfg.square_size, gui_cfg.square_size)
		)
		scaled_image_rect = scaled_image.get_rect()
		scaled_image_rect.x = xy[0]
		scaled_image_rect.y = xy[1]

		surface.blit(scaled_image, scaled_image_rect)

	def draw_piece(self, piece: Piece):
		"""
		draw the given piece on its coordinate.
		"""
		filepath = f'assets/pieces/{gui_cfg.pieces_theme}/'

		# add color letter
		color = piece.color
		if color == Color.WHITE:
			filepath += Color.WHITE.value
		else:
			filepath += Color.BLACK.value

		# add piece type letter
		if piece.piece_type == PieceType.KING:
			filepath += 'k'
		if piece.piece_type == PieceType.QUEEN:
			filepath += 'q'
		if piece.piece_type == PieceType.ROOK:
			filepath += 'r'
		if piece.piece_type == PieceType.BISHOP:
			filepath += 'b'
		if piece.piece_type == PieceType.KNIGHT:
			filepath += 'n'
		if piece.piece_type == PieceType.PAWN:
			filepath += 'p'

		# add file extension
		filepath += '.png'

		row, col = piece.coordinate.regular
		# if row==0 -> rank 1 -> y = (7-row)*square_size = 7*square_size
		# if row==1 -> rank 2 -> y = (7-row)*square_size = 6*square_size
		# if col==0 -> file a -> x = col*square_size = 0
		# if col==1 -> file b -> x = col*square_size = square_size
		xy: tuple[int, int] = (
			col * gui_cfg.square_size, (7-row) * gui_cfg.square_size
		)

		self._draw_image_at(self.board_screen, filepath, xy)

	def draw_coordinates(self):
		pass

	def draw_board(self):
		self.board_screen = pg.surface.Surface(gui_cfg.dimensions)

		first = True
		for r, row in enumerate(reversed(self.board.board_matrix)):
			for f, sq in enumerate(row):
				if sq.color == Color.BLACK:
					color = gui_cfg.black_color
				else:
					color = gui_cfg.white_color

				l = gui_cfg.square_size * 'abcdefgh'.index(sq.coordinate.file)
				t = gui_cfg.square_size * '12345678'.index(sq.coordinate.rank)


				pg.draw.rect(
					self.board_screen,
					color,
					((l, t), (gui_cfg.square_size, gui_cfg.square_size))
				)

				if first:
					c = self.font.render(sq.coordinate.file, True, (0, 0, 0))
					pg.draw.rect(
						self.board_screen,
						(150, 150, 150),
						((f*100 + 1, 800), (98, 24))
					)
					self.board_screen.blit(c, (f*100 + 48, 805))

			first = False

			c = self.font.render(sq.coordinate.rank, True, (0, 0, 0))
			pg.draw.rect(
				self.board_screen,
				(150, 150, 150),
				((800, r*100 + 1), (24, 98))
			)
			self.board_screen.blit(c, (805, r*100 + 50))

		for row in self.board.board_matrix:
			for sq in row:
				if sq.piece:
					self.draw_piece(sq.piece)

		self.screen.blit(self.board_screen, (0, 0))

	def update_screen(self):
		self.draw_board()

		pg.display.update()
		self.clock.tick(gui_cfg.fps)

	def step(self):
		self.handle_events()

		self.update_screen()


def main():
	game = ChessGUI()
	while True:
		game.step()

if __name__ == '__main__':
	main()