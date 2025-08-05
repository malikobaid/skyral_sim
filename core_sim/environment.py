class Environment:
    def __init__(self, grid_size=(10, 10)):
        self.grid_size = grid_size
        self.grid = [[0 for _ in range(grid_size[1])] for _ in range(grid_size[0])]

    def is_exit(self, x, y):
        return (
            x == 0 or
            y == 0 or
            x == self.grid_size[0] - 1 or
            y == self.grid_size[1] - 1
        )

    def is_within_bounds(self, x, y):
        return 0 <= x < self.grid_size[0] and 0 <= y < self.grid_size[1]
