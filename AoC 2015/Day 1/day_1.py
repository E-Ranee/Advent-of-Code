import collections

file = "input.txt"

f = open(file, "r")
data = f.readlines()
f.close()

counter = collections.Counter(*data)
counts = counter.most_common()

print("Part 1:", counts[0][1] - counts[1][1])

floor = 0
for index, char in enumerate(data[0]):
    floor += 1 if char == "(" else -1
    if floor < 0:
        print("Part 2:", index)
        break

