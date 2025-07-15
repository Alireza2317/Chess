from chess.engine.piece import Piece, PieceType
from chess.engine.core import Color, Coordinate, Direction
from chess.engine.moves.move import Move

def create_move(piece: Piece, to_coord: Coordinate) -> Move:
	from_coord: Coordinate = piece.coordinate
	captured_piece: Piece | None = piece.owner.board[to_coord].piece

	# check en passant
	en_passant: bool = (
		piece.type == PieceType.PAWN and
		to_coord.file != from_coord.file and # pawn capture
		captured_piece is None
	)

	# check castle
	is_castle: bool = (
		piece.type == PieceType.KING and
		to_coord in (
			piece.coordinate.shift(Direction(-2, 0)),
			piece.coordinate.shift(Direction(2, 0)),
		)
	)

	# check promotion
	promotion: PieceType | None = None
	if piece.type == PieceType.PAWN:
		promotion_rank: str = '1' if piece.owner.color == Color.WHITE else '8'
		if to_coord.rank == promotion_rank:
			promotion = PieceType.QUEEN # TODO: get this from input


	return Move(
		piece=piece,
		start=from_coord,
		end=to_coord,
		captured=captured_piece,
		is_castling=is_castle,
		is_en_passant=en_passant,
		promotion=promotion,
	)