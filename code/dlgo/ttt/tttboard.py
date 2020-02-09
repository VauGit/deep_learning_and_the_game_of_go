import copy

from dlgo.ttt.ttttypes import Player, Point

__all__ = [
    'Board',
    'GameState',
    'Move',
]


class IllegalMoveError(Exception):
    pass


BOARD_SIZE = 3
ROWS = tuple(range(1, BOARD_SIZE + 1))
COLS = tuple(range(1, BOARD_SIZE + 1))
# Top left to lower right diagonal
DIAG_1 = (Point(1, 1), Point(2, 2), Point(3, 3))
# Top right to lower left diagonal
DIAG_2 = (Point(1, 3), Point(2, 2), Point(3, 1))


class Board:
    def __init__(self):
        self._grid = {}

    def place(self, player, point):
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None
        self._grid[point] = player

    @staticmethod
    def is_on_grid(point):
        return 1 <= point.row <= BOARD_SIZE and \
            1 <= point.col <= BOARD_SIZE

    def get(self, point):
        """Return the content of a point on the board.

        Returns None if the point is empty, or a Player if there is a
        stone on that point.
        """
        return self._grid.get(point)

    def move_pawn(self, player, from_point, to_point):
        assert self.is_on_grid(from_point)
        assert self.is_on_grid(to_point)
        self._grid[from_point] = None
        self._grid[to_point] = player


class Move:
    def __init__(self, from_point, to_point):
        # Update Move class to now have a from and to point for Hexapawn
        self.from_point = from_point
        self.to_point = to_point


class GameState:
    def __init__(self, board, next_player, move):
        self.board = board
        self.next_player = next_player
        self.last_move = move

    def apply_move(self, move):
        """Return the new GameState after applying the move."""
        next_board = copy.deepcopy(self.board)
        next_board.move_pawn(self.next_player, move.from_point, move.to_point)
        return GameState(next_board, self.next_player.other, move)

    @classmethod
    def new_game(cls):
        board = Board()
        # Initialize starting Hexapawn pieces:
        board.place(Player.o, Point(1, 1))
        board.place(Player.o, Point(1, 2))
        board.place(Player.o, Point(1, 3))

        board.place(Player.x, Point(3, 2))
        board.place(Player.x, Point(3, 3))
        board.place(Player.x, Point(3, 1))

        return GameState(board, Player.x, None)

    def is_valid_move(self, move):
        # Check from and to point:
        # If 1 in front is blank
        # If diagonal is black

        return (
            # Can move to empty spot
            # self.board.get(move.to_point) is None or
            # Must use your piece as origin
            # self.board.get(move.from_point) == self.next_player.other and
            # Capture other player logic:
            
            # not (self.board.get(move.from_point) is None)
            # Can't move straight if other player is there
            # not (self.board.get(move.to_point) == Player.o and move.to_point[0] == move.from_point[0]) or
            # not (self.board.get(move.to_point) == Player.x and move.to_point[1] == move.from_point[1]) and
            # Starting point must be one of your own pieces:
            # Destination must be within 1 square radius:
            # ((move.to_point[0] == move.from_point[0] - 1) or
            # (move.to_point[0] == move.from_point[0] + 1) or
            # (move.to_point[1] == move.from_point[1] - 1) or
            # (move.to_point[1] == move.from_point[1] + 1)) and
            # Game isn't over
            not self.is_over())

    def legal_moves(self):
        moves = []
        for row_1 in ROWS:
            for col_1 in COLS:
                #For each point, also loop through every other point as a possible move
                for row_2 in ROWS:
                    for col_2 in COLS:
                        move = Move(Point(row_1, col_1), Point(row_2, col_2))
                        if self.is_valid_move(move):
                            moves.append(move)
        return moves

    def is_over(self):
        if self._reached_end_white(Player.x):
            return True
        if self._reached_end_black(Player.o):
            return True
        return False

    def _reached_end_white(self, player):
        """Check to see if white player has moved a piece to end
        of the board."""
        if self.board.get(Point(1, 1)) == player or \
                self.board.get(Point(1, 2)) == player or \
                self.board.get(Point(1, 3)) == player:
            return True
        return False

    def _reached_end_black(self, player):
        """Check to see if black player has moved a piece to end
        of the board."""
        if self.board.get(Point(3, 1)) == player or \
                self.board.get(Point(3, 2)) == player or \
                self.board.get(Point(3, 3)) == player:
            return True
        return False

    def winner(self):
        if self._reached_end_white(Player.x):
            return Player.x
        if self._reached_end_black(Player.o):
            return Player.o
        return None
