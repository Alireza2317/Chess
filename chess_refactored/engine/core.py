from __future__ import annotations
import enum
from typing import Iterator, TYPE_CHECKING
if TYPE_CHECKING:
	from chess_refactored.engine.piece import Piece


class Color(enum.Enum):
	"""
	Represents the color of a player/piece and squares in a game of chess.
	"""
	WHITE = 1
	BLACK = -1

	def __invert__(self) -> Color:
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

	def __hash__(self) -> int:
		return hash(f'{self.file}{self.rank}')

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, Coordinate):
			raise TypeError(
				f'Cannot compare {self.__class__.__name__} with {type(other)}.'
			)

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

	def in_direction(self, direction: tuple[int, int]) -> list[Coordinate]:
		coords: list[Coordinate] = []

		current: Coordinate | None = self
		if not current:
			return []

		while current := current.shift(*direction):
			coords.append(current)

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

class Board:
	def __init__(self) -> None:
		self._grid: dict[Coordinate, Square] = {
			(coord := Coordinate(file, rank)): Square(coord)
			for file in Coordinate.FILES
			for rank in Coordinate.RANKS
		}

	def get_square(self, coordinate: Coordinate) -> Square:
		if not isinstance(coordinate, Coordinate):
			raise TypeError(
				f'Invalid coordinate! should be of type {Coordinate.__name__}'
			)

		return self._grid[coordinate]

	def __getitem__(self, coordinate: Coordinate) -> Square:
		return self.get_square(coordinate)

	def place_piece(self, piece: Piece, coordinate: Coordinate) -> None:
		self.get_square(coordinate).set_piece(piece)

	def remove_piece(self, coordinate: Coordinate) -> None:
		self.get_square(coordinate).remove_piece()

	def move_piece(self, from_coord: Coordinate, to_coord: Coordinate) -> None:
		if not isinstance(from_coord, Coordinate) or not isinstance(to_coord, Coordinate):
			raise TypeError(
				f'Invalid coordinate! should be of type {Coordinate.__name__}'
			)

		from_square: Square = self.get_square(from_coord)
		to_square: Square = self.get_square(to_coord)

		if not from_square.piece:
			raise ValueError(
				f'Invalid move from {from_coord}. No piece present.'
			)

		# remove the piece from the original square and
		# put it in the new square
		to_square.set_piece(from_square._piece)
		from_square.remove_piece()

	def all_squares(self) -> list[Square]:
		return list(self._grid.values())

	def __iter__(self) -> Iterator[tuple[Coordinate, Square]]:
		return iter(self._grid.items())

	def __repr__(self) -> str:
		def colored_str(text: str, color: str) -> str:
			"""
			supported colors:
			red, green, yellow, blue, magenta, cyan
			"""
			if color in ('red', 'r'):
				start = '\033[91m'
			elif color in ('green', 'g'):
				start = '\033[92m'
			elif color in ('yellow', 'y'):
				start = '\033[93m'
			elif color in ('blue', 'b'):
				start = '\033[94m'
			elif color in ('magenta', 'm'):
				start = '\033[95m'
			elif color in ('cyan', 'c'):
				start = '\033[96m'

			return start + text + '\033[0m'

		board_str: str = ''
		square_delimiter: str = ' '*3
		for rank in reversed(Coordinate.RANKS):
			for file in Coordinate.FILES:
				sq: Square = self._grid[Coordinate(file, rank)]
				piece = sq.piece
				square_str: str = '□' if sq.color == Color.WHITE else '■'
				board_str += f'{piece}' if piece else square_str
				board_str += square_delimiter

			board_str += colored_str(rank, 'g') + '\n'

		board_str += colored_str(square_delimiter.join(Coordinate.FILES), 'g')

		return board_str

if __name__ == '__main__':
	c = Coordinate.from_str('a8')
	print(c.in_direction((1, -1)))