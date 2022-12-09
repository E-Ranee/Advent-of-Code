from math import sqrt

f = open(f"input.txt", "r")
# f = open(f"example_input.txt", "r")
data = f.readlines()
f.close()

# Must always be touching! Diagnoally, adjacently or overlapped
# If H is ever two steps directly up/down/left/right of the tail, the tail moves one step in that direction (to where H was)
# If they are touching diagonally and H moves more in that direction, T moves diagonally to where H was
# HT start in the same position (overlapping)

rope_dict = {
    "H": (0,0),
    "1": (0,0),
    "2": (0,0),
    "3": (0,0),
    "4": (0,0),
    "5": (0,0),
    "6": (0,0),
    "7": (0,0),
    "8": (0,0),
    "9": (0,0)
}

list_of_visited_locations_part_1 = [(0,0)]
list_of_visited_locations_part_2 = [(0,0)]

def move_rope(instruction):
    # instruction is a string of format "R 4"
    direction, quantity = instruction.split()

    for i in range(int(quantity)):
        apply_direction(direction, "H", "1")
        for j in range(8):
            follow_after(str(j+1), str(j+2))

def apply_direction(direction, head, tail):
    head_coord = rope_dict[head]
    tail_coord = rope_dict[tail]

    # direction is a string which is U/D/L/R
    direction_dict = {
        "R": (1,0),
        "L": (-1,0),
        "U": (0,1),
        "D": (0,-1)
    }

    coord_change = direction_dict[direction]
    new_h_coordinates = tuple(sum(x) for x in zip(head_coord, coord_change))
    distance_between_h_and_t = sqrt(abs(new_h_coordinates[0] - tail_coord[0])**2 + abs(new_h_coordinates[1]-tail_coord[1])**2)

    # If H is ever two steps directly up/down/left/right of the tail, the tail moves one step in that direction (to where H was)
    if distance_between_h_and_t == 2:
        tail_coord = tuple(sum(x) for x in zip(tail_coord, coord_change))
    # If they are touching diagonally and H moves more in that direction, T moves diagonally to where H was
    elif distance_between_h_and_t > 2:
        tail_coord = head_coord
    rope_dict[head] = new_h_coordinates
    rope_dict[tail] = tail_coord

    list_of_visited_locations_part_1.append(tail_coord)

def follow_after(head, tail):
    head_coord = rope_dict[head]
    tail_coord = rope_dict[tail]
    
    distance_between_h_and_t = sqrt(abs(head_coord[0] - tail_coord[0])**2 + abs(head_coord[1]-tail_coord[1])**2)
    midpoint = ((head_coord[0]+tail_coord[0])/2, (head_coord[1]+tail_coord[1])/2)

    # If H is ever two steps directly up/down/left/right of the tail, the tail moves one step in that direction (to where H was)
    if distance_between_h_and_t == 2:
        tail_coord = midpoint
    # If they are touching diagonally and H moves more in that direction, T moves diagonally to where H was
    elif distance_between_h_and_t == sqrt(5):
        # one coordinate has a difference of +-2, the other has a difference of +-1. Make the 2 --> 1 and the 1 --> 0
        difference = ((head_coord[0] - tail_coord [0]), head_coord[1] - tail_coord[1])
        if abs(difference[0]) == 2:
            tail_coord = (tail_coord[0] + int(difference[0]/2), head_coord[1])
        else:
            tail_coord = (head_coord[0], tail_coord[1] + int(difference[1]/2))
    # If H and T are diagonally separated by one space, move to the middle space
    elif distance_between_h_and_t == 2*sqrt(2):
        tail_coord = midpoint


    rope_dict[tail] = tail_coord

    if tail == "9":
        list_of_visited_locations_part_2.append(tail_coord)

for movement in data:
    move_rope(movement.strip())

print(len(set(list_of_visited_locations_part_1)))
print(len(set(list_of_visited_locations_part_2)))