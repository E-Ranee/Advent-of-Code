from math import trunc, lcm, gcd
import re

f = open(f"input.txt", "r")
# f = open(f"example_input.txt", "r")
data = f.readlines()
f.close()

# list of monkeys (so you know which number corresponds to which monkey)



class Monkey:
    def __init__(self, inventory, operation, divisor, true_, false_):
        self.inventory = inventory
        self.operation = operation # function (lambda function)
        self.test = divisor # number = divisible by x
        self.true_ = true_ # monkey A to give to
        self.false_ = false_ # monkey B to give to

        self.times_inspected = 0

    def inspect(self, index):
        # apply operation to worry level
        worry_level = self.inventory[index] % supermodulo
        worry_level = self.operation(worry_level)
        # add to self.times_inspected
        self.times_inspected += 1
        # divide worry level by worry modifier
        worry_level = int(trunc(worry_level * worry_modifier))
        # apply test to remaining worry level
        if worry_level % self.test == 0:
        # give to monkey (add to their inventory)
            self.give_item_to_monkey(worry_level, self.true_)
        else:
            self.give_item_to_monkey(worry_level, self.false_)

    def give_item_to_monkey(self, item, monkey):
        dict_of_monkeys[monkey].inventory.append(item)

    def play_round(self):
        for index in range(len(self.inventory)):
            self.inspect(index)
        self.inventory = []

#######################################################################

# Groups text by monkey

list_of_monkey_text = []
temp_list = []

for line in data:
    if line.strip() == "":
        list_of_monkey_text.append(temp_list)
        temp_list = []
    else:
        temp_list.append(line.strip())
list_of_monkey_text.append(temp_list)

#######################################################################

def operation_to_lambda(text):
    # text takes the form eg "* 19", "* old", "+ 4"
    operator, variable = re.split(" ", text)

    if operator == "*":
        if variable == "old":
            return lambda x: x * x
        else:
            return lambda x: x * int(variable)

    elif operator == "+":
        if variable == "old":
            return lambda x: x + x
        else:
            return lambda x: x + int(variable)

dict_of_monkeys = {}
number_of_monkeys = 0
list_of_modulos = []

for monkey in list_of_monkey_text:
    monkey_number = int(re.findall("\d+", monkey[0])[0])
    monkey_inventory = [int(x) for x in re.findall("\d+", monkey[1])]
    monkey_operation = re.split("old ", monkey[2])[1] # returns eg "* 19"
    monkey_lambda = operation_to_lambda(monkey_operation)
    monkey_divisor = int(re.findall("\d+", monkey[3])[0])
    monkey_true = int(re.findall("\d+", monkey[4])[0])
    monkey_false = int(re.findall("\d+", monkey[5])[0])

    monkey_object = Monkey(monkey_inventory, monkey_lambda, monkey_divisor, monkey_true, monkey_false)
    dict_of_monkeys[monkey_number] = monkey_object
    number_of_monkeys += 1
    list_of_modulos.append(monkey_divisor)

def lowest_common_multiple_of_array(array):
    lcm = array[0]
    for i in range(1, len(array)):
        lcm = lcm * array[i] // gcd(lcm, array[i])
    return lcm

round = 1
max_rounds = 10000 # 20 for part 1
worry_modifier = 1 # 1/3 for part 1
supermodulo = lowest_common_multiple_of_array(list_of_modulos)

while round <= max_rounds:
    for index in range(number_of_monkeys):
        dict_of_monkeys[index].play_round()
    round += 1

inspections = []
for index in range(number_of_monkeys):
    inspections.append(dict_of_monkeys[index].times_inspected)

print(inspections)

print(sorted(inspections)[-1]*sorted(inspections)[-2])