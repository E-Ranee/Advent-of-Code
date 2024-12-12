from typing import List, Dict
from time import perf_counter
import numpy as np
from scipy.ndimage import label
import string

file = "input.txt"
file = "test.txt"
file = "test_2.txt"

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

class Region:
    def __init__(self, letter_label: str, coordinates: List[int]):
        self.letter_label = letter_label # initialises the letter label field with eg "R"
        self.coordinates = coordinates
        self.area = len(coordinates)

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

    def get_number_of_corners(self, coord: List[int]):
        north, east, south, west = get_adjacent_coords(coord) # get the coordinates of the squares in the four directions

        n = value_at_coords_if_within_bounds(north) == self.letter_label # true if same
        e = value_at_coords_if_within_bounds(east) == self.letter_label
        s = value_at_coords_if_within_bounds(south) == self.letter_label
        w = value_at_coords_if_within_bounds(west) == self.letter_label

        if sum([n, e, s, w]) == 0:
            # no neighbours
            # it's an orphaned piece
            return 4

        if sum([n, e, s, w]) == 1:
            # only one neightbour
            # it's a sticky out piece
            # changes direction two times
            return 2

        if sum([n, e, s, w]) == 2:
            # has two parts of the perimeter
            if n and s or e and w:
                # opposite sides means it's not a corner
                # unless there's an internal region
                return 0
            else:
                return 1

        if sum([n, e, s, w]) == 4 or sum([n, e, s, w]) == 3:
            # three or four neighbours means it's an internal piece or a side piece
            # not a corner unless there's an internal region
            return 0

    def get_number_of_sides(self):
        total_number_of_sides = 0
        for square in self.coordinates:
            total_number_of_sides += self.get_number_of_corners(square)

        # total number of sides corresponds to all the interal corners of the shape, whose angle would be 90 degrees
        # the total internal angle of the shape would be 360 degrees
        # the external corners would be equal to the total angle inside the shape - 360 divided by 90 degrees
        # add the number of internal corners to the number of external corners 
        return int(((total_number_of_sides * 90 - 360) / 90) + total_number_of_sides)

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
    print(f"{region.letter_label} with price {region.area} x {region.get_number_of_sides()} = {region.area * region.get_number_of_sides()}")
    fence_cost += region.area * region.get_number_of_sides()
print(f"Part 2: {fence_cost}")