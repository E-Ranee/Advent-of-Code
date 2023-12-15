import re

file = "input.txt"
# file = "test.txt"

f = open(file, "r")
file_data = f.read().strip()
f.close()

data = file_data.split(",")

def hash_algorithm(current_value, new_character):
    ascii_code = ord(new_character)
    new_value = current_value + ascii_code
    new_value *= 17
    new_value = new_value % 256
    return new_value

hashmap_dict = {}

sum_of_hashes = 0
for row in data: # for each instruction in comma separated list
    hash = 0 # the result of the hash algorithm
    label = re.findall("\w+", row)[0] # everything before the dash or equals
    focal_length = int(row[-1]) # the number at the end
    for character in row:
        if character == "=":
            # if there is no box already, create a new one with hash as key
            if hash not in hashmap_dict:
                hashmap_dict[hash] = [(label, focal_length)]

            # if there is a lens with the same label, overwrite it
            elif label in [x[0] for x in hashmap_dict[hash]]: # look up in the first part of each tuple
                for index, lens in enumerate(hashmap_dict[hash]):
                    if lens[0] == label:
                        hashmap_dict[hash][index] = (label, focal_length) # replace tuple at the same index

            # if there isn't a lens with the same label, append to end
            else:
                hashmap_dict[hash].append((label, focal_length))

        elif character == "-":
            if hash in hashmap_dict: # if it exists already, delete it. If it doesn't exist, all good
                for lens in hashmap_dict[hash]:
                    if lens[0] == label: # check each lens for the right label
                        hashmap_dict[hash].remove(lens) # remove in place from list

            # go to box and remove the lens with that label if present from box
            # move all other lenses forwards
        hash = hash_algorithm(hash, character)

    sum_of_hashes += hash

def calculate_lens_power(box_number, index, focal_length):
    return (1 + box_number) * (index + 1) * focal_length

total_focal_power = 0
for box_number, list_of_lenses in hashmap_dict.items():
    for index, lens in enumerate(list_of_lenses): # format ("label", power)
        total_focal_power += calculate_lens_power(box_number, index, lens[1])

print("Part 1:", sum_of_hashes)
print("Part 2:", total_focal_power)