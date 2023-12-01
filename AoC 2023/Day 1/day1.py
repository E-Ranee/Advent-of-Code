import re

puzzle_data = "input.txt"
test_data_part1 = "example.txt"
test_data_part2 = "example2.txt"


f = open(puzzle_data, "r")
data = f.readlines()
f.close()
# Open and close the file safely


rows = []
for row in data:
    rows.append(row.strip())
# make a list of every row in the input file

def part1():
    pattern = "\d"
    cumulative_total = 0
    for string in rows:
        result = re.findall(pattern,string)
        # extracts the numbers from each row
        first_digit = int(result[0])
        last_digit = int(result[-1])
        subtotal = first_digit * 10 + last_digit
        cumulative_total += subtotal

    print(cumulative_total)


### part 2 ###

written_numbers = {
    "zero" : 0,
    "one" : 1,
    "two" : 2,
    "three" : 3,
    "four" : 4,
    "five" : 5,
    "six" : 6,
    "seven" : 7,
    "eight" : 8,
    "nine" : 9
}

def part2():
    pattern = "(\d|one|two|three|four|five|six|seven|eight|nine|ten|zero)"
    cumulative_total = 0
    for string in rows:
        result = re.findall(pattern,string) # this is a list of mixed words and digits
        for index, item in enumerate(result):
            # all digits are of length 1 and need to be converted into an int
            if len(item) == 1:
                result[index] = int(item)
            elif len(item) > 1: # words are longer than one digit and need to be looked up in the dictionary to return an int
                result[index] = written_numbers[item]
            else:
                raise Exception(f"Item length lower than 1. Item: {item} found in {string}")
            
        first_digit = int(result[0])

        # The regex doesn't account for eg "oneight" being potentially both a one and an eight
        # it reads left to right and dismisses the second number, which makes the last digit sometimes incorrect
        # In order to search in a way that will guarantee that we have the right last digit, we reverse the input (and the search patterns!) and find the "first" digit
            
        reversed_pattern = "(orez|net|enin|thgie|neves|xis|evif|ruof|eerht|owt|eno|\d)" # it looks so silly but it works
        reversed_string = "".join(reversed(string)) # the reversed() function returns an iterator so we have to join it back into a string

        result = re.findall(reversed_pattern, reversed_string)
        for index, item in enumerate(result):
            # digits only have one character but need to be turned into an int
            if len(item) == 1:
                result[index] = int(item)
            elif len(item) > 1: # words need to be looked up using the CORRECT ORDER of letters
                result[index] = written_numbers["".join(reversed(item))]
            else:
                raise Exception(f"Item length lower than 1. Item: {item} found in {string}")

        last_digit = int(result[0]) # the first item in the reversed list
        subtotal = first_digit * 10 + last_digit
        cumulative_total += subtotal

    print(cumulative_total)

part2()