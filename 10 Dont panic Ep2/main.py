nb_floors, width, nb_rounds, exit_floor, exit_pos, nb_total_clones, nb_additional_elevators, nb_elevators = [int(i) for
                                                                                                             i in
                                                                                                             input().split()]
elevator_dict = {}
for i in range(nb_elevators):
    # elevator_floor: floor on which this elevator is found
    # elevator_pos: position of the elevator on its floor
    elevator_floor, elevator_pos = [int(j) for j in input().split()]
    elevator_dict[str(elevator_floor)] = elevator_pos

global_need_to_block = True


def think(f_destination, f_clone_location, f_direction):
    global global_need_to_block
    if global_need_to_block:
        # need to block the leading bot when necessary
        if (f_destination > f_clone_location and f_direction == 'RIGHT') or (
                f_destination < clone_pos and direction == 'LEFT'):
            # exit and bot direction are same, wait:
            return "WAIT"
        else:
            # exit and bot direction are different, block the leading bot:
            global_need_to_block = False
            return "BLOCK"
    else:
        # do not need to block the leading bot when necessary
        # the previous leading bot is already blocked
        return "WAIT"


# game loop
while True:
    inputs = input().split()
    clone_floor = int(inputs[0])  # floor of the leading clone
    clone_pos = int(inputs[1])  # position of the leading clone on its floor
    direction = inputs[2]  # direction of the leading clone: LEFT or RIGHT
    # decide if need to go upstairs
    levels_need_to_go = exit_floor - 0
    # think if the exit and leading bot are on same floor
    if levels_need_to_go == 0:
        # the exit floor is the current floor
        # decide if the exit location is on leading bot same direction
        action = think(exit_pos, clone_pos, direction)
    else:
        # the exit floor not on the current floor
        # move the elevator
        # step 1: find the elevator locates on the current floor
        local_elevator_pos = elevator_dict.get(str(clone_floor))
        if local_elevator_pos is None:
            # after climbing up, exit is on current floor
            action = think(exit_pos, clone_pos, direction)
        else:
            # after climbing up, exit is not on current floor
            # update the current level elevator pos
            local_elevator_pos = elevator_dict.get(str(clone_floor))
            if direction == "RIGHT":
                action = think(local_elevator_pos+1, clone_pos, direction)
            else:
                action = think(local_elevator_pos-1, clone_pos, direction)
            if local_elevator_pos == clone_pos:
                # signal me when the leading bot reached the elevator
                global_need_to_block = True
    print(action)
