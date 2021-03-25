def run():
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

    class Node:
        def __init__(self, data, parent):
            self.data = data
            self.parent = parent

    class Person:
        def __init__(self, name, parent, birth, death, religion, gender):
            self.name = name
            self.parent = parent
            self.birth = birth
            self.death = death
            self.religion = religion
            self.gender = gender

        def __lt__(self, other):
            # self after other
            if self.gender == 'F' and other.gender == 'M': return True
            if self.gender == other.gender:
                if self.birth > other.birth: return True
            return False

        def __eq__(self, other):
            if self.gender == other.gender and self.birth == other.birth:
                return True
            return False

    def expand(person, people):
        # return all children of the person
        children = []
        for p in people:
            if p.parent == person.name:
                children.append(p)
        children.sort(reverse=False)
        return children

    def search(people):
        # initialize
        old_one = people[0]
        start_node = Node(data=old_one, parent=None)

        frontier = Stack()
        frontier.push(start_node)

        expanded = []
        expanded_node = Stack()
        solution = []

        while not frontier.isEmpty():
            node = frontier.pop()

            if len(expanded) == len(people) - 1:  # finish all people
                # print(expanded)
                if node.data.death == '-' and node.data.religion != 'Catholic':
                    solution.append(node.data.name)
                while not expanded_node.isEmpty():

                    n = expanded_node.pop()
                    if n.data.death == '-' and n.data.religion != 'Catholic':
                        solution.append(n.data.name)
                solution.reverse()
                return solution

            if node.data.name not in expanded:
                expanded.append(node.data.name)
                expanded_node.push(node)
                children = expand(node.data, people)  # triple (nextPos)
                for child in children:
                    child_node = Node(data=child,
                                      parent=node)
                    frontier.push(child_node)
        return None

    n = int(input())
    people = []

    for i in range(n):
        inputs = input().split()
        name = inputs[0]
        parent = inputs[1]
        birth = int(inputs[2])
        death = inputs[3]
        religion = inputs[4]
        gender = inputs[5]
        person = Person(name, parent, birth, death, religion, gender)
        people.append(person)
    solution = search(people)
    for s in solution:
        print(s)


run()
