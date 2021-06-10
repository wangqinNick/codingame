def simple_print_board(board_):
    for i in range(len(board_)):
        for j in range(len(board_)):
            print(board_[i][j], end='')
        print()

def print_board(board_):
    for i in range(len(board_)):
        if i % 3 == 0 and i != 0:
            print("-- -- -- -- -- -- -- --")
        for j in range(len(board_[i])):

            if j % 3 == 0 and j != 0:
                print(' | ', end='')
            print(board_[i][j], end=' ')
        print()


def select_unsigned_variable(board_):
    for i in range(len(board_)):
        for j in range(len(board_[0])):
            if board_[i][j] == 0:
                return i, j  # row, col

    return None


def valid(board_, row, col, value):
    for i in range(len(board_[0])):
        if board_[row][i] == value and col != i:
            return False

    # if board_[row].count(value) > 2:
    #     return False

    # Check column
    for i in range(len(board_)):
        if board_[i][col] == value and row != i:
            return False

        # Check box
    box_x = col // 3
    box_y = row // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board_[i][j] == value and (i, j) != (row, col):
                return False

    return True

def solve(board_):
    find = select_unsigned_variable(board_)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(board_, row, col, i):
            board_[row][col] = i

            if solve(board_):
                return True

            board_[row][col] = 0

    return False

def test():
    board_ = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]
    import time
    start = time.time()
    solve(board_)
    end = time.time()
    print(end - start)
    print_board(board_)


if __name__ == '__main__':
    # test()
    board = [[0 for i in range(9)] for j in range(9)]

    for i in range(9):
        line = input()
        for j in range(9):
            num = int(line[j])
            board[i][j] = num

    # print_board(board)

    solve(board)
    simple_print_board(board)



