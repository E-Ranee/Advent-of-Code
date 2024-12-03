import re

file = "input.txt"
# file = "test.txt"

f = open(file, "r")
file_data = f.readlines()
f.close()

data = []
for row in file_data:
    data.append(row.strip())

pattern = "mul\((\d+),(\d+)\)" # returns a tuple ('2', '4')
pattern_part_2 = "mul\((\d+),(\d+)\)|(don't)|(do)" 

total = 0
for row in data:
    result = re.findall(pattern, row) # returns a list [('2', '4'), ('5', '5'), ('11', '8'), ('8', '5')]
    for pair in result: # ('2', '4')
        total += int(pair[0]) * int(pair[1])

print("Part 1:", total)

total = 0
enabled = True
for row in data:
    result = re.findall(pattern_part_2, row)
    for pair in result:
        if pair[3] == "do":
            enabled = True
        elif pair[2] == "don't":
            enabled = False
        elif enabled:
            total += int(pair[0]) * int(pair[1])
        else:
            pass

print("Part 2:", total)