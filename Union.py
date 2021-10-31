import array


class Union:
    NORTH = 121
    SOUTH = 122
    WEST = 123
    EAST = 124

    def __init__(self):
        self.indices = array.array("I", [i for i in range(121 + 4)])
        self.sizes = array.array("I", [1 for i in range(121 + 4)])

    def root(self, idx):
        # finds the root of the element
        current = idx
        while self.indices[current] != current:
            self.indices[current] = self.indices[self.indices[current]]
            current = self.indices[current]
        return current

    def merge(self, idx, idy):
        rootx = self.root(idx)
        rooty = self.root(idy)
        if rootx == rooty:
            return
        if self.sizes[rootx] > self.sizes[rooty]:
            self.indices[rooty] = rootx
            self.sizes[rootx] += self.sizes[rooty]
        else:
            self.indices[rootx] = rooty
            self.sizes[rooty] += self.sizes[rootx]

    def in_same_set(self, idx, idy):
        return self.root(idx) == self.root(idy)

    @staticmethod
    def is_north_edge(idx):
        row = idx // 11
        return row == 0

    @staticmethod
    def is_south_edge(idx):
        row = idx // 11
        return row == 10

    @staticmethod
    def is_west_edge(idx):
        col = idx % 11
        return col == 0

    @staticmethod
    def is_east_edge(idx):
        col = idx % 11
        return col == 10

    @staticmethod
    def is_edge(idx):
        return Union.is_east_edge(idx) or Union.is_west_edge(idx) or Union.is_north_edge(idx) or Union.is_south_edge(
            idx)


def __repr__(self):
    r = ""
    for cell in self.indices:
        r = r + str(cell)
        r = r + "\n"

    return r
