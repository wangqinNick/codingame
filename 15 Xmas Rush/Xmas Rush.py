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
MAX_THINKING_DEPTH = 4


class Util:
    @classmethod
    def is_vertical(cls, dir):
        return dir == 0 or dir == 2

    @classmethod
    def manhattan_distance(cls, x0, y0, x1, y1):
        return abs(x0 - x1) + abs(y0 - y1)

    # [['1', '1', '0', '0',], ...]
    @classmethod
    def read_grid(cls):
        cells = []
        for _ in range(7):
            row = []
            for tile in input().split():
                row.append(tile)
            cells.append(row)
        return cells.copy()

    @classmethod
    def inside(cls, r, c):
        """
        Check if (row, col) is inside the grid
        :param r: row
        :param c: col
        :return: True for inside
        """
        return 0 <= r < N and 0 <= c < N

    @classmethod
    def inv_dir(cls, direction):
        """
        Inverse the direction, from (row_dest, col_dest) to (row, col)
        :param direction: 0, 1, 2, 3 for Up, Right, Down, Left
        :return: 2, 3, 0, 1
        """
        return direction ^ 2

    @classmethod
    def can_go(cls, grid, row, col, direction):
        assert 0 <= direction <= 3  # Up, Right, Down, Left
        row_dest = row + d_row[direction]
        col_dest = col + d_col[direction]
        return grid[row][col][direction] == '1' and Util.inside(row_dest, col_dest) and grid[row_dest][col_dest][
            Util.inv_dir(direction)] == '1'

    @classmethod
    def print_moves(cls, dirs):
        assert len(dirs) != 0
        print("MOVE", end="")
        for i in dirs:
            print(" {}".format(dir_name[i]), end="")
        print()

    @classmethod
    def rotate_grid(cls, grid, which, dir):
        dir = int(dir)
        which = int(which)
        assert 0 <= dir < 4
        if cls.is_vertical(dir):
            if dir == 0:  # push up
                grid[:][which] = grid[1:][which] + grid[0][which]
            else:  # push down
                grid[:][which] = grid[-1][which] + grid[1:][which]
        else:
            if dir == 1:  # push right
                grid[which] = grid[which][-1] + grid[which][1:]
            else:  # push left
                grid[which] = grid[which][1:] + grid[which][0]


class GameState:
    def getLegalActions(self, turn):
        if self.isWin() or self.isLose():
            return []
        if turn == 0 or turn == 1:  # PUSH TURN
            # Format "which dir"
            actions = []
            direction_list = [0, 1, 2, 3]
            which_list = [i for i in range(N)]
            for i in which_list:
                for j in direction_list:
                    s = str(i) + " " + str(j)
                    actions.append(s)
            return actions

        if turn == 2:
            return self.players[0].getLegalActions(self.grid)
        if turn == 3:
            return self.players[1].getLegalActions(self.grid)

    def getNextState(self, turn, action):
        assert not self.isWin() or self.isLose()
        if turn == 0 or 2:
            playerId = MY_ID
        else:
            playerId = HIS_ID

        state = self.deepCopy()
        if turn == 0 or turn == 1:
            log(action)
            temp = action.split()
            which = temp[0]
            dir = temp[1]
            Util.rotate_grid(grid=state.grid, which=which, dir=dir)
            for player in state.players:
                # if the player is on the tiles pushed
                if player.row == which or player.col == which:
                    if dir == 0:  # up
                        player.row -= 1
                        if player.row == -1:
                            player.row = N - 1
                        else:
                            log("Invalid player position")
                    elif dir == 1:  # right
                        player.col += 1
                        if player.col == N:
                            player.col = 0
                        else:
                            log("Invalid player position")
                    elif dir == 2:  # down
                        player.row += 1
                        if player.row == N:
                            player.row = 0
                        else:
                            log("Invalid player position")
                    elif dir == 3:  # left
                        player.col -= 1
                        if player.col == -1:
                            player.col = N - 1
                        else:
                            log("Invalid player position")
                    else:
                        log("Invalid direction")

        elif turn == 2 or turn == 3:
            dir = int(action)
            log(dir)
            for player_ in state.players:
                if player_.id == playerId:
                    player_.go(self.grid, dir)
                    break
        return state

    def isWin(self):
        for p in self.players:
            if p.id == MY_ID:
                return p.num_completed == p.cntCards

    def isLose(self):
        for p in self.players:
            if p.id == HIS_ID:
                return p.num_completed == p.cntCards

    def __init__(self, players, items, grid):
        self.players = players  # [me, he]
        self.items = items
        self.grid = grid

    def deepCopy(self):
        new_players = []
        for player in self.players:
            new_player = player.deepCopy()
            new_players.append(new_player)

        new_items = []
        for item in self.items:
            new_item = item.deepCopy()
            new_items.append(new_item)

        new_grid = self.grid.copy()

        return GameState(players=new_players, items=new_items, grid=new_grid)


class Player:
    def __init__(self, id, num_completed):
        self.row = None
        self.col = None
        self.cntCards = None
        self.tile = None
        self.id = id
        self.num_completed = num_completed
        self.goal = None

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
        return Util.can_go(grid, self.row, self.col, direction)

    def go(self, grid, dir):
        assert self.can_go(grid, dir)
        self.row += d_row[dir]
        self.col += d_col[dir]
        if self.row == self.goal.row and self.col == self.goal.col:
            self.num_completed += 1

    def setGoal(self, goal):
        self.goal = goal

    def getLegalActions(self, grid):
        legal_actions = []
        for dir in [0, 1, 2, 3]:
            if self.can_go(grid=grid, direction=dir):
                legal_actions.append(dir)
        return legal_actions

    def setters(self, row, col, cntCards, tile, id, num_completed, goal):
        self.row = row
        self.col = col
        self.cntCards = cntCards
        self.tile = tile
        self.id = id
        self.num_completed = num_completed
        self.goal = goal

    def deepCopy(self):
        new_player = Player(id=self.id, num_completed=self.num_completed)
        new_player.setters(self.row, self.col, self.cntCards, self.tile, self.id, self.num_completed,
                           Goal(self.goal.row, self.goal.col))
        return new_player


class Item:
    def __init__(self):
        self.name = None
        self.row = None
        self.col = None
        self.player = None  # player id

    def read(self):
        inputs = input().split()
        self.name = inputs[0]
        self.col = int(inputs[1])
        self.row = int(inputs[2])
        self.player = int(inputs[3])

    def setters(self, name, row, col, player):
        self.name = name
        self.row = row
        self.col = col
        self.player = player

    def deepCopy(self):
        new_item = Item()
        new_item.setters(self.name, self.row, self.col, self.player)
        return new_item


class Goal(Item):
    def __init__(self, row, col):
        super(Goal, self).__init__()
        self.row = row
        self.col = col


def getAction(gameState, turn):
    # 0 for MY_TURN_PUSH, 2 for MY_TURN_MOVE, 1 for HIS_TURN_PUSH, 3 for HIS+_TURN_MOVE

    def evaluationFunction(state):
        return 0

    def isTerminate(state, d):
        return state.isWin() or state.isLose() or d == MAX_THINKING_DEPTH

    """
    turnIndex: 0 for MY_TURN_PUSH, 1 for MY_TURN_MOVE, 2 for HIS_TURN_PUSH, 3 for HIS+_TURN_MOVE
    """

    def min_value(state, d, turnIndex):  # minimizer
        turnIndex %= 4
        if isTerminate(state, d):
            return evaluationFunction(state)

        v = float('inf')
        for action in state.getLegalActions(turnIndex):
            v = min(v, max_value(state.getNextState(turnIndex, action), d + 1, turnIndex + 1))
        return v

    def max_value(state, d, turnIndex):  # maximizer
        turnIndex %= 4
        if isTerminate(state, d):
            return evaluationFunction(state)

        v = -float('inf')
        for action in state.getLegalActions(turnIndex):
            v = max(v, min_value(state.getNextState(turn=turnIndex, action=action), d, turnIndex + 1))
        return v

    res = [(action, max_value(gameState.getNextState(turn=1, action=action), d=0, turnIndex=1)) for action in
           gameState.getLegalActions(turn=0)]
    res.sort(key=lambda k: k[1])

    return res[-1][0]


def run():
    while True:
        turn_type = int(input())
        grid = Util.read_grid()
        me = Player(id=0, num_completed=0)
        he = Player(id=1, num_completed=0)
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
        his_goal = None

        for i in range(num_quests):
            inputs = input().split()
            quest_item_name = inputs[0]
            quest_player_id = int(inputs[1])

            # search for the goal
            if quest_player_id == MY_ID:
                for item in items:
                    if item.name == quest_item_name and item.player == MY_ID:
                        goal = Goal(row=item.row, col=item.col)
            else:
                for item in items:
                    if item.name == quest_item_name and item.player == HIS_ID:
                        his_goal = Goal(row=item.row, col=item.col)

        # the goal must be found
        assert goal is not None and his_goal is not None
        me.setGoal(goal)
        he.setGoal(his_goal)

        def think_simple():
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
                            if goal.row < 0 or distance_to_goal_now > distance_to_goal_next:
                                moves.append(dir)
                                me.go(grid, dir)
                                break

                if len(moves) == 0:
                    log("NO WAY TO MOVE AT ALL!")
                    print("PASS")
                else:
                    Util.print_moves(moves)
            else:
                dir_push = random.randint(0, 3)
                to_push = me.row
                if Util.is_vertical(dir_push):
                    to_push = me.col

                print("PUSH {0} {1}".format(to_push, dir_name[dir_push]))

        def think_hard():
            state = GameState(players=[me, he], items=items, grid=grid)

            if turn_type == TURN_PUSH:
                action = getAction(gameState=state, turn=0)
                which, dir = action.split()
                print("PUSH {0} {1}".format(which, dir_name[dir]))
            else:
                action = getAction(gameState=state, turn=1)
                print("MOVE {0}".format(dir_name[action]))

        think_simple()
        # think_hard()


if __name__ == '__main__':
    run()
