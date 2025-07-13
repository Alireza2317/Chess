from __future__ import annotations
from chess_refactored.engine.core import Board, Color, Coordinate
from chess_refactored.engine.piece import Piece
from chess_refactored.engine.player import Player

class Game:
	def __init__(self) -> None:
		self.board: Board = Board()
		self.white: Player = Player(self.board, Color.WHITE)
		self.black: Player = Player(self.board, Color.BLACK)

		self.white.set_opponent(self.black)

		self.turn: Color = Color.WHITE

	@property
	def current_player(self) -> Player:
		return self.white if self.turn == Color.WHITE else self.black

	def switch_turn(self) -> None:
		self.turn = ~self.turn

	def move(self, from_coord: Coordinate, to_coord: Coordinate) -> bool:
		piece: Piece | None = self.board[from_coord].piece

		# unable to move
		if not piece or piece.owner is not self.current_player:
			return False

		piece.update_legal_moves() # TODO

		if to_coord not in piece.legal_moves: # TODO
			return False

		captured_piece: Piece | None = self.board[to_coord].piece
		if captured_piece:
			self.current_player.opponent.remove_piece(captured_piece)

		self.board.move_piece(from_coord, to_coord)

		self.switch_turn()

		return True