from Union import *
import random
from copy import deepcopy


class Board:
    """
    The black player tries to connect the North and South edges of the board
    while the white player tries to connect the East and West edge of the board.

    Black stones are represented by the value -1 while white stones have the value 1
    """

    def __init__(self):
        self.squares = [0 for i in range(121)]
        self.mover = -1.0
        self.union = Union()
        self.num_empty = 121

    def add_to_union(self, hex_point):
        if self.mover == -1 and Union.is_north_edge(hex_point):
            self.union.merge(Union.NORTH, hex_point)

        if self.mover == -1 and Union.is_south_edge(hex_point):
            self.union.merge(Union.SOUTH, hex_point)

        if self.mover == 1 and Union.is_west_edge(hex_point):
            self.union.merge(Union.WEST, hex_point)

        if self.mover == 1 and Union.is_east_edge(hex_point):
            self.union.merge(Union.EAST, hex_point)

        neigh = self.get_neighbours(hex_point)
        for sq in neigh:
            if self.squares[sq] == self.mover:
                self.union.merge(sq, hex_point)

    def get_winner(self):
        if self.union.in_same_set(Union.NORTH, Union.SOUTH):
            return -1
        elif self.union.in_same_set(Union.WEST, Union.EAST):
            return 1
        else:
            return 0

    def play_out(self):
        white_stones = []
        black_stones = []
        moves = [i for i, x in enumerate(self.squares) if x == 0]
        while self.get_winner() == 0:
            index = random.choice(moves)
            moves.remove(index)
            self.make_move(index)

        for index, sq in enumerate(self.squares):
            if sq == -1:
                black_stones.append(index)
            else:
                white_stones.append(index)
        return white_stones, black_stones, self.get_winner()

    def make_move(self, idx: int):
        self.squares[idx] = self.mover
        self.add_to_union(idx)
        self.mover = -self.mover
        self.num_empty -= 1

    def get_num_empty(self):
        return self.num_empty

    def get_empty_list(self):
        return [i for i in range(121) if self.squares[i] == 0]

    def get_num_full(self):
        return sum(map(lambda sq: 1 if sq != 0 else 0, self.squares))

    def get_neighbours(self, hex_point):
        liste = []
        if not Union.is_north_edge(hex_point):
            liste.append(hex_point - 11)

        if not Union.is_south_edge(hex_point):
            liste.append(hex_point + 11)

        if not Union.is_west_edge(hex_point):
            liste.append(hex_point - 1)
            if not Union.is_south_edge(hex_point):
                liste.append(hex_point + 10)

        if not Union.is_east_edge(hex_point):
            liste.append(hex_point + 1)
            if not Union.is_north_edge(hex_point):
                liste.append(hex_point - 10)

        return liste



    def __repr__(self):
        r = ""
        for i in range(11):
            r += " _ "
        r += "\n"
        for i in range(11):
            for p in range(i):
                r += " "
            r += "\\"
            for k in range(11):
                c = self.squares[11 * i + k]
                r += (" B " if c == -1 else " W " if c == 1 else " . ")
            r += "\\"
            r += "\n"

        return r

    def __deepcopy__(self, memo):
        copy = Board()
        copy.mover = deepcopy(self.mover)
        copy.num_empty = deepcopy(self.num_empty)
        copy.union.sizes = deepcopy(self.union.sizes)
        copy.union.indices = deepcopy(self.union.indices)
        copy.squares = deepcopy(self.squares)
        return copy
