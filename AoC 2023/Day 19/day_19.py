import re

file = "input.txt"
# file = "test.txt"

f = open(file, "r")
file_data = f.readlines()
f.close()

work_flows = []
parts = []
currently_adding_to = work_flows
for row in file_data:
    if row == "\n":  # swaps which list it adds to on a new line
        currently_adding_to = parts
        continue
    currently_adding_to.append(row.strip())

work_flow_dict = {}

def parse_workflow(workflow_string):
    """Creates a dictionary with a name as the key and then a tuple of instructions and else case"""
    # format = px{a<2006:qkq,m>2090:A,rfg}
    name, csv = re.findall("(\w+){(.+)}", workflow_string)[0]
    instructions = csv.split(",")
    destination = instructions.pop(-1) # moves the else case to its own variable
    work_flow_dict[name] = (instructions, destination)

def apply_instruction(part):
    # format = Part_object, "in"
    instructions_name = part.instruction
    instructions, else_case = work_flow_dict[instructions_name]
    for instruction in instructions: # format = ['s<537:gd', 'x>2440:R']
        # format = 's<537:gd'
        variable_to_check, outcome = instruction.split(":") # format "s<537", "gd"
        value_to_check = getattr(part, variable_to_check[0]) # gets eg the x value of the part
        value_to_compare_against = int(re.findall("\d+", variable_to_check)[0]) # gets the digits

        if ">" in variable_to_check:
            check_passed = value_to_check > value_to_compare_against
        else: # "<"
            check_passed = value_to_check < value_to_compare_against

        if check_passed:
            # check if destination is A/R or new instruction
            # if any of these are true, it leaves the current set of instructions early
            if outcome == "A":
                part.state = "approved"
                return
            elif outcome == "R":
                part.state = "rejected"
                return
            else:
                part.instruction = outcome # eg go to workflow "gd"
                return
            
    # cycled through all instructions, now for final verdict or new set of instructions
    if else_case == "A":
        part.state = "approved"
    elif else_case == "R":
        part.state = "rejected"
    else:
        part.instruction = else_case

class Part():
    def __init__(self, x, m, a, s):
        self.x = x
        self.m = m
        self.a = a
        self.s = s
        self.state = None
        self.instruction = "in"
        self.total = sum([x,m,a,s])

for work_flow_string in work_flows:
    # Formats each string and adds it to the dictionary
    parse_workflow(work_flow_string)

list_of_parts = [] # this will be a list of members of the Part class

for part in parts:
    # format = "{x=2127,m=1623,a=2188,s=1013}"
    x, m, a, s = [int(x) for x in re.findall("\d+", part)]
    list_of_parts.append(Part(x, m, a, s))

for part in list_of_parts:
    while part.state == None:
        apply_instruction(part)

total = sum([part.total for part in list_of_parts if part.state == "approved"])
print("total: ", total)

x = (1, 4000)
m = (1, 4000)
a = (1, 4000)
s = (1, 4000)

