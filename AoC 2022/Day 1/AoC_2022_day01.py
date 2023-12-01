f = open(f"input.txt", "r")
data = f.readlines()
f.close()

list_of_calories = []
current_elf = []
for entry in data:
    if entry != "\n":
        current_elf.append(int(entry))
    else:
        list_of_calories.append(sum(current_elf))
        current_elf = []

sorted_list = sorted(list_of_calories).copy()
print(sum(sorted_list[-3:]))