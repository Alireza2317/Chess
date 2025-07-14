from __future__ import annotations
from chess.engine.core import Color, Coordinate
from chess.engine.board import Board
from chess.engine.piece import Piece
from chess.engine.player import Player
from chess.engine.moves.move import Move
from chess.engine.moves.executer import MoveExecuter
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

		self.current_player.update_legal_moves()

		if to_coord not in piece.legal_moves:
			return False

		executer: MoveExecuter = MoveExecuter(self.current_player)
		move: Move = create_move(piece, to_coord)
		executer.execute(move)
		self.history.record(move)

		self.switch_turn()

		return True