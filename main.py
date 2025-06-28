
import random


import string


class Union:

    def __init__(self, size):
        padded = size+1
        self.idx = [0 if i == 0 or i == padded - 1 else 1 if j == 0 or j ==
                    padded - 1 else i*padded+j for i in range(padded) for j in range(padded)]

        self.sizes = [padded if i == 0 or i == padded - 1 or j == 0 or j ==
                      padded-1 else 1 for i in range(padded) for j in range(padded)]

    def merge(self, x, y):
        self.idx[y] = x

    def root(self, x):
        current = self.idx[x]
        while current != self.idx[current]:
            current = self.idx[current]

        return current

    def is_connected(self, x, y):
        return self.root(x) == self.root(y)


class HexPosition:

    def __init__(self, size):
        self.size = size
        padded = size + 1
        self.mover = -1
        self.pieces = [0 for _ in range(padded * padded)]

    def make_move(self, x, union: Union):
        self.pieces[x] = self.mover
        self.mover = -self.mover

    # TODO muss noch angepasst werden
    def print_position(self, board=None):
        if self.size > 26:
            raise ValueError("Max size is 26 due to alphabet column labels.")

        # Create column labels
        columns = list(string.ascii_lowercase[:self.size])

        # Create default board state if none provided
        if board is None:
            board = [['.' for _ in range(self.size)] for _ in range(self.size)]

        # Print top column labels
        indent = ' '*3
        print(f"{indent}{'  '.join(columns)}")

        # Print board rows
        for row in range(self.size):
            leading_spaces = ' ' * row
            row_label = f"{row+1:<2}\\"
            row_cells = '  '.join(board[row])
            print(f"{leading_spaces}{row_label} {row_cells} \\{row+1}")

        indent = ' ' * (self.size + 3)
        # Print bottom column labels
        print(f"{indent}{'  '.join(columns)}")

    def get_neighbours(self, square):
        padded = self.size + 1
        return [square + 1, square - 1, square + padded, square - padded, square - padded + 1, square + padded - 1]

    def playout(self):
        empty_squares = [idx for idx, value in enumerate(
            self.pieces) if value == 0]
        print(empty_squares)
        # then we can shuffle and check the win condition

        # shuffling the empty square
        random.shuffle(empty_squares)


if __name__ == "__main__":
    position = HexPosition(13)
    position.print_position()
