def find_best_paths(dict_of_valves, list_of_valves, list_of_non_0_flow_valves, max_minutes, distances_dict):
    current_minute = 1
    valves_open = []
    pressure_released_per_minute = 0
    current_pressure_released = 0

    max_possible_pressure_released = sum(  [dict_of_valves[x].flow_rate for x in list_of_non_0_flow_valves]  ) 
    current_hypothetical_maximum_pressure = 0
    still_possible = True

    best_total_pressure_released = 0
    best_path = []

    permutations_of_paths = permutations(list_of_non_0_flow_valves, len(list_of_non_0_flow_valves))
    path_length = len(list_of_non_0_flow_valves) + 1

    for path in permutations_of_paths:
        # format eg ('JJ', 'HH', 'EE', 'BB', 'DD', 'CC')
        # have to start at equivalent of AA
        # add initial valve to the start of the path
        
        path = list(path)
        path.insert(0, list_of_valves[0])

        for index in range(path_length - 1):
            # travel to the next node
            distance = distances_dict[(path[index], path[index + 1])]

            for unit in range(distance):
                current_pressure_released += pressure_released_per_minute
                # print(current_minute, pressure_released_per_minute, valves_open)
                current_minute += 1
                if current_minute > max_minutes:
                    break

            # print(current_minute, pressure_released_per_minute, valves_open)
            current_minute += 1
            if current_minute > max_minutes:
                break
            # open the next valve
            valves_open.append(path[index + 1])
            pressure_released_per_minute += dict_of_valves[path[index + 1]].flow_rate
            current_pressure_released += pressure_released_per_minute

            current_hypothetical_maximum_pressure = current_pressure_released + (max_possible_pressure_released * (max_minutes-current_minute + 1))
            still_possible = current_hypothetical_maximum_pressure > best_total_pressure_released
            if not still_possible:
                break
        # if not still_possible:
        #     break

        current_pressure_released += pressure_released_per_minute * (max_minutes - current_minute - 1)

        print(path)

        if current_pressure_released > best_total_pressure_released:
            best_total_pressure_released = current_pressure_released
            best_path = valves_open

        current_pressure_released = 0
        current_minute = 0
        pressure_released_per_minute = 0
        valves_open = []

    print(best_path)
    return best_total_pressure_released

# print(find_best_paths(dict_of_valves, list_of_valves, list_of_non_0_flow_valves, 30, distances_dict))
