import copy

global N
N = input()
result = []

board = [[0 for j in range(N)]
         for i in range(N)]


def print_board(board_):
    for i in range(len(board_)):
        for j in range(len(board_)):
            print(board_[i][j], end='')
        print()


def select_unassigned_variable(board_):
    for i in range(len(board_)):
        for j in range(len(board_[0])):
            if board_[i][j] == -1:
                return i, j  # row, col

    return None


def valid(board_, row, col, value=1):
    for i in range(col):
        if board_[row][i] == 1:
            return False

        # Check upper diagonal on left side
    for i, j in zip(range(row, -1, -1),
                    range(col, -1, -1)):
        if board_[i][j] == 1:
            return False

        # Check lower diagonal on left side
    for i, j in zip(range(row, N, 1),
                    range(col, -1, -1)):
        if board_[i][j] == 1:
            return False

    return True


def solve(board_, col):
    if col >= N:
        return True
    for i in range(N):

        if valid(board_, i, col, 1):

            # Place this queen in board[i][col]
            board[i][col] = 1

            # recur to place rest of the queens
            if solve(board, col + 1):
                return True

            # If placing queen in board[i][col
            # doesn't lead to a solution, then
            # queen from board[i][col]
            board[i][col] = 0

        # if the queen can not be placed in any row in
        # this colum col then return false
    return False


def solveNQUtil(board_, col):
    """ base case: If all queens are placed
    then return true """
    if col == N:
        v = []
        for i in board_:
            for j in range(len(i)):
                if i[j] == 1:
                    v.append(j + 1)
        result.append(v)
        return True

    ''' Consider this column and try placing
    this queen in all rows one by one '''
    res = False
    for i in range(N):

        ''' Check if queen can be placed on
        board[i][col] '''
        if valid(board_, i, col):
            # Place this queen in board[i][col]
            board_[i][col] = 1

            # Make result true if any placement
            # is possible
            res = solveNQUtil(board_, col + 1) or res

            ''' If placing queen in board[i][col]
            doesn't lead to a solution, then
            remove queen from board[i][col] '''
            board_[i][col] = 0  # BACKTRACK

    ''' If queen can not be place in any row in
        this column col then return false '''
    return res

def solveNQ():
    result.clear()
    solveNQUtil(board, 0)
    result.sort()
    return result


if __name__ == '__main__':
    res = solveNQ()
    print(len(res))
