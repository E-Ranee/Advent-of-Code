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

total_score = 0 # used for part 1
dict_of_games = {} # used for part 2

for i in range(len(rows)): # autofilling a dictionary that has one copy of each scratch card (part 2)
    dict_of_games[i + 1] = 1

for game in rows:
    game_number_string, all_numbers_string = game.split(":") # separates the game number so it doesn't sneak into the winning numbers
    winning_numbers_string, my_numbers_string = all_numbers_string.split("|") # splits winning numbers and my numbers into two groups

    winning_nums = re.findall("\d+", winning_numbers_string) # each number is still a string but that should be okay
    my_nums = re.findall("\d+", my_numbers_string)
    game_number = int(re.findall("\d+", game_number_string)[0]) # does need to be an int so it can be used in calculations in part 2

    game_score = 0
    matches = 0 # used for generating duplicate scratchcards in part 2
    for num in my_nums: # find and score the winning numbers for part 1
        if num in winning_nums:
            matches += 1
            if game_score == 0:
                game_score = 1
            else:
                game_score *= 2

    total_score += game_score # solution to part 1

    # working on part 2
    for i in range(matches):
        # make a copy of the next i cards, according to how many copies of the current card you have
        dict_of_games[game_number + i + 1] += 1 * dict_of_games[game_number] # I'm not sure why this doesn't break when we get to the last few scratchcards

number_of_scratchcards = 0 # total the number of iterations of all scratch cards
for key, value in dict_of_games.items():
    number_of_scratchcards += value


print(total_score)
print(number_of_scratchcards)