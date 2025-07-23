from __future__ import annotations
from typing import TYPE_CHECKING
from chess.engine.core import Coordinate
from chess.engine.castle import CastleSide
from chess.engine.moves.move import Move
from chess.engine.piece import Piece, PieceType
if TYPE_CHECKING:
	from chess.game.game import Game
	from chess.engine.player import Player

class PGNConverter:
	def __init__(self, game: Game):
		self.game: Game = game

	def move2pgn(self, move: Move) -> str:
		pgn: str = ''

		p: Piece = move.piece
		if p.type == PieceType.PAWN:
			if not move.captured and not move.is_en_passant:
				pgn = f'{move.end.file}{move.end.rank}'
			elif move.captured or move.is_en_passant:
				pgn = f'{move.start.file}x{move.end.file}{move.end.rank}'

			if move.promotion:
				pgn += f'={move.promotion.name.upper()}'
			return pgn

		if move.castle_side:
			if move.castle_side == CastleSide.KINGSIDE:
				pgn = 'O-O'
			elif move.castle_side == CastleSide.QUEENSIDE:
				pgn = 'O-O-O'
			return pgn

		pgn = repr(move.piece).upper()

		clearification: str | None = self._check_ambiguity(move)
		if clearification:
			pgn += clearification

		if move.captured:
			pgn += 'x'
		pgn += f'{move.end.file}{move.end.rank}'


		if move.piece.owner.opponent.is_in_check():
			pgn += '+'
		elif move.piece.owner.opponent.is_checkmated():
			pgn += '#'

		return pgn

	def _check_ambiguity(self, move: Move) -> str | None:
		# returns the intended rank or file or both
		main_piece: Piece = move.piece

		possible_pieces: list[Piece] = []
		for other_piece in move.piece.owner.pieces:
			if other_piece is main_piece:
				continue
			if other_piece.type == main_piece.type:
				if move.end in other_piece.legal_moves:
					possible_pieces.append(other_piece)

		# check common files:
		common_files: int = 0
		for piece in possible_pieces:
			if piece.coordinate.file == main_piece.coordinate.file:
				common_files += 1

		# check common ranks:
		common_ranks: int = 0
		for piece in possible_pieces:
			if piece.coordinate.rank == main_piece.coordinate.rank:
				common_ranks += 1

		if common_files == 0 and common_ranks == 0:
			return None

		if common_files == 0:
			return main_piece.coordinate.file
		if common_ranks == 0:
			return main_piece.coordinate.rank

		return main_piece.coordinate.file + main_piece.coordinate.rank

	def _find_piece(
		self,
		target_coord: Coordinate,
		piece_type: PieceType,
		additional_info: str | None = None
	) -> Piece:
		if additional_info and len(additional_info) > 2:
			raise ValueError('Invalid additional info provided! should be either a rank, a file or both.')
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

				return Move(
					piece=piece,
					start=piece.coordinate,
					end=target_coord
				)

			elif '=' in pgn: # a promotion
				pgn_move_part: str = pgn[:pgn.index('=')]
				if len(pgn_move_part) == 2:
					target_coord = Coordinate.from_str(pgn_move_part)
					piece = self._find_piece(target_coord, PieceType.PAWN)
					return Move(
						piece=piece,
						start=piece.coordinate,
						end=target_coord
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
					return Move(
						piece=piece,
						start=piece.coordinate,
						end=target_coord,
						captured=captured
					)
				else:
					raise ValueError('Invalid PGN string!')

			elif len(pgn) == 4: # a pawn capture like 'exd5'
				...
			else:
				raise ValueError('Invalid PGN string!')

		elif pgn[0] == 'O': # castle move
			if pgn == 'O-O-O':
				...
			elif pgn == 'O-O-O':
				...
			else:
				raise ValueError('Invalid PGN string!')

		elif pgn[0] in 'KQRBN':
			# check capture
			if 'x' in pgn:
				...

			...

		else:
			raise ValueError('Invalid PGN string!')


		return None