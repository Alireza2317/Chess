from chess.engine.moves.move import Move


class MoveHistory:
    def __init__(self) -> None:
        self._history: list[Move] = []
        self._future: list[Move] = []

    def record(self, move: Move) -> None:
        self._history.append(move)
        self._future.clear() # no redo after a move

    def undo(self) -> Move | None:
        if not self._history:
            return None

        move = self._history.pop()
        self._future.append(move)

        return move

    def redo(self) -> Move | None:
        if not self._future:
            return None

        move = self._future.pop()
        self._history.append(move)

        return move

    def clear(self) -> None:
        self._history.clear()
        self._future.clear()

    def last(self) -> Move | None:
        return self._history[-1] if self._history else None

    def all(self) -> list[Move]:
        return self._history.copy()

    def __len__(self) -> int:
        return len(self._history)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} with {len(self)} moves>"
