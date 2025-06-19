import sys
import pygame as pg
from gui.config import gui_cfg
from chess.components import Board, Coordinate, Color, Piece
from chess.pieces.king import King
from chess.pieces.queen import Queen
from chess.pieces.rook import Rook
from chess.pieces.bishop import Bishop
from chess.pieces.knight import Knight
from chess.pieces.pawn import Pawn


class ChessGUI:
	def __init__(self):
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

	def draw_image_at(self, surface: pg.Surface, filepath: str, rect: tuple[int, int]):
		"""
		puts the given image on the given surface and position.
		"""
		image = pg.image.load(filepath)

		scaled_image = pg.transform.scale(
			image,
			(gui_cfg.square_size, gui_cfg.square_size)
		)
		scaled_image_rect = scaled_image.get_rect()
		scaled_image_rect.x = rect[0]
		scaled_image_rect.y = rect[1]

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
		if isinstance(piece, King):
			filepath += 'k'
		elif isinstance(piece, Queen):
			filepath += 'q'
		elif isinstance(piece, Rook):
			filepath += 'r'
		elif isinstance(piece, Bishop):
			filepath += 'b'
		elif isinstance(piece, Knight):
			filepath += 'n'
		elif isinstance(piece, Pawn):
			filepath += 'p'

		# add file extension
		filepath += '.png'

		row, col = piece.coordinate.regular
		# if row==0 -> rank 1 -> y = (7-row)*square_size = 7*square_size
		# if row==1 -> rank 2 -> y = (7-row)*square_size = 6*square_size
		# if col==0 -> file a -> x = col*square_size = 0
		# if col==1 -> file b -> x = col*square_size = square_size
		rect: tuple[int, int] = (
			col * gui_cfg.square_size, (7-row) * gui_cfg.square_size
		)

		self.draw_image_at(self.board_screen, filepath, rect)

	def draw_coordinates(self):
		pass

	def create_dummy_board(self):
		# dummy board
		self.board = Board()
		for file in 'abcdefgh':
			Pawn(Color.WHITE, self.board, Coordinate(f'{file}2'))
			Pawn(Color.BLACK, self.board, Coordinate(f'{file}7'))

		King(Color.WHITE, self.board, Coordinate('e1'))
		King(Color.BLACK, self.board, Coordinate('e8'))

		Queen(Color.WHITE, self.board, Coordinate('d1'))
		Queen(Color.BLACK, self.board, Coordinate('d8'))

		Rook(Color.WHITE, self.board, Coordinate('a1'))
		Rook(Color.WHITE, self.board, Coordinate('h1'))
		Rook(Color.BLACK, self.board, Coordinate('a8'))
		Rook(Color.BLACK, self.board, Coordinate('h8'))

		Bishop(Color.WHITE, self.board, Coordinate('c1'))
		Bishop(Color.WHITE, self.board, Coordinate('f1'))
		Bishop(Color.BLACK, self.board, Coordinate('c8'))
		Bishop(Color.BLACK, self.board, Coordinate('f8'))

		Knight(Color.WHITE, self.board, Coordinate('b1'))
		Knight(Color.WHITE, self.board, Coordinate('g1'))
		Knight(Color.BLACK, self.board, Coordinate('b8'))
		Knight(Color.BLACK, self.board, Coordinate('g8'))


	def draw_board(self):
		self.board_screen = pg.surface.Surface(gui_cfg.dimensions)

		self.create_dummy_board()
		
		first = True
		for r, row in enumerate(reversed(self.board.board)):
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

		for row in self.board.board:
			for sq in row:
				if sq.piece:
					self.draw_piece(sq.piece)

		self.screen.blit(self.board_screen, (0, 0))

	def step(self):
		self.handle_events()

		self.draw_board()

		pg.display.update()
		self.clock.tick(gui_cfg.fps)


def main():
	game = ChessGUI()
	while True:
		game.step()

if __name__ == '__main__':
	main()