from __future__ import annotations
import enum


class Color(enum.Enum):
	"""
	Represents the color of a player/piece and squares in a game of chess.
	"""
	WHITE = 1
	BLACK = -1

	def __invert__(self):
		# Toggles the Color object when ~ is applied.
		return Color.WHITE if self == Color.BLACK else Color.BLACK


class Coordinate:
	FILES: str = 'abcdefgh'
	RANKS: str = '12345678'

	def __init__(self, file: str, rank: str):
		if not self.is_valid(file, rank):
			raise ValueError(f'Invalid chess coordinate{file}{rank}.')

		self.file: str = file
		self.rank: str = rank

	@classmethod
	def is_valid(cls, file: str, rank: str) -> bool:
		if not isinstance(file, str) or not isinstance(rank, str):
			raise TypeError('file and rank should be a str!')

		return file in cls.FILES and rank in cls.RANKS

	def __eq__(self, other: object):
		if not isinstance(other, Coordinate):
			return NotImplemented

		return self.file == other.file and self.rank == other.rank

	def shift(self, file_offset: int, rank_offset: int) -> Coordinate | None:
		"""
		Returns a new coordinate shifted by file_offset and rank_offset,
		or None if off board.
		"""
		file_i: int = self.FILES.index(self.file) + file_offset
		rank_i: int = self.RANKS.index(self.rank) + rank_offset

		if (file_i > 7 or file_i < 0) or (rank_i > 7 or rank_i < 0):
			return None

		new_file: str = self.FILES[file_i]
		new_rank: str = self.RANKS[rank_i]

		return Coordinate(new_file, new_rank)

	@classmethod
	def from_str(cls, coord: str) -> Coordinate:
		if (len(coord) != 2) or not cls.is_valid(coord[0], coord[1]):
			raise ValueError(f'Invalid chess coordinate {coord}.')

		return cls(coord[0], coord[1])

	def __repr__(self) -> str:
		return f'<{self.file}{self.rank}>'


if __name__ == '__main__':
	pass