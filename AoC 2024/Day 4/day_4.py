file = "input.txt"
# file = "test.txt"

f = open(file, "r")
file_data = f.readlines()
f.close()

data = []
for row in file_data:
    data.append([x for x in row.strip()]) # array of letters

number_of_rows = len(data)
number_of_cols = len(data[0])

def search_for_xmas(row_index, col_index, row_change, col_change, data=data, 
                    number_of_rows=number_of_rows, number_of_cols=number_of_cols):
    """Returns a count for the number of times -MAS follows the starting character (X) in a given direction: 1 or 0"""
    # is it possible to move 3 away in either direction without going out of bounds?
    # number of rows - 1 because index starts at 0
    if row_index + (row_change * 3) < 0 or row_index + (row_change * 3) > number_of_rows - 1:
        return 0
    elif col_index + (col_change * 3) < 0 or col_index + (col_change * 3) > number_of_cols - 1:
        return 0
    
    # safely within bounds, time to check next letters
    if (data[row_index + row_change][col_index + col_change] == "M" and 
        data[row_index + row_change * 2][col_index + col_change * 2] == "A" and
        data[row_index + row_change * 3][col_index + col_change * 3] == "S"
        ):
        return 1
    else:
        return 0

xmas_found = 0

for row_index in range(number_of_rows):
    for col_index in range(number_of_cols):
        current_letter = data[row_index][col_index]
        
        # counting how many Xs are the start of the word xmas
        # disregard other letters

        if current_letter != "X":
            pass
        else:
            # xmas could occur multiple times for a single starting letter

            # xmas could be horizontal forwards
            xmas_found += search_for_xmas(row_index, col_index, 0, 1, data, number_of_rows, number_of_cols)
            # horizontal backwards
            xmas_found += search_for_xmas(row_index, col_index, 0, -1, data, number_of_rows, number_of_cols)
            # vertical forwards
            xmas_found += search_for_xmas(row_index, col_index, 1, 0, data, number_of_rows, number_of_cols)
            # vertical backwards
            xmas_found += search_for_xmas(row_index, col_index, -1, 0, data, number_of_rows, number_of_cols)
            # diagonal up/right
            xmas_found += search_for_xmas(row_index, col_index, -1, 1, data, number_of_rows, number_of_cols)
            # diagonal up/left
            xmas_found += search_for_xmas(row_index, col_index, -1, -1, data, number_of_rows, number_of_cols)
            # diagonal down/right
            xmas_found += search_for_xmas(row_index, col_index, 1, 1, data, number_of_rows, number_of_cols)
            # diagonal down/left
            xmas_found += search_for_xmas(row_index, col_index, 1, -1, data, number_of_rows, number_of_cols)

####################################### PART 2 ################################################

def search_for_mas(row_index, col_index, row_change, col_change, data=data, 
                    number_of_rows=number_of_rows, number_of_cols=number_of_cols):
    """Returns the number of times M and S occur around the starting character (A) in a given direction
    row change/col change refer to the direction of the first character of the word, with the last character in the opposite direction"""
    # is it possible to move 1 away in either direction without going out of bounds?
    # A is the centre of the word so look 1 away in all directions
    # number of rows - 1 because index starts at 0
    if row_index + 1 < 0 or row_index + 1 > number_of_rows - 1:
        return 0
    elif row_index - 1 < 0 or row_index - 1 > number_of_rows - 1:
        return 0
    elif col_index + 1 < 0 or col_index + 1 > number_of_cols - 1:
        return 0
    elif col_index - 1 < 0 or col_index - 1 > number_of_cols - 1:
        return 0
    
    # safely within bounds, time to check next letters
    if (data[row_index + row_change][col_index + col_change] == "M" and 
        data[row_index - row_change][col_index - col_change] == "S" # inverse direction
        ):
        return 1
    else:
        return 0
    
mas_found = 0
    
for row_index in range(number_of_rows):
    for col_index in range(number_of_cols):
        current_letter = data[row_index][col_index]

        if current_letter != "A": # A at the centre of MAS
            pass
        else:
            mas_count = 0

            # look in all diagonals for MAS

            # diagonal up/right
            mas_count += search_for_mas(row_index, col_index, -1, 1, data, number_of_rows, number_of_cols)
            # diagonal up/left
            mas_count += search_for_mas(row_index, col_index, -1, -1, data, number_of_rows, number_of_cols)
            # diagonal down/right
            mas_count += search_for_mas(row_index, col_index, 1, 1, data, number_of_rows, number_of_cols)
            # diagonal down/left
            mas_count += search_for_mas(row_index, col_index, 1, -1, data, number_of_rows, number_of_cols)

            # Only counts if there's two MAS, one for each diagonal

            if mas_count == 2:
                mas_found += 1

print(xmas_found)
print(mas_found)
