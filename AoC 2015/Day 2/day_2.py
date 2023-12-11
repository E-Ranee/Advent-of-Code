file = "input.txt"

f = open(file, "r")
data = f.readlines()
f.close()

wrapping_paper_needed = 0
for row in data:
    length, width, height = [int(num) for num in row.strip().split("x")]
    side_1 = 2 * length * width
    side_2 = 2 * width * height
    side_3 = 2 * height * length
    bonus_paper = min(side_1, side_2, side_3) / 2
    wrapping_paper_needed += (side_1 + side_2 + side_3 + bonus_paper)

print("Part 1:", wrapping_paper_needed)
    