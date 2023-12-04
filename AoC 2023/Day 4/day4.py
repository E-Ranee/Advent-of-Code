import re

file = "input.txt"
# file = "test.txt"

f = open(file, "r")
data = f.readlines()
f.close()

rows = []
for row in data:
    rows.append(row.strip())

# data in format list of "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"
# data in format "Card \d: winning numbers | my numbers"

# make list of winning numbers
# make list of my numbers
# for num in my numbers, see if in list
# score the game
# add it to the total

total_score = 0

for game in rows:
    all_numbers_string = game.split(":")[1] # deletes the game number so it doesn't sneak into the winning numbers
    winning_numbers_string, my_numbers_string = all_numbers_string.split("|")

    winning_nums = re.findall("\d+", winning_numbers_string) # each number is still a string but that should be okay
    my_nums = re.findall("\d+", my_numbers_string)

    game_score = 0
    for num in my_nums:
        if num in winning_nums:
            if game_score == 0:
                game_score = 1
            else:
                game_score *= 2

    total_score += game_score

print(total_score)
