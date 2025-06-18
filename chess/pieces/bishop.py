from chess.components import Piece, Coordinate, Color, Board


class Bishop(Piece):
	def __init__(self, color: Color, board: Board, coordinate: Coordinate):
		super().__init__(color, board, coordinate)

	def available_moves(self) -> list[Coordinate]:
		pass


def main():
	pass

if __name__ == '__main__':
	main()