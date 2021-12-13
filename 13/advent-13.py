class TransparentPaper:
    def __init__(self, dots: list[tuple]):
        self.dots = set(dots)

    def __repr__(self):
        return f"TransparentPaper({self.dots})"

    def __str__(self):
        max_x = max([x[0] for x in self.dots])
        max_y = max([x[1] for x in self.dots])
        dot_matrix = []
        for y in range(max_y + 1):
            row = []
            for x in range(max_x + 1):
                if (x, y) in self.dots:
                    row.append("#")
                else:
                    row.append(".")
            dot_matrix.append(row)
        return "\n".join(["".join(row) for row in dot_matrix])

    def fold(self, axis: str, n: int):
        if axis == "x":
            moved_dots = [x for x in self.dots if x[0] > n]
            new_dots = [(n - (x - n), y) for x, y in moved_dots]
        elif axis == "y":
            moved_dots = [x for x in self.dots if x[1] > n]
            new_dots = [(x, n - (y - n)) for x, y in moved_dots]
        for dot in moved_dots:
            self.dots.remove(dot)
        self.dots.update(new_dots)


dots = []
folds = []

with open("input.txt") as f:
    for line in f.readlines():
        if line.startswith("fold"):
            rel = line.strip().split(" ")[-1].split("=")
            folds.append((rel[0], int(rel[1])))
        elif line == "\n":
            continue
        else:
            dots.append(tuple([int(x) for x in line.strip().split(",")]))

paper = TransparentPaper(dots)

# part one

paper.fold(*folds[0])
print(len(paper.dots))

# part two
for f in folds[1:]:
    paper.fold(*f)
print(paper)
