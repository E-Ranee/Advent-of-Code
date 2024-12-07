import re
from itertools import product
from time import perf_counter

timer_script_start=perf_counter()
timer_parse_start=perf_counter()

file = "input.txt"
# file = "test.txt"

f = open(file, "r")
file_data = f.readlines()
f.close()

timer_parse_end=timer_part1_start=perf_counter()

pattern = "\d+"

data = []
for row in file_data: # data in the form "190: 10 19"
    data.append([int(x) for x in re.findall(pattern, row.strip())]) # makes a list of integers from the row, where the first is the target value

def will_it_calibrate(target_value, list_of_ints, part2=False):
    number_of_operators = 3 if part2 else 2
    operators = list(product(range(number_of_operators), repeat = len(list_of_ints) - 1))
    # product makes a list of tuples showing all the possible permuations with replacement of the operators (eg + +, + x, x +, x x)
    # makes one operation per gap between numbers
    # 0 is add, 1 is multiply, 2 is concatonate
    for order_of_operations in operators: # eg (1,1,1)
        total = list_of_ints[0]
        for i in range(len(list_of_ints)-1): # iterate through numbers in list applying the operators
            if order_of_operations[i] == 0:
                total = total + list_of_ints[i+1]
            elif order_of_operations[i] == 1:
                total = total * list_of_ints[i+1]
            else:
                total = int( str(total) + str(list_of_ints[i+1]) )

            if total > target_value:
                break

        if total == target_value:
            return target_value
        
    return 0 # no variation worked

total_calibration_result = 0
for line in data:
    total_calibration_result += will_it_calibrate(line[0], line[1:])
timer_part1_end=timer_part2_start=perf_counter()
print("Part 1:", total_calibration_result)

part_2_calibration_result = 0
for line in data:
    part_2_calibration_result += will_it_calibrate(line[0], line[1:], part2=True)
timer_part2_end=timer_script_end=perf_counter()
print("Part 2:", part_2_calibration_result)

print(f"""
Execution times (sec)
Parse: {timer_parse_end-timer_parse_start:3.3f}
Part1: {timer_part1_end-timer_part1_start:3.3f}
Part2: {timer_part2_end-timer_part2_start:3.3f}
Total: {timer_script_end-timer_script_start:3.3f}""")