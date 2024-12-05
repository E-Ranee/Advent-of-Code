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
    if row.__contains__("|"):
        # needs to be an ordered pair
        # remove new line characters, split on pipe character, turn list of strings into ints
        page_ordering_rules.append([int(x) for x in row.strip().split("|")])
    elif row == "\n":
        ...
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

total_middle_pages = 0
for booklet in update_page_numbers:
    list_of_relevant_rules = get_relevant_rules(booklet, page_ordering_rules)
    # we have the rules where both numbers are in the booklet. Time to compare them to the booklet
    times_failed_rule = 0
    while times_failed_rule < 1:
        for rule in list_of_relevant_rules:
            relevant_pages = []
            for page in booklet:
                if page in rule:
                    relevant_pages.append(page)
            if relevant_pages != rule:
                times_failed_rule += 1
        break

    # if it passed, return the middle page
    if times_failed_rule == 0:
        total_middle_pages += booklet[int(((len(booklet) / 2) - 0.5))]
    

print(total_middle_pages)
