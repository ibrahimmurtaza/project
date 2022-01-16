import random

# strings and lists are used to make a coordinate system

# functions and one loop is used to make the game run

#Assets and functions
ui_wall = [
    "......",
    "......",
    "......",  # these are used to replace the small original map parts
    "......"   # this render a larger more readable map
]

ui_ghost = [
    " .-.  ",
    "|0-0| ",
    "|-_-| ",
    "'---' "
]

ui_pacman = [
    " ---- ",
    "/ _--|",
    "\-_--|",
    " '--' "
]

ui_empty = [
    "      ",
    "      ",
    "      ",
    "      "
]

ui_pill = [
    "      ",
    " .-.  ",
    " '-'  ",
    "      "
]

# output display thingy


def ui_print(map):
    for row in map:
        for piece in range(4):
            for column in row:
                if column == 'G':
                    print(ui_ghost[piece], end='')
                if column == 'P':
                    print(ui_pill[piece], end='')
                if column == '@':
                    print(ui_pacman[piece], end='')
                if column == '.':
                    print(ui_empty[piece], end='')
                if column == '-' or column == '|':
                    print(ui_wall[piece], end='')

            print("")

# input


def ui_key():
    return input()

# lose


def ui_msg_lost():
    print("You lost! Please restart the program to continue.")

# win


def find_pacman(map):
    pacman_x = -1
    pacman_y = -1

    for x in range(len(map)):
        for y in range(len(map[x])):
            if map[x][y] == '@':
                pacman_x = x
                pacman_y = y

    return pacman_x, pacman_y


def ui_msg_win():
    print("You won!")

# moving function


def move_pacman(map, next_pacman_x, next_pacman_y):
    pacman_x, pacman_y = find_pacman(map)

    # the place where the pacman was is now empty
    everything_to_the_left = map[pacman_x][0:pacman_y]
    everything_to_the_right = map[pacman_x][pacman_y+1:]
    map[pacman_x] = everything_to_the_left + "." + everything_to_the_right

    # the new place has the pacman
    everything_to_the_left = map[next_pacman_x][0:next_pacman_y]
    everything_to_the_right = map[next_pacman_x][next_pacman_y+1:]
    map[next_pacman_x] = everything_to_the_left + "@" + everything_to_the_right

# this function returns two conds
# the first shows whether the pressed key was a valid key
# the second shows whether the pacman is still alive
# '''''''''''third shows whether the pacman won the game

# checks keys and moves


def play(map, key):
    next_x, next_y = next_position(map, key)

    # if it is a invalid key
    is_an_invalid_key = next_x == -1 and next_y == -1
    if is_an_invalid_key:
        return False, True, False

    # if it is not within borders
    if not within_borders(map, next_x, next_y):
        return False, True, False

    # if it is a wall
    if is_a_wall(map, next_x, next_y):
        return False, True, False

    is_a_ghost = map[next_x][next_y] == 'G'
    if is_a_ghost:
        return True, False, False  # these are important parameters used in the play function

    move_pacman(map, next_x, next_y)

    remaining_pills = total_pills(map)
    if remaining_pills == 0:
        return True, True, True
    else:
        return True, True, False


def is_a_wall(map, next_x, next_y):
    is_a_wall = map[next_x][next_y] == '|' or map[next_x][next_y] == '-'
    return is_a_wall


def is_a_ghost(map, next_x, next_y):
    return map[next_x][next_y] == 'G'


def is_a_pill(map, next_x, next_y):
    return map[next_x][next_y] == 'P'


def is_pacman(map, next_x, next_y):
    return map[next_x][next_y] == '@'


def within_borders(map, next_x, next_y):
    number_of_rows = len(map)
    x_is_valid = 0 <= next_x < number_of_rows

    number_of_columns = len(map[0])
    y_is_valid = 0 <= next_y < number_of_columns

    return x_is_valid and y_is_valid


def total_pills(map):
    total = 0
    for x in range(len(map)):
        for y in range(len(map[x])):
            if map[x][y] == 'P':
                total = total + 1
    return total


def next_position(map, key):
    x, y = find_pacman(map)
    next_x = -1
    next_y = -1

    if key == 'a':
        next_x = x
        next_y = y - 1
    elif key == 'd':
        next_x = x
        next_y = y + 1
    elif key == 'w':
        next_x = x - 1
        next_y = y
    elif key == 's':
        next_x = x + 1
        next_y = y

    return next_x, next_y

# ghost locations:used to get all ghosts loc in the ghost ai


def find_ghosts(map):
    all_ghosts = []
    for x in range(len(map)):
        for y in range(len(map[x])):
            if map[x][y] == 'G':
                all_ghosts.append([x, y])
    return all_ghosts

# ghost ai


def move_ghosts(map):
    all_ghosts = find_ghosts(map)
    for ghost in all_ghosts:
        ghost_x = ghost[0]
        ghost_y = ghost[1]

        possible_directions = [
            [ghost_x, ghost_y + 1],
            [ghost_x, ghost_y - 1],
            [ghost_x - 1, ghost_y],
            [ghost_x + 1, ghost_y]
        ]

        # select a random possible movement and get the x,y of the movement
        random_number = random.randint(0, 3)
        next_ghost_x = possible_directions[random_number][0]
        next_ghost_y = possible_directions[random_number][1]

        # checks before actually moving it!
        if not within_borders(map, next_ghost_x, next_ghost_y):
            continue

        if is_a_wall(map, next_ghost_x, next_ghost_y):
            continue

        if is_a_ghost(map, next_ghost_x, next_ghost_y):
            continue

        if is_a_pill(map, next_ghost_x, next_ghost_y):
            continue

        if is_pacman(map, next_ghost_x, next_ghost_y):
            return True

        # move the ghost to the random position
        everything_to_the_left = map[ghost_x][0:ghost_y]
        everything_to_the_right = map[ghost_x][ghost_y + 1:]
        map[ghost_x] = everything_to_the_left + "." + everything_to_the_right

        # the new place has the pacman
        everything_to_the_left = map[next_ghost_x][0:next_ghost_y]
        everything_to_the_right = map[next_ghost_x][next_ghost_y + 1:]
        map[next_ghost_x] = everything_to_the_left + \
            "G" + everything_to_the_right

    return False


# old map // main map
map = [
    "|--------|",
    "|G..|..G.|",
    "|...PP...|",
    "|G...@.|.|",
    "|........|",
    "|--------|"
]

game_finished = False
# main loops of game
while not game_finished:
    ui_print(map)
    key = ui_key()
    valid_key, pacman_alive, won = play(map, key)

    pacman_was_hit = move_ghosts(map)

    if (not pacman_alive) or (pacman_was_hit):
        ui_msg_lost()
        game_finished = True
    elif won:
        ui_msg_win()
        game_finished = True
