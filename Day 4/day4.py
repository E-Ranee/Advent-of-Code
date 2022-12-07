import re

f = open(f"input.txt", "r")
data = f.readlines()
f.close()

def string_to_ranges(section_IDs):
    regex_pattern = "([0-9]*)" # Pulls out the digits
    numbers = re.findall(regex_pattern, section_IDs) # returns a list of strings
    numbers = [int(x) for x in numbers if x != ""] # turns strings into ints and removes empty results

    range1 = list(range(numbers[0], numbers[1]+1)) # turns start and end points into the full range
    range2 = list(range(numbers[2], numbers[3]+1))

    return range1, range2

def check_if_fully_contained(range1, range2):
    set1 = set(range1)
    set2 = set(range2)
    intersection = set1.intersection(set2)

    if len(intersection) == min(len(set1), len(set2)): # if the intersection has as many items as a set, it contains the entire set
        return 1
    else:
        return 0

def check_if_overlapped(range1, range2):
    set1 = set(range1)
    set2 = set(range2)
    intersection = set1.intersection(set2)

    if len(intersection) > 0:  # if the intersention has any items, the two sets overlap
        return 1
    else:
        return 0

counter = 0

for item in data:
    ranges = string_to_ranges(item.strip())
    # counter += check_if_fully_contained(ranges[0], ranges[1])
    counter += check_if_overlapped(ranges[0], ranges[1])

print(counter)
