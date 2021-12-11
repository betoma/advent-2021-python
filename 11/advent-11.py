import itertools


with open("input.txt") as f:
    cave = [[int(y) for y in x.strip()] for x in f.readlines()]


def adjacent(x: int, y: int):
    x_options = [x]
    y_options = [y]
    if x > 0:
        x_options.append(x - 1)
    if x < 9:
        x_options.append(x + 1)
    if y > 0:
        y_options.append(y - 1)
    if y < 9:
        y_options.append(y + 1)
    return itertools.product(x_options, y_options)


def flashes(cave: list[list[int]], rounds: int = None):
    n_flashes = 0
    yield n_flashes, cave
    all_octos = set([x for x in itertools.product(range(10), range(10))])
    if not rounds:
        rounds = 10000
    for r in range(rounds):
        flashers = []
        new_flashers = []
        cave = [[x + 1 for x in row] for row in cave]
        for i, row in enumerate(cave):
            for j, octopus in enumerate(row):
                if octopus > 9:
                    new_flashers.append((i, j))
        while new_flashers:
            ultraneu = set()
            for x, y in new_flashers:
                cave[x][y] = 0
                for i, j in adjacent(x, y):
                    if (
                        (i, j) not in new_flashers
                        and (i, j) not in flashers
                        and (i, j) not in ultraneu
                    ):
                        cave[i][j] += 1
                        if cave[i][j] > 9:
                            ultraneu.add((i, j))
            flashers.extend(new_flashers)
            new_flashers = list(ultraneu)
        n_flashes += len(flashers)
        if set(flashers) == all_octos:
            print(f"Simultaneous flash! Round: {r+1}")
            break
        yield n_flashes, cave


# part one

for number, _ in flashes(cave, 100):
    pass

print(number)


# part two

for _ in flashes(cave):
    pass
