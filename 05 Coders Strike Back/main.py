import math

def main():
    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def distance(self, p):
            return math.sqrt((self.x-p.x)**2 + (self.y-p.y)**2)

    class Unit(Point):
        def __init__(self, id, r, vx, vy, x, y):
            super(Unit, self).__init__(x, y)
            self.id = id
            self.r = r
            self.vx = vx
            self.vy = vy

    class CheckPoint(Unit):
        def bounce(self, u):
            pass

    class Pod(Unit):
        def __init__(self, id, r, vx, vy, x, y, angle, nextCheckPointId, num_checked, timeout, partner, has_shield):
            super(Pod, self).__init__(id, r, vx, vy, x, y)
            self.angle = angle
            self.nextCheckPointId = nextCheckPointId
            self.num_checked = num_checked
            self.timeout = timeout
            self.partner = partner
            self.has_shield = has_shield

    while True:
        x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in
                                                                                             input().split()]
        opponent_x, opponent_y = [int(i) for i in input().split()]

