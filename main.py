#!python3

from os import system
from random import choice
from time import sleep

MARKS = ["O", "X"]
TIME_DELAY = 2
WINNING_COMBINATIONS = [
    ["1", "2", "3"], ["1", "4", "7"], ["1", "5", "9"], ["2", "5", "8"],
    ["3", "5", "7"], ["3", "6", "9"], ["4", "5", "6"], ["7", "8", "9"]
]


class Player():
    def __init__(self, mark, name, number):
        self.is_human = True
        self.mark = mark
        self.name = name
        self.number = number

    def _choose_square(self):
        square = input(
            f"{self.name}, " +
            f"where do you want to place {self.mark} [1-9]? "
        )
        return square

    def make_move(self):
        return self._choose_square()


class ComputerPlayer(Player):
    def __init__(self, mark, name, number):
        super().__init__(mark, name, number)
        self.current_strategy = None
        self.is_human = False
        self.marked_squares = []

    def _check_if_current_strategy_still_possible(self):
        for square in self.current_strategy:
            if board[square] == player_1.mark:
                return False
        return True

    def _choose_square(self):
        if len(self.marked_squares) == 0:
            self._choose_strategy()
            return self._follow_current_strategy()
        else:
            if self._check_if_current_strategy_still_possible():
                return self._follow_current_strategy()
            else:
                # Choose a new strategy.
                self._choose_strategy()
                if self.current_strategy:
                    return self._follow_current_strategy()
                else:
                    # Choose a random free square as a fail-safe.
                    return choice(free_squares)

    def _choose_strategy(self):
        relevant_squares = set(self.marked_squares + free_squares)
        possible_strategies = []
        for combination in WINNING_COMBINATIONS:
            if set(combination).issubset(relevant_squares):
                possible_strategies.append(combination)
        if len(possible_strategies) > 0:
            self.current_strategy = choice(possible_strategies)
        else:
            self.current_strategy = None

    def _follow_current_strategy(self):
        for square in self.current_strategy:
            if board[square] != self.mark:
                return square


def check_game_state():
    game_over = False
    winner = check_if_player_wins(current_player)
    if winner:
        draw_board()
        if winner == "Computer":
            print(f"Sorry {player_1.name}, you lost.")
        else:
            print(f"Congratulations {winner}, you are the winner!")
        game_over = True
    if not winner and len(free_squares) == 0:
        draw_board()
        print("It's a tie.")
        game_over = True
    if game_over:
        play_again = input("\nDo you want to play again [Y/N]? ")
        if play_again.lower() == "y":
            if not multiplayer:
                player_2.marked_squares = []
            return (game_over, True)
        else:
            return (game_over, False)
    return (game_over, False)


def draw_board():
    rows = [
        "\n     |     |     ",
        f"\n  {board['7']}  |  {board['8']}  |  {board['9']}  ",
        "\n     |     |     ",
        "\n", "-" * 18,
        "\n     |     |     ",
        f"\n  {board['4']}  |  {board['5']}  |  {board['6']}  ",
        "\n     |     |     ",
        "\n", "-" * 18,
        "\n     |     |     ",
        f"\n  {board['1']}  |  {board['2']}  |  {board['3']}  ",
        "\n     |     |     ",
        "\n" * 2
    ]
    system("clear")
    for row in rows:
        print(row, end="")


def get_player_info(player_number):
    if not multiplayer and player_number == 2:
        return ComputerPlayer(MARKS[0], "Computer", player_number)
    else:
        name = input(f"Player {player_number}, enter your name: ")
        if player_number == 1:
            mark = input(
                f"{name}, choose your mark [{'/'.join(MARKS)}]: "
            ).upper()
            MARKS.remove(mark)
        else:
            mark = MARKS[0]
        return Player(mark, name, player_number)


def check_if_player_wins(player):
    marked_squares = list(
        filter(lambda square: board[square] == player.mark, list(board))
    )
    for winning_combination in WINNING_COMBINATIONS:
        for square in winning_combination:
            if square not in marked_squares:
                break
        else:
            return player.name
    return None


def start_new_game():
    board = {
        "7": " ", "8": " ", "9": " ",
        "4": " ", "5": " ", "6": " ",
        "1": " ", "2": " ", "3": " ",
    }
    free_squares = list(board)
    starting_player = player_1 if choice([1, 2]) == 1 else player_2
    print(f"\n{starting_player.name} will have the opening move.")
    sleep(TIME_DELAY)
    return (False, "n", board, free_squares, starting_player)


def switch_player():
    return player_2 if current_player.number == 1 else player_1


def validate_move(square):
    if board[square] != " ":
        return False
    else:
        board[square] = f"{current_player.mark}"
        free_squares.remove(square)
        if not current_player.is_human:
            current_player.marked_squares.append(square)
        return True


if __name__ == "__main__":
    print("1) Singleplayer\n2) Multiplayer\n")
    game_mode = input("Select game mode (1): ")
    if game_mode in ["", "1"]:
        multiplayer = False
    else:
        multiplayer = True
    print("")
    player_1 = get_player_info(1)
    player_2 = get_player_info(2)

    game_over, play_again, board, free_squares, \
        current_player = start_new_game()

    while not game_over:
        mark_placed = False
        while not mark_placed:
            draw_board()
            chosen_square = current_player.make_move()
            if not multiplayer and not current_player.is_human:
                draw_board()
                print(
                    f"{current_player.name} placed {current_player.mark} " +
                    f"in square {chosen_square}."
                )
                sleep(TIME_DELAY)
            mark_placed = validate_move(chosen_square)
        game_over, play_again = check_game_state()
        if game_over:
            if play_again:
                game_over, play_again, board, free_squares, \
                    current_player = start_new_game()
        else:
            current_player = switch_player()
