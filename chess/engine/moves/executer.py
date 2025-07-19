from __future__ import annotations
from typing import TYPE_CHECKING
from chess.engine.core import Coordinate
from chess.engine.board import Board
from chess.engine.moves.move import Move
from chess.engine.pieces.queen import Queen
from chess.engine.pieces.rook import Rook
from chess.engine.pieces.bishop import Bishop
from chess.engine.pieces.knight import Knight
from chess.engine.piece import Piece, PieceType

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
		if move.captured:
			self.player.opponent.remove_piece(move.captured)
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
			self.player.opponent.add_piece(move.captured)

	def redo(self, move: Move) -> None:
		pass
	
	def _execute_castle(self, move: Move) -> None:
		king: Piece = move.piece
		king_end: Coordinate = move.end

		rank: str = king.coordinate.rank
		rook_start_file: str
		rook_end_file: str
		if move.is_castle_kingside:
			rook_start_file = 'h'
			rook_end_file = 'f'
		elif move.is_castle_queenside:
			rook_start_file = 'a'
			rook_end_file = 'd'
		else:
			raise ValueError('Invalid castle move!')

		rook_start: Coordinate = Coordinate(rook_start_file, rank)
		rook_end: Coordinate = Coordinate(rook_end_file, rank)

		rook: Piece | None = self.board[rook_start].piece
		if not rook:
			raise ValueError('Rook not found!')

		self.board.move_piece(king.coordinate, king_end)
		self.board.move_piece(rook_start, rook_end)

	def _execute_en_passant(self, move: Move) -> None:
		captured_pawn_coord: Coordinate = Coordinate(
			move.end.file, move.start.rank
		)
		captured: Piece | None = self.board[captured_pawn_coord].piece
		if captured:
			self.player.opponent.remove_piece(captured)
			# ^ this also removes from board

		self.board.move_piece(move.start, move.end)

	def _execute_promotion(self, move: Move) -> None:
		if move.promotion is None:
			raise ValueError('Promotion must be provided as a PieceType!')

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
		if not move.is_castling:
			raise ValueError(
				'Move was not a castling move! Cannot undo!'
			)

		king: Piece = move.piece
		king_end: Coordinate = move.start

		rank: str = king.coordinate.rank
		rook_start_file: str
		rook_end_file: str
		if move.is_castle_kingside:
			rook_start_file = 'f'
			rook_end_file = 'h'
		elif move.is_castle_queenside:
			rook_start_file = 'd'
			rook_end_file = 'a'
		else:
			raise ValueError('Invalid undo castle move!')

		rook_start: Coordinate = Coordinate(rook_start_file, rank)
		rook_end: Coordinate = Coordinate(rook_end_file, rank)

		rook: Piece | None = self.board[rook_start].piece
		if not rook:
			raise ValueError('Rook not found!')

		self.board.move_piece(king.coordinate, king_end)
		self.board.move_piece(rook_start, rook_end)

	def _undo_en_passant(self, move: Move) -> None:
		captured_pawn_coord: Coordinate = Coordinate(
			move.end.file, move.start.rank
		)

		captured_pawn: Piece | None = self.board[captured_pawn_coord].piece
		if not captured_pawn or not move.is_en_passant:
			raise ValueError('Invalid undo en passant move!')

		self.player.opponent.add_piece(captured_pawn)

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

