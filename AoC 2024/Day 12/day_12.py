from typing import List, Dict
from time import perf_counter
import numpy as np
from scipy.ndimage import label
import string

file = "input.txt"
file = "test.txt"
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
        self.list_of_internal_corners = []

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
        for neighbour in neighbours:
            for diagonal in diagonal_directions:
                if diagonal.value == self.letter_label:
                    # if starting tile, neighbour, diagonal form a right angle:
                    start_x, start_y = current_tile.coords
                    diagonal_x, diagonal_y = diagonal.coords

                    direction_1 = Direction([start_x, diagonal_y], self.letter_label)
                    direction_2 = Direction([diagonal_x, start_y], self.letter_label)

                    internal_corner_square = None

                    if neighbour.coords == direction_1.coords:
                        internal_corner_square = direction_2
                    elif neighbour.coords == direction_2.coords:
                        internal_corner_square = direction_1
                    else:
                        break
                    print(f"starting coords = {current_tile.coords} value = {current_tile.value}")
                    print(f"neightbour coords = {neighbour.coords} value = {neighbour.value}")
                    print(f"diagonal coords = {diagonal.coords} value = {diagonal.value}")
                    print(f"internal square coords = {internal_corner_square.coords} value = {internal_corner_square.value}")

                    if internal_corner_square.value == self.letter_label:
                        print("Rejected due to being part of region")
                        print()
                        return
                    else:
                        internal_corner_direction = ((internal_corner_square.coords[0], internal_corner_square.coords[1]), (neighbour.coords[0], neighbour.coords[1]))
                        if internal_corner_direction not in self.list_of_internal_corners:
                            self.list_of_internal_corners.append(internal_corner_direction)
                            print("Added to the list")
                        else:
                            print("Rejected due to being a duplicated")

                    print()


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

        for neighbour in neighbours:
            print(neighbour.coords)    
        self.get_internal_corner(current_tile, neighbours, diagonal_directions)

        if len(neighbours) == 1:
            # only one neightbour
            # it's a sticky out piece
            # changes direction two times so has two external corners
            print(f"Two external corners found at {current_tile.coords}")
            print()
            return 2

        if len(neighbours) == 2:
            # has two parts of the perimeter
            if north in neighbours and south in neighbours or east in neighbours and west in neighbours: # opposite sides mean no external corners
                print(f"Neighbours are {neighbours[0].coords} and {neighbours[1].coords}")
                print(f"Side found at {current_tile.coords}")
                print()
                return 0
            else:
                print(f"One external corner found at {current_tile.coords}")
                print()
                return 1

        if len(neighbours) == 3:
            # three corners means it's a side piece = no extenal corners
            # not a corner unless there's an internal region
            return 0
    
        else: # 4 neighbours = internal piece with no external or internal corners
            return 0

    def get_number_of_sides(self):
        total_number_of_sides = 0
        for square in self.coordinates:
            total_number_of_sides += self.get_number_of_corners(square)
            
        print(f"total external sides = {total_number_of_sides}, total internal sides = {len(self.list_of_internal_corners)}")
        return total_number_of_sides + len(self.list_of_internal_corners)

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

# we now have a list of every region
fence_cost = 0
for region in list_of_regions:
    fence_cost += region.area * region.get_perimeter()
print(f"Part 1: {fence_cost}")

fence_cost = 0
for region in list_of_regions:
    if region.letter_label == "E":
        # print(f"{region.letter_label} with price {region.area} x {region.get_number_of_sides()} = {region.area * region.get_number_of_sides()}")
        fence_cost += region.area * region.get_number_of_sides()
print(f"Part 2: {fence_cost}")