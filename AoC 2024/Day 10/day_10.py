from typing import List
from time import perf_counter

# after import lines
timer_script_start=perf_counter()
timer_parse_start=perf_counter()

file = "input.txt"
# file = "test.txt"

f = open(file, "r")
file_data = f.readlines()
f.close()

data: List[int] = []
for row in file_data:
    data.append([int(x) for x in row.strip()]) # turn input string into list of ints

def value_at_coords_if_within_bounds(coords):
    # data type is [row_index, col_index]
    it_exists = coords[0] >= 0 and coords[0] < len(data) and coords[1] >= 0 and coords[1] < len(data[0])
    return data[coords[0]][coords[1]] if it_exists else -1

def get_adjacent_coords(coords):
    # data type is [row_index, col_index]
    north = [coords[0] - 1, coords[1]] # one row up
    east = [coords[0], coords[1] + 1] # one col to the right
    south = [coords[0] + 1, coords[1]] # one row down
    west = [coords[0], coords[1] - 1] # one col to the left
    return [north, east, south, west]

class Trailhead:
    def __init__(self, coords):
        self.coords: List[int] = coords # initialise where the trailhead is on the map
        self.peaks: List[List[int]] = [] # list of coords of 9s that can be reached with 1 step intervals
        self.unique_trails: List[List[int]] = []
        
    def __search_for_peaks(self, current_coords, current_height=0):
        """Recursive function"""
        # exit condition
        if current_height == 9 and current_coords not in self.peaks:
            self.peaks.append(current_coords)
        if current_height == 9:
            self.unique_trails.append(current_coords)
            return
        
        # Look for current_height + 1 in the 4 directions (if within bounds)
        for new_direction in get_adjacent_coords(current_coords):
            # is the value one higher than current value?
            new_value = value_at_coords_if_within_bounds(new_direction)
            if new_value == current_height + 1:
                # keep going in this direction and call function again on new coords
                self.__search_for_peaks(new_direction, new_value)
            else:
                pass
            
    def get_peaks(self):
        self.__search_for_peaks(self.coords)
        return self.peaks

# after processing input and running past functions
timer_parse_end=timer_part1_start=perf_counter()
# solve part 1
timer_part1_end=timer_part2_start=perf_counter()

list_of_trailheads: List[Trailhead] = []
for row_index in range(len(data)):
    for col_index in range(len(data[0])):
        if data[row_index][col_index] == 0:
            list_of_trailheads.append(Trailhead([row_index, col_index]))

part_1_total = 0
for trailhead in list_of_trailheads:
    part_1_total += len(trailhead.get_peaks())

print(f"Part 1: {part_1_total}")

# solve part 2
part_2_total = 0
for trailhead in list_of_trailheads:
    part_2_total += len(trailhead.unique_trails)
timer_part2_end=timer_script_end=perf_counter()
print(f"Part 2: {part_2_total}")

print(f"""Execution times (sec)
Parse: {timer_parse_end-timer_parse_start:3.3f}
Part1: {timer_part1_end-timer_part1_start:3.3f}
Part2: {timer_part2_end-timer_part2_start:3.3f}
Total: {timer_script_end-timer_script_start:3.3f}""")