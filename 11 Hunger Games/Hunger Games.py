def think():
    class Player:
        def __init__(self, name):
            self.name = name
            self.killed = []
            self.killer = None
            self.isDead = False
            self.isLast = False

        def addKilled(self, name):
            self.killed.append(name)
            self.killed.sort()

        def setKiller(self, name):
            self.killer = name
            self.isDead = True

        def prettyPrint(self):
            print("Name:", self.name)
            print("Killed: ", end="")
            if len(self.killed) == 0:
                print("None")
            else:
                print(*self.killed, sep=", ")

            print("Killer: ", end="")
            if self.killer is None:
                print("Winner")
            else:
                print(self.killer)

            if not self.isLast:
                print()

    players = []

    tributes = int(input())
    for i in range(tributes):
        player_name = input()
        player = Player(name=player_name)
        players.append(player)

    players.sort(key=lambda x: x.name, reverse=False)
    players[-1].isLast = True

    turns = int(input())
    for i in range(turns):
        info = input()
        # Mario killed Bowser
        names = info.split("killed")
        killer_name = names[0].replace(" ", "")
        killed_name = names[1].replace(" ", "")
        killed_names = killed_name.split(",")
        # print(name1, name2)
        for killed_name in killed_names:
            for player in players:
                if player.name == killer_name:  # find killer
                    player.addKilled(killed_name)
                if player.name == killed_name:  # find killed
                    player.setKiller(killer_name)



    for player in players:
        player.prettyPrint()


if __name__ == '__main__':
    think()
