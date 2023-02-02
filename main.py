import sys
import json

_AVOID = "avoid"
_PAIR = "pair"
_NOPREF = 0

def create_guest_matrix(guest_list, preferences):
    no_prefs = {guest: 0 for guest in guest_list}
    matrix = {guest: no_prefs.copy() for guest in guest_list}
    for perference in preferences:
        matrix[perference['guests'][0]][perference['guests'][1]] = perference['preference']
        matrix[perference['guests'][1]][perference['guests'][0]] = perference['preference']
    return matrix

def solve_for_member(guest, guest_list, preferences):
    remaining_guests = [g for g in guest_list if g != guest]
    current_table = [guest]
    current_guest = 0
    while current_guest < len(current_table):
        current_guest_prefs = preferences[current_table[current_guest]]
        for (other_guest, pref) in current_guest_prefs.items():
            if pref == _PAIR and other_guest not in current_table:
                remaining_guests = [g for g in remaining_guests if g != other_guest]
                current_table.append(other_guest)
        current_guest = current_guest + 1
    return (current_table, remaining_guests)

def solve_max_tables(guest_list, preferences):
    tables = []
    while len(guest_list) > 0:
        (current_table, guest_list) = solve_for_member(guest_list[0], guest_list, preferences)
        tables.append(current_table)
    return tables

def can_merge_tables(table1, table2, preferences):
    for guest1 in table1:
        for guest2 in table2:
            if preferences[guest1][guest2] == _AVOID:
                return False
    return True

def merge_max_solution(tables, preferences):
    merged_tables = []
    seen = {}
    for i in range(len(tables)):
        if i in seen:
            continue
        seen[i] = True
        table = tables[i]
        for j in range(i+1, len(tables)):
            if (j not in seen) and (can_merge_tables(table, tables[j], preferences)):
                table = table + tables[j]
                seen[j] = True
        merged_tables.append(table)
    return merged_tables

def solve(num_tables, guest_list, preference_list):
    preferences = create_guest_matrix(guest_list, preference_list)
    max_soln = solve_max_tables(guest_list, preferences)
    if len(max_soln) <= num_tables:
        return max_soln
    merged_soln = merge_max_solution(max_soln, preferences)
    if len(merged_soln) <= num_tables:
        return merged_soln
    return []

def main(*args):
    with open(args[3]) as preferences_file:
        preferences_list = json.load(preferences_file)
        solution = solve(args[1], args[2], preferences_list)
        solution_dict = {f"table_{i+1}": table for (i, table) in enumerate(solution)}
        with open("output.json", "w") as outfile:
            json.dump(solution_dict, outfile)

if __name__ == "__main__":
    main(sys.argv)
