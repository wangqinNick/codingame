def calculatePath(map, startPoint, w, h):
    """
    .>>v
    .^#v
    ..#v
    ...T
    """
    is_first = True
    x = startPoint[0]
    y = startPoint[1]
    length = 0

    while True:

        if y < 0 or y >= w or x < 0 or x >= h:
            return -1

        elif not is_first and x == startPoint[0] and y == startPoint[1]:
            return -1

        elif map[x][y] == '>':
            y += 1
            length += 1
            is_first = False

        elif map[x][y] == '<':
            y -= 1
            length += 1
            is_first = False

        elif map[x][y] == 'v':
            x += 1
            length += 1
            is_first = False

        elif map[x][y] == '^':
            x -= 1
            length += 1
            is_first = False

        elif map[x][y] == 'T':
            return length + 1

        elif map[x][y] == '.' or map[x][y] == '#':
            return -1


def run():
    w, h = [int(i) for i in input().split()]
    start_row, start_col = [int(i) for i in input().split()]
    n = int(input())

    map = []  # store one single map
    length = []

    for i in range(n):
        map.clear()
        for j in range(h):
            map_row = input()
            map.append(map_row)

        # find the path
        length.append(calculatePath(map, (start_row, start_col), w, h))

    min_index = -1
    min_length = float('inf')
    for i in range(n):
        if 0 <= length[i] < min_length:
            min_index = i
            min_length = length[i]
    if min_index == -1:
        print("TRAP")
    else:
        print(min_index)


run()
