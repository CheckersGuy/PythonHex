from Union import *
from Board import *
import time
from Node import *
from Search import Search
import matplotlib.pyplot as plt
import numpy as np

# Press the green button in the gutter to run the script.

# board = Board()
# search = Search()
# search.max_nodes =1000
#
# search.iterate()
# search.iterate()
# print("Visits: ", search.num_visits())
#some commment

if __name__ == '__main__':
    white_wins = 0
    black_wins = 0
    for p in range(100):
        search = Search()
        rand_index = random.choice([index for index, value in enumerate(search.board.squares) if value == 0])
        search.board.make_move(rand_index)
        print(search.board)
        for k in range(121):
            if search.board.get_winner() != 0:
                white_wins += 1 if search.board.get_winner() == 1 else 0
                black_wins += 1 if search.board.get_winner() == -1 else 0
                print("White Wins:  ", white_wins, " and Black Wins ", black_wins)
                break
            start = time.time()
            t = 100 if search.board.mover == 1 else 100
            search.max_time = t
            Node.use_rave = True if search.board.mover == 1 else False
            search.board.save_bridge = False if search.board.mover == 1 else False
            print("Using save_bridge" if search.board.save_bridge else "Not using save_bridge")
            search.search()
            end = time.time()
            print("Time taken: ", end - start)
            print("Visits: ", search.num_visits())
            best_move = search.root.best_child().move
            best_value = search.root.best_child().results / search.root.best_child().num_visits
            # print("Move ", best_move)
            print("Value: ", search.board.mover * best_value)
            search.board.make_move(best_move)
            print(search.board)
            search.clear()
