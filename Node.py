import math
from Board import Board
import random


class Node:

    use_rave = False

    def __init__(self):
        self.parent = None
        self.num_visits = 0
        self.results = 0
        self.children = {}
        self.move = -1
        self.is_terminal = False

    def best_child(self):
        max_value = -math.inf
        max_key = -1
        for key, node in self.children.items():
            val = node.num_visits
            if val > max_value:
                max_value = val
                max_key = key
        return self.children[max_key]

    def select(self):
        uct = lambda x: (x.results / x.num_visits) + math.sqrt(2 * (math.log(self.num_visits) / x.num_visits))

        max_value = -math.inf
        max_key = -1
        for key, node in self.children.items():
            val = uct(node)
            if val > max_value:
                max_value = val
                max_key = key
        return max_key

    def make_terminal(self, result):
        self.results = result
        self.is_terminal = True

    def num_avail_actions(self, board: Board):
        opt = board.get_num_empty() - len(self.children)
        return opt

    def has_actions(self, board: Board):
        return self.num_avail_actions(board) != 0

    def update(self, value):
        self.results += value
        self.num_visits += 1

    def back_up(self,result):
        node = self
        while node is not None:
            node.update(result)
            result = -result


    # adds a new node the list of children
    # new node is at the end of our list
    def expand(self, board: Board):
        empt_squares = board.get_empty_list()
        num_opt = self.num_avail_actions(board)
        rand_index = random.randrange(num_opt)
        counter = 0

        for sq in empt_squares:
            if sq in self.children:
                continue
            if counter == rand_index:
                node = Node()
                node.move = sq
                self.children[sq] = node
                return sq
            counter += 1

    def __repr__(self):
        s = ""
        for child in self.children.values():
            t = (child.move, child.num_visits, child.results, child.is_terminal)
            s += str(t)
            s += "\n"

        return s
