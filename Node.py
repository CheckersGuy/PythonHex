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
        self.qRave = 0
        self.nRave = 0
        self.is_terminal = False

    def best_child(self):
        return max(self.children.values(), key=lambda node: node.num_visits)

    def value(self):

        if self.num_visits == 0:
            return math.inf

        q_value = lambda x: (x.results / x.num_visits)
        uct_pol = lambda x: (math.sqrt(2.0 * (math.log(self.num_visits) / x.num_visits)))
        rave_b = lambda x: (math.sqrt(2000 / (3 * self.num_visits + 2000)))
        rave_value = lambda x: (x.qRave / (1.0 + x.nRave))
        rave_combined = lambda x: ((1.0 - rave_b(x)) * q_value(x) + rave_b(x) * rave_value(x))
        uct = lambda x: (q_value(x) + uct_pol(x))

        if Node.use_rave:
            return rave_combined(self)
        else:
            return uct(self)

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

    def is_loss(self):
        return self.is_terminal and self.results == -1.0

    def is_win(self):
        return self.is_terminal and self.results == 1.0

    def back_up(self, result, white_stones, black_stones, turn):
        node = self
        reward = -1 if result == turn else 1
        while node is not None:
            if node.parent is not None:
                if turn == 1:
                    for stone in white_stones:
                        if stone in node.children:
                            curr: Node = node.parent.children[stone]
                            curr.qRave += -reward
                            curr.nRave += 1
                else:
                    for stone in black_stones:
                        if stone in node.children:
                            curr: Node = node.parent.children[stone]
                            curr.qRave += -reward
                            curr.nRave += 1

            node.update(reward)
            node = node.parent
            turn = -turn
            reward = -reward

    # adds a new node the list of children
    # new node is at the end of our list
    def expand(self, board: Board):
        empt_indices = [index for index, sq in enumerate(board.squares) if sq == 0]
        for sq in empt_indices:
            node = Node()
            node.move = sq
            node.parent = self
            self.children[sq] = node

    def __repr__(self):
        s = ""
        for child in self.children:
            t = (child.move, child.num_visits, child.results, child.is_terminal)
            s += str(t)
            s += "\n"

        return s
