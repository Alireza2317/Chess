from __future__ import annotations
from chess.engine.move import Move
from chess.engine.board import Board
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from chess.engine.player import Player

class MoveSimulator:
	"""
	A context manager that applies a move to the board and reverts it 
	automatically when the context ends.
	Useful for move validation, check detection, etc.
	"""
	def __init__(self, board: Board, move: Move, player: Player):
		self.board: Board = board
		self.move: Move = move
		self.player: Player = player
		self.opponent: Player = player.opponent


	def __enter__(self) -> MoveSimulator:
		# remove captured piece (if any)
		if self.move.captured:
			self.opponent.remove_piece(self.move.captured)

		self.board.move_piece(self.move.start, self.move.end)

		return self

	def __exit__(self, *args) -> None: # type: ignore
		# undo move
		self.board.move_piece(self.move.end, self.move.start)

		# restore captured piece (if any)
		if self.move.captured:
			self.opponent.add_piece(self.move.captured)
			self.board.place_piece(self.move.captured, self.move.end)