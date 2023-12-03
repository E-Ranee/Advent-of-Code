file = "input.txt"
# file = "test.txt"

f = open(file, "r")
data = f.readlines()
f.close()

rows = []
for row in data:
    rows.append(row.strip())
        
parts_found = [] 
current_part = []
current_part_coordinates = []
gear_locations = {}

for row, string in enumerate(rows): 
    """fills the gear locations dictionary with the coordinates of where all the gears are
    so that it can be checked against for part 2 while solving part 1"""
    for col, character in enumerate(string):
        if character == "*":
            gear_locations[(row, col)] = []

def is_symbol(character):
    """This finds just the symbols without hardcoding a list and risking missing one"""
    return character.isnumeric() == False and character != "."

def look_around_for_symbols(data, coords, part_name, gear_locations):
    """Takes the coordinates that the number spans and searches one square in all directions for symbols. Returns true or false
    If an asterisk is found, this updates the dictionary which logs which numbers are next to 'gears'"""


    # Needed to avoid searching out of bounds of the data
    max_rows = len(data) - 1
    max_cols = len(data[0]) - 1

    # coords in the format [(1,1), (1,2), (1,3)]
    # will always have same row number
    # we'll be searching a rectangle from (row - 1, min(col) - 1) to (row + 1, max(col) + 1)
    unzipped_list_of_coords = list(zip(*coords)) # prouduces [(1,1,1), (1,2,3)] # aka [(rows), (cols)]
    part_row = unzipped_list_of_coords[0][0]

    for r in range(part_row - 1, part_row + 2): # end point not included in range(start, end)
        for c in range(min(unzipped_list_of_coords[1]) - 1, max(unzipped_list_of_coords[1]) + 2): # one to the left and right of the part
            if r >= 0 and r <= max_rows and c >= 0 and c <= max_cols: # make sure it's within bounds
                if data[r][c] == "*": # part 2, if next to a gear add that to the dictionary so it can be searched later
                    gear_locations[(r,c)] += [part_name]

                if is_symbol(data[r][c]):
                    return True
    
    return False

for row, string in enumerate(rows):
    for col, character in enumerate(string):
        if character.isnumeric(): # builds the part number and logs the coordinates it spans across
            current_part.append(character)
            current_part_coordinates.append((row,col))
        elif len(current_part) > 0:
            # reached the end of a number!
            # check around for symbols
            if look_around_for_symbols(rows, current_part_coordinates, int("".join(current_part)), gear_locations): 
                # part 2 hastily attached here to add the part name and the dict of gear locations so that if the symbol found was an *
                # then the name and gear can be linked together here
                # if there is a symbol, add it to the parts found list
                parts_found.append(int("".join(current_part)))
            # reset the current part + coords ready to search for the next one
            current_part = []
            current_part_coordinates = []

# we have a dictionary of gears and adjacent numbers
# Need to find the keys with exactly 2 items
# and multiply them together

gear_ratios = []

for item in gear_locations.items(): # produces a format of (gear_coord, [part 1, part 2])
    if len(item[1]) == 2: # there are exactly two adjacent numbers
        gear_ratios.append(item[1][0] * item[1][1]) # multiply them and add it to the list

        
print("Part 1:", sum(parts_found))
print("Part 2:", sum(gear_ratios))