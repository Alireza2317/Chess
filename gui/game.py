import sys
import pygame as pg
import enum
from chess.pieces.king import King
from chess.pieces.queen import Queen
from chess.pieces.rook import Rook
from chess.pieces.bishop import Bishop
from chess.pieces.knight import Knight
from chess.pieces.pawn import Pawn
from gui.config import gui_cfg, RGBColor
from chess.components import Color, Coordinate, Piece, PieceType, Square
from chess.game.game import ChessGame, GameEndState

class Mode(enum.Enum):
	PIECE_SELECT = enum.auto()
	MOVE_SELECT = enum.auto()

class ChessGUI(ChessGame):
	def __init__(self) -> None:
		super().__init__()
		self.classic_setup()

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
				gui_cfg.dimensions[1]+gui_cfg.square_size
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
		self.main_font = pg.font.Font(
			pg.font.get_default_font(), gui_cfg.font_size
		)
		self.coordinates_font = pg.font.Font(
			pg.font.get_default_font(), gui_cfg.coordinates_font_size
		)

		self.draw_coordinates()

	def highlight_valid_moves(self, piece: Piece):
		"""	highlights the valid moves of the given piece on the board. """
		# mark the piece if it is not a checked king
		if piece != piece.player.king or not piece.player.is_in_check():
			self.draw_square(self.board.get(piece.coordinate), gui_cfg.selected_piece_color)

		for move in piece.valid_moves:
			square = self.board.get(move)

			row, col = square.coordinate.regular
			l =  col * gui_cfg.square_size
			t = (7-row) * gui_cfg.square_size

			rect = pg.Rect((l, t), (gui_cfg.square_size, gui_cfg.square_size))
			rect_surface = pg.Surface(rect.size, pg.SRCALPHA)
			center = (gui_cfg.square_size//2, gui_cfg.square_size//2)

			if not square.piece:
				radius = gui_cfg.square_size/6.5
				pg.draw.circle(
					rect_surface, gui_cfg.valid_color, center, radius
				)
			else: # capture
				radius = gui_cfg.square_size*0.49
				pg.draw.circle(
					rect_surface, gui_cfg.valid_color, center, radius, width=10
				)

			self.board_screen.blit(rect_surface, rect)

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
		if not Coordinate.is_valid(c_s): return None

		return Coordinate(c_s)

	def select_piece(self, coordinate: Coordinate) -> Piece | None:
		"""
		selects the piece that was clicked, highlights its valid moves
		on the board
		and returns the piece 
		"""
		p: Piece | None = self.board.get(coordinate).piece

		if p and self.turn == p.color:
			# then we are trying to check the valid moves
			# of our own piece

			if p.valid_moves:
				self.highlight_valid_moves(p)
				return p

		# no valid moves
		# or it was a misclick
		return None

	def select_move(self, coordinate: Coordinate):
		"""	selects the move that was clicked. """
		coords = self.selected_piece.valid_moves.copy() + [
			self.selected_piece.coordinate,
			self.selected_piece.player.king.coordinate
		]

		if coordinate in self.selected_piece.valid_moves:
			# trying to move our piece to one of the valid moves
			self.move(self.selected_piece, coordinate)

		self.update_board(coordinates=coords)

	def handle_click(self, pos: tuple[int, int]):
		c: Coordinate | None = self.get_coordinate_on_click(pos)
		if not c: return

		if self.mode == Mode.PIECE_SELECT:
			piece: Piece | None = self.select_piece(coordinate=c)
			if piece and piece.valid_moves:
				self.selected_piece = piece
				self.mode = Mode.MOVE_SELECT
			return

		if self.mode == Mode.MOVE_SELECT:
			self.select_move(coordinate=c)
			self.mode = Mode.PIECE_SELECT

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
				self.handle_click(event.pos)

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
				c = self.coordinates_font.render(
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

			c = self.coordinates_font.render(
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
		p = square.piece
		# if king is in check, do not draw the default square color
		if ((p and p == p.player.king and p.player.is_in_check()) and color is None): return

		if color is None:
			if square.color == Color.BLACK:
				color = gui_cfg.black_color
			else:
				color = gui_cfg.white_color

		row, col = square.coordinate.regular
		l = gui_cfg.square_size * col
		t = gui_cfg.square_size * (7-row)

		rect = pg.Rect(l, t, gui_cfg.square_size, gui_cfg.square_size)
		rect_surface = pg.Surface(rect.size, pg.SRCALPHA)
		pg.draw.rect(rect_surface, color, rect_surface.get_rect())
		self.board_screen.blit(rect_surface, rect)

		# border
		pg.draw.rect(
			self.board_screen,
			gui_cfg.bg_color,
			((l, t), (gui_cfg.square_size, gui_cfg.square_size)), width=1
		)

		if square.piece:
			self.draw_piece(square.piece)

	def update_board(self, /, all_board: bool = False, coordinates: list[Coordinate] | None = None):
		"""
		draws the whole game board.
		draws all the pieces of the game on appropriate coordinates
		and draws empty squares if a piece moved from it.
		"""
		if all_board:
			for row in self.board.board_matrix:
				for square in row:
					self.draw_square(square)
		elif coordinates:
			for c in coordinates:
				sq = self.board.get(c)
				self.draw_square(sq)

		self.screen.blit(self.board_screen, (0, 0))

	def update_screen(self):
		""" update all the dynamic gui elements. """
		self.update_board()

		pg.display.update()
		self.clock.tick(gui_cfg.fps)

	def custom_setup(self):
		King(self.white_p, Coordinate('e1'))
		King(self.black_p, Coordinate('e8'))
		Pawn(self.white_p, Coordinate('b7'))

	def set_promotion_piece(self) -> None:
		"""
		draw 4 buttons representing options for promotion pieces.
		and setting self.promotion_piece to the corresponding piece type
		"""

		buttons: list[pg.Rect] = []
		pieces: list[PieceType] = [
			PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT
		]
		y_pos = gui_cfg.dimensions[1]+gui_cfg.square_size//2
		for x, pt in enumerate(pieces, 1):
			x_pos = int((x/4) * gui_cfg.dimensions[0] * 0.6 - 50)
			r = pg.Rect(x_pos, y_pos, 90, 30)
			buttons.append(r)
			pg.draw.rect(
				self.screen,
				(200, 200, 200),
				rect=r,
				border_radius=2,
			)

			text = self.main_font.render(
				pt.name.title(), True, gui_cfg.bg_color
			)
			self.screen.blit(text, (x_pos+10, y_pos+7))

		pg.display.update()
		index = None
		while True:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit()
					sys.exit()
				elif event.type == pg.MOUSEBUTTONDOWN:
					for btn in buttons:
						if btn.collidepoint(*event.pos):
							index = buttons.index(btn)
			if index is not None: break

		self.screen.fill(gui_cfg.bg_color)
		self.promotion_piece = pieces[index]

	def on_game_over(self, state: GameEndState):
		color: RGBColor = (255, 255, 255)

		if state == GameEndState.WHITE_WON:
			text = 'White Won!'
		elif state == GameEndState.BLACK_WON:
			text = 'Black Won!'
		elif state == GameEndState.DRAW:
			text = 'Draw!'

		text_renderd = self.main_font.render(
			text, True, color
		)

		self.screen.blit(
			text_renderd,
			(
				gui_cfg.dimensions[0]//2 - 4*len(text),
				gui_cfg.dimensions[1]+ gui_cfg.coordinates_width + 15
			)
		)
		self.update_screen()
		while True:
			self.handle_events()

	def highlight_checked_king(self):
		player = self.white_p if self.turn == Color.WHITE else self.black_p
		if player.is_in_check():
			square = self.board.get(player.king.coordinate)
			self.draw_square(square, gui_cfg.in_check_color)

	def step(self) -> bool:
		""" one step in the chess game + gui updates."""
		self.handle_events()

		self.update_screen()

		self.white_p.update_valid_moves()
		self.black_p.update_valid_moves()

		self.highlight_checked_king()

		state: GameEndState = self.check_state()
		if state != GameEndState.ONGOING:
			self.on_game_over(state)
			return True

		return False

def main():
	game = ChessGUI()
	while True:
		if game.step(): break

if __name__ == '__main__':
	main()