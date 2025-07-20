from typing import Iterator
from chess.engine.core import Color, Coordinate, Square
from chess.engine.piece import Piece


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
		self[coordinate].set_piece(piece)
		# update piece's coordinate
		piece.coordinate = coordinate

	def remove_piece(self, coordinate: Coordinate) -> None:
		self[coordinate].remove_piece()

	def move_piece(self, from_coord: Coordinate, to_coord: Coordinate) -> None:
		if not isinstance(from_coord, Coordinate) or not isinstance(to_coord, Coordinate):
			raise TypeError(
				f'Invalid coordinate! should be of type {Coordinate.__name__}'
			)
		piece: Piece | None = self[from_coord].piece

		if not piece:
			raise ValueError(
				f'Invalid move from {from_coord}. No piece present.'
			)

		# remove the piece from the original square and
		self.remove_piece(from_coord)

		# put it in the new square
		self.place_piece(piece, to_coord)

	def all_squares(self) -> list[Square]:
		return list(self._grid.values())

	def all_pieces(self) -> set[Piece]:
		return {
			sq.piece for sq in self.all_squares() if sq.piece
		}

	def __iter__(self) -> Iterator[tuple[Coordinate, Square]]:
		return iter(self._grid.items())

	def print(self, checked: Coordinate | None = None) -> str:
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

		piece_symbols: dict[str, str] = {
			'P': '♙',
			'N': '♘',
			'B': '♗',
			'R': '♖',
			'Q': '♕',
			'K': '♔',
			'p': '♟',
			'n': '♞',
			'b': '♝',
			'r': '♜',
			'q': '♛',
			'k': '♚'
		}

		board_str: str = ''
		square_delimiter: str = ' '*2
		for rank in reversed(Coordinate.RANKS):
			for file in Coordinate.FILES:
				coord: Coordinate = Coordinate(file, rank)
				sq: Square = self._grid[coord]
				piece = sq.piece
				square_str: str = '□' if sq.color == Color.WHITE else '■'
				if checked and coord == checked:
					board_str += colored_str(piece_symbols[f'{piece}'], 'r') if piece else square_str
				else:
					board_str += piece_symbols[f'{piece}'] if piece else square_str
				board_str += square_delimiter

			board_str += colored_str(rank, 'g') + '\n'

		board_str += colored_str(square_delimiter.join(Coordinate.FILES), 'g')

		print(board_str)
		return board_str


	def __repr__(self) -> str:
		return self.print()
