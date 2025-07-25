import pygame as pg
from chess.engine.core import Coordinate
from chess.engine.piece import Piece
from chess.game.game import Game
from chess.engine.setup import classic_setup
from chess.gui.renderer import Renderer
from chess.gui.input_handler import get_coord_from_mouse
from chess.gui.config import cfg

pg.init()
screen = pg.display.set_mode(cfg.dimensions)
pg.display.set_caption("Chess")


def handle_left_click(
		game: Game, current_selected: Coordinate | None
) -> Coordinate | None :
	new_selected: Coordinate | None = None
	coord: Coordinate | None = get_coord_from_mouse(pg.mouse.get_pos())
	if not coord:
		return None
	if current_selected:
		piece: Piece | None = game.board[current_selected].piece
		# allow move if selected square is a piece of current player
		if piece is not None and piece.owner == game.current_player:
			if coord in piece.legal_moves:
				try:
					game.play_turn(current_selected, coord)
					game.update_legal_moves()
				except Exception as e:
					print(f'Error while moving piece: {e}')
				new_selected = None
			elif coord == current_selected:
				new_selected = None  # Deselect if clicking same square
			else:
				other_piece: Piece | None = game.board[coord].piece
				# Basically selecting another of our own piece, while
				# we have a piece selected already
				if other_piece is not None and other_piece.owner == game.current_player:
					new_selected = coord  # Select it

		else: # selected empty square or enemy piece
			new_selected = None
	else: # No selected piece yet
		# Only select if square has a piece belonging to current player
		piece = game.board[coord].piece
		if piece and piece.owner == game.current_player:
			new_selected = coord
		else:
			new_selected = None

	return new_selected

def gui_loop(game: Game) -> None:
	game.update_legal_moves()
	renderer: Renderer = Renderer(game.board, screen)
	selected: Coordinate | None = None
	screen.fill(cfg.bg_color)
	while True:
		renderer.draw_board()
		renderer.draw_pieces()

		# Highlight legal moves for selected piece
		if selected:
			piece: Piece | None = game.board[selected].piece
			if piece and piece.owner == game.current_player:
				renderer.highlight_squares(piece.legal_moves)
			else:
				selected = None

		pg.display.update()

		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				exit()
			elif event.type == pg.MOUSEBUTTONDOWN:
				print(event.button)
				if event.button == 1: # left click
					selected = handle_left_click(game, selected)
				elif event.button == 3: # right click
					pass

if __name__ == '__main__':
	game = classic_setup()
	gui_loop(game)
