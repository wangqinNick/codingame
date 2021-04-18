import math, copy


def main():
    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def distance(self, p):
            return math.sqrt((self.x - p.x) ** 2 + (self.y - p.y) ** 2)

    class Agent(Point):
        def __init__(self, x, y, player_id, walls_left, goal):
            super(Agent, self).__init__(x, y)
            self.player_id = player_id
            self.walls_left = walls_left
            self.goal = goal

    class Wall(Point):
        def __init__(self, x, y, orientation):
            super(Wall, self).__init__(x, y)
            self.orientation = orientation

    class Actions:
        _directions = {'UP': (-1, 0),
                       'DOWN': (1, 0),
                       'RIGHT': (0, 1),
                       'LEFT': (0, -1)}

        _directionsAsList = [('UP', (-1, 0)), ('DOWN', (1, 0)), ('RIGHT', (0, 1)),
                             ('LEFT', (0, -1))]

    class Grid:
        def __init__(self, width, height):
            self.width = width
            self.height = height
            self.data = [[False for y in range(
                height)] for x in range(width)]

        def __getitem__(self, i):
            return self.data[i]

        def __setitem__(self, key, item):
            self.data[key] = item

    class State:
        def __init__(self, agents, walls, my_id, w, h):
            self.all_agents = agents
            self.my_agents = []
            self.enemy_agents = []
            self.walls_list = walls
            self.my_id = my_id
            self.wall_grid = Grid(width=w, height=h)
            self.width = w
            self.height = h

            for agent in agents:
                if agent.player_id == self.my_id:
                    self.my_agents.append(agent)
                else:
                    self.enemy_agents.append(agent)

            for wall in self.walls_list:
                for i in range(2):
                    if wall.orientation == 'H':
                        wall[wall.x][wall.y + i] = True
                    else:
                        wall[wall.x + i][wall.y] = True

        def getNumAgents(self):
            return len(self.all_agents)

        def isWin(self):
            for agent in self.all_agents:
                if agent.player_id == self.my_id:
                    if agent.goal == "UP" and agent.y == 0: return True
                    if agent.goal == "DOWN" and agent.y == self.height - 1: return True
                    if agent.goal == "RIGHT" and agent.x == self.width - 1: return True
                    if agent.goal == "LEFT" and agent.x == 0: return True

        def isLose(self):
            for agent in self.all_agents:
                if agent.player_id != self.my_id:
                    if agent.goal == "UP" and agent.y == 0: return True
                    if agent.goal == "DOWN" and agent.y == self.height - 1: return True
                    if agent.goal == "RIGHT" and agent.x == self.width - 1: return True
                    if agent.goal == "UP" and agent.x == 0: return True

        def getLegalActions(self, player_id):
            if self.isWin() or self.isLose():
                return []

            agent = self.all_agents[player_id]
            possible = []

            for dir, vec in Actions._directionsAsList:
                dx, dy = vec
                next_y = agent.x + dy
                next_x = agent.y + dx
                if not self.wall_grid[next_x][next_y] and next_x > 0 and next_y > 0\
                        and next_x < self.width and next_y < self.height:
                    possible.append(dir)
            return possible

        def getNextState(self, agentIndex, action):
            if self.isWin() or self.isLose():
                raise Exception('Can\'t generate a child of a terminal state.')
            state = copy.deepcopy(self)
            agent = state.all_agents[agentIndex]
            if action == "LEFT":
                agent.x -= 1
            elif action == "RIGHT":
                agent.x += 1
            elif action == "DOWN":
                agent.y += 1
            elif action == "UP":
                agent.y -= 1

    def evaluationFunction(state):

        if state.isWin(): return float('inf')
        if state.isLose(): return float('-inf')

        my_distance = None
        enemy_distance_list = []
        for agent in state.all_agents:
            if agent.player_id == state.my_id:
                if agent.goal == "UP":
                    my_distance = agent.y
                elif agent.goal == "DOWN":
                    my_distance = state.height - agent.y - 1
                elif agent.goal == "RIGHT":
                    my_distance = state.width - agent.x - 1
                elif agent.goal == "LEFT":
                    my_distance = agent.x
            else:
                distance = None
                if agent.goal == "UP":
                    distance = agent.y
                elif agent.goal == "DOWN":
                    distance = state.height - agent.y - 1
                elif agent.goal == "RIGHT":
                    distance = state.width - agent.x - 1
                elif agent.goal == "LEFT":
                    distance = agent.x
                enemy_distance_list.append(distance)
        best_enemy = min(enemy_distance_list)
        score = (min(my_distance) / min(best_enemy)) ** 1.3
        return score

    def getAction(gameState, max_depth):
        GhostIndex = [i for i in range(0, gameState.getNumAgents())]

        def isTerminate(state, depth):
            return state.isWin() or state.isLose() or depth == max_depth

        def value(state, alpha, beta, depth, ghostIndex=0):
            if isTerminate(state, depth): return evaluationFunction(state)
            if ghostIndex == state.my_id:


        def max_value(state, alpha, beta, depth, ghostIndex=0):
            if isTerminate(state, depth): return evaluationFunction(state)

            v = -float('inf')
            for action in state.getLegalActions(0):
                v = max(v, value(state=state.getNextState(0, action),
                                     alpha=alpha,
                                     beta=beta,
                                     depth=depth,
                                     ghostIndex=1))
                if v > beta: return v
                alpha = max(alpha, v)
            return v

        def min_value(state, alpha, beta, depth, ghostIndex):
            if isTerminate(state, depth): return evaluationFunction(state)

            v = float('inf')
            for action in state.getLegalActions(ghostIndex):
                if ghostIndex == GhostIndex[-1]:
                    v = min(v, value(state=state.getNextState(ghostIndex, action),
                                         alpha=alpha,
                                         beta=beta,
                                         depth=depth + 1))
                else:
                    v = min(v, value(state=state.getNextState(ghostIndex, action),
                                         alpha=alpha,
                                         beta=beta,
                                         depth=depth,
                                         ghostIndex=ghostIndex + 1))
                if v < alpha: return v
                beta = min(beta, v)
            return v

        def alpha_beta():
            v = -float('inf')
            move = None
            A = -float('inf')
            B = float('inf')
            for action in gameState.getLegalActions(0):
                tmp = min_value(state=gameState.getNextState(0, action),
                                alpha=A,
                                beta=B,
                                depth=0,
                                ghostIndex=1)
                if v < tmp:  # updating best move
                    v = tmp
                    move = action
                if v > B:  # pruning
                    continue
                A = max(A, v)  # updating best value so far
            return move

        return alpha_beta()

    def run():
        w, h, player_count, my_id = [int(i) for i in input().split()]

        agents = []
        walls = []

        # game loop
        while True:
            # load agents
            for i in range(player_count):
                x, y, walls_left = [int(j) for j in input().split()]
                if x == 0:
                    agent = Agent(x=x, y=y, player_id=i,
                                  walls_left=walls_left,
                                  goal='RIGHT')

                elif y == 0:
                    agent = Agent(x=x, y=y, player_id=i,
                                  walls_left=walls_left,
                                  goal='DOWN')
                elif x == w - 1:
                    agent = Agent(x=x, y=y, player_id=i,
                                  walls_left=walls_left,
                                  goal='LEFT')
                else:
                    agent = Agent(x=x, y=y, player_id=i,
                                  walls_left=walls_left,
                                  goal='UP')

                agents.append(agent)

            # load walls
            wall_count = int(input())  # number of walls on the board
            for i in range(wall_count):
                inputs = input().split()
                wall_x = int(inputs[0])  # x-coordinate of the wall
                wall_y = int(inputs[1])  # y-coordinate of the wall
                wall_orientation = inputs[2]  # wall orientation ('H' or 'V')
                wall = Wall(x=wall_x, y=wall_y, orientation=wall_orientation)
                walls.append(wall)
            state = State(agents=agents, walls=walls, my_id=my_id, w=w, h=h)
            action = getAction(gameState=state, max_depth=4)
            print(action)
    run()


if __name__ == '__main__':
    main()
