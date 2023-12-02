import re

file = "input.txt"
# file = "test.txt"

f = open(file, "r")
data = f.readlines()
f.close()

rows = []
for row in data:
    rows.append(row.strip())

# Step 1: extract the information

# example data
# Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
# [Game x:] [\d blue|red|green] split on ;

def day1(input_data, max_reds, max_greens, max_blues):

    game_number_pattern = "(Game \d+)" # game number is game_number_pattern[5:], works for multidigit numbers of any length
    colours_pattern = "((\d+) (red|green|blue))"

    list_of_valid_game_IDs = []
    list_of_powers = []

    for game in input_data:
        game_number = int(re.findall(game_number_pattern, game)[0][5:])
        subsets_string = game.split(";") # This is a list of strings for each subgame

        max_colours_present = {
            "red" : 0,
            "blue" : 0,
            "green" : 0
        }

        for subset in subsets_string:
            colours_present = re.findall(colours_pattern, subset) # produces a format like [('3 blue', '3', 'blue'), ('4 red', '4', 'red')]
            for option in colours_present:
                quantity = int(option[1])
                colour = option[2]

                if quantity > max_colours_present[colour]:
                    max_colours_present[colour] = quantity

        # check if game is valid

        if max_colours_present["red"] <= max_reds and max_colours_present["blue"] <= max_blues and max_colours_present["green"] <= max_greens:
            list_of_valid_game_IDs.append(game_number)

        power = max_colours_present["red"] * max_colours_present["blue"] * max_colours_present["green"]
        list_of_powers.append(power)

    print("Part 1:", sum(list_of_valid_game_IDs))
    print("Part 2:", sum(list_of_powers))
            
    
day1(rows, 12, 13, 14)