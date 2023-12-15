file = "input.txt"
# file = "test.txt"

f = open(file, "r")
file_data = f.readlines()
f.close()

data = []
for row in file_data:
    data.append([x for x in row.strip()])

def move_rock_up(row_index, col_index):
    # has it reached the top of the box
    if row_index > 0:
        # is there anything above it?
        if data[row_index - 1][col_index] == ".": # if empty space above
            data[row_index][col_index] = "." # replace current coord with space
            data[row_index - 1][col_index] = "O" # move rock to space above
            move_rock_up(row_index - 1, col_index) # see if rock can go up again

def calculate_score():
    highest_multiplier = len(data)
    total_score = 0
    for index, row in enumerate(data):
        number_of_rocks = row.count("O")
        total_score += number_of_rocks * (highest_multiplier - index)
    return total_score 


for row_index, row in enumerate(data):
    for col_index, char in enumerate(row):
        if char == "O":
            move_rock_up(row_index, col_index)

print(calculate_score())