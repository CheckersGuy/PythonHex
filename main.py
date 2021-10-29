from Union import *
from Board import *
import time
from Node import *
from Search import Search

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    search = Search()

    for k in range(121):
        start = time.time()
        t = 10000 if search.board.mover == -1 else 180000
        search.max_time = t
        search.search()
        end = time.time()
        print("Time taken: ", end - start)
        if search.board.get_winner() != 0:
            break
        print("Visits: ", search.num_visits())
        best_move = search.root.best_child().move
        best_value = search.root.best_child().results / search.root.best_child().num_visits
        print("Move ", best_move)
        print("Value: ", search.board.mover * best_value)
        search.board.make_move(best_move)
        print(search.board)
        search.clear()
