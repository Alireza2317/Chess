from chess.engine.core import Coordinate
from gui.config import cfg # type: ignore

def get_coord_from_mouse(pos: tuple[int, int]) -> Coordinate | None:
    x, y = pos
    file_idx: int = x // cfg.square_size
    rank_idx: int = 7 - (y // cfg.square_size)

    if 0 <= file_idx < 8 and 0 <= rank_idx < 8:
        file: str = Coordinate.FILES[file_idx]
        rank: str = Coordinate.RANKS[rank_idx]
        return Coordinate(file, rank)

    return None
