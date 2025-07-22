from __future__ import annotations
from typing import TYPE_CHECKING
from chess.engine.castle import CastleSide
from chess.engine.moves.move import Move
from chess.engine.piece import Piece, PieceType
if TYPE_CHECKING:
	from chess.game.game import Game

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

		clearification: str | None = self.check_ambiguity(move)
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

	def check_ambiguity(self, move: Move) -> str | None:
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