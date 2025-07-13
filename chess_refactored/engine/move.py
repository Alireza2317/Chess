from __future__ import annotations
from chess_refactored.engine.core import Coordinate
from chess_refactored.engine.piece import Piece, PieceType
from chess_refactored.engine.pieces.pawn import Pawn
from chess_refactored.engine.pieces.king import King
from chess_refactored.engine.pieces.rook import Rook


class Move:
	def __init__(
			self,
			piece: Piece,
			start: Coordinate,
			end: Coordinate,
			captured: Piece | None = None,
			promotion: PieceType | None = None,
			en_passant: bool = False,
			castling: bool = False
	):
		self.piece: Piece = piece
		self.start: Coordinate = start
		self.end: Coordinate = end
		self.captured: Piece | None = captured

		self.promotion: PieceType | None = promotion
		self.en_passant: bool = en_passant
		self.castling: bool = castling

		modes: list[bool] = [
			(self.promotion is not None), self.en_passant, self.castling
		]
		if sum(modes) > 1:
			raise ValueError(
				'Only one of promotion, en_passant, and castling can be True!'
			)

	def is_promotion(self) -> bool:
		return (
			self.promotion is not None and
			self.piece.piece_type == PieceType.PAWN
		)

	def is_castle_kingside(self) -> bool:
		return self.castling and self.end.file == 'g'

	def is_castle_queenside(self) -> bool:
		return self.castling and self.end.file == 'c'

	def is_castle(self) -> bool:
		return self.castling

	def __repr__(self) -> str:
		desc: str = f'{self.piece} from {self.start} to {self.end}'

		if self.captured:
			desc += f', captured {self.captured}'
		elif self.promotion:
			desc += f', promoted to {self.promotion.name.title()}'
		elif self.en_passant:
			desc += ', en passant'
		elif self.is_castle_kingside():
			desc += ', castling kingside'
		elif self.is_castle_queenside():
			desc += ', castling queenside'

		return f'<Move {desc}>'
