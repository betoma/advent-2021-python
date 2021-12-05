from collections import Counter


class Vent:
    def __init__(self, start: tuple[int], stop: tuple[int]):
        if start[0] == stop[0]:
            self.horivert = True
            if start[1] < stop[1]:
                downward = start[1]
                upward = stop[1]
            else:
                downward = stop[1]
                upward = start[1]
            self.contents = [(start[0], x) for x in range(downward, upward + 1)]
        elif start[1] == stop[1]:
            self.horivert = True
            if start[0] < stop[0]:
                leftward = start[0]
                rightward = stop[0]
            else:
                leftward = stop[0]
                rightward = start[0]
            self.contents = [(x, start[1]) for x in range(leftward, rightward + 1)]
        else:
            self.horivert = False
            if start[0] < stop[0]:
                leftward = start[0]
                rightward = stop[0]
                ltr = True
            else:
                leftward = stop[0]
                rightward = start[0]
                ltr = False
            if start[1] < stop[1]:
                downward = start[1]
                upward = stop[1]
                btt = True
            else:
                downward = stop[1]
                upward = start[1]
                btt = False
            x_list = (
                [x for x in range(leftward, rightward + 1)]
                if ltr
                else [x for x in range(leftward, rightward + 1)][::-1]
            )
            y_list = (
                [x for x in range(downward, upward + 1)]
                if btt
                else [x for x in range(downward, upward + 1)][::-1]
            )
            self.contents = list(zip(x_list, y_list))

    def __repr__(self):
        return f"Vent({self.contents})"

    def __contains__(self, item):
        return item in self.contents


with open("input.txt", "r") as f:
    vents = [
        Vent(*[tuple([int(y) for y in x.strip().split(",")]) for x in line.split("->")])
        for line in f.readlines()
    ]

# part one

map = Counter()

for v in vents:
    if v.horivert:
        map.update(v.contents)

print(len([x for x in map.most_common() if x[1] > 1]))

# part two

map = Counter()

for v in vents:
    map.update(v.contents)

print(len([x for x in map.most_common() if x[1] > 1]))
