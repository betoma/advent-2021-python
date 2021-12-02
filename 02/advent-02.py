with open("input.txt") as f:
    data = [tuple(line.split()) for line in f.readlines()]

# part one

position = 0
depth = 0

for x, y in data:
    n = int(y)
    if x == "forward":
        position += n
    elif x == "down":
        depth += n
    elif x == "up":
        depth -= n
    else:
        raise ValueError("Something's borked")

print(position * depth)

# part two

position = 0
depth = 0
aim = 0

for x, y in data:
    n = int(y)
    if x == "forward":
        position += n
        depth += aim * n
    elif x == "down":
        aim += n
    elif x == "up":
        aim -= n
    else:
        raise ValueError("Something's borked")

print(position * depth)
