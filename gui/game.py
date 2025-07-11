import sys
import pygame as pg
from gui.config import gui_cfg, RGBColor
from chess.components import Color, Coordinate, Piece, PieceType, Square
from chess.game.game import ChessGame, GameEndState

class ChessGUI(ChessGame):
	def __init__(self) -> None:
		super().__init__()
		self.classic_setup()

		self.init_gui_elements()

		self.draw_coordinates()
		self.update_board()

		self.selected_piece: Piece | None = None

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
		self.board_screen.fill(gui_cfg.bg_color)

		self.clock = pg.time.Clock()
		self.main_font = pg.font.Font(
			pg.font.get_default_font(), gui_cfg.font_size
		)
		self.coordinates_font = pg.font.Font(
			pg.font.get_default_font(), gui_cfg.coordinates_font_size
		)

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

	def handle_click(self, pos: tuple[int, int]):
		"""
		handles gameplay and clicks. selects a piece first, then 
		highlights its valid moves.
		and then moves the piece to the selected coordinate.
		"""
		c: Coordinate | None = self.get_coordinate_on_click(pos)
		if not c: return

		if not self.selected_piece:
			p: Piece | None = self.board.get(c).piece
			# ignore if not our piece or has no moves
			if not (p and p.color == self.turn and p.valid_moves): return

			self.selected_piece = p

			self.highlight_valid_moves(self.selected_piece)
			return

		# here we already have selected a piece before
		if c in self.selected_piece.valid_moves:
			if gui_cfg.animation:
				self.animate_piece(self.selected_piece, c)
			self.move(self.selected_piece, c)
			self.selected_piece = None
			self.update_board()
			return

		# here we had a selected_piece but the move selection failed
		# it means it either was a misclick, or the player wanted to
		# select another piece
		p = self.board.get(c).piece
		if p and p.color == self.turn and p.valid_moves:
			if p == self.selected_piece:
				# selected the same piece, ignore and deselect
				self.update_board()
				self.selected_piece = None
				return

			# selected a new piece
			self.selected_piece = p
			self.update_board()
			self.highlight_valid_moves(self.selected_piece)
			return
		else: # completely wrong click
			# deselect piece
			self.selected_piece = None

		self.update_board()

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

			elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
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

	def animate_piece(
		self,
		piece: Piece,
		end_coord: Coordinate
	) -> None:
		""" animate the piece while moving across the board. """

		def get_initial_inc():
			"""
			get the initial increment(in pixels) for the animation.
			this is dynamic and based on the total distance.
			longer distances work better with smaller initial increment
			values and vice versa.
			"""
			srow, scol = start_coord.regular
			erow, ecol = end_coord.regular

			# coordinate-wise distance
			diff = max(abs(srow-erow), abs(scol-ecol)) # 1 <= diff <= 7

			# THESE RANGES CAN BE CHANGED, BUT CAREFULLY
			start = 0.04
			end = 0.10

			i = (end - start) / 6
			init_inc = round((start + (7-diff)*i) * gui_cfg.square_size)

			return init_inc

		def find_r(initial_inc: int, total_distance: int, n_frames: int):
			"""
			Newton-Raphson method to estimate the ratio of a geometric 
			series. this is used in	the animation transitions to make
			the animation slower at the beginning and faster in the end.
			"""
			def f(a, Sn, n, r):
				return a*(1 - r**n) - Sn*(1 - r)

			def fprime(a, Sn, n, r):
				return a*n*(r**(n-1)) + Sn

			if total_distance == 0: return 0

			a = initial_inc
			Sn = total_distance
			n = n_frames

			# initial guess
			rk = 1.5
			while True:
				rkp1 = rk + f(a, Sn, n, rk)/fprime(a, Sn, n, rk)
				if abs(rkp1 - rk) < 1e-4: return rkp1
				rk = rkp1

		# remove the piece to make it not stick to its starting position
		self.board.remove(piece.coordinate)
		self.update_board()

		piece_filepath: str = self.get_piece_image_path(piece)
		start_coord: Coordinate = piece.coordinate

		start_pos: tuple[int, int] = self.coord_to_pixels_xy(start_coord)
		end_pos: tuple[int, int] = self.coord_to_pixels_xy(end_coord)

		n_frames: int = max(int(gui_cfg.fps * gui_cfg.anim_duration), 1)

		x_inc: int = get_initial_inc()
		y_inc: int = x_inc
		x_inc_sign = -1 if (end_pos[0] - start_pos[0] < 0) else 1
		y_inc_sign = -1 if (end_pos[1] - start_pos[1] < 0) else 1

		rx: float = find_r(x_inc, abs(end_pos[0] - start_pos[0]), n_frames)
		ry: float = find_r(y_inc, abs(end_pos[1] - start_pos[1]), n_frames)

		current_pos_x, current_pos_y = start_pos

		for frame in range(n_frames):
			self.update_board()
			self._draw_image_at(
				self.board_screen,
				piece_filepath,
				(current_pos_x, current_pos_y)
			)
			self.update_screen()

			current_pos_x += (x_inc:=abs(int(x_inc * rx)) * x_inc_sign)
			current_pos_y += (y_inc:=abs(int(y_inc * ry)) * y_inc_sign)

	def get_piece_image_path(self, piece: Piece) -> str:
		"""
		returns the filepath of the image file for the given piece.
		"""
		filepath = f'assets/pieces/{gui_cfg.pieces_theme}/'

		# add color letter
		color = piece.color
		if color == Color.WHITE:
			filepath += 'w'
		else:
			filepath += 'b'

		# add piece type letter
		filepath += piece.piece_type.value

		# add file extension
		filepath += '.png'

		return filepath

	def coord_to_pixels_xy(self, coordinate: Coordinate) -> tuple[int, int]:
		"""
		returns the x and y pixel position for a given chess coordinate
		"""
		row, col = coordinate.regular
		# if row==0 -> rank 1 -> y = (7-row)*square_size = 7*square_size
		# if row==1 -> rank 2 -> y = (7-row)*square_size = 6*square_size
		# if col==0 -> file a -> x = col*square_size = 0
		# if col==1 -> file b -> x = col*square_size = square_size
		xy: tuple[int, int] = (
			col * gui_cfg.square_size, (7-row) * gui_cfg.square_size
		)

		return xy

	def draw_piece(self, piece: Piece):
		"""	draws the given piece on its coordinate. """
		filepath: str = self.get_piece_image_path(piece)

		xy: tuple[int, int] = self.coord_to_pixels_xy(piece.coordinate)

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

	def update_board(self):
		"""
		draws the whole game board.
		draws all the pieces of the game on appropriate coordinates
		and draws empty squares if a piece moved from it.
		"""
		for row in self.board.board_matrix:
			for square in row:
				self.draw_square(square)

	def update_screen(self):
		""" update all the dynamic gui elements. """
		self.screen.blit(self.board_screen, (0, 0))

		pg.display.update()
		self.clock.tick(gui_cfg.fps)

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
		if self.current_player.is_in_check():
			square = self.board.get(self.current_player.king.coordinate)
			self.draw_square(square, gui_cfg.in_check_color)

	def step(self) -> bool:
		""" one step in the chess game + gui updates."""
		self.white_p.update_valid_moves()
		self.black_p.update_valid_moves()
		if self.en_passant_target_square:
			for pawn in self.en_passant_pawns:
				pawn.valid_moves.append(self.en_passant_target_square)

		self.handle_events()

		self.update_screen()

		self.highlight_checked_king()

		state: GameEndState = self.check_state()
		if state != GameEndState.ONGOING:
			self.on_game_over(state)
			return True

		return False

def main():
	game = ChessGUI()
	game.load_FEN('k5r1/8/8/8/8/8/8/B5RK w - - 1 0')
	game.update_board()
	game.update_screen()
	while True:
		if game.step(): break

if __name__ == '__main__':
	main()