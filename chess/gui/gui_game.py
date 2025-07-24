import pygame as pg
from chess.engine.core import Coordinate
from chess.game.game import Game
from chess.engine.setup import classic_setup
from chess.gui.renderer import Renderer
from chess.gui.input_handler import get_coord_from_mouse
from chess.gui.config import cfg

pg.init()
screen = pg.display.set_mode(cfg.dimensions)
pg.display.set_caption("Chess")


def gui_loop(game: Game) -> None:
	renderer: Renderer = Renderer(game.board, screen)
	selected: Coordinate | None = None

	running: bool = True
	while running:
		screen.fill(cfg.bg_color)
		renderer.draw_board()
		renderer.draw_pieces()

		if selected:
			piece: Piece | None = game.board[selected].piece
			if piece:
				renderer.highlight_squares({selected, *piece.legal_moves})

		pg.display.flip()

		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False

			elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
				coord: Coordinate = get_coord_from_mouse(pg.mouse.get_pos())
				if not coord:
					continue

				piece = game.board[coord].piece

				if selected and piece and coord in piece.legal_moves:
					game.play_turn(selected, coord)
					selected = None
				elif piece and piece.owner == game.current_player:
					game.update_legal_moves()
					selected = coord
				else:
					selected = None

	pg.quit()

if __name__ == '__main__':
	game = classic_setup()
	gui_loop(game)
