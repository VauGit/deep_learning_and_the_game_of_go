from dlgo import minimax
from dlgo import ttt

from six.moves import input

COL_NAMES = 'ABC'


def print_board(board):
    print('   A   B   C')
    for row in (1, 2, 3):
        pieces = []
        for col in (1, 2, 3):
            piece = board.get(ttt.Point(row, col))
            if piece == ttt.Player.x:
                pieces.append('X')
            elif piece == ttt.Player.o:
                pieces.append('O')
            else:
                pieces.append(' ')
        print('%d  %s' % (row, ' | '.join(pieces)))


def point_from_coords(text):
    col_name = text[0]
    row = int(text[1])
    return ttt.Point(row, COL_NAMES.index(col_name) + 1)


def main():
    game = ttt.GameState.new_game()

    human_player = ttt.Player.x
    # bot_player = ttt.Player.o

    bot = minimax.MinimaxAgent()

    while not game.is_over():
        print_board(game.board)
        if game.next_player == human_player:
            #Now take two inputs to move pawns from "from_point" to "to_point"
            human_from_move = input('--Enter piece to move: ')
            human_to_move = input('--Enter location to move to: ')
            from_point = point_from_coords(human_from_move.strip())
            to_point = point_from_coords(human_to_move.strip())
            move = ttt.Move(from_point, to_point)
            print("Moved piece from: ", from_point, " to: ", to_point)
        else:
            move = bot.select_move(game)
            print (move.from_point, move.to_point)
        #Check valid from/to movement
        game = game.apply_move(move)

    print_board(game.board)
    winner = game.winner()
    if winner is None:
        print("It's a draw.")
    else:
        print('Winner: ' + str(winner))


if __name__ == '__main__':
    main()
