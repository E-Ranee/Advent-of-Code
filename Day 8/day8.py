f = open(f"input.txt", "r")
# f = open(f"example_input.txt", "r")
data = f.readlines()
f.close()

tree_grid = []
number_of_rows = len(data)
number_of_cols = len(data[0].strip())
boolean_grid = []
for line in data:
    processed_row = [int(x) for x in list(line.strip())] # remove \n and turn into integers
    tree_grid.append(processed_row)
    boolean_grid.append([int(x) for x in list("0" * number_of_cols)]) # make an identical array of 0s (int)



# for each row, column, backwards row, backwards column, 
# find the first 9, then the first 8 before that, then 7 before that

def visible_trees(list_of_numbers):
    """Takes a list of numbers and returns the index of which ones are visible"""
    # Example: 30733
    max_index = len(list_of_numbers)
    iterate = True
    tree_height = max(list_of_numbers)

    list_of_indices = []

    while iterate == True:
        for i in range(max_index):
            if list_of_numbers[i] == tree_height:
                list_of_indices.append(i)
                max_index = i
                break
        tree_height -= 1
        if tree_height < 0:
            iterate = False

    return list_of_indices # example: [2, 0]

def get_columns(array):
    """Makes the columns go horizontally and the rows go vertically"""
    return list(map(list, zip(*array)))

### Update the identical grid of 0s to show 1s for the visible trees

# Left to right
for row in range(number_of_rows):
    columns_visible = visible_trees(tree_grid[row]) # returns eg [2, 0]
    for col in columns_visible:
        boolean_grid[row][col] = 1 

# Right to left
for rev_row in range(number_of_rows):
    reversed_row = tree_grid[rev_row][::-1]
    columns_visible = visible_trees(reversed_row)
    for col in columns_visible:
        boolean_grid[rev_row][number_of_cols - col - 1] = 1

# Up to down
for col in range(number_of_cols):
    rows_visible = visible_trees(get_columns(tree_grid)[col])
    for row in rows_visible:
        boolean_grid[row][col] = 1

# Down to up
for rev_col in range(number_of_cols):
    reversed_column = get_columns(tree_grid)[rev_col][::-1]
    rows_visible = visible_trees(reversed_column)
    for row in rows_visible:
        boolean_grid[number_of_rows - row - 1][rev_col] = 1

final_result_list = []
for row in boolean_grid: # Concatonate the boolean grid
    final_result_list += row

print(sum(final_result_list))

############################################################################################

################################ PART 2 ####################################################

ideal_row = 0
ideal_col = 0
best_scenic_score = 0

def look_north(row, col):
    """Compares the tree to the trees in the rows above"""
    if row - 1 < 0:
        return 0
    
    current_tree_height = tree_grid[row][col]
    counter = 0
    new_row = row - 1

    while new_row > -1:
        if current_tree_height > tree_grid[new_row][col]:   # If it can see past the trees
            counter += 1
            new_row -= 1
        else:                       # If it hits a tree
            return counter + 1
    return counter                  # if it hits the edge of the map

def look_east(row, col):
    """Compares the tree to the trees in the columns to the right"""
    # col + 1
    if col + 1 > number_of_cols - 1:
        return 0

    current_tree_height = tree_grid[row][col]
    counter = 0
    new_col = col + 1

    while new_col < number_of_cols:
        if current_tree_height > tree_grid[row][new_col]:   # If it can see past the trees
            counter += 1
            new_col += 1
        else:                       # If it hits a tree
            return counter + 1
    return counter                  # If it hits the edge of the map

def look_south(row, col):
    """Compares the current tree to the trees in the rows below"""
    if row + 1 > number_of_rows - 1:
        return 0

    current_tree_height = tree_grid[row][col]
    counter = 0
    new_row = row + 1

    while new_row < number_of_rows:
        if current_tree_height > tree_grid[new_row][col]:   # If it can see past the other trees
            counter += 1
            new_row += 1
        else:
            return counter + 1      # If it hits a tree
    return counter                  # If it hits the edge of the map

def look_west(row, col):
    """Compares the current trees to the trees to its left"""
    if col - 1 < 0:
        return 0
    
    current_tree_height = tree_grid[row][col]
    counter = 0
    new_col = col - 1

    while new_col > -1:
        if current_tree_height > tree_grid[row][new_col]:   # If it can see past the trees
            counter += 1
            new_col -= 1
        else:                       # If it hits a tree
            return counter + 1
    return counter                  # If it hits the edge of th emap

def scenic_score(row, col):
    """Multiplies the scores together"""
    n = look_north(row, col)
    e = look_east(row, col)
    s = look_south(row, col)
    w = look_west(row, col)
    # print(n,e,s,w,"=", n*e*s*w)
    return n * e * s * w

for row in range(number_of_rows):
    for col in range(number_of_cols): # eg [3,0,3,7,3]
        score = scenic_score(row, col)
        if score > best_scenic_score:
            best_scenic_score = score
            ideal_row = row
            ideal_col = col

print(best_scenic_score)