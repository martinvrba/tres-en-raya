#!python3

from itertools import combinations
from os import system
from random import choice
from time import sleep

MARKS = ["O", "X"]
TIME_DELAY = 3
WINNING_COMBINATIONS = [
    ["1", "2", "3"], ["1", "4", "7"], ["1", "5", "9"], ["2", "5", "8"],
    ["3", "5", "7"], ["3", "6", "9"], ["4", "5", "6"], ["7", "8", "9"]
]


class Player():
    def __init__(self, mark, name, number):
        self.is_human = True
        self.mark = mark
        self.marked_squares = list()
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

    def _block_human_player(self):
        if len(player_1.marked_squares) >= 2:
            blocking_squares = set()
            for combination in combinations(player_1.marked_squares, 2):
                _combination = set(combination)
                for winning_combination in WINNING_COMBINATIONS:
                    _winning_combination = set(winning_combination)
                    if _combination.issubset(_winning_combination):
                        blocking_square = \
                            _winning_combination.difference(_combination).pop()
                        if blocking_square not in self.marked_squares:
                            blocking_squares.add(blocking_square)
            if len(blocking_squares) > 0:
                return choice(list(blocking_squares))

        return None

    def _check_if_current_strategy_possible(self):
        if len(self.marked_squares) > 0:
            for square in self.current_strategy:
                if board[square] == player_1.mark:
                    return False

        return True

    def _choose_square(self):
        if len(self.marked_squares) == 0:
            self._choose_strategy()

        if self._check_if_current_strategy_possible():
            needed_squares = self._follow_current_strategy()
            if len(needed_squares) > 1:
                if choice(difficulty):
                    blocking_square = self._block_human_player()
                    if blocking_square:
                        return blocking_square
            return choice(needed_squares)
        else:
            # Choose a new strategy.
            self._choose_strategy()
            if self.current_strategy:
                return self._choose_square()  # Recursion (⌐■_■)
            else:
                # Choose a random free square as a fail-safe.
                return choice(free_squares)

    def _choose_strategy(self):
        relevant_squares = set(self.marked_squares + free_squares)
        possible_strategies = list()
        for combination in WINNING_COMBINATIONS:
            if set(combination).issubset(relevant_squares):
                possible_strategies.append(combination)

        if len(possible_strategies) > 0:
            optimal_strategies = list()
            for strategy in possible_strategies:
                for square in self.marked_squares:
                    if square in strategy:
                        optimal_strategies.append(strategy)
                        break
            if len(optimal_strategies) > 0:
                self.current_strategy = choice(optimal_strategies)
            else:
                self.current_strategy = choice(possible_strategies)
        else:
            self.current_strategy = None

    def _follow_current_strategy(self):
        needed_squares = list()
        for square in self.current_strategy:
            if board[square] != self.mark:
                needed_squares.append(square)

        return needed_squares


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
        play_again = input("\nDo you want to play again [Y/(N)]? ")
        if play_again.lower() == "y":
            for player in [player_1, player_2]:
                player.marked_squares.clear()
            return (game_over, True)
        else:
            return (game_over, False)

    return (game_over, False)


def check_if_player_wins(player):
    marked_squares = list(
        filter(lambda square: board[square] == player.mark, list(board))
    )
    for combination in WINNING_COMBINATIONS:
        for square in combination:
            if square not in marked_squares:
                break
        else:
            return player.name

    return None


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
    if singleplayer and player_number == 2:
        return ComputerPlayer(MARKS[0], "Computer", player_number)

    name = input(
        f"Player {player_number}, enter your name (Player {player_number}): "
    )
    if not name:
        name = f"Player {player_number}"

    if player_number == 1:
        mark = input(
            f"{name}, choose your mark [({MARKS[0]})/{MARKS[1]}]: "
        ).upper()
        if not mark:
            mark = MARKS[0]
        MARKS.remove(mark)
    else:
        mark = MARKS[0]

    return Player(mark, name, player_number)


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
        current_player.marked_squares.append(square)
        return True


if __name__ == "__main__":
    system("clear")
    print("""
 ____  ____  ____  ____    ____  __ _    ____   __   _  _  __
(_  _)(  _ \(  __)/ ___)  (  __)(  ( \  (  _ \ / _\ ( \/ )/ _\ 
  )(   )   / ) _) \___ \   ) _) /    /   )   //    \ )  //    \ 
 (__) (__\_)(____)(____/  (____)\_)__)  (__\_)\_/\_/(__/ \_/\_/

    """)  # noqa: W291,W605

    print("(1) SINGLEPLAYER\n(2) MULTIPLAYER\n")
    game_mode = input("Select game mode [(1)/2]: ")
    singleplayer = False if game_mode == "2" else True
    if singleplayer:
        difficulty = input("Select difficulty [E/(M)/H]: ")
        if difficulty.lower() == "e":
            difficulty = [False]
        elif difficulty.lower() == "h":
            difficulty = [True]
        else:
            difficulty = [True, False]
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
            mark_placed = validate_move(chosen_square)

        if not current_player.is_human:
            draw_board()
            print(
                f"{current_player.name} placed {current_player.mark} " +
                f"in square {chosen_square}."
            )
            sleep(TIME_DELAY)

        game_over, play_again = check_game_state()
        if game_over:
            if play_again:
                game_over, play_again, board, free_squares, \
                    current_player = start_new_game()
        else:
            current_player = switch_player()
