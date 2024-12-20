from typing import List, Tuple
from time import perf_counter
import numpy as np
from scipy.ndimage import label
import string

# after import lines
timer_script_start=perf_counter()
timer_parse_start=perf_counter()

file = "input.txt"
# file = "test.txt"
# file = "test_2.txt"

f = open(file, "r")
file_data = f.readlines()
f.close()

data = []
for row in file_data:
    data.append([x for x in row.strip()])
numpy_array = np.array(data)

def value_at_coords_if_within_bounds(coords: List[int]):
    # data type is [row_index, col_index]
    it_exists = coords[0] >= 0 and coords[0] < len(data) and coords[1] >= 0 and coords[1] < len(data[0])
    return numpy_array[coords[0]][coords[1]] if it_exists else "ZZZ"

def get_adjacent_coords(coords: List[int]):
    north = [coords[0] - 1, coords[1]] # one row up
    east = [coords[0], coords[1] + 1] # one col to the right
    south = [coords[0] + 1, coords[1]] # one row down
    west = [coords[0], coords[1] - 1] # one col to the left
    return [north, east, south, west]

class Direction:
    def __init__(self, coords: List[int], region_label: str):
        self.coords = coords
        self.value = value_at_coords_if_within_bounds(coords)
        self.matches_region_label = self.value == region_label
class Region:
    def __init__(self, letter_label: str, coordinates: List[int]):
        self.letter_label = letter_label # initialises the letter label field with eg "R"
        self.coordinates = coordinates
        self.area = len(coordinates)
        self.list_of_internal_corners: List[Tuple[Tuple[int]]] = [] # This will be the list of pairs of coordinates to form a kind of vector pointing at the corner

    def get_number_of_neighbours(self, coord: List[int]):
        coords_to_check = get_adjacent_coords(coord) # get the coordinates of the squares in the four directions
        neighbours = 0
        for direction in coords_to_check:
            if value_at_coords_if_within_bounds(direction) == self.letter_label: # check if it's both within bounds and matches
                neighbours += 1
        return 4 - neighbours # you have a square with 4 walls, remove walls where the square touches another square

    def get_perimeter(self):
        total_perimeter = 0
        for square in self.coordinates:
            total_perimeter += self.get_number_of_neighbours(square)
        return total_perimeter

    def get_internal_corner(self, current_tile: Direction, neighbours: Direction, diagonal_directions: Direction):
        """This works by forming a 2x2 grid of the starting square, a neighbouring square, a diagonal square and fourth square
        If the first three form a right angle within the region and the fourth square is not part of the region, an internal corner is present
        One square could have two internal corners so a tuple is added to the list (fourth square coords, neighbour square coords)
        This is the starting point and direction of corner"""
        for neighbour in neighbours:
            for diagonal in diagonal_directions:
                # check if the diagonal is actually part of the region
                if diagonal.value == self.letter_label:
                    # Check if starting tile, neighbour, diagonal form a right angle:
                    start_x, start_y = current_tile.coords
                    diagonal_x, diagonal_y = diagonal.coords

                    # square to check is in one of the coordinates that isn't the starting square or diagonal square
                    direction_1 = Direction([start_x, diagonal_y], self.letter_label)
                    direction_2 = Direction([diagonal_x, start_y], self.letter_label)

                    internal_corner_square = None

                    # square to check is whichever coordinate ISN'T the neighbour square
                    if neighbour.coords == direction_1.coords:
                        internal_corner_square = direction_2
                    elif neighbour.coords == direction_2.coords:
                        internal_corner_square = direction_1
                    else:
                        continue

                    if internal_corner_square.value == self.letter_label:
                        # square is part of the region so no internal corner present
                        continue
                    else:
                        internal_corner_direction = ((internal_corner_square.coords[0], internal_corner_square.coords[1]), (neighbour.coords[0], neighbour.coords[1]))
                        # The same corner can be found multiple times (switching the starting square and diagonal) so only add it if it's new
                        if internal_corner_direction not in self.list_of_internal_corners:
                            self.list_of_internal_corners.append(internal_corner_direction)
                        else:
                            continue


    def get_number_of_corners(self, coord: List[int]):
        cardinal_directions = get_adjacent_coords(coord) # get the coordinates of the squares in the four directions

        north = Direction(cardinal_directions[0], self.letter_label)
        east = Direction(cardinal_directions[1], self.letter_label)
        south = Direction(cardinal_directions[2], self.letter_label)
        west = Direction(cardinal_directions[3], self.letter_label)

        neighbours = [x for x in [north, east, south, west] if x.matches_region_label]

        if len(neighbours) == 0:
            # no neighbours
            # it's an orphaned piece
            return 4
        
        
        current_tile = Direction(coord, self.letter_label)
        north_east = Direction([coord[0] - 1, coord[1] + 1], self.letter_label)
        south_east = Direction([coord[0] + 1, coord[1] + 1], self.letter_label)
        south_west = Direction([coord[0] + 1, coord[1] - 1], self.letter_label) 
        north_west = Direction([coord[0] - 1, coord[1] + 1], self.letter_label)
        diagonal_directions = [x for x in [north_east, south_east, south_west, north_west] if x != "ZZZ"]
   
        self.get_internal_corner(current_tile, neighbours, diagonal_directions)

        if len(neighbours) == 1:
            # only one neightbour
            # it's a sticky out piece
            # changes direction two times so has two external corners
            return 2

        if len(neighbours) == 2:
            # has two parts of the perimeter
            if north in neighbours and south in neighbours or east in neighbours and west in neighbours: # opposite sides mean no external corners
                return 0
            else:
                return 1

        if len(neighbours) == 3:
            # three corners means it's a side piece = no extenal corners
            # not a corner unless there's an internal region
            return 0
    
        else: # 4 neighbours = internal piece with no external or internal corners
            return 0

    def get_number_of_sides(self):
        external_corner_total = 0
        for square in self.coordinates:
            external_corner_total += self.get_number_of_corners(square)
        internal_corner_total = len(self.list_of_internal_corners)
        return external_corner_total + internal_corner_total

alphabet = string.ascii_uppercase

list_of_regions: List[Region] = []
for letter in alphabet:
    if letter in numpy_array:
        new_array = numpy_array == letter # Turns the array into 1s where the letter is present and 0 where it's another letter
        labelled_array, max_number_of_regions = label(new_array) # Returns an array where the 1s are replaced with the region number

        for region_number in range(1, max_number_of_regions + 1, 1): # for every numbered region
            coords = np.argwhere(labelled_array == region_number) # get the coordinates of every plot in region
            new_region = Region(letter, coords) # create a region object and add it to the list
            list_of_regions.append(new_region)

# after processing input and running past functions
timer_parse_end=timer_part1_start=perf_counter()

# we now have a list of every region
fence_cost = 0
for region in list_of_regions:
    fence_cost += region.area * region.get_perimeter()
print(f"Part 1: {fence_cost}")

# solve part 1
timer_part1_end=timer_part2_start=perf_counter()

fence_cost = 0
for region in list_of_regions:
    # print(f"{region.letter_label} with price {region.area} x {region.get_number_of_sides()} = {region.area * region.get_number_of_sides()}")
    fence_cost += region.area * region.get_number_of_sides()
print(f"Part 2: {fence_cost}")

# solve part 2
timer_part2_end=timer_script_end=perf_counter()

print(f"""
Execution times (sec)
Parse: {timer_parse_end-timer_parse_start:3.3f}
Part1: {timer_part1_end-timer_part1_start:3.3f}
Part2: {timer_part2_end-timer_part2_start:3.3f}
Total: {timer_script_end-timer_script_start:3.3f}""")