file = "input.txt"
# file = "test.txt"
# file = "test2.txt"

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
    ascending = sorted(report_list)
    descending = sorted(report_list, reverse=True)
    if report_list == ascending or report_list == descending:
        # check the difference between adjacent numbers
        for i in range(len(report_list)-1):
            difference = abs(report_list[i] - report_list[i+1])
            if difference < 1:
                if part2: # check if removing a duplicated digit solves the problem
                    return problem_dampened_safety_check(report_list)

                else:
                    print(report_list, "Failed to differ by at least 1")
                    return False # failed to differ by at least 1
            elif difference > 3:
                if part2:
                    return problem_dampened_safety_check(report_list)
                print(report_list, "Safety check: Failed to differ by at most 3")
                return False # failed to differ by at most 3
            
        print(report_list, "Passed both checks")    
        return True # passed both checks

    else: # failed the ascending/descending step
        if part2:
            print(report_list, "Failed the ascending/descending step: progressing to dampened saftety check") 
            return problem_dampened_safety_check(report_list)
            
        else:
            print(report_list, "Failed the ascending/descending step") 
            return False
    
def problem_dampened_safety_check(report_list):
    #################
    # try ascending order
    new_report = []
    removed_numbers = 0

    if report_list[0] <= report_list[1]: # is the first number less than the second number?
        new_report.append(report_list[0])
    else: 
        print(f"removed {report_list[0]}")
        removed_numbers += 1

    for i in range(len(report_list)-1):
        if i == 0:
            pass
        elif report_list[i] <= report_list[i+1]: # is less than the next number
            new_report.append(report_list[i])
        else:
            print(f"removed {report_list[i]}") 
            removed_numbers += 1

    if len(new_report) > 0:
        if report_list[-1] >= new_report[-1]: # check last digit, if it exists
            new_report.append(report_list[-1])
    else:
        print(f"removes {report_list[-1]}")
        removed_numbers += 1

    # Check that this produces a sorted list
    is_ascending = new_report == sorted(new_report)

    if is_ascending and removed_numbers <= 1:
        print(new_report, "is ascending")

    else:
        print("Ascending order failed, trying descending order")
        #################
        # try descending order
        new_report = []
        removed_numbers = 0

        if report_list[0] >= report_list[1]: # is the first number more than the second number?
            new_report.append(report_list[0])
        else:
            print(f"removed {report_list[0]}")
            removed_numbers += 1

        for i in range(len(report_list)-1):
            if i == 0:
                pass
            elif report_list[i] >= report_list[i+1]: # is more than the next number
                new_report.append(report_list[i])
            else:
                print(f"removed {report_list[i]}") 
                removed_numbers += 1

        if report_list[-1] <= new_report[-1]: # check last digit
            new_report.append(report_list[-1])
        else:
            print(f"removed {report_list[-1]}")
            removed_numbers += 1

        # Check that this produces a sorted list
        is_descending = new_report == sorted(new_report, reverse=True)

        if is_descending and removed_numbers <= 1:
            print(new_report, "is descending")
            pass
        else:
            print(new_report, "Failed the ascending/descending step")
            return False

        ##################


    for i in range(len(new_report)-1):
        difference = abs(new_report[i] - new_report[i+1])
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

    
    if removed_numbers <= 1:
        print(removed_numbers)
        print(new_report, "SUCCESS Passed the dampened safety checks") 
        return True # passed both checks
    else:
        print(new_report, "Dampened check: FAILURE Had to remove too many numbers") 
        return False # had to remove multiple numbers to make it work

safe_reports = 0
problem_dampened_safe_reports = 0
for row in data:
    if safety_check(row): safe_reports += 1
    if safety_check(row, part2=True): problem_dampened_safe_reports += 1
    print("")

print("-------------")
print(safe_reports)
print(problem_dampened_safe_reports)

# print(safety_check([37, 36, 37, 39, 36], True))