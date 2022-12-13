import ast

f = open(f"input.txt", "r")
# f = open(f"example_input.txt", "r")
data = f.readlines()
f.close()

list_of_pairs = []
temp_list = []

for line in data:
    if line != "\n":
        temp_list.append(ast.literal_eval(line.strip()))
    else:
        list_of_pairs.append(temp_list)
        temp_list = []
list_of_pairs.append(temp_list)

def compare_pairs(left, right):
    left_len = len(left)
    right_len = len(right)

    for index in range(min(left_len, right_len)):
        left_chunk = left[index]
        right_chunk = right[index]
        left_type = type(left_chunk)
        right_type = type(right_chunk)

        # If both values are integers, the lower integer should come first. 
        # If the left integer is lower than the right integer, the inputs are in the right order. 
        # If the left integer is higher than the right integer, the inputs are not in the right order. 
        # Otherwise, the inputs are the same integer; continue checking the next part of the input.
        if left_type == int and right_type == int:
            if left_chunk < right_chunk:
                return True
            elif left_chunk > right_chunk:
                return False
            else:
                continue

        # If both values are lists, compare the first value of each list, then the second value, and so on. 
        # If the left list runs out of items first, the inputs are in the right order. 
        # If the right list runs out of items first, the inputs are not in the right order. 
        # If the lists are the same length and no comparison makes a decision about the order, continue checking the next part of the input.
        if left_type == list and right_type == list:
            result = compare_pairs(left_chunk, right_chunk)
            if result == None:
                continue
            else:
                return result


        # If exactly one value is an integer, convert the integer to a list which contains that integer as its only value, then retry the comparison. 
        # For example, if comparing [0,0,0] and 2, convert the right value to [2] (a list containing 2); the result is then found by instead comparing [0,0,0] and [2].
        if left_type == int:
            left_chunk = [left_chunk]
        else:
            right_chunk = [right_chunk]

        result = compare_pairs(left_chunk, right_chunk)
        if result == None:
            continue
        else:
            return result


    if left_len < right_len:
        return True
    elif right_len < left_len:
        return False
    else:
        return None




counter = 1
list_of_indices = []
for pairs in list_of_pairs:
    if compare_pairs(pairs[0], pairs[1]):
        list_of_indices.append(counter)
    counter += 1

print(sum(list_of_indices))