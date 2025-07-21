from __future__ import annotations
from typing import TYPE_CHECKING
from chess.engine.core import Coordinate, Color
from chess.engine.piece import Piece
from chess.engine.pieces.king import King
from chess.engine.pieces.queen import Queen
from chess.engine.pieces.rook import Rook
from chess.engine.pieces.bishop import Bishop
from chess.engine.pieces.knight import Knight
from chess.engine.pieces.pawn import Pawn
from chess.engine.moves.move import Move
from chess.engine.castle import CastleSide, CastleInfo
from chess.game.game import Game

if TYPE_CHECKING:
	from chess.engine.player import Player

class FENLoader:
	def __init__(self, fen: str) -> None:
		fields: list[str] = fen.split()
		if len(fields) != 6:
			raise ValueError('Invalid FEN string!')

		self.fields: list[str] = fields
		self._game: Game = Game()

		self.setup_pieces()
		self.handle_turn()
		self.handle_castle_rights()
		self.handle_en_passant()

	def setup_pieces(self) -> None:
		fen_pieces_part: str = self.fields[0]
		p_placements_ranks: list[str] = fen_pieces_part.split('/')
		if len(p_placements_ranks) != 8:
			raise ValueError('Invalid FEN string!')

		for rank, rank_pieces in zip(Coordinate.RANKS[::-1], p_placements_ranks):
			file_idx: int = 0
			file: str = Coordinate.FILES[file_idx]
			for piece in rank_pieces:
				# can be 'KQRBNPkqrbnp' or a number between 1 and 8
				# the number denotes the number of consecutive empty squares
				if piece.isdigit():
					file_idx += int(piece)
					continue

				player: Player
				if piece.isupper():
					player = self.game.white
				else:
					player = self.game.black

				file = Coordinate.FILES[file_idx]
				coord = Coordinate(file, rank)

				piece_map: dict[str, type] = {
					'k': King,
					'q': Queen,
					'r': Rook,
					'b': Bishop,
					'n': Knight,
					'p': Pawn,
				}

				piece_t: type = piece_map[piece.lower()]
				piece_t(player, coord)

				file_idx += 1

	def handle_turn(self) -> None:
		fen_turn: str = self.fields[1]
		if len(fen_turn) != 1 or fen_turn not in 'wb':
			raise ValueError('Invalid FEN string!')

		if fen_turn == 'b':
			self.game.switch_turn()

	def handle_castle_rights(self) -> None:
		fen_castle: str = self.fields[2]
		if len(fen_castle) > 4:
			raise ValueError('Invalid FEN string!')

		to_disable: list[str] = ['K', 'k', 'Q', 'q']
		for castle_char in fen_castle:
			if castle_char in to_disable:
				to_disable.remove(castle_char)

		for move in to_disable:
			color: Color
			if move.isupper():
				color  = Color.WHITE
			else:
				color = Color.BLACK

			info: CastleInfo = CastleInfo(color)
			if move in 'Kk':
				info.update_info(CastleSide.KINGSIDE)
			elif move in 'Qq':
				info.update_info(CastleSide.QUEENSIDE)

			rook: Piece | None = self.game.board[info.rook_start].piece
			if rook:
				rook.move_count += 1 # disables castling

	def handle_en_passant(self) -> None:
		fen_en_passant: str = self.fields[3]
		if fen_en_passant == '-':
			return

		if len(fen_en_passant) != 2:
			raise ValueError('Invalid FEN string!')

		target_coord: Coordinate = Coordinate.from_str(fen_en_passant)

		if target_coord.rank == '6':
			rank = '5'
		elif target_coord.rank == '3':
			rank = '4'
		else:
			raise ValueError('Invalid FEN string!')

		cap_pawn_coord: Coordinate = Coordinate(target_coord.file, rank)
		cap_pawn: Piece | None = self.game.board[cap_pawn_coord].piece
		if not cap_pawn:
			raise ValueError('Not possible to handle this en passant target!')

		# creating the last move that enabled en passant for the next move
		move: Move = Move(
			piece=cap_pawn,
			start=Coordinate(cap_pawn_coord.file, '7' if rank=='5' else '2'),
			end=cap_pawn_coord
		)
		self.game._last_move = move

	@property
	def game(self) -> Game:
		return self._game
