from collections import Counter


def simulate_population(pop_list: list[int], days: int):
    population = Counter(pop_list)
    new_fish = Counter()
    yield population, new_fish
    for d in range(days):
        today = d % 7
        if (new_day := d - 9) in new_fish:
            population[today] += new_fish[new_day]
            new_fish[new_day] = 0
        if today in population:
            new_fish[d] = population[today]
        yield population, new_fish


with open("input.txt") as f:
    population = [int(n) for n in f.read().split(",")]


# part one

for pop, new in simulate_population(population, 80):
    pass

print("Part One: {}".format(sum(pop.values()) + sum(new.values())))


# part two


for pop, new in simulate_population(population, 256):
    pass

print("Part Two: {}".format(sum(pop.values()) + sum(new.values())))
