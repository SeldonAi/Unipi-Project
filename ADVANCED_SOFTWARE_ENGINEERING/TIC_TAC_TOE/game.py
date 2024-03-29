from itertools import cycle
from typing import NamedTuple

class Player(NamedTuple):
    label: str
    color: str


class Move(NamedTuple):
    row: int
    col: int
    label: str = ""


BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player(label="X", color="blue"),
    Player(label="O", color="red"),
)


class Game:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = []
        self.move_counter = 0
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()
    
    def _setup_board(self):
        """I setup the board grid"""
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self):
        """Return all possible winning combinations, i.e. rows, columns and diagonals."""
        # List rows' possible winning combo
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        # List columns' possible winning combo
        columns = [list(col) for col in zip(*rows)]
        # List diagonals' possible winning combo
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    def is_valid_move(self, move):
        """Return True if move is valid, and False otherwise."""
        row, col = move.row, move.col
        # Check that the target cell has not already been played (must be empty).
        move_not_played = (self._current_moves[row][col].label == "")
        # Check that there is no winner
        no_winner = (self.has_winner() == False)
        # Return result        
        return no_winner and move_not_played

    def process_move(self, move):
        """Process the current move and check if it's a win."""
        # Update the board with the current move and add up 1 to move_counter
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        self.move_counter += 1 # Add one to the te move_counter

        # Check for a win
        for combo in self._winning_combos:
            if all(self._current_moves[r][c].label == move.label for r, c in combo):
                self._has_winner = True
                self.winner_combo = combo  # Store the winning combination
                break  # No need to check further if a winner is found


    def has_winner(self):
        """Return True if the game has a winner, and False otherwise."""
        return self._has_winner

    def is_tied(self):
        """Return True if the game is tied, and False otherwise."""
        if self._has_winner == False and self.move_counter == 9:
            return True
        return False

    def toggle_player(self):
        """Return a toggled player."""
        self.current_player = next(self._players)
       
    def reset_game(self):
        """Reset the game state to play again."""
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = [] # Reset winner_combo list 
        self.move_counter = 0 # Reset move_counter
