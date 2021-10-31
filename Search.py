from Node import Node
from Board import Board
import copy
import math
import time
import random


class Search:

    def __init__(self):
        self.max_nodes = math.inf
        self.max_time = math.inf
        self.root = Node()
        self.board = Board()
        self.use_rave = 0
        self.cpuct = math.sqrt(2)

    def num_visits(self):
        return self.root.num_visits

    def clear(self):
        self.root = Node()

    def iterate(self):
        iter_board = copy.deepcopy(self.board)
        current = self.root
        while len(current.children) != 0:
            max_value = max(current.children.values(), key=lambda node: node.value()).value()
            max_values = [node for node in current.children.values() if node.value() == max_value]
            current = random.choice(max_values)
            iter_board.make_move(current.move)

        current.expand(iter_board)
        current = random.choice(list(current.children.values()))
        iter_board.make_move(current.move)

        mover = iter_board.mover
        white_stones, black_stones, result = iter_board.play_out()
        current.back_up(result, white_stones, black_stones, mover)

    def search(self):
        iter_count = 0
        start = time.time_ns()
        while iter_count < self.max_nodes:
            self.iterate()
            iter_count += 1
            end = time.time_ns()
            if self.max_time*1000000 <= (end - start):
                break
