with open("input.txt") as f:
    positions = [int(x) for x in f.read().split(",")]


# part one


def fuel_cost(crabs: list[int], location: int):
    return sum([abs(x - location) for x in crabs])


options = [fuel_cost(positions, n) for n in range(min(positions), max(positions) + 1)]

print(min(options))


# part two


def new_fuel_cost(crabs: list[int], location: int):
    return sum([sum(range(abs(x - location) + 1)) for x in crabs])


options = [
    new_fuel_cost(positions, n) for n in range(min(positions), max(positions) + 1)
]

print(min(options))
