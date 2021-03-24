def main():
    class State:
        def __init__(self, ships, barrels, game_round):
            self.my_ships = []
            self.enemy_ships = []

            for ship in ships:
                if ship.owner == 1:
                    self.my_ships.append(ship)
                else:
                    self.enemy_ships.append(ship)
            self.num_my_ship = len(self.my_ships)
            self.num_enemy_ship = len(self.enemy_ships)
            self.barrels = barrels
            self.game_round = game_round
            self.max_thinking_depth = 5

        def getLegalActions(self, playerId):
            possible_actions = []
            for i in range(5):
                next_coord = self.my_ships[0].coordinate[0] + 


    class Barrel:
        def __init__(self, coordinate, rum):
            self.coordinate = coordinate
            self.rum = rum

    class Ship:
        def __init__(self, coordinate, rotation, speed, rum, owner):
            self.coordinate = coordinate
            self.rotation = rotation
            self.speed = speed
            self.rum = rum
            self.owner = owner

        def isMine(self):
            return self.owner == 1

    def getAction(gameState):

        def isTerminate(state, thinking_depth):
            # reach max thinking depth
            if thinking_depth == state.max_thinking_depth:
                return True

            # run out of turns
            if gameState.game_round > 200:
                return True

            # run out of ship
            if state.num_my_ship == 0 or state.num_enemy_ship == 0:
                return True

            return False

        def evaluationFunction(state):
            if state.num_my_ship == 0: return float('-inf')
            if state.num_enemy_ship == 0: return float('inf')
            my_rum = 0
            for ship in state.my_ships:
                my_rum += ship.rum
            enemy_rum = 0
            for ship in state.enemy_ships:
                enemy_rum += ship.rum
            return my_rum / enemy_rum

        def max_value(state, alpha, beta, depth):
            if isTerminate(state, depth): return evaluationFunction(state)

            v = -float('inf')
            for action in state.getLegalActions(0):
                v = max(v, min_value(state=state.getNextState(0, action),
                                     alpha=alpha,
                                     beta=beta,
                                     depth=depth))
                if v > beta: return v
                alpha = max(alpha, v)
            return v

        def min_value(state, alpha, beta, depth):
            if isTerminate(state, depth): return evaluationFunction(state)

            v = float('inf')
            for action in state.getLegalActions(1):
                v = min(v, max_value(state=state.getNextState(1, action),
                                     alpha=alpha,
                                     beta=beta,
                                     depth=depth + 1))

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
                                depth=0)
                if v < tmp:  # updating best move
                    v = tmp
                    move = action
                if v > B:  # pruning
                    continue
                A = max(A, v)  # updating best value so far
            return move

        return alpha_beta()

    game_round = 1
    # game loop
    while True:
        my_ship_count = int(input())  # the number of remaining ships
        entity_count = int(input())  # the number of entities (e.g. ships, mines or cannonballs)
        ships = []
        barrels = []
        for i in range(entity_count):
            inputs = input().split()
            entity_id = int(inputs[0])
            entity_type = inputs[1]
            x = int(inputs[2])
            y = int(inputs[3])
            arg_1 = int(inputs[4])
            arg_2 = int(inputs[5])
            arg_3 = int(inputs[6])
            arg_4 = int(inputs[7])
            # check for ship
            if entity_type == "SHIP":
                ship = Ship(coordinate=(x, y), rotation=arg_1, speed=arg_2, rum=arg_3, owner=arg_4)
                ships.append(ship)
            if entity_type == "BARREL":
                barrel = Barrel(coordinate=(x, y), rum=arg_1)
                barrels.append(barrel)

        state = State(ships=ships, barrels=barrels, game_round=game_round)

        action = getAction(gameState=state)
        print(action)
        game_round += 1
