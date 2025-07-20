import enum
from dataclasses import dataclass
from chess.engine.core import Coordinate, Color

class CastleSide(enum.Enum):
	KINGSIDE = enum.auto()
	QUEENSIDE = enum.auto()


@dataclass
class CastleInfo:
	color: Color
	side: CastleSide

	def __post_init__(self) -> None:
		self.rank: str = '1' if self.color == Color.WHITE else '8'

		king_end_file: str
		rook_start_file: str
		rook_end_file: str
		if self.side == CastleSide.KINGSIDE:
			king_end_file = 'g'
			rook_start_file = 'h'
			rook_end_file = 'f'
		elif self.side == CastleSide.QUEENSIDE:
			king_end_file = 'c'
			rook_start_file = 'a'
			rook_end_file = 'd'

		self.king_path: tuple[Coordinate, Coordinate] = (
			Coordinate(rook_end_file, self.rank),
			Coordinate(king_end_file, self.rank),
		)
		self.king_end: Coordinate = Coordinate(king_end_file, self.rank)

		self.rook_start: Coordinate = Coordinate(rook_start_file, self.rank)
		self.rook_end: Coordinate = Coordinate(rook_end_file, self.rank)


info = CastleInfo(Color.WHITE, CastleSide.QUEENSIDE)
print(f'{info.rank=}')
print(f'{info.king_end=}')
print(f'{info.king_path=}')
print(f'{info.rook_start=}')
print(f'{info.rook_end=}')