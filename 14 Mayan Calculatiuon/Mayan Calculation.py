import math


def run():
    l, h = [int(i) for i in input().split()]

    pieces = []

    for i in range(h):
        numeral = input()
        for j in range(20):  # 20 numbers
            s = numeral[j * l: (j + 1) * l]  # l = 4, j = 0
            pieces.append(s)

    # print(len(pieces))  # 80

    numbers = [["" for i in range(h)] for j in range(20)]

    for i in range(20):
        numbers[i].clear()

    for i in range(len(pieces)):
        reminder = i % 20
        # print(reminder)
        numbers[reminder].append(pieces[i])

    numbers_ = ["" for _ in range(20)]

    for i in range(20):
        numbers_[i] = "".join(numbers[i])

    number1s = []

    s1 = int(input())
    for _ in range(int(s1 // h)):
        number1 = []
        for _ in range(h):
            num_1line = input()
            number1.append(num_1line)
        number1_ = "".join(number1)
        number1s.append(number1_)

    number2s = []

    s2 = int(input())
    for _ in range(int(s2 // h)):
        number2 = []
        for _ in range(h):
            num_2line = input()
            number2.append(num_2line)
        number2_ = "".join(number2)
        number2s.append(number2_)

    operation = input()

    num1 = []
    # print(number1s)
    num2 = []

    for j in number1s:
        for i in range(len(numbers)):
            if j == numbers_[i]: num1.append(i)
    for j in number2s:
        for i in range(len(numbers)):
            if j == numbers_[i]: num2.append(i)

    num1_ = 0
    num1.reverse()
    num2.reverse()
    num2_ = 0
    # print(num1, num2)

    for i in range(len(num1)): num1_ += num1[i] * math.pow(20, i)
    for i in range(len(num2)): num2_ += num2[i] * math.pow(20, i)

    # print(num1_, operation, num2_, end=' ')
    res = None
    if operation == '*':
        res = num1_ * num2_
    elif operation == '+':
        res = num1_ + num2_
    elif operation == '-':
        res = num1_ - num2_
    elif operation == '/':
        res = num1_ / num2_
    res = int(res)
    # print("res", res)

    reminder_ = []
    while res > 0:
        reminder = res % 20
        reminder_.append(reminder)
        res = res // 20

    reminder_.reverse()
    # print(reminder_)
    for i in reminder_:
        for j in numbers[i]:
            print(j)
    if len(reminder_) == 0:
        for i in numbers[0]:
            print(i)
if __name__ == '__main__':
    run()
