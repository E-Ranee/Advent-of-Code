import string

f = open(f"input.txt", "r")
data = f.readlines()
f.close()

alphabet = list(string.ascii_letters)

def identify_common_element(rucksack):
    length_of_half = int(len(rucksack)/2)
    first_half = set(rucksack[0:length_of_half])
    second_half = set(rucksack[length_of_half:])
    item_in_common = first_half.intersection(second_half)

    return str(list(item_in_common)[0])

def priority_calc(letter):
    return alphabet.index(letter)+1

priority_results = []

for items in data:
    priority_results.append(priority_calc(identify_common_element(items.strip())))

total_priority = sum(priority_results)
print(total_priority)

groups = []
current_group = []
badge_priority_total = 0

for items in data:
    current_group.append(set(items.strip()))
    if len(current_group) == 3:
        groups.append(current_group)
        current_group = []

for group in groups:
    intersection = group[0] & group[1] & group[2]
    badge_priority_total += priority_calc(str(list(intersection)[0]))

print(badge_priority_total)