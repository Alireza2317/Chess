from __future__ import annotations
from dataclasses import dataclass
from chess.engine.core import Coordinate
from chess.engine.piece import Piece, PieceType
from chess.engine.castle import CastleSide

@dataclass
class Move:
	piece: Piece
	start: Coordinate
	end: Coordinate
	captured: Piece | None = None
	castle_side: CastleSide | None = None
	is_en_passant: bool = False
	promotion: PieceType | None = None

	def __post_init__(self) -> None:
		exclusive_flags: list[bool] = [
			(self.promotion is not None), self.is_en_passant, self.is_castling
		]
		if sum(exclusive_flags) > 1:
			raise ValueError(
				'Only one of promotion, en_passant, and castling can be True!'
			)

		assert self.start != self.end, 'Start and end coordinates were the same!'

	@property
	def is_castling(self) -> bool:
		return self.castle_side is not None

	@property
	def is_promotion(self) -> bool:
		return (
			self.promotion is not None and
			self.piece.type == PieceType.PAWN
		)

	def __repr__(self) -> str:
		desc: str = f'{self.piece} from {self.start} to {self.end}'

		if self.captured:
			desc += f', captured {self.captured}'
		elif self.is_en_passant:
			desc += ', en passant'
		elif self.castle_side:
			desc += f', castling {self.castle_side.name.title()}'

		if self.promotion:
			desc += f', promoted to {self.promotion.name.title()}'

		return f'<Move {desc}>'
