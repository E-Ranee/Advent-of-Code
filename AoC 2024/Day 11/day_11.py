from typing import List, Dict
from time import perf_counter

# after import lines
timer_script_start=perf_counter()
timer_parse_start=perf_counter()

file = "input.txt"
# file = "test.txt"

f = open(file, "r")
file_data = f.readlines()
f.close()

data: List[int] = [int(x) for x in file_data[0].strip().split()] # remove spaces, turn to into list of ints

# after processing input and running past functions
timer_parse_end=timer_part2_start=perf_counter()

############################ PARTS 1 AND 2 ##########################

# solution based on this comment https://www.reddit.com/r/adventofcode/comments/1hbmu6q/comment/m1ibyi5/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
"""
Each stone spawns 1 or 2 stones. 
But if you have N stones of value X, this will also spawn N new stones or 2*N (depending on digits). 
As the positioning of the stones does not matter, you know that if you have 202 stones of value 1000, 
you will get 202 new 10s and 202 new 0s. 
So basically you just remember how many stones of which value you have, 
and in the next epoch, what they will turn into
"""

known_transformations = {}

def blink(value):
    str_version = str(value)

    if value in known_transformations:
        return known_transformations[value]

    if value == 0:
        new_value = [1]
    elif len(str_version) % 2 == 0:
        # split into two stones
        midpoint = int(len(str_version)/2)
        left_stone = str_version[:midpoint]
        right_stone = str_version[midpoint:]
        new_value = [int(left_stone), int(right_stone)]
    else:
        new_value = [value * 2024]

    if value not in known_transformations:
        known_transformations[value] = new_value
    
    return new_value

dict_of_values = {} # initialise dictionary from the input
for item in data:
    if item in dict_of_values:
        dict_of_values[item] += 1
    else:
        dict_of_values[item] = 1

part_1_dict_of_values = {}

for i in range(75):
    temp_dict = {}
    # work through current dictionary and then put the results in a blank dictionary so you don't change this one in place while iterating
    for number_value, frequency in dict_of_values.items():
        result = blink(number_value)
        for new_value in result:
            if new_value in temp_dict:
                temp_dict[new_value] += frequency
            else:
                temp_dict[new_value] = frequency
    
    dict_of_values = temp_dict
    if i == 24: # break off early for part 1
        part_1_dict_of_values = temp_dict

# We know how many stones of each value there are so just add up all the frequencies
part_1_total = 0
for _, frequency in part_1_dict_of_values.items():
    part_1_total += frequency
print(part_1_total)

part_2_total = 0
for _, frequency in dict_of_values.items():
    part_2_total += frequency
print(part_2_total)

timer_part2_end=timer_script_end=perf_counter()

print(f"""Execution times (sec)
Parse:         {timer_parse_end-timer_parse_start:3.3f}
Parts 1 and 2: {timer_part2_end-timer_part2_start:3.3f}
Total:         {timer_script_end-timer_script_start:3.3f}""")
