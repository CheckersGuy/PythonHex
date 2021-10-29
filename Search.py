from Node import Node
from Board import Board
import copy
import math
import time


class Search:

    def __init__(self):
        self.max_nodes = 1000
        self.max_time = None
        self.root = Node()
        self.board = Board()
        self.use_rave = 0
        self.cpuct = math.sqrt(2)

    def num_visits(self):
        return self.root.num_visits

    def clear(self):
        self.root = Node()

    def iterate(self):
        visited = []
        iter_board = copy.deepcopy(self.board)
        current = self.root
        visited.append(current)
        while not current.has_actions(iter_board):
            max_key = current.select()
            current = current.children[max_key]
            visited.append(current)
            iter_board.make_move(current.move)

        key = current.expand(iter_board)
        current = current.children[key]
        iter_board.make_move(current.move)
        visited.append(current)

        mover = iter_board.mover
        roll_value = -mover * iter_board.play_out()
        for visit in reversed(visited):
            visit.num_visits += 1
            visit.results += roll_value
            roll_value = -roll_value

    def search(self):
        iter_count = 0
        if self.max_time is not None:
            self.max_nodes = 1000000000
        start = time.time_ns()
        while iter_count < self.max_nodes:
            self.iterate()
            iter_count += 1
            end = time.time_ns()
            if self.max_time * 1000000 <= (end - start):
                break
