def run():
    n, m, c = [int(i) for i in input().split()]
    isBlown = False
    apps = []

    for i in input().split():
        nx = int(i)
        apps.append(nx)

    bool_apps = [False] * len(apps)
    total_consumption = 0
    max_total = -1

    for i in input().split():
        mx = int(i) - 1
        if bool_apps[mx]:  # was on, turning off
            bool_apps[mx] = False
            total_consumption -= apps[mx]
        else:
            bool_apps[mx] = True
            total_consumption += apps[mx]

        if total_consumption > c:
            print("Fuse was blown.")
            isBlown = True
            break
        else:
            if max_total < total_consumption:
                max_total = total_consumption

    if not isBlown:
        print("Fuse was not blown.")
        print("Maximal consumed current was {} A.".format(max_total))


if __name__ == '__main__':
    run()
