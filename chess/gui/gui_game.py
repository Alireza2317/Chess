import pygame as pg
from chess.engine.core import Coordinate, Color
from chess.engine.piece import Piece, PieceType
from chess.game.game import Game
from chess.engine.setup import classic_setup, custom_setup
from chess.gui.renderer import Renderer
from chess.gui.utils.mouse import get_coord
from chess.gui.utils.highlight import build_highlight_map
from chess.gui.promotion_selection import PromotionSelector

def check_promotion(game: Game, start: Coordinate, end: Coordinate) -> bool:
	piece: Piece | None = game.board[start].piece
	if not piece:
		return False

	if piece.type == PieceType.PAWN:
		promotion_rank: str = '8' if piece.owner.color == Color.WHITE else '1'
		if end.rank == promotion_rank:
			return True

	return False

def handle_left_click(
	game: Game, current_selected: Coordinate | None, renderer: Renderer | None = None
) -> Coordinate | None :
	new_selected: Coordinate | None = None
	coord: Coordinate | None = get_coord(pg.mouse.get_pos())
	if not coord:
		return None
	if current_selected:
		piece: Piece | None = game.board[current_selected].piece
		# allow move if selected square is a piece of current player
		if piece is not None and piece.owner == game.current_player:
			if coord in piece.legal_moves:
				try:
					promotion = None
					if renderer and check_promotion(game, piece.coordinate, coord):
						selector: PromotionSelector = PromotionSelector(
							renderer.screen,
							piece.owner.color,
							renderer.images
						)
						promotion = selector.show()

					game.play_turn(
						current_selected,
						coord,
						promotion=promotion
					)
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

def update_display(renderer: Renderer) -> None:
	renderer.screen.blit(renderer.board_screen, (0, 0))
	pg.display.update()

def gui_loop(game: Game) -> None:
	game.update_legal_moves()
	renderer: Renderer = Renderer(game.board)
	selected: Coordinate | None = None
	renderer.draw_coordinates()
	while True:
		renderer.draw_board()
		renderer.draw_pieces()

		if game.current_player.king:
			if game.current_player.is_in_check():
				renderer.highlight_check(game.current_player.king)

		# Highlight legal moves for selected piece
		if selected:
			piece: Piece | None = game.board[selected].piece
			if piece and piece.owner == game.current_player:
				renderer.highlight_squares(
					build_highlight_map(game, piece.legal_moves)
				)
			else:
				selected = None

		update_display(renderer)

		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				exit()
			elif event.type == pg.MOUSEBUTTONDOWN:
				if event.button == 1: # left click
					selected = handle_left_click(game, selected, renderer)
				elif event.button == 3: # right click
					pass
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_u:
					game.undo()
				elif event.key == pg.K_r:
					game.redo()

if __name__ == '__main__':
	pg.init()
	pg.display.set_caption("Chess")
	#game = classic_setup()
	game = custom_setup()
	gui_loop(game)
