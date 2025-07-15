from __future__ import annotations
from dataclasses import dataclass
from chess.engine.core import Coordinate
from chess.engine.piece import Piece, PieceType


@dataclass
class Move:
	piece: Piece
	start: Coordinate
	end: Coordinate
	captured: Piece | None = None
	is_castling: bool = False
	is_en_passant: bool = False
	promotion: PieceType | None = None

	def __post_init__(self) -> None:
		modes: list[bool] = [
			(self.promotion is not None), self.is_en_passant, self.is_castling
		]
		if sum(modes) > 1:
			raise ValueError(
				'Only one of promotion, en_passant, and castling can be True!'
			)

	@property
	def is_castle_kingside(self) -> bool:
		return self.is_castling and self.end.file == 'g'

	@property
	def is_castle_queenside(self) -> bool:
		return self.is_castling and self.end.file == 'c'

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
		elif self.promotion:
			desc += f', promoted to {self.promotion.name.title()}'
		elif self.is_en_passant:
			desc += ', en passant'
		elif self.is_castle_kingside:
			desc += ', castling kingside'
		elif self.is_castle_queenside:
			desc += ', castling queenside'

		return f'<Move {desc}>'
