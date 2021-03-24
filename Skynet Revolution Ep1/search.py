""""""
from queue import PriorityQueue

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
for i in range(l):
    # n1: N1 and N2 defines a link between these nodes
    n1, n2 = [int(j) for j in input().split()]
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
    for exit in exits:
        solution = search(startPos=si, exitPos=exit, links=links)
        if solution is None:
            continue
        if min_length > len(solution):
            min_length = len(solution)
            target_solution = solution
    if target_solution is None:
        print(links[0][0], links[0][1])
        links.remove((links[0][0], links[0][1]))
    else:
        print(target_solution[0], target_solution[1])
        if (target_solution[0], target_solution[1]) in links:
            links.remove((target_solution[0], target_solution[1]))
        else:
            links.remove((target_solution[1], target_solution[0]))
