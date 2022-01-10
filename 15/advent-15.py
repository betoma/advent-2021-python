from tqdm import tqdm

FILENAME = "input.txt"

def infinite_loop():
    while True:
        yield

def adjacent_nodes(x: int, y: int, n_rows: int, row_length: int):
    neighbors = []
    if x - 1 >= 0:
        neighbors.append((x - 1, y))
    if x + 1 < n_rows:
        neighbors.append((x + 1, y))
    if y - 1 >= 0:
        neighbors.append((x, y - 1))
    if y + 1 < row_length:
        neighbors.append((x, y + 1))
    return neighbors


def dijkstra(grid: list[list]):
    n_rows = len(grid)
    row_length = len(grid[0])
    costs = {}
    unvisited = set()
    dest = (n_rows - 1, row_length - 1)

    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            node = (i, j)
            unvisited.add(node)
            costs[node] = val

    current_node = (0, 0)
    total_costs = {(0, 0): 0}
    for _ in tqdm(infinite_loop(),total=len(unvisited)):
        # print(current_node)
        for node in adjacent_nodes(*current_node, n_rows=n_rows, row_length=row_length):
            if node in unvisited:
                new_cost = total_costs[current_node] + costs[node]
                if node not in total_costs or total_costs[node] > new_cost:
                    total_costs[node] = new_cost
        unvisited.remove(current_node)
        next_candidates = {n: total_costs[n] for n in unvisited if n in total_costs}
        # print(unvisited)
        # print(next_candidates)
        if dest not in unvisited:
            answer = total_costs[dest]
            break
        if not next_candidates:
            answer = None
            break
        else:
            current_node = min(next_candidates.items(), key=lambda x: x[1])[0]
    return answer


with open(FILENAME) as f:
    starting_grid = [[int(x) for x in line.strip()] for line in f.readlines()]

# part one
print("Part One Solution: {}".format(dijkstra(starting_grid)))

# part two
def wraparound(n:int,added:int):
    if (new_val := n+added) <= 9:
        return new_val
    else:
        return new_val % 9

bigger_grid = []
for row in starting_grid:
    output_row = []
    for n in range(5):
        output_row.extend([wraparound(x,n) for x in row])
    bigger_grid.append(output_row)
addition_to_bigger = []
for n in range(4):
    for row in bigger_grid:
        addition_to_bigger.append([wraparound(x,n+1) for x in row])
bigger_grid.extend(addition_to_bigger)

print("Part Two Solution: {}".format(dijkstra(bigger_grid)))