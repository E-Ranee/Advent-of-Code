def check_for_horizontal_mirror(input_list):

    # which rows are duplicated?
    counter = collections.Counter(input_list)
    counts = counter.most_common() # list of tuples ("element", count)
    repeated_elements = [x[0] for x in counts if x[1] > 1] # element for tuple in counts if occurrences is greater than 1

    # are the repeated elements clustered around a line
    indices = []
    likely_spot = []
    for element in repeated_elements:
        first_occurrence = input_list.index(element)
        second_occurrence = input_list.index(element, first_occurrence+1)
        indices.append(first_occurrence)
        indices.append(second_occurrence)


        likely_spot.append((second_occurrence + first_occurrence)/2)

    if len(indices) > 0:
        if max(indices) == len(data) - 1 or min(indices) == 0:
            counter = collections.Counter(likely_spot)
            counts = counter.most_common()
            return counts[0][0] + 0.5

    # clustering - are the indices sequential?
    if len(indices) > 0:
        if check_if_sequential(indices):
            mirror_line = (max(indices) + min(indices)) / 2 # will be a number and a half
            rows_above_mirror_line = mirror_line + 0.5
        else:
            return 0
    else:
        return 0

    # Are the remaining rows valid?
    # Need to have some rows outside of the reflection area
    # On ONE side only

    remaining_row_indices = [x for x in range(len(input_list)) if x not in indices]
    if check_if_sequential(remaining_row_indices):
        return rows_above_mirror_line
    else:
        return 0