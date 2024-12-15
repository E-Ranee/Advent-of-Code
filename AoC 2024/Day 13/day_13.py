from typing import List
from time import perf_counter
import re

# after import lines
timer_script_start = perf_counter()
timer_parse_start = perf_counter()

file = "input.txt"
# file = "test.txt"

f = open(file, "r")
file_data = f.readlines()
f.close()


class Button:
    def __init__(self, x_change: int, y_change: int, token_cost: int):
        self.x_change = x_change
        self.y_change = y_change
        self.token_cost = token_cost


class Button_A(Button):
    def __init__(self, x_change: int, y_change: int):
        super().__init__(x_change, y_change, 3)  # new Button A (costs three tokens)


class Button_B(Button):
    def __init__(self, x_change: int, y_change: int):
        super().__init__(x_change, y_change, 1)  # new Button A (costs three tokens)


class Claw_Machine_Scenario:
    def __init__(
        self, prize_x: int, prize_y: int, button_A: Button_A, button_B: Button_B
    ):
        self.button_A = button_A
        self.button_B = button_B
        self.prize_x = prize_x
        self.prize_y = prize_y

    def __str__(self):
        return f"""Button A: X + {self.button_A.x_change}, Y + {self.button_A.y_change}
Button B: X + {self.button_B.x_change}, Y + {self.button_B.y_change}
Prize: X = {self.prize_x}, Y = {self.prize_y}
"""

    def solve_simultaneous_equation(self, part_2=False):
        """Returns the number of times each button needs to be pressed to reach the prize, if it is a whole number"""

        button_A_x = self.button_A.x_change
        button_A_y = self.button_A.y_change
        prize_x = self.prize_x + 10000000000000 if part_2 else self.prize_x
        button_B_x = self.button_B.x_change
        button_B_y = self.button_B.y_change
        prize_y = self.prize_y + 10000000000000 if part_2 else self.prize_y

        # info from https://www.reddit.com/r/adventofcode/comments/1hdde78/comment/m1va2jf/

        # eg 94a + 22b = 8400   # (Ax * a) + (Bx * b) = prize_x
        # 34a + 67b = 5400      # (Ay * a) + (By * b) = prize_y

        # An equation will be the same if you multiply both sides so lets do that to both of them with a not so random picked number:
        # 34*(94a + 22b) = 34 * 8400
        # 94*(34a + 67b) = 94 * 5400

        # Next step, equations are also the same if you add/subtract the same thing to both sides, so we can just subtract one of these from the other and it is still true:
        # 34*(94a + 22b) - 94*(34a + 67b) = 34 * 8400 - 94 * 5400

        # And by pure magic 34*94a - 94*34a means the a's disappear! And we are left with:
        # (34*22 - 94*67) * b = 34 * 8400 - 94 * 5400

        # And then we have b:
        # b = (34 * 8400 - 94 * 5400) /  (34*22 - 94*67);

        button_B_presses = (button_A_y * prize_x - button_A_x * prize_y) / (
            button_A_y * button_B_x - button_A_x * button_B_y
        )

        # When we have b, calculating a becomes easy, its just to take one of the equations and replace b with its value and shuffle bits around some there:
        # 94a + 22b = 8400 => a = (8400 - 22b) / 94
        button_A_presses = (prize_x - button_B_x * button_B_presses) / button_A_x

        return (
            [int(button_A_presses), int(button_B_presses)]
            if button_A_presses.is_integer() and button_B_presses.is_integer()
            else []
        )

    def find_cheapest_prize(self, part_2=False):

        results = self.solve_simultaneous_equation(part_2)
        if len(results) == 0:
            return 0

        a_presses = results[0]
        b_presses = results[1]
        max_presses = 100 + 10000000000000 if part_2 else 100
        if (
            a_presses <= max_presses
            and a_presses >= 0
            and b_presses <= max_presses
            and b_presses >= 0
        ):
            return a_presses * 3 + b_presses


##################### PROCESSING INPUT #################################
# Look at the input in blocks of 4 rows and extract the pairs of numbers in each row
# Then create buttons and a scenario to put them and the goal coordinates in

regex_pattern = "\d+"

data: List[Claw_Machine_Scenario] = []
for i in range(0, len(file_data), 4):
    button_A_x_change, button_A_y_change = [
        int(x) for x in re.findall(regex_pattern, file_data[i])
    ]
    button_B_x_change, button_B_y_change = [
        int(x) for x in re.findall(regex_pattern, file_data[i + 1])
    ]
    prize_x, prize_y = [int(x) for x in re.findall(regex_pattern, file_data[i + 2])]
    #  i + 4 is a blank line

    button_A = Button_A(
        button_A_x_change, button_A_y_change
    )  # The only difference in button types is that it prefills the token cost
    button_B = Button_B(button_B_x_change, button_B_y_change)
    scenario = Claw_Machine_Scenario(prize_x, prize_y, button_A, button_B)
    data.append(scenario)

# after processing input and running past functions
timer_parse_end = timer_part1_start = perf_counter()

############################ PART 1 ###############################
part_1 = 0
for scenario in data:
    part_1 += scenario.find_cheapest_prize()

print("Part 1:", part_1)
timer_part1_end = timer_part2_start = perf_counter()

########################### PART 2 ####################################
part_2 = 0
for scenario in data:
    part_2 += scenario.find_cheapest_prize(part_2=True)

print("Part 2:", part_2)
timer_part2_end = timer_script_end = perf_counter()

########################## TIMER #######################################

print(
    f"""
Execution times (sec)
Parse: {timer_parse_end-timer_parse_start:3.3f}
Part1: {timer_part1_end-timer_part1_start:3.3f}
Part2: {timer_part2_end-timer_part2_start:3.3f}
Total: {timer_script_end-timer_script_start:3.3f}"""
)
