from __future__ import annotations
import enum
from chess.engine.core import Color, Coordinate
from chess.engine.board import Board
from chess.engine.piece import Piece, PieceType
from chess.engine.player import Player
from chess.engine.moves.move import Move
from chess.engine.moves.history import MoveHistory
from chess.engine.moves.simulator import MoveSimulator
from chess.engine.moves.factory import create_move
from chess.engine.en_passant import add_en_passant_if_possible

class GameStatus(enum.Enum):
	WHITE_WON = enum.auto()
	BLACK_WON = enum.auto()
	DRAW = enum.auto()
	STALEMATE = enum.auto()
	ONGOING = enum.auto()

class Game:
	def __init__(self) -> None:
		self.history: MoveHistory = MoveHistory()
		self._last_move: Move | None = None # for en passant
		self.board: Board = Board()
		self.white: Player = Player(self.board, Color.WHITE)
		self.black: Player = Player(self.board, Color.BLACK)

		self.white.set_opponent(self.black)

		self.turn: Color = Color.WHITE

	@property
	def current_player(self) -> Player:
		return self.white if self.turn == Color.WHITE else self.black

	@property
	def last_move(self) -> Move | None:
		# for the sake of en passant
		return self.history.last() or self._last_move

	def update_legal_moves(self) -> None:
		"""
		Update each piece's legal_moves set for the current player.
		A legal move:
		- Is within the board
		- Does not leave the player in check
		"""
		player: Player = self.current_player

		for piece in player.pieces:
			legal_moves: set[Coordinate] = set()

			for target in piece.all_moves():
				move: Move = create_move(piece, target, simulation=True)
				if move.captured and move.captured.type == PieceType.KING:
					continue # do not simulate capturing a king!

				# simulate move
				with MoveSimulator(player, move):
					if not player.is_in_check():
						legal_moves.add(target)

			piece.legal_moves = legal_moves

			# check en passant move
			if piece.type == PieceType.PAWN and self.last_move:
				add_en_passant_if_possible(piece, self.last_move)

		player._add_castling_moves()

	def switch_turn(self) -> None:
		self.turn = ~self.turn

	def move(
		self,
		from_coord: Coordinate,
		to_coord: Coordinate,
		*,
		promotion: PieceType | None = None
	) -> bool:
		piece: Piece | None = self.board[from_coord].piece

		# unable to move
		if not piece or piece.owner is not self.current_player:
			return False

		if to_coord not in piece.legal_moves:
			return False

		move: Move = create_move(piece, to_coord, promotion=promotion)
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

		self.current_player.executer.redo(move)

		# BUG: redoing a capture of a promoted piece leads to error
		return True

	def play_turn(
		self,
		from_coord: Coordinate,
		to_coord: Coordinate,
		*,
		promotion: PieceType | None = None
	) -> bool:
		self.update_legal_moves()

		move_success: bool = self.move(from_coord, to_coord, promotion=promotion)

		if move_success:
			self.switch_turn()
			return True

		return False
