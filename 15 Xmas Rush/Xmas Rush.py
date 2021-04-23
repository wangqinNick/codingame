import math
import random
import sys

""" for debugging only """


def log(msg):
    print(msg, file=sys.stderr, flush=True)


""" Const """
MY_ID = 0
HIS_ID = 1
# grid size
N = 7
# Up, Right, Down, Left
d_row = [-1, 0, 1, 0]
d_col = [0, 1, 0, -1]
dir_name = ["UP", "RIGHT", "DOWN", "LEFT"]
TURN_MOVE = 1
TURN_PUSH = 0

class Util:
    @classmethod
    def is_vertical(cls, dir):
        return dir == 0 or dir == 2

    @classmethod
    def manhattan_distance(cls, x0, y0, x1, y1):
        return abs(x0 - x1) + abs(y0 - y1)


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
    return grid[row][col][direction] == '1' and inside(row_dest, col_dest) and grid[row_dest][col_dest][
        inv_dir(direction)] == '1'


def print_moves(dirs):
    assert len(dirs) != 0
    print("MOVE", end="")
    for i in dirs:
        print(" {}".format(dir_name[i]), end="")
    print()


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
        :param grid: the grid
        :param direction: 0, 1, 2, 3, 4 for UP, RIGHT, DOWN, LEFT
        :return: TRUE / FALSE
        """
        return can_go(grid, self.row, self.col, direction)

    def go(self, grid, dir):
        assert self.can_go(grid, dir)
        self.row += d_row[dir]
        self.col += d_col[dir]


class Item:
    def __init__(self):
        self.name = None
        self.row = None
        self.col = None
        self.player = None

    def read(self):
        inputs = input().split()
        self.name = inputs[0]
        self.col = int(inputs[1])
        self.row = int(inputs[2])
        self.player = int(inputs[3])


class Goal(Item):
    def __init__(self, row, col):
        super(Goal, self).__init__()
        self.row = row
        self.col = col


def run():
    while True:
        turn_type = int(input())
        grid = read_grid()
        me = Player()
        he = Player()
        me.read()
        he.read()

        num_items = int(input())  # the total number of items available on board and on player tiles

        items = []
        for _ in range(num_items):
            item = Item()
            item.read()
            items.append(item)

        num_quests = int(input())  # the total number of revealed quests for both players
        goal = None

        for i in range(num_quests):
            inputs = input().split()
            quest_item_name = inputs[0]
            quest_player_id = int(inputs[1])

            # search for the goal
            if quest_player_id == MY_ID:
                for item in items:
                    if item.name == quest_item_name and item.player == MY_ID:
                        goal = Goal(row=item.row, col=item.col)

            # the goal must be found
            assert goal is not None

        if turn_type == TURN_MOVE:
            moves = []
            for rep in range(20):
                dir_list = [0, 1, 2, 3]
                random.shuffle(dir_list)
                for dir in dir_list:
                    row_next = me.row + d_row[dir]
                    col_next = me.col + d_col[dir]
                    distance_to_goal_now = Util.manhattan_distance(me.row, me.col, goal.row, goal.col)
                    distance_to_goal_next = Util.manhattan_distance(row_next, col_next, goal.row, goal.col)
                    if me.can_go(grid, dir):
                        if goal.row == -1 or goal.row == -2 or distance_to_goal_now > distance_to_goal_next:
                            moves.append(dir)
                            me.go(grid, dir)
                            break

            if len(moves) == 0:
                log("NO WAY TO MOVE AT ALL!")
                print("PASS")
            else:
                print_moves(moves)
        else:
            dir_push = random.randint(0, 3)
            to_push = me.row
            if Util.is_vertical(dir_push):
                to_push = me.col

            print("PUSH {0} {1}".format(to_push, dir_name[dir_push]))


if __name__ == '__main__':
    run()
