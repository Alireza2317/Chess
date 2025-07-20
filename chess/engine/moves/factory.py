from chess.engine.piece import Piece, PieceType
from chess.engine.core import Color, Coordinate
from chess.engine.moves.move import Move
from chess.engine.castle import CastleSide, CastleInfo


def create_move(
    piece: Piece,
	to_coord: Coordinate,
	*,
	promotion: PieceType | None = None,
	simulation: bool = False
) -> Move:
	if not simulation and (to_coord not in piece.legal_moves):
		raise ValueError(
			'Move cannot be created since it is illegal!'
		)

	from_coord: Coordinate = piece.coordinate
	captured_piece: Piece | None = piece.owner.board[to_coord].piece

	# check en passant
	en_passant: bool = (
		piece.type == PieceType.PAWN and
		to_coord.file != from_coord.file and # pawn capture
		captured_piece is None
	)
	# TODO: if it is en passant, calculate the captured piece, and not
	# TODO: just use the to_coord to derive it

	# check castle
	castle_side: CastleSide | None = None
	if piece.type == PieceType.KING:
		info: CastleInfo = CastleInfo(piece.owner.color)
		for side in (CastleSide.KINGSIDE, CastleSide.QUEENSIDE):
			info.update_info(side)
			if to_coord == info.king_end:
				castle_side = side

	# check promotion
	if not simulation: # don't care about promotion in simulation mode
		if piece.type == PieceType.PAWN:
			promotion_rank: str = '8' if piece.owner.color == Color.WHITE else '1'
			if to_coord.rank == promotion_rank:
				if promotion is None :
					raise ValueError('A promotion PieceType should be provided!')
			else:
				if promotion is not None:
					raise ValueError(
						'A promotion PieceType was provided, while this is not a promotion move!'
					)

	return Move(
		piece=piece,
		start=from_coord,
		end=to_coord,
		captured=captured_piece,
		castle_side=castle_side,
		is_en_passant=en_passant,
		promotion=promotion,
	)