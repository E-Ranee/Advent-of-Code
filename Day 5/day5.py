import re

f = open(f"input.txt", "r")
data = f.readlines()
f.close()

# The leftmost letter is on "top" of the stack
crate_stacks = [
    ["T", "R", "G", "W", "Q", "M", "F", "P"],
    ["R", "F", "H"],
    ["D", "S", "H", "G", "V", "R", "Z", "P"],
    ["G", "W", "F", "B", "P", "H", "Q"],
    ["H", "J", "M", "S", "P"],
    ["L", "P", "R", "S", "H", "T", "Z", "M"],
    ["L", "M", "N", "H", "T", "P"],
    ["R", "Q", "D", "F"],
    ["H", "P", "L", "N", "C", "S", "D"]
]

def parse_instruction(movement_instruction):
    regex_pattern = "([0-9]*)"
    results = re.findall(regex_pattern, movement_instruction)
    relevant_numbers = [int(x) for x in results if x != ""]

    return relevant_numbers

def carry_out_instruction(relevant_numbers):
    number_to_move = relevant_numbers[0]
    starting_stack = relevant_numbers[1]-1
    ending_stack = relevant_numbers[2]-1

    for i in range(number_to_move):
        crate = crate_stacks[starting_stack].pop(0) # Delete from starting stack
        crate_stacks[ending_stack].insert(0, crate) # Add to start of new stack

def carry_out_instruction_part2(relevant_numbers):
    number_to_move = relevant_numbers[0]
    starting_stack = relevant_numbers[1]-1
    ending_stack = relevant_numbers[2]-1

    temp_list = []

    for i in range(number_to_move):
        crate = crate_stacks[starting_stack].pop(0)
        temp_list.insert(0, crate) # Reverse order of crates being moved

    for item in temp_list:
        crate_stacks[ending_stack].insert(0, item)

for item in data:
    carry_out_instruction_part2(parse_instruction(item.strip()))

for stack in crate_stacks:
    print(stack[0], end="")