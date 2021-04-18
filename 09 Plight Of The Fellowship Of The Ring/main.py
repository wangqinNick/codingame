import heapq, math


def main():
    class PriorityQueue:
        """
        Implements a priority queue data structure. Each inserted item
        has a priority associated with it and the client is usually interested
        in quick retrieval of the lowest-priority item in the queue. This
        data structure allows O(1) access to the lowest-priority item.
        """

        def __init__(self):
            self.heap = []
            self.count = 0

        def push(self, item, priority):
            entry = (priority, self.count, item)
            heapq.heappush(self.heap, entry)
            self.count += 1

        def pop(self):
            (_, _, item) = heapq.heappop(self.heap)
            return item

        def isEmpty(self):
            return len(self.heap) == 0

        def update(self, item, priority):
            # If item already in priority queue with higher priority, update its priority and rebuild the heap.
            # If item already in priority queue with equal or lower priority, do nothing.
            # If item not in priority queue, do the same thing as self.push.
            for index, (p, c, i) in enumerate(self.heap):
                if i == item:
                    if p <= priority:
                        break
                    del self.heap[index]
                    self.heap.append((priority, c, item))
                    heapq.heapify(self.heap)
                    break
            else:
                self.push(item, priority)

    class Spot:
        def __init__(self, index, x, y):
            self.index = index
            self.x = x
            self.y = y

    def heuristic(spot, end_spot):
        distance_to_goal = calcDistance(spot.x, spot.y, end_spot.x, end_spot.y)
        return distance_to_goal

    class Node:
        def __init__(self, spot, parent, cost, prev_cost, goal):
            self.spot = spot
            self.parent = parent
            self.g = cost + prev_cost
            self.h = heuristic(spot=spot, end_spot=goal)
            self.f = self.g + self.h

    def calcDistance(x0, y0, x1, y1):
        return math.sqrt((x0 - y0) ** 2 + (x1 - y1) ** 2)

    def expand(node, links, orc_list, spot_list):
        children = []
        for link in links:  # (2, 5)
            if node.spot.index in link:

                next_index = None
                if link[0] == node.spot.index and link[1] != link[0]:
                    next_index = link[1]
                elif link[1] == node.spot.index and link[1] != link[0]:
                    next_index = link[1]

                next_spot = spot_list[next_index]
                distance = calcDistance(node.spot.x, node.spot.y,
                                        next_spot.x, next_spot.y)
                distances = []
                for orc in orc_list:
                    distance = calcDistance(x0=orc[0], y0=orc[1],
                                            x1=next_spot.x, y1=next_spot.y)
                    distances.append(distance)
                if len(orc_list) == 0 or min(distances) > distance:
                    children.append(next_index)

        return children

    def search(spot_list, orc_list, links, start_spot, end_spot):
        # initialize
        start_node = Node(spot=start_spot, parent=None, cost=0, prev_cost=0, goal=end_spot)

        frontier = PriorityQueue()
        frontier.push(start_node, priority=0)
        expanded = []

        while not frontier.isEmpty():
            node = frontier.pop()

            if node.spot.index == end_spot.index:
                solution = [node.spot.index]
                while node.parent is not None:
                    node = node.parent
                    solution.append(node.spot.index)
                solution.reverse()
                return solution

            if node.spot.index not in expanded:
                expanded.append(node.spot.index)
                children = expand(node, links, orc_list, spot_list)
                for child_index in children:
                    spot = spot_list[child_index]
                    cost = calcDistance(spot.x, spot.y, node.spot.x, node.spot.y)
                    child_node = Node(spot=spot, parent=node,
                                      prev_cost=node.g,
                                      cost=cost,
                                      goal=end_spot)
                    frontier.push(item=child_node, priority=child_node.f)

        return None

    def run():
        spot_list = []
        orc_list = []  # a list of (x, y), ...
        links = []  # a list of (sp1, sp2), ...

        n = int(input())  # an integer N denoting the number of spots
        m = int(input())  # an integer M denoting the number of orcs
        l = int(input())  # an integer L denoting the number of portals

        for i in range(n):
            xs, ys = [int(j) for j in input().split()]  # 2 integers XS, YS, the coordinates of the spots
            spot = Spot(index=i, x=xs, y=ys)
            spot_list.append(spot)

        for i in range(m):
            xo, yo = [int(j) for j in input().split()]  # 2 integers XO, YO, the coordinates of the orcs
            orc_list.append((xo, yo))

        for i in range(l):
            n1, n2 = [int(j) for j in input().split()]  # N1, N2, the indexes of 2 spots of a path forming a portal
            links.append((n1, n2))

        s = int(input())  # an integer S denoting the spot from which the fellowship start (the index)
        e = int(input())  # an integer E denoting the spot where the fellowship need to reach (the index)
        start_spot = None
        end_spot = None

        for spot in spot_list:
            if spot.index == s:
                start_spot = spot
            elif spot.index == e:
                end_spot = spot

        solution = search(spot_list, orc_list, links, start_spot, end_spot)
        if solution is None: print("IMPOSSIBLE")
        else: print(*solution)

    run()


main()
