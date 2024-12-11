from typing import List, Dict
from time import perf_counter

file = "input.txt"
# file = "test.txt"

f = open(file, "r")
file_data = f.readlines()
f.close()

data: List[int] = [int(x) for x in file_data[0].strip().split()] # remove spaces, turn to into

def blink(value):
    if value == 0:
        return [1]
    
    str_version = str(value)
    if len(str_version) % 2 == 0:
        # split into two stones
        midpoint = int(len(str_version)/2)
        left_stone = str_version[:midpoint]
        right_stone = str_version[midpoint:]
        return [int(left_stone), int(right_stone)]
    
    return [value * 2024]

def blink_across_line(list_of_values):
    new_list = []
    for item in list_of_values:
        new_list += blink(item)
    return new_list

temp_list = data
for _ in range(25):
    temp_list = blink_across_line(temp_list)

print(len(temp_list))
