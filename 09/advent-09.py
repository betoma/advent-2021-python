from math import prod


class HeightMap:
    def __init__(self, numbers: list[list[int]]):
        self.rows = numbers
        self.column_length = len(self.rows)
        self.row_length = len(self.rows[0])

    @classmethod
    def fromfile(cls, filename):
        with open(filename) as f:
            contents = [[int(n) for n in line.strip()] for line in f.readlines()]
        return cls(contents)

    def adjacent_points(self, i, j):
        points = []
        if i > 0:
            points.append((i - 1, j))
        if (further := i + 1) < self.column_length:
            points.append((further, j))
        if j > 0:
            points.append((i, j - 1))
        if (farther := j + 1) < self.row_length:
            points.append((i, farther))
        return points

    def low_points(self):
        low_points = []
        for i in range(self.column_length):
            for j in range(self.row_length):
                if all(
                    [
                        self.rows[i][j] < self.rows[x][y]
                        for x, y in self.adjacent_points(i, j)
                    ]
                ):
                    low_points.append((i, j))
        return low_points

    def risk_level(self):
        return sum([self.rows[x][y] + 1 for x, y in self.low_points()])

    def get_basin(self, x, y, overbasin: set = set()):
        basin = set()
        basin.add((x, y))
        basin_points = [
            (i, j)
            for i, j in self.adjacent_points(x, y)
            if self.rows[i][j] != 9 and (i, j) not in overbasin
        ]
        for i, j in basin_points:
            basin.update(self.get_basin(i, j, basin | overbasin))
        return basin

    def all_basins(self):
        return sorted(
            [len(self.get_basin(x, y)) for x, y in self.low_points()], reverse=True
        )


pointmap = HeightMap.fromfile("input.txt")

# part one
print("Part One: {}".format(pointmap.risk_level()))

# part two
print("Part Two: {}".format(prod(pointmap.all_basins()[:3])))
