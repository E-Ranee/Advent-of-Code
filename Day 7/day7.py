f = open(f"input.txt", "r")
# f = open(f"example_input.txt", "r")
data = f.readlines()
f.close()

# cd = change directory
# cd x = move IN one level (to a directory inside this one)
# cd .. = move OUT one level (to the directory that contains this one)
# cd / = switch to outermost directory /

# ls = list. Prints all files/directories within the current directory
# 123 abc = file called abc with a size of 123
# dir xyz = current directory contains a directory named xyz

dict_of_directory_sizes = {}

# "/ > abc > def > ghi"
current_path = ["/"]
current_folder = "/"

iterate_through_directory = False

for lines in data:
    line = lines.strip() # get rid of new line characters

    if iterate_through_directory == True: # going through list of contents of a folder
        if line[0] == "$":
            iterate_through_directory = False # if you get to a command, stop
        else:
            if line[0].isdigit(): # if it's file add the file size to its folder and each one above it
                for i in range(len(current_path)):
                    current_path_string = " > ".join(current_path[0:i+1])
                    try:
                        dict_of_directory_sizes[current_path_string] += int(line.split()[0]) 
                    except:
                        dict_of_directory_sizes[current_path_string] = 0
                        dict_of_directory_sizes[current_path_string] += int(line.split()[0]) 

    if line == "$ cd /": # parent director, doesn't need to do anything
        pass
    elif line == "$ ls": # time to loop through the folder
        iterate_through_directory = True
    elif line == "$ cd ..": # go up a folder
        del current_path[-1]
        current_folder = current_path[-1]
    elif line[:5] == "$ cd ": # go into a folder
        current_path.append(line[5:])
        current_folder = line[5:]

max_file_size = 100000
total_to_be_deleted = 0
for file_size in dict_of_directory_sizes.values():
    if file_size <= max_file_size:
        total_to_be_deleted += file_size

print(total_to_be_deleted)

total_disk_space = 70000000
needed_free_space = 30000000
current_used_space = dict_of_directory_sizes["/"]
current_free_space = total_disk_space - current_used_space
amount_needed_to_free_up = needed_free_space - current_free_space

import operator
sorted_dict = sorted(dict_of_directory_sizes.items(), key=operator.itemgetter(1)) # produced a list of tuples with the quantity sorted from low to high
for item in sorted_dict:
    if item[1] > amount_needed_to_free_up: # when you get to the first size greater than the amount needed, print that size
        print(item[1])
        break
