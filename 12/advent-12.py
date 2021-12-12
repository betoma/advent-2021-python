from collections import defaultdict

conn_set = defaultdict(set)

with open("input.txt") as f:
    for pair in [x.strip().split("-") for x in f.readlines()]:
        conn_set[pair[0]].add(pair[1])
        conn_set[pair[1]].add(pair[0])

connections = {k: list(v) for k, v in conn_set.items()}

# part one


def get_options(cave):
    possible_paths = [["start", x] for x in cave["start"]]
    good_paths = []
    while possible_paths:
        continued_paths = []
        for path in possible_paths:
            for option in cave[path[-1]]:
                if option == "end":
                    good_paths.append(path + [option])
                elif option.islower() and option in path:
                    continue
                else:
                    continued_paths.append(path + [option])
        possible_paths = continued_paths
    return good_paths


paths = get_options(connections)

print(len(paths))


# part two


def get_more_options(cave):
    possible_paths = [(["start", x], False) for x in cave["start"]]
    good_paths = []
    while possible_paths:
        continued_paths = []
        for path, used_up in possible_paths:
            for option in cave[path[-1]]:
                if option == "end":
                    good_paths.append(path + [option])
                elif option.islower() and option in path:
                    if option == "start" or used_up:
                        continue
                    else:
                        continued_paths.append((path + [option], True))
                else:
                    continued_paths.append((path + [option], used_up))
        possible_paths = continued_paths
    return good_paths


more_paths = get_more_options(connections)

print(len(more_paths))
