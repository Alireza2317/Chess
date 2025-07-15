from __future__ import annotations
from chess.engine.core import Color, Coordinate
from chess.engine.board import Board
from chess.engine.piece import Piece
from chess.engine.player import Player
from chess.engine.moves.move import Move
from chess.engine.moves.history import MoveHistory
from chess.engine.moves.factory import create_move

class Game:
	def __init__(self) -> None:
		self.history: MoveHistory = MoveHistory()
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

		if to_coord not in piece.legal_moves:
			return False

		move: Move = create_move(piece, to_coord)
		self.current_player.executer.execute(move)
		self.history.record(move)

		return True

	def undo(self) -> bool:
		move: Move | None = self.history.undo()
		if not move:
			return False

		self.switch_turn()

		self.current_player.executer.undo(move)

		return True

	def redo(self) -> bool:
		move: Move | None = self.history.redo()
		if not move:
			return False

		self.switch_turn()

		self.current_player.executer.execute(move)

		return True

	def play_turn(self, from_coord: Coordinate, to_coord: Coordinate) -> bool:
		self.current_player.update_legal_moves()

		move_success: bool = self.move(from_coord, to_coord)

		if move_success:
			self.switch_turn()
			return True

		return False
