f = open(f"input.txt", "r")
data = f.readlines()
f.close()

goal_unique_letters = 14 # 4 for part 1, 14 for part 2
counter = 0
signal_marker = []

for letter in data[0]:
    if len(signal_marker) == goal_unique_letters:
        # check if it fits the pattern
        if len(set(signal_marker)) == goal_unique_letters:
            print(counter)
            break # if yes, end
        else:
            signal_marker.pop(0)
            signal_marker.append(letter)
            counter += 1 # if no, shift focus right one letter and try again
    else:
        signal_marker.append(letter) # initial setup
        counter += 1