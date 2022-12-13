f = open(f"input.txt", "r")
# f = open(f"example_input.txt", "r")
data = f.readlines()
f.close()

# addx V takes two cycles to complete. After two cycles, the X register is increased by the value V. (V can be negative.)
# noop takes one cycle to complete. It has no other effect.

cycle = 0
CPU_x = 1
timeline = {}

for instruction in data:
    command = instruction.strip()

    if command == "noop":
        cycle += 1
        timeline[cycle] = CPU_x
    elif command.split()[0] == "addx":
        cycle += 1
        timeline[cycle] = CPU_x
        cycle += 1
        timeline[cycle] = CPU_x
        CPU_x += int(command.split()[1])

total_signal_strength = 0
for items in [20, 60, 100, 140, 180, 220]:
    total_signal_strength += timeline[items] * items

print(total_signal_strength)

def CRT_printer(timeline):
    list_of_rows = []

    def print_row(start, end, timeline):
        current_row = []
        for num in range(start, end +1):
            middle = timeline[num] # signal strength at that number = position of sprite
            left = middle - 1
            right = middle + 1

            adjusted_position = (num % 40) - 1

            if adjusted_position in [left, middle, right]:
                current_row.append("#")
            else:
                current_row.append(".")
        return current_row

    list_of_rows.append(print_row(1, 40, timeline))
    list_of_rows.append(print_row(41, 80, timeline))
    list_of_rows.append(print_row(81, 120, timeline))
    list_of_rows.append(print_row(121, 160, timeline))
    list_of_rows.append(print_row(161, 200, timeline))
    list_of_rows.append(print_row(201, 240, timeline))

    return list_of_rows

image = CRT_printer(timeline)

for row in image:
    print("".join(row))
