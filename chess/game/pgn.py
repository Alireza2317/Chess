from __future__ import annotations
from typing import TYPE_CHECKING
from chess.engine.core import Coordinate
from chess.engine.castle import CastleSide, CastleInfo
from chess.engine.moves.move import Move
from chess.engine.moves.factory import create_move
from chess.engine.piece import Piece, PieceType
if TYPE_CHECKING:
	from chess.game.game import Game
	from chess.engine.player import Player

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

	def _check_ambiguity(self, move: Move) -> str:
		"""Return clarification string for ambiguous moves (file/rank/both)."""
		main_piece: Piece = move.piece
		start_coord: Coordinate = main_piece.coordinate

		possible_pieces: list[Piece] = []
		for other_piece in main_piece.owner.pieces:
			if other_piece is main_piece:
				continue
			if other_piece.type != main_piece.type:
				continue
			if move.end in other_piece.legal_moves:
				possible_pieces.append(other_piece)

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
		target_coord: Coordinate,
		piece_type: PieceType,
		additional_info: str | None = None
	) -> Piece:
		if additional_info and len(additional_info) > 2:
			raise ValueError(
				'Invalid additional info provided! ' +
				'should be either a rank, a file or both.'
			)
		player: Player = self.game.current_player
		for piece in player.pieces:
			if piece.type != piece_type:
				continue
			if target_coord not in piece.legal_moves:
				continue

			if additional_info:
				if len(additional_info) == 1:
					if additional_info in Coordinate.FILES:
						if piece.coordinate.file == additional_info:
							return piece
					elif additional_info in Coordinate.RANKS:
						if piece.coordinate.rank == additional_info:
							return piece
					elif Coordinate.is_valid(*additional_info):
						if piece.coordinate == Coordinate.from_str(additional_info):
							return piece
					else:
						raise ValueError('Invalid additional info provided!')

			return piece

		raise ValueError(
			f'No piece was found for {player} to go {target_coord}!'
		)

	def pgn2move(self, pgn: str) -> Move:
		if not isinstance(pgn, str) or not pgn:
			raise TypeError('PGN should be a non-empty string!')

		if pgn[0] in Coordinate.FILES: # is a pawn move
			if len(pgn) == 2: # a simple pawn move
				if not Coordinate.is_valid(*pgn):
					raise ValueError('Invalid PGN string!')

				target_coord: Coordinate = Coordinate.from_str(pgn)
				# find the pawn which can go there
				piece: Piece = self._find_piece(target_coord, PieceType.PAWN)

				return create_move(piece, target_coord)

			elif '=' in pgn: # a promotion
				pgn_move_part: str = pgn[:pgn.index('=')]
				if len(pgn_move_part) == 2:
					target_coord = Coordinate.from_str(pgn_move_part)
					piece = self._find_piece(target_coord, PieceType.PAWN)

					promotion_map: dict[str, PieceType] = {
						'Q': PieceType.QUEEN,
						'R': PieceType.ROOK,
						'B': PieceType.BISHOP,
						'N': PieceType.KNIGHT
					}
					return create_move(
						piece,
						target_coord,
						promotion=promotion_map[pgn[-1]]
					)

				elif len(pgn_move_part) == 4: # also a capture
					target_coord = Coordinate.from_str(pgn_move_part[2:])
					piece = self._find_piece(
						target_coord, PieceType.PAWN, pgn_move_part[0]
					)
					captured: Piece | None = self.game.board[target_coord].piece
					if not captured:
						raise ValueError(
							f'No piece on {target_coord} to be captured!'
						)
					return create_move(
						piece,
						target_coord,
						promotion=promotion_map[pgn[-1]]
					)
				else:
					raise ValueError('Invalid PGN string!')

			elif len(pgn) == 4: # a regular pawn capture like 'exd5'
				if 'x' not in pgn:
					raise ValueError('Invalid PGN string!')
				target_coord = Coordinate.from_str(pgn[2:])
				piece = self._find_piece(target_coord, PieceType.PAWN, pgn[0])
				return create_move(piece, target_coord)
			else:
				raise ValueError('Invalid PGN string!')

		elif pgn[0] == 'O': # castle move
			info: CastleInfo = CastleInfo(self.game.current_player.color)
			if pgn == 'O-O':
				info.update_info(CastleSide.KINGSIDE)
				target_coord = info.king_end
			elif pgn == 'O-O-O':
				info.update_info(CastleSide.QUEENSIDE)
				target_coord = info.king_end
			else:
				raise ValueError('Invalid PGN string!')

			return create_move(
				self._find_piece(target_coord, PieceType.KING),
				target_coord
			)

		elif pgn[0] in 'KQRBN':
			# check capture
			additional_info: str | None = None
			if 'x' in pgn:
				target_coord = Coordinate.from_str(pgn[pgn.index('x')+1:])
				additional_info = pgn[1:pgn.index('x')]
			else:
				target_coord = Coordinate.from_str(pgn[-2:])
				additional_info = pgn[1:-2]

			if len(additional_info) > 2:
				raise ValueError('Invalid PGN string!')

			piece_map: dict[str, PieceType] = {
				'K': PieceType.KING,
				'Q': PieceType.QUEEN,
				'R': PieceType.ROOK,
				'B': PieceType.BISHOP,
				'N': PieceType.KNIGHT,
			}

			piece = self._find_piece(
				target_coord,
				piece_map[pgn[0]],
				additional_info=additional_info
			)

			return create_move(piece, target_coord)

		else:
			raise ValueError('Invalid PGN string!')
