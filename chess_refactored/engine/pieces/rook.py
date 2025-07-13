from chess_refactored.engine.core import Color, Coordinate, Direction
from chess_refactored.engine.piece import Piece, PieceType

class Rook(Piece):
	from chess_refactored.engine.player import Player

	def __init__(self, player: Player, coordinate: Coordinate) -> None:
		super().__init__(player, coordinate)

	@property
	def piece_type(self) -> PieceType:
		return PieceType.ROOK

	def attacking_coordinates(self) -> list[Coordinate]:
		moves: list[Coordinate] = []

		directions: tuple[Direction, ...] = (
			Direction(file_offset=1, rank_offset=0), # right
			Direction(file_offset=-1, rank_offset=0), # left
			Direction(file_offset=0, rank_offset=1), # up
			Direction(file_offset=0, rank_offset=-1) # down
		)

		for direction in directions:
			moves.extend(self.coordinate.in_direction(direction))

		return moves