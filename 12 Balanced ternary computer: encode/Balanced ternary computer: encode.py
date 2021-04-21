n = int(input())
ans = []

while n != 0:
    result = n // 3
    reminder = n - result * 3
    if reminder > 1:
        result += 1
        reminder = n - result * 3
    n = result
    ans.append(reminder)

if len(ans) != 0:
    ans.reverse()
    for i in ans:
        if i == -1:
            print('T', end='')
        else:
            print(i, end='')
    print()
else:
    print(0)

