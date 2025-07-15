from chess.engine.board import Board
from chess.engine.player import Player


def print_player_pieces(player: Player) -> None:
    print(f'\n{player.color.name.title()} Player Pieces:')
    for piece in sorted(
        player.pieces,
        key=lambda p: (p.coordinate.rank, p.coordinate.file)
    ):
        print(f'{piece} at {piece.coordinate}')

def print_legal_moves(player: Player) -> None:
    print(f'\n{player.color.name.title()} Legal Moves:')
    for piece in player.pieces:
        moves = getattr(piece, 'legal_moves', None)
        if not moves:
            continue
        print(f'{piece} at {piece.coordinate}:')
        for move in sorted(moves, key=lambda m: (m.rank, m.file)):
            print(f'  → {move}')

def check_piece_sync(player: Player, board: Board) -> None:
    print("\nChecking sync between board and player's pieces:")
    board_pieces = board.all_pieces()
    player_pieces = player.pieces

    board_only = board_pieces - player_pieces
    player_only = player_pieces - board_pieces

    if not board_only and not player_only:
        print("✅ Sync OK")
    else:
        print("❌ Desync Found")
        if board_only:
            print("Pieces on board but not in player's list:")
            for p in board_only:
                 print(p)
        if player_only:
            print("Pieces in player but not on board:")
            for p in player_only:
                 print(p)
