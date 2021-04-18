import heapq


def main():
    h_values = []
    successors = []
    # e: num of edges
    # s: start
    # g: goal
    n, e, s, g = [int(i) for i in input().split()]
    for i in input().split():
        node = int(i)
        h_values.append(node)
    for i in range(e):
        x, y, c = [int(j) for j in input().split()]
        successor = (x, y, c)
        successors.append(successor)
    solution = aStarSearch(s, g, h_values, successors)
    for i in solution:
        print(i[0], i[1])


def expand(nodeIndex, successors):
    possible_successors = []
    for successor in successors:
        if successor[0] == nodeIndex:
            possible_successors.append(successor)
        elif successor[1] == nodeIndex:
            possible_successors.append((successor[1], successor[0], successor[2]))
    possible_successors.sort()
    return possible_successors


def aStarSearch(start, goal, h_values, successors):
    """Search the node that has the lowest combined cost and heuristic first."""

    class Stack:
        "A container with a last-in-first-out (LIFO) queuing policy."

        def __init__(self):
            self.list = []

        def push(self, item):
            "Push 'item' onto the stack"
            self.list.append(item)

        def pop(self):
            "Pop the most recently pushed item from the stack"
            return self.list.pop()

        def __len__(self):
            return len(self.list)

        def isEmpty(self):
            "Returns true if the stack is empty"
            return len(self.list) == 0

        def __contains__(self, item):
            return item in self.list

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

    class Node:
        def __init__(self, index, parent, prev_cost, cost, h_value):
            self.index = index  # a tuple (x, y)
            self.parent = parent  # parent nodes
            self.g_value = prev_cost + cost
            self.f = self.g_value + h_value  # for any node, f(n) = g(n) + h(n)

        def __lt__(self, other):
            if self.f < other.f: return True
            if self.f > other.f: return False
            if self.f == other.f:
                if self.index < other.index: return True
            return False

        def __eq__(self, other):
            if self.f == other.f and self.index == other.index:
                return True
            return False

    startNode = Node(index=start,
                     parent=None,
                     prev_cost=0,
                     cost=0,
                     h_value=h_values[start]
                     )

    frontier = Stack()
    frontier.push(startNode)

    # expanded = {}
    expanded = []
    solutions = []

    # while frontier is not empty:
    while not frontier.isEmpty():

        # node = frontier.pop()
        node = frontier.pop()

        # if isGoal(node):
        if node.index == goal:
            # return path_to_node

            solutions.append((node.index, node.f))
            return solutions

        # if node not in expanded:
        if node.index not in expanded:
            # expanded.add(node)
            expanded.append(node.index)
            solutions.append((node.index, node.f))
            triples = expand(node.index, successors)  # (parent, child, cost)
            for i in triples:
                child_index = i[1]
                child_cost = i[2]
                child_node = Node(index=child_index,
                                  parent=node,
                                  prev_cost=node.g_value,
                                  cost=child_cost,
                                  h_value=h_values[child_index]
                                  )
                frontier.push(child_node)
    return None


if __name__ == '__main__':
    main()
