from chess.components import Piece, Coordinate, Color, Board


class Rook(Piece):
	def __init__(self, color: Color, board: Board, coordinate: Coordinate):
		super().__init__(color, board, coordinate)

	def available_moves(self) -> list[Coordinate]:
		pass

	def __repr__(self):
		return 'R' if self.color == Color.WHITE else 'r'

def main():
	pass

if __name__ == '__main__':
	main()