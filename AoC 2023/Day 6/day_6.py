file = "input.txt"
# file = "test.txt"

f = open(file, "r")
data = f.readlines()
f.close()

# data in format: "Time:        54     70     82     75"
# strips new line, splits on white space, discards "Time:", converts to integers
times = [int(number) for number in data[0].strip().split()[1:]]
distances = [int(number) for number in data[1].strip().split()[1:]]

def simulate_game(duration_of_game, distance_to_beat):
    """Runs through every possibility and returns the number of options with a successful outcome"""

    successful_outcomes = 0
    for i in range(duration_of_game + 1): # includes every state from 0 acceleration to full acceleration 0 distance
        speed = i
        distance = (duration_of_game - i) * speed
        if distance > distance_to_beat:
            successful_outcomes += 1

    return successful_outcomes

margin_of_error = 1
for i in range(len(times)):
    margin_of_error *= simulate_game(times[i], distances[i])

print("Part 1:", margin_of_error)


import cmath, math

megatime = int("".join([str(num) for num in times])) # convert list to strings to concatonate them, then back to integer
megadistance = int("".join([str(num) for num in distances]))

# if distance = (duration_of_game - i) * speed 
# where speed = i
# then (megatime - index) * index = distance
# -index^2 + megatime*index = distance
# -index^2 + megatime*index - distance = 0
# ax^2 +bx + c = 0

a = -1
b = megatime
c = -megadistance

discriminant = (b**2) - (4*a*c)

# find two solutions
sol1 = (-b-cmath.sqrt(discriminant))/(2*a)
sol2 = (-b+cmath.sqrt(discriminant))/(2*a)

lower_bound = math.floor(min(sol1.real,sol2.real))
upper_bound = math.floor(max(sol1.real,sol2.real))

print("Part 2:", upper_bound-lower_bound)