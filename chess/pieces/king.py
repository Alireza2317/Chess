from chess.components import Piece, Coordinate, Side, Board


class King(Piece):
	def __init__(self, side: Side, board: Board, coordinate: Coordinate):
		super().__init__(side, board, coordinate)

	def available_moves(self) -> list[Coordinate]:
		moves: list[Coordinate] = []

		file_ord: int = ord(self.coordinate.file)
		for file_code in range(file_ord-1, file_ord+2):
			file: str = chr(file_code)
			if file not in 'abcdefgh': continue

			rank_ord: int = ord(self.coordinate.rank)
			for rank_s in range(rank_ord-1, rank_ord+2):
				rank: str = chr(rank_s)
				if rank not in '12345678': continue

				c = Coordinate(f'{file}{rank}')

				# if there is a piece there
				piece: Piece | None = self.board.get(c)
				if piece:
					# check its side
					# if its a piece of our own, can't move there
					if piece.side == self.side: continue

				moves.append(c)

		return moves


def main():
	board = Board()
	Piece(Side.BLACK, board, Coordinate('h2'))
	Piece(Side.WHITE, board, Coordinate('g1'))
	Piece(Side.BLACK, board, Coordinate('g2'))

	king = King(Side.WHITE, board, Coordinate('h1'))

	print(king.available_moves())

if __name__ == '__main__':
	main()