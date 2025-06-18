from chess.components import Piece, Coordinate, Side, Board


class Rook(Piece):
	def __init__(self, side, board, coordinate):
		super().__init__(side, board, coordinate)

	def available_moves(self) -> list[Coordinate]:
		pass


def main():
	pass

if __name__ == '__main__':
	main()