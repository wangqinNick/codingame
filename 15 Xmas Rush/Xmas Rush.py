import numpy
import random
import numpy
import sys

def log(msg):
    print(msg, file=sys.stderr, flush=True)
# grid size
N = 7
# Up, Right, Down, Left
d_row = [-1, 0, 1, 0]
d_col= [0, 1, 0, -1]
dir_name = ["UP", "RIGHT", "DOWN", "LEFT"]
TURN_MOVE = 1
TURN_PUSH = 0

# [['1', '1', '0', '0',], ...]

def read_grid():
    cells = []
    for _ in range(7):
        row = []
        for tile in input().split():
            row.append(tile)
        cells.append(row)
    return cells.copy()


def inside(r, c):
    """
    Check if (row, col) is inside the grid
    :param r: row
    :param c: col
    :return: True for inside
    """
    return 0 <= r < N and 0 <= c < N


def inv_dir(direction):
    """
    Inverse the direction, from (row_dest, col_dest) to (row, col)
    :param direction: 0, 1, 2, 3 for Up, Right, Down, Left
    :return: 2, 3, 0, 1
    """
    return direction ^ 2


def can_go(grid, row, col, direction):
    assert 0 <= direction <= 3  # Up, Right, Down, Left
    row_dest = row + d_row[direction]
    col_dest = col + d_col[direction]
    return grid[row][col][direction] == '1' and inside(row_dest, col_dest) and grid[row_dest][col_dest][inv_dir(direction)] == '1'


class Player:
    def __init__(self):
        self.row = None
        self.col = None
        self.cntCards = None
        self.tile = None

    def read(self):
        inputs = input().split()
        self.cntCards = int(inputs[0])  # the total number of quests for a player (hidden and revealed)
        self.col = int(inputs[1])
        self.row = int(inputs[2])
        self.tile = inputs[3]

    def can_go(self, grid, direction):
        """
        Check if can go to UP / RIGHT / DOWN / LEFT
        :param direction: 0, 1, 2, 3, 4 for UP, RIGHT, DOWN, LEFT
        :return: TRUE / FALSE
        """
        return can_go(grid, self.row, self.col, direction)


def run():
    while True:
        turn_type = int(input())
        grid = read_grid()
        me = Player()
        he = Player()
        me.read()
        he.read()

        # Todo: refactor
        num_items = int(input())  # the total number of items available on board and on player tiles
        for i in range(num_items):
            inputs = input().split()
            item_name = inputs[0]
            item_x = int(inputs[1])
            item_y = int(inputs[2])
            item_player_id = int(inputs[3])
        num_quests = int(input())  # the total number of revealed quests for both players
        for i in range(num_quests):
            inputs = input().split()
            quest_item_name = inputs[0]
            quest_player_id = int(inputs[1])

        if turn_type == TURN_MOVE:
            has_moved = False
            for dir_ in range(4):
                if me.can_go(grid, dir_):
                    print("MOVE {}".format(dir_name[dir_]))
                    has_moved = True
                    break
            if not has_moved:
                log("NO WAY TO MOVE AT ALL!")
                print("PASS")
        else:
            # Todo: PUSH Turn
            print("PUSH 3 RIGHT")


if __name__ == '__main__':
    run()