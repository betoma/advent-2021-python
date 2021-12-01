with open("input.txt", "r") as f:
    depths = [int(x.strip()) for x in f.readlines()]

# part one

increasing = 0
previous_n = None
for n in depths:
    if previous_n:
        if n > previous_n:
            increasing += 1
    previous_n = n

print(increasing)


# part two

last_depth = len(depths) - 2

increasing = 0
previous_sum = None
for i in range(last_depth):
    current_sum = sum(depths[i : i + 3])
    if previous_sum:
        if current_sum > previous_sum:
            increasing += 1
    previous_sum = current_sum

print(increasing)
