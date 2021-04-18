""""""
from queue import PriorityQueue
import operator

'''compute possible results from a given start'''


def expand(startPos, links):
    poss = []
    for link in links:
        if startPos in link:
            if link[0] == startPos:
                poss.append(link[1])
            else:
                poss.append(link[0])
    return poss


'''search for the shortest solution that lead to exit, 
   return a list of points from start to exit      '''


def search(startPos, exitPos, links):
    """Search the node that has the lowest combined cost and heuristic first."""

    class Node:
        def __init__(self, pos, parent, prev_cost):
            self.pos = pos  # a tuple (x, y)
            self.parent = parent  # parent node
            self.cost_sum = prev_cost + 1
            self.f = self.cost_sum

        def __lt__(self, other):
            return self.cost_sum < other.cost_sum

        def __eq__(self, other):
            return self.cost_sum == other.cost_sum

    # frontier = {startNode}
    start_node = Node(pos=startPos,
                      parent=None,
                      prev_cost=0)

    frontier = PriorityQueue()
    frontier.put(start_node)

    # expanded = {}
    expanded = []
    solutions = []

    # while frontier is not empty:
    while not frontier.empty():

        # node = frontier.pop()
        node = frontier.get()

        # if isGoal(node):
        if node.pos == exitPos:
            # return path_to_node
            solutions.append(node.pos)
            while node.parent is not None:
                node = node.parent
                solutions.append(node.pos)
            # solutions.reverse()
            return solutions

        # if node not in expanded:
        if node.pos not in expanded:
            # expanded.add(node)
            expanded.append(node.pos)
            triples = expand(node.pos, links)  # triple (nextPos)
            for i in triples:
                child_pos = i
                child_node = Node(pos=child_pos,
                                  parent=node,
                                  prev_cost=node.cost_sum)
                frontier.put(child_node)
    return None


# n: the total number of nodes in the level, including the gateways
# l: the number of links
# e: the number of exit gateways
n, l, e = [int(i) for i in input().split()]  # 4  4  1
exits = []
links = []
nodes = []
for i in range(l):
    # n1: N1 and N2 defines a link between these nodes
    n1, n2 = [int(j) for j in input().split()]
    if n1 not in nodes:
        nodes.append(n1)
    if n2 not in nodes:
        nodes.append(n2)

    links.append((n1, n2))
for i in range(e):
    ei = int(input())  # the index of a gateway node
    exits.append(ei)

# game loop
while True:
    si = int(input())  # The index of the node on which the Skynet agent is positioned this turn
    # find the path from the agent position to exit
    min_length = float('inf')
    target_solution = None

    exits_links = []  # links that contains exit (exit, node) or (node, exit)
    for exit in exits:
        for link in links:
            if exit in link:
                exits_links.append(link)

    # classify nodes
    dangerous_nodes = []
    for node in nodes:
        count = 0
        for link in exits_links:
            if node in link:
                count += 1
        if count >= 2:
            dangerous_nodes.append((node, count))

    all_solutions = []
    for exit in exits:
        solution = search(startPos=si, exitPos=exit, links=links)
        if solution is None:
            continue
        if min_length > len(solution):
            min_length = len(solution)
            target_solution = solution
        all_solutions.append(solution)

    isFlag = False
    if target_solution is None:  # already won
        print(links[0][0], links[0][1])
        links.remove((links[0][0], links[0][1]))
    else:
        for path in target_solution:
            if path in dangerous_nodes:
                isFlag = True
                break
            elif min_length <= 2:
                isFlag = True
            else:
                isFlag = False

        # if 1-step-away
        if isFlag and min_length <= 3:
            print(target_solution[0], target_solution[1])
            if (target_solution[0], target_solution[1]) in links:
                links.remove((target_solution[0], target_solution[1]))
            else:
                links.remove((target_solution[1], target_solution[0]))
        else:
            # at least 2-step-away
            all_solutions.sort(key=len)
            # and the exit is on one of the solution

            if len(dangerous_nodes) != 0:
                for solution in all_solutions:
                    if dangerous_nodes[0][0] in solution:
                        print(solution[0], solution[1])
                        links.remove((solution[0], solution[1]))
                        break
            else:
                print(target_solution[0], target_solution[1])
                if (target_solution[0], target_solution[1]) in links:
                    links.remove((target_solution[0], target_solution[1]))
                else:
                    links.remove((target_solution[1], target_solution[0]))
