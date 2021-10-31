from Union import *
from Board import *
import time
from Node import *
from Search import Search

# Press the green button in the gutter to run the script.

# board = Board()
# search = Search()
# search.max_nodes =1000
#
# search.iterate()
# search.iterate()
# print("Visits: ", search.num_visits())
if __name__ == '__main__':
    total_winner = 0
    search = Search()
    for k in range(121):
        start = time.time()
        t = 20000 if search.board.mover == -1 else 20000
        search.max_time = t
        Node.use_rave = False if search.board.mover == -1 else True
        search.search()
        end = time.time()
        print("Time taken: ", end - start)
        if search.board.get_winner() != 0:
            total_winner += search.board.get_winner()
            print("Winner ", total_winner)
            # print(search.board)
            break
        print("Visits: ", search.num_visits())
        best_move = search.root.best_child().move
        best_value = search.root.best_child().results / search.root.best_child().num_visits
        # print("Move ", best_move)
        print("Value: ", search.board.mover * best_value)
        search.board.make_move(best_move)
        print(search.board)
        search.clear()
