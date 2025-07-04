import sys
import pygame as pg
from copy import deepcopy
from enum import Enum
from chess.pieces.pawn import Pawn
from gui.config import gui_cfg, RGBColor
from chess.components import Color, Coordinate, Piece, PieceType, Square
from chess.game.game import ChessGame

class Mode(Enum):
	PIECE_SELECT = 'p'
	MOVE_SELECT = 'm'

class ChessGUI(ChessGame):
	def __init__(self):
		super().__init__()
		self.classic_setup()

		self.old_board = deepcopy(self.board)

		self.init_gui_elements()

		self.draw_coordinates()
		self.update_board(all_board=True)

		self.mode: Mode = Mode.PIECE_SELECT

	def init_gui_elements(self):
		"""
		initialize important gui properties and functionalities.
		"""
		pg.init()
		pg.display.set_caption('Chess')

		self.screen = pg.display.set_mode(
			(
				gui_cfg.dimensions[0]+gui_cfg.coordinates_width,
				gui_cfg.dimensions[1]+gui_cfg.square_size//2
			)
		)
		self.screen.fill(gui_cfg.bg_color)

		board_size = (
			gui_cfg.dimensions[0]+gui_cfg.coordinates_width,
			gui_cfg.dimensions[1]+gui_cfg.coordinates_width
		)
		self.board_screen = pg.surface.Surface(board_size)
		self.board_screen.fill((0, 0, 0))

		self.clock = pg.time.Clock()
		self.font = pg.font.Font(
			pg.font.get_default_font(), gui_cfg.font_size
		)

	def highlight_valid_moves(self, piece: Piece):
		"""	highlights the valid moves of the given piece on the board. """
		for move in piece.valid_moves:
			square = self.board.get(move)

			self.draw_square(square, gui_cfg.valid_color)

			# redraw the opponent pieces, since the line above will
			# kind of remove them from the board
			if square.piece:
				self.draw_piece(square.piece)

	def get_coordinate_on_click(self, pos: tuple[int, int]) -> Coordinate | None:
		"""
		returns a chess coordinate based on the user's click.
		returns None if the click is outside the board. 
		"""
		x, y = pos

		row = 7
		col = 0
		for i in range(1, 8+1):
			if x < i*gui_cfg.square_size: break
			col += 1

		for i in range(1, 8+1):
			if y < i*gui_cfg.square_size: break
			row -= 1

		file = chr(ord('a')+col)
		rank = chr(ord('1')+row)

		c_s: str = f'{file}{rank}'
		if not Coordinate.is_valid(c_s):
			print('clicked outside the chess board.')
			return None

		return Coordinate(c_s)

	def select_piece(self, coordinate: Coordinate) -> Piece | None:
		"""
		selects the piece that was clicked, highlights its valid moves
		on the board
		switches modes
		and returns the piece 
		"""
		self.update_board(all_board=True)
		p: Piece | None = self.board.get(coordinate).piece

		if self.mode != Mode.PIECE_SELECT: return

		if p and self.turn == p.color:
			# then we are trying to check the valid moves
			# of our own piece
			self.highlight_valid_moves(p)
			print(f'highlighting {p.color} moves')

		# switch modes
		self.mode = Mode.MOVE_SELECT

		return p

	def select_move(self, piece: Piece, coordinate: Coordinate):
		"""
		selects the move that was clicked
		switches modes
		returns the piece and the coordinate
		"""
		if self.mode != Mode.MOVE_SELECT: return

		if coordinate not in piece.valid_moves: return

		# trying to move our piece to one of the valid moves
		# self.move(piece, coordinate) and handling moves and captures
		print(f'moving {piece} to {coordinate}')

		# switch modes
		self.mode = Mode.PIECE_SELECT

		return piece, coordinate

	def handle_click(self, pos: tuple[int, int]):
		#self.update_board(all_board=True)

		c: Coordinate | None = self.get_coordinate_on_click(pos)
		if not c: return

		piece: Piece | None = self.select_piece(coordinate=c)
		if not piece: return

		self.select_move(piece, coordinate=c)

	def handle_events(self):
		""" handle user events. """
		# get user input in event loop
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()

			elif event.type == pg.KEYDOWN:
				print('keydown')
				if event.key == pg.K_q:
					pg.quit()
					sys.exit()

			elif event.type == pg.MOUSEBUTTONUP:
				#self.handle_click(event.pos)
				c = self.get_coordinate_on_click(event.pos)
				if not c: continue
				p = self.board.get(c).piece
				if not p: continue
				if p.color != self.turn: continue
				if p.valid_moves:
					self.update_board(all_board=True)
					self.highlight_valid_moves(p)

	def _draw_image_at(
		self,
		surface: pg.Surface,
		filepath: str,
		xy: tuple[int, int]
	):
		"""
		puts the given image in `filepath` on the given surface and position.
		"""
		try:
			image = pg.image.load(filepath)
		except Exception as e:
			print(f'error loading the piece image in {filepath}: {e}')
			return

		scaled_image = pg.transform.scale(
			image,
			(gui_cfg.square_size, gui_cfg.square_size)
		)
		scaled_image_rect = scaled_image.get_rect()
		scaled_image_rect.x = xy[0]
		scaled_image_rect.y = xy[1]

		surface.blit(scaled_image, scaled_image_rect)

	def draw_piece(self, piece: Piece):
		"""	draws the given piece on its coordinate. """
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
		""" draws the chess coordinates on the side of the board. """
		for rank, row in enumerate(reversed(self.board.board_matrix)):
			for file, square in enumerate(row):
				c = self.font.render(
					square.coordinate.file, True, gui_cfg.coordinates_text_color
				)

				pg.draw.rect(
					self.board_screen,
					gui_cfg.coordinates_bg_color,
					(
						(file*gui_cfg.square_size + 1, gui_cfg.dimensions[1]),
						(gui_cfg.square_size-2, gui_cfg.coordinates_width)
					)
				)
				self.board_screen.blit(
					c,
					(
						file*gui_cfg.square_size + 2*gui_cfg.coordinates_width,
						gui_cfg.dimensions[1]+5
					)
				)

			c = self.font.render(
				square.coordinate.rank, True, gui_cfg.coordinates_text_color
			)

			pg.draw.rect(
				self.board_screen,
				gui_cfg.coordinates_bg_color,
				(
					(gui_cfg.dimensions[0], rank*gui_cfg.square_size + 1),
					(gui_cfg.coordinates_width, gui_cfg.square_size-2)
	 			)
			)
			self.board_screen.blit(
				c,
				(
					gui_cfg.dimensions[0]+6,
					rank*gui_cfg.square_size + gui_cfg.square_size/2
				)
			)
		pg.draw.rect(
			self.board_screen,
			gui_cfg.coordinates_bg_color,
			(
				gui_cfg.dimensions[0]-1,
				gui_cfg.dimensions[1]-1,
				gui_cfg.coordinates_width+1,
				gui_cfg.coordinates_width+1
			)
		)

		pg.draw.line(
			self.board_screen,
			(0, 0, 0),
			start_pos=gui_cfg.dimensions,
			end_pos=(
				gui_cfg.dimensions[0]+gui_cfg.coordinates_width,
				gui_cfg.dimensions[1]+gui_cfg.coordinates_width,
			),
			width=2
		)

	def draw_square(self, square: Square, color: RGBColor | None = None):
		""" draws the given square object. """
		if color is None:
			if square.color == Color.BLACK:
				color = gui_cfg.black_color
			else:
				color = gui_cfg.white_color

		row, col = square.coordinate.regular
		l = gui_cfg.square_size * col
		t = gui_cfg.square_size * (7-row)

		# draw board squares
		pg.draw.rect(
			self.board_screen,
			color,
			((l, t), (gui_cfg.square_size, gui_cfg.square_size))
		)
		# border
		pg.draw.rect(
			self.board_screen,
			gui_cfg.bg_color,
			((l, t), (gui_cfg.square_size, gui_cfg.square_size)), width=1
		)

	def update_board(self, all_board: bool = False):
		"""
		draws the whole game board.
		draws all the pieces of the game on appropriate coordinates
		and draws empty squares if a piece moved from it.
		"""
		self.draw_coordinates()
		for i, row in enumerate(self.board.board_matrix):
			for j, square in enumerate(row):
				# skip if not changed OR not asked to draw all board
				if (self.old_board.board_matrix[i][j] == square) and not(all_board):
					continue

				# draw board squares
				self.draw_square(square)

				# draw pieces
				if square.piece:
					self.draw_piece(square.piece)

		self.screen.blit(self.board_screen, (0, 0))

	def update_screen(self):
		""" update all the dynamic gui elements. """
		self.update_board()

		pg.display.update()
		self.clock.tick(gui_cfg.fps)

	def step(self):
		""" one step in the chess game + gui updates."""
		self.handle_events()

		self.update_screen()

		# set self.old_board
		self.old_board = deepcopy(self.board)

def main():
	game = ChessGUI()
	while True:
		if game.step(): break

if __name__ == '__main__':
	main()