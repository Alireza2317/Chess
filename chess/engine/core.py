from __future__ import annotations
from typing import NamedTuple, TYPE_CHECKING
import enum

if TYPE_CHECKING:
	from chess.engine.piece import Piece


class Color(enum.Enum):
	"""
	Represents the color of a player/piece and squares in a game of chess.
	"""
	WHITE = 1
	BLACK = -1

	def __invert__(self) -> Color:
		# Toggles the Color object when ~ is applied.
		return Color.WHITE if self == Color.BLACK else Color.BLACK


class Direction(NamedTuple):
	file_offset: int
	rank_offset: int


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

	def __hash__(self) -> int:
		return hash(f'{self.file}{self.rank}')

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, Coordinate):
			raise TypeError(
				f'Cannot compare {self.__class__.__name__} with {type(other)}.'
			)

		return self.file == other.file and self.rank == other.rank

	def shift(self, direction: Direction) -> Coordinate | None:
		"""
		Returns a new coordinate shifted by file_offset and rank_offset,
		or None if off board.
		"""
		file_i: int = self.FILES.index(self.file) + direction.file_offset
		rank_i: int = self.RANKS.index(self.rank) + direction.rank_offset

		if (file_i > 7 or file_i < 0) or (rank_i > 7 or rank_i < 0):
			return None

		new_file: str = self.FILES[file_i]
		new_rank: str = self.RANKS[rank_i]

		return Coordinate(new_file, new_rank)

	def in_direction(self, direction: Direction) -> set[Coordinate]:
		coords: set[Coordinate] = set()

		current: Coordinate | None = self
		if not current:
			return set()

		while current := current.shift(direction):
			coords.add(current)

		return coords

	@classmethod
	def from_str(cls, coord: str) -> Coordinate:
		if (len(coord) != 2) or not cls.is_valid(coord[0], coord[1]):
			raise ValueError(f'Invalid chess coordinate {coord}.')

		return cls(coord[0], coord[1])

	def __repr__(self) -> str:
		return f'<{self.file}{self.rank}>'


class Square:
	def __init__(self, coordinate: Coordinate):
		if not isinstance(coordinate, Coordinate):
			raise TypeError(
				f'Invalid coordinate! should be of type {Coordinate.__name__}'
			)

		self._piece: Piece | None = None
		self.coordinate: Coordinate = coordinate
		self.color: Color = self._set_color()

	def _set_color(self) -> Color:
		file_i: int = ord(self.coordinate.file) - ord('a')
		rank_i: int = int(self.coordinate.rank) - 1
		if (file_i + rank_i)%2 == 1:
			return Color.WHITE
		else:
			return Color.BLACK

	def remove_piece(self) -> None:
		self._piece = None

	@property
	def piece(self) -> Piece | None:
		return self._piece

	def set_piece(self, piece: Piece | None) -> None:
		self._piece = piece

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, Square):
			raise TypeError(
				f'Cannot compare {self.__class__.__name__} with {type(other)}'
			)

		same_coord: bool = self.coordinate == other.coordinate
		same_color: bool = self.color == other.color
		same_piece: bool = self.piece == other.piece

		return same_coord and same_color and same_piece

	def __repr__(self) -> str:
		return f'{self.__class__.__name__}({self.coordinate}, {self._piece})'



if __name__ == '__main__':
	c = Coordinate.from_str('a8')
	print(c.in_direction(Direction(1, -1)))