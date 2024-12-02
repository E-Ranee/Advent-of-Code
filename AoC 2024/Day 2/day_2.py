file = "input.txt"
# file = "test.txt"
# file = "test2.txt"
# file = "test3.txt"
# file = "test4.txt"

f = open(file, "r")
file_data = f.readlines()
f.close()

data = []
for row in file_data:
    report_string = row.strip() # format '7 6 4 2 1'
    report_list = list(map(lambda x: int(x), report_string.split())) # makes a list of ints [7, 6, 4, 2, 1]
    data.append(report_list)

"""a report only counts as safe if both of the following are true:

The levels are either all increasing or all decreasing.
Any two adjacent levels differ by at least one and at most three."""

def safety_check(report_list, part2=False):
    """This works perfectly well for part 1"""
    ascending = sorted(report_list)
    descending = sorted(report_list, reverse=True)
    if report_list == ascending or report_list == descending:
        # check the difference between adjacent numbers
        for i in range(len(report_list)-1):
            difference = abs(report_list[i] - report_list[i+1]) # look ahead to next number
            if difference < 1:
                print(report_list, "PART 1: FAILED, repeated number")
                if part2: # check if removing a duplicated digit solves the problem
                    return problem_dampened_safety_check(report_list)
                else:
                    return False # failed to differ by at least 1
            elif difference > 3:
                print(report_list, "PART 1: FAILED Difference >3")
                if part2:
                    return problem_dampened_safety_check(report_list)
                return False # failed to differ by at most 3
            
        print(report_list, "PART 1: SUCCESS")    
        return True # passed both checks

    else: # failed the ascending/descending step
        print(report_list, "PART 1: FAILED the ascending/descending step") 
        if part2:
            return problem_dampened_safety_check(report_list)   
        else:
            return False
    
def check_ascending_order(list_of_ints, reversed=False):
    """This takes a list of integers, figures out if it is in ascending order give or take 1 number, and returns a list without that number or empty list"""
    report_list = list_of_ints if reversed == False else list_of_ints[::-1] # reverse the list if descending
    if reversed == True: 
        print("now checking descending")
    
    new_report = []
    removed_numbers = 0

    if report_list[0] <= report_list[1]: # is the first number less than the second number?
        new_report.append(report_list[0])
    else: 
        # is the first number less than the third number?
        if report_list[0] <= report_list[2]: # [2, 0, 4, 5, 6] needs to drop the 0 not the 2
            # check the difference
            # HYPOTHETICALLY WE KEEP CURRENT NUMBER
            keep_first = report_list[2] - report_list[0] # third number - first number
            keep_second = report_list[2] - report_list[1] # third number - second number
            if keep_first < 0: # if third number is less than first number, ditch first number
                print(f"removed {report_list[0]}")
                removed_numbers += 1 
            elif abs(keep_second) > 3: # first number is bigger than second number but not the third. 
                new_report.append(report_list[0]) #If jump from 2nd to 3rd too big, keep first
            else:
                print(f"removed {report_list[0]}") # if jump from 2nd to 3rd okay, ditch first
                removed_numbers += 1 

        else:
            print(f"removed {report_list[0]}")
            removed_numbers += 1

    for i in range(len(report_list)-1):
        current_number = report_list[i]
        next_number = report_list[i+1]
        previous_number = 0 if new_report == [] else new_report[-1]

        if i == 0:
            pass
        elif new_report == []:
            new_report.append(current_number)

        elif current_number >= previous_number and current_number <= next_number: # if neighbours are ordered, add to list
            new_report.append(current_number)

        elif current_number >= previous_number and next_number <= previous_number: # if next one lower, check if it's greater than previous number
            new_report.append(current_number)
        elif current_number >= previous_number and next_number >= previous_number:
            # either number could be the one which needs to be removed
            # is there a number after the next number
            if i + 2 <= len(report_list)-1:
                # there is another number
                # check the difference between current number and next next number
                # HYPOTHETICALLY WE KEEP CURRENT NUMBER
                prev_diff = current_number - previous_number
                next_diff = report_list[i+2] - current_number
                if next_diff <= 0:
                    print(f"removed {current_number}")
                    removed_numbers += 1 
                elif prev_diff <= 3 and next_diff <= 3:
                    new_report.append(current_number)
                else:
                    print(f"removed {current_number}")
                    removed_numbers += 1 
            else:
                # there isn't another number
                # check if current number is more than 3 different than previous number
                if current_number - previous_number > 3:
                    print(f"removed {current_number}") 
                    removed_numbers += 1
                else:
                    new_report.append(current_number)


        else:
            print(f"removed {current_number}") 
            removed_numbers += 1

    if len(new_report) > 0:
        if report_list[-1] >= new_report[-1]: # check last digit, if it exists
            new_report.append(report_list[-1])
    else:
        print(f"removes {report_list[-1]}")
        removed_numbers += 1

    # Check that this produces a sorted list
    is_ascending = new_report == sorted(new_report)

    if is_ascending and len(report_list) - len(new_report) <= 1:
        return new_report if reversed == False else new_report[::-1]
    else:
        return []

def problem_dampened_safety_check(report_list):
    ##############################################################
    # try ascending order

    ascended_list = check_ascending_order(report_list)
    if len(ascended_list) < len(report_list) - 1:
        descended_list = check_ascending_order(report_list, reversed=True)

    if len(ascended_list) >= len(report_list) - 1:
        new_report = ascended_list
    elif len(descended_list) >= len(report_list) - 1:
        new_report = descended_list
    else:
        print(f"{report_list} FAILED sorting, had to remove too many numbers")
        return False

    ######################################################################################################################

    removed_numbers = len(report_list) - len(new_report)
    for i in range(len(new_report)-1):
        difference = abs(new_report[i] - new_report[i+1]) # look ahead to next digit
        if difference < 1:
            if removed_numbers > 0:
                print(new_report, "Dampened check: FAILURE Difference failed to differ by at least 1") 
                return False # failed to differ by at least 1
            else:
                removed_numbers += 1 # remove this number and try again
        elif difference > 3:
            if removed_numbers < 1 and i == len(new_report) - 2: 
                print(new_report, "Dampened check: SUCCESS The only digit to differ by more than 3 was the last one")
                return True
            elif removed_numbers < 1 and i == 0:
                print(new_report, "First number differed by more than 3")
                difference += 1 # remove this number and try again
            else: 
                print(new_report, "Dampened check: FAILURE Difference failed to differ by at most 3") 
                return False # failed to differ by at most 3
        
            # !!! Don't need to remove a number and try again because the next number will have an even more extreme difference !!!
            # !!! UNLESS it is the final number


    print(new_report, "Part 2: SUCCESS") 
    return True # passed both checks
        

safe_reports = 0
problem_dampened_safe_reports = 0
for row in data:
    # if safety_check(row): safe_reports += 1
    if safety_check(row, part2=True): problem_dampened_safe_reports += 1
    print("")

print("-------------")
# print(safe_reports)
print(problem_dampened_safe_reports)

# safety_check([2, 3, 4, 6, 5, 6], part2=True)