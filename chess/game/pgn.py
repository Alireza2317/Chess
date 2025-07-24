from __future__ import annotations
from typing import TYPE_CHECKING, NoReturn
from chess.engine.core import Coordinate
from chess.engine.castle import CastleSide, CastleInfo
from chess.engine.moves.move import Move
from chess.engine.moves.factory import create_move
from chess.engine.piece import Piece, PieceType
if TYPE_CHECKING:
	from chess.game.game import Game

class PGNConverter:
	def __init__(self, game: Game):
		self.game: Game = game

	def move2pgn(self, move: Move) -> str:
		"""Convert a Move object to its PGN string representation."""
		if not isinstance(move, Move):
			raise TypeError("move2pgn expects a Move object!")

		pgn: str = ''

		# Pawn moves
		if move.piece.type == PieceType.PAWN:
			if move.captured or move.is_en_passant:
				pgn = f'{move.start.file}x'

			pgn += f'{move.end.file}{move.end.rank}'

			if move.promotion:
				pgn += f'={move.promotion.name[0].upper()}'

		# Castling
		elif move.castle_side:
			if move.castle_side == CastleSide.KINGSIDE:
				pgn = 'O-O'
			elif move.castle_side == CastleSide.QUEENSIDE:
				pgn = 'O-O-O'
			else:
				raise ValueError("Invalid castle side!")

		else:
			# Other pieces
			pgn = repr(move.piece).upper()
			clarification: str | None = self._check_ambiguity(move)

			if clarification:
				pgn += clarification

			if move.captured:
				pgn += 'x'

			pgn += f'{move.end.file}{move.end.rank}'

		# Check or checkmate
		if move.piece.owner.opponent.is_checkmated():
			pgn += '#'
		elif move.piece.owner.opponent.is_in_check():
			pgn += '+'

		return pgn

	def candidates_for_move(
		self, piece_type: PieceType, end_coord: Coordinate
	) -> list[Piece]:
		possible_pieces: list[Piece] = []
		for other_piece in self.game.current_player.pieces:
			if other_piece.type != piece_type:
				continue
			if end_coord in other_piece.legal_moves:
				possible_pieces.append(other_piece)

		return possible_pieces

	def _check_ambiguity(self, move: Move) -> str:
		"""Return clarification string for ambiguous moves (file/rank/both)."""
		main_piece: Piece = move.piece
		start_coord: Coordinate = main_piece.coordinate

		possible_pieces: list[Piece] = self.candidates_for_move(
			main_piece.type, move.end
		)
		possible_pieces.remove(main_piece)

		file_ambiguous: bool = any(
			piece.coordinate.file == start_coord.file
			for piece in possible_pieces
		)
		rank_ambiguous: bool = any(
			piece.coordinate.rank == start_coord.rank
			for piece in possible_pieces
		)
		if file_ambiguous and rank_ambiguous:
			return start_coord.file + start_coord.rank
		if file_ambiguous:
			return start_coord.rank
		if rank_ambiguous:
			return start_coord.file

		return ''

	def _find_piece(
		self,
		piece_type: PieceType,
		target_coord: Coordinate,
		clarification: str | None = None
	) -> Piece:
		"""
		Find the exact piece of the current player that should
		move to target_coord, with optional disambiguation.
		"""
		candidates: list[Piece] = self.candidates_for_move(
			piece_type, target_coord
		)
		if not candidates:
			raise ValueError(
				f'No {piece_type.name.lower()} can move' +
				f'to {target_coord} for {self.game.current_player}!'
			)

		if len(candidates) == 1:
			if clarification is not None and piece_type != PieceType.PAWN:
				raise ValueError(
					f'There is only one {piece_type.name.lower()} ' +
					f'that can move to {target_coord}! ' +
					'No clarification should be provided!'
				)
			return candidates[0]


		if clarification is not None:
			if not isinstance(clarification, str):
				raise ValueError(
					'Invalid clarification provided! Must be a string.'
				)
			if len(clarification) > 2:
				raise ValueError(
					'Invalid clarification provided!' +
					'Should be either a rank, a file, or both.'
				)

			filtered_pieces: list[Piece] = []

			if len(clarification) == 1:
				if clarification in Coordinate.FILES:
					filtered_pieces = [
						p
						for p in candidates
						if p.coordinate.file == clarification
					]
				elif clarification in Coordinate.RANKS:
					filtered_pieces = [
						p
						for p in candidates
						if p.coordinate.rank == clarification
					]
				else:
					raise ValueError('Invalid clarification string!')
			elif len(clarification) == 2:
				if Coordinate.is_valid(*clarification):
					filtered_pieces = [
						p
						for p in candidates
						if p.coordinate == Coordinate.from_str(clarification)
					]
				else:
					raise ValueError('Invalid clarification string!')

			if not filtered_pieces:
				raise ValueError(
					f'No {piece_type.name.lower()} found with `{clarification}`' +
					f'for {self.game.current_player} to go {target_coord}!'
				)
			elif len(filtered_pieces) > 1:
				self._raise_ambiguity_error(piece_type, target_coord, filtered_pieces)

			return filtered_pieces[0]

		else: # no clarification
			if len(candidates) > 1:
				self._raise_ambiguity_error(
					piece_type, target_coord, candidates
				)

			return candidates[0]

	def _raise_ambiguity_error(
		self,
		piece_type: PieceType,
		target_coord: Coordinate,
		candidates: list[Piece]
	) -> NoReturn:
		raise ValueError(
			f'Ambiguous move: multiple {piece_type.name.lower()}s can move to ' +
			f'{target_coord}: {[p.coordinate for p in candidates]}'
		)

	def pgn2move(self, pgn: str) -> Move:
		"""Convert a PGN string to a Move object. Raises ValueError on error."""
		if not isinstance(pgn, str):
			raise TypeError('PGN should be a string!')

		pgn = pgn.strip()
		if not pgn:
			raise ValueError('PGN string is empty!')

		if pgn[-1] in '+#':
			# ignore it for now!
			pgn.removesuffix('+')
			pgn.removesuffix('#')

		# Pawn moves
		if pgn[0] in Coordinate.FILES:
			if len(pgn) == 2: # regular pawn move
				if not Coordinate.is_valid(*pgn):
					raise ValueError('Invalid PGN string!')
				target_coord: Coordinate = Coordinate.from_str(pgn)
				piece: Piece = self._find_piece(PieceType.PAWN, target_coord)
				return create_move(piece, target_coord)
			elif '=' in pgn: # a promotion
				pgn_move_part: str = pgn[:pgn.index('=')]
				promotion_map: dict[str, PieceType] = {
					'Q': PieceType.QUEEN,
					'R': PieceType.ROOK,
					'B': PieceType.BISHOP,
					'N': PieceType.KNIGHT
				}
				promo_letter: str = pgn[-1].upper()
				if promo_letter not in promotion_map:
					raise ValueError('Invalid promotion piece!')
				if len(pgn_move_part) == 2:
					target_coord = Coordinate.from_str(pgn_move_part)
					piece = self._find_piece(PieceType.PAWN, target_coord)
					return create_move(
						piece,
						target_coord,
						promotion=promotion_map[promo_letter]
					)
				elif len(pgn_move_part) == 4: # also a capture
					if (
						'x' not in pgn_move_part or
		 				pgn_move_part[0] not in Coordinate.FILES
					):
						raise ValueError('Invalid PGN string!')
					clarification: str = pgn_move_part[0]
					target_coord = Coordinate.from_str(pgn_move_part[2:])
					piece = self._find_piece(
						PieceType.PAWN, target_coord, clarification
					)
					captured = self.game.board[target_coord].piece
					if not captured:
						raise ValueError(
							f'No piece on {target_coord} to be captured!'
						)

					return create_move(
						piece,
						target_coord,
						promotion=promotion_map[promo_letter]
					)
				else:
					raise ValueError('Invalid PGN string!')
			elif len(pgn) == 4:
				if 'x' not in pgn:
					raise ValueError('Invalid PGN string!')
				clarification = pgn[0]

				target_coord = Coordinate.from_str(pgn[pgn.index('x')+1:])
				piece = self._find_piece(
					PieceType.PAWN, target_coord, clarification
				)
				return create_move(piece, target_coord)
			else:
				raise ValueError('Invalid PGN string!')
		# Castling
		elif pgn[0] == 'O':
			info = CastleInfo(self.game.current_player.color)
			if pgn == 'O-O':
				info.update_info(CastleSide.KINGSIDE)
				target_coord = info.king_end
			elif pgn == 'O-O-O':
				info.update_info(CastleSide.QUEENSIDE)
				target_coord = info.king_end
			else:
				raise ValueError('Invalid PGN string!')

			piece = self._find_piece(PieceType.KING, target_coord)
			return create_move(piece, target_coord)
		# Piece moves
		elif pgn[0] in 'KQRBN':
			piece_map: dict[str, PieceType] = {
				'K': PieceType.KING,
				'Q': PieceType.QUEEN,
				'R': PieceType.ROOK,
				'B': PieceType.BISHOP,
				'N': PieceType.KNIGHT
			}
			if 'x' in pgn:
				target_coord = Coordinate.from_str(
					pgn[pgn.index('x')+1:pgn.index('x')+3]
				)
				clarification = pgn[1:pgn.index('x')]
			else:
				# FIXME: consider + and # at the end of pgn
				target_coord = Coordinate.from_str(pgn[1:3])
				clarification = pgn[1:-2]
			if len(clarification) > 2:
				raise ValueError('Invalid PGN string!')
			piece = self._find_piece(
				piece_map[pgn[0]],
				target_coord,
				clarification=clarification or None
			)
			return create_move(piece, target_coord)
		else:
			raise ValueError('Invalid PGN string!')
