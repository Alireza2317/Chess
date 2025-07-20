from chess.engine.core import Coordinate, Direction
from chess.engine.piece import Piece, PieceType
from chess.engine.pieces.pawn import Pawn
from chess.engine.moves.move import Move

def add_en_passant_if_possible(pawn: Piece, last_move: Move | None) -> None:
	if not isinstance(pawn, Pawn):
		return

	if not last_move:
		return

	if last_move.piece.owner is pawn.owner:
		return

	if last_move.piece.type != PieceType.PAWN:
		return

	op_pawn: Piece = last_move.piece

	# the opponent's pawn move is not a double-step move
	if abs(int(last_move.start.rank) - int(last_move.end.rank)) != 2:
		return

	side_coords: tuple[Coordinate | None, Coordinate | None] = (
		pawn.coordinate.shift(Direction(1, 0)),
		pawn.coordinate.shift(Direction(-1, 0))
	)

	if op_pawn.coordinate not in side_coords:
		return

	target_ep: Coordinate = Coordinate(
		op_pawn.coordinate.file, pawn.en_passant_target_rank
	)

	pawn.legal_moves.add(target_ep)
