import enum
from chess.engine.core import Coordinate, Color

class CastleSide(enum.Enum):
	KINGSIDE = enum.auto()
	QUEENSIDE = enum.auto()


class CastleInfo:
	def __init__(self, color: Color) -> None:
		self.color: Color = color
		self.rank: str = '1' if self.color == Color.WHITE else '8'

	def update_info(self, side: CastleSide) -> None:
		king_end_file: str
		rook_start_file: str
		rook_end_file: str
		if side == CastleSide.KINGSIDE:
			king_end_file = 'g'
			rook_start_file = 'h'
			rook_end_file = 'f'
		elif side == CastleSide.QUEENSIDE:
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