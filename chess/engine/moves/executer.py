from __future__ import annotations
from typing import TYPE_CHECKING
from chess.engine.core import Coordinate
from chess.engine.board import Board
from chess.engine.moves.move import Move
from chess.engine.pieces.queen import Queen
from chess.engine.pieces.rook import Rook
from chess.engine.pieces.bishop import Bishop
from chess.engine.pieces.knight import Knight
from chess.engine.pieces.pawn import Pawn
from chess.engine.piece import Piece, PieceType
from chess.engine.castle import CastleInfo

if TYPE_CHECKING:
	from chess.engine.player import Player

class MoveExecuter:
	"""
    Executes a Move object on the board and updates all relevant state:
    - board positions
    - player pieces lists
    - castling
    - en passant
    - promotion (if input provided)
    """

	def __init__(self, player: Player) -> None:
		self.player: Player = player
		self.board: Board = player.board

	def _move_piece(self, move: Move) -> None:
		move.piece.has_moved = True

		if move.captured:
			move.captured.detach_from_game()
		self.board.move_piece(move.start, move.end)

	def execute(self, move: Move) -> None:
		"""
        Executes the move on the board.
        Assumes the move is already validated.
        """
		if move.is_castling:
			self._execute_castle(move)
		elif move.is_en_passant:
			self._execute_en_passant(move)
		else:
			self._move_piece(move)

		if move.is_promotion:
			self._execute_promotion(move)

	def undo(self, move: Move) -> None:
		if move.is_castling:
			self._undo_castle(move)
		elif move.is_en_passant:
			self._undo_en_passant(move)
		elif move.is_promotion:
			self._undo_promotion(move)
		else:
			self.board.move_piece(move.end, move.start)

		if move.captured:
			move.captured.attach_to_game()

	def redo(self, move: Move) -> None:
		self.execute(move)

	def _execute_castle(self, move: Move) -> None:
		if not move.castle_side:
			raise ValueError(
				'The provided move was not a castling move; ' +
				'yet attempted executing a castle move!'
			)

		king: Piece = move.piece

		info: CastleInfo = king.owner.castle_info
		info.update_info(move.castle_side)

		rook: Piece | None = self.board[info.rook_start].piece
		if not rook:
			raise ValueError('Rook not found!')

		self.board.move_piece(king.coordinate, info.king_end)
		self.board.move_piece(info.rook_start, info.rook_end)

		king.has_moved = True
		rook.has_moved = True

	def _execute_en_passant(self, move: Move) -> None:
		if not move.is_en_passant:
			raise ValueError(
				'The provided move was not an en passant move; ' +
				'yet attempted executing an en passant move!'
			)

		captured_pawn_coord: Coordinate = Coordinate(
			move.end.file, move.start.rank
		)
		captured: Piece | None = self.board[captured_pawn_coord].piece
		if captured:
			captured.detach_from_game()

		self.board.move_piece(move.start, move.end)

	def _execute_promotion(self, move: Move) -> None:
		if move.promotion is None:
			raise ValueError('Promotion piece must be provided as a PieceType!')

		pawn: Piece = move.piece
		self.player.remove_piece(pawn)

		# will automatically add to player and board
		match move.promotion:
			case PieceType.QUEEN:
				Queen(self.player, move.end)
			case PieceType.ROOK:
				Rook(self.player, move.end)
			case PieceType.BISHOP:
				Bishop(self.player, move.end)
			case PieceType.KNIGHT:
				Knight(self.player, move.end)

	def _undo_castle(self, move: Move) -> None:
		if not move.castle_side:
			raise ValueError(
				'Move was not a castling move! Cannot undo!'
			)

		king: Piece = move.piece
		king_end: Coordinate = move.start

		info: CastleInfo = king.owner.castle_info
		info.update_info(move.castle_side)

		self.board.move_piece(king.coordinate, king_end)
		self.board.move_piece(info.rook_end, info.rook_start)

		# BUG: should update has_moved for king and rook

	def _undo_en_passant(self, move: Move) -> None:
		captured_pawn_coord: Coordinate = Coordinate(
			move.end.file, move.start.rank
		)

		if not move.is_en_passant:
			raise ValueError('Invalid en passant move! Cannot undo it!')

		Pawn(move.piece.owner.opponent, captured_pawn_coord)

		self.board.move_piece(move.end, move.start)

	def _undo_promotion(self, move: Move) -> None:
		promotion_coord: Coordinate = move.end
		promoted_piece: Piece | None = self.board[promotion_coord].piece
		if not promoted_piece:
			raise ValueError('No promoted piece was found! Cannot undo!')

		self.player.remove_piece(promoted_piece)

		original_pawn: Piece = move.piece
		self.player.add_piece(original_pawn)

		# since the pawn was moved to the promotion square, its coordinate
		# should be restored back to the starting coordinate
		self.player.board.move_piece(original_pawn.coordinate, move.start)

