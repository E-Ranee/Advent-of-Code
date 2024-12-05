file = "input.txt"
# file = "test.txt"

f = open(file, "r")
file_data = f.readlines()
f.close()


"""
# Data comes in the form
# rows of pipe separated pairs of numbers
# empty line
# rows of comma separated numbers

...
75|13
53|13

75,47,61,53,29
97,61,53,29,13
...
"""

page_ordering_rules = []
update_page_numbers = []

for row in file_data:
    if "|" in row:
        # needs to be an ordered pair
        # remove new line characters, split on pipe character, turn list of strings into ints
        page_ordering_rules.append([int(x) for x in row.strip().split("|")])
    elif row == "\n":
        pass
    else:
        # remove new line characters, split on comma, turn to list of ints
        update_page_numbers.append([int(x) for x in row.strip().split(",")])
        # NOTE: I checked the length of the list compared to the length of the set of the list and found no duplicate numbers

def get_relevant_rules(booklet, page_ordering_rules):
    """Returns only the rules where both numbers are present in the booklet"""
    list_of_relevant_rules = []
    for rule in page_ordering_rules:
        if set(rule).issubset(booklet): # both numbers contained in the booklet
            list_of_relevant_rules.append(rule)
    return list_of_relevant_rules

def check_booklet_against_rules(booklet, page_ordering_rules):
    list_of_relevant_rules = get_relevant_rules(booklet, page_ordering_rules)
    # we have the rules where both numbers are in the booklet. Time to compare them to the booklet
    list_of_failed_rules = []

    for rule in list_of_relevant_rules:
        relevant_pages = []
        for page in booklet:
            if page in rule:
                relevant_pages.append(page)
        if relevant_pages != rule:
            list_of_failed_rules.append(rule)

    return (booklet, list_of_failed_rules)

total_middle_pages = 0
failed_booklets = []
for booklet in update_page_numbers:
    result = check_booklet_against_rules(booklet, page_ordering_rules) # form (booklet, [rules failed])
    # if it passed, return the middle page
    if len(result[1]) == 0:
        total_middle_pages += booklet[int(((len(booklet) / 2) - 0.5))]
    else:
        failed_booklets.append(result)
    
#### PART 2: FIX THE BOOKLETS #####
from collections import Counter

total_fixed_middle_pages = 0
for item in failed_booklets:
    booklet = item[0]
    failed_rules = item[1]
    list_of_relevant_rules = get_relevant_rules(booklet, page_ordering_rules)
    # NOTE: I checked the that the list of rules contains rules for every pairing of numbers in the input
    # There is no case of orphaned numbers which could go anywhere
    # import math
    # test = len(list_of_relevant_rules) == math.comb(len(booklet), 2) # is the number of relevant rules equal to the number of ways you can choose 2 numbers?

    # if the rules are always in the form [left number, right number]
    # add all pairs are accounted for
    # then the 1st number would occur in the first position n times, then the 2nd n-1 times etc
    left_number = [x[0] for x in list_of_relevant_rules]
    counter = Counter(left_number)
    counts = counter.most_common() # in the form [(97, 4), (75, 3), (47, 2), (61, 1)] NOTE: rightmost number excluded
    # middle page is the length of this / 2 where the index starts at 0 
    # eg booklet has 5 pages, middle page is 3rd. 
    # last page is excluded so 4 pages remaining (middle page 3rd)
    # 4/2 = 2 (middle page 3rd)
    # 2 is the third index

    total_fixed_middle_pages += counts[int(len(counts)/2)][0]


print("Part 1:", total_middle_pages)
print("Part 2:", total_fixed_middle_pages)
