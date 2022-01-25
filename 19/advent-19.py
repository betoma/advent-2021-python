import itertools
from collections import Counter

from black import re

class Scanner:
    def __init__(self, points: list[tuple[int]]):
        self.points = points

    def __repr__(self):
        return f"Scanner({self.points})"

    @classmethod
    def from_file(cls, filename: str):
        with open(filename) as f:
            content = f.readlines()
        scanners = []
        for line in content:
            if line.startswith("---"):
                points_list = []
            elif line == "\n":
                scanners.append(cls(points_list))
            else:
                points_list.append(tuple([int(x) for x in line.strip().split(",")]))
        scanners.append(cls(points_list))
        return scanners

    def orientations(self):
        versions = []
        versions.append(self)
        point_variations = [
            [(x,-z,y) for x,y,z in self.points],
            [(x,-y,-z) for x,y,z in self.points],
            [(x,z,-y) for x,y,z in self.points],
            [(-x,-y,z) for x,y,z in self.points],
            [(-x,z,y) for x,y,z in self.points],
            [(-x,y,-z) for x,y,z in self.points],
            [(-x,-z,-y) for x,y,z in self.points],
            [(y,z,x) for x,y,z in self.points],
            [(y,-x,z) for x,y,z in self.points],
            [(y,-z,-x) for x,y,z in self.points],
            [(y,x,-z) for x,y,z in self.points],
            [(-y,-z,x) for x,y,z in self.points],
            [(-y,x,z) for x,y,z in self.points],
            [(-y,z,-x) for x,y,z in self.points],
            [(-y,-x,-z) for x,y,z in self.points],
            [(z,x,y) for x,y,z in self.points],
            [(z,-y,x) for x,y,z in self.points],
            [(z,-x,-y) for x,y,z in self.points],
            [(z,y,-x) for x,y,z in self.points],
            [(-z,-x,y) for x,y,z in self.points],
            [(-z,y,x) for x,y,z in self.points],
            [(-z,x,-y) for x,y,z in self.points],
            [(-z,-y,-x) for x,y,z in self.points],
        ]
        versions.extend([type(self)(x) for x in point_variations])
        for v in versions:
            yield v

    def differences(self, other):
        the_x = Counter([x-y for x,y in itertools.product([x for x,_,_ in self.points],[x for x,_,_ in other.points])])
        x_diff, x_freq = the_x.most_common(1)[0]
        if x_freq >= 12:
            the_y = Counter([x-y for x,y in itertools.product([y for _,y,_ in self.points],[y for _,y,_ in other.points])])
            y_diff, y_freq = the_y.most_common(1)[0]
            if y_freq >= 12:
                the_z = Counter([x-y for x,y in itertools.product([z for _,_,z in self.points],[z for _,_,z in other.points])])
                z_diff, z_freq = the_z.most_common(1)[0]
                if z_freq >= 12:
                    return x_diff, y_diff, z_diff
                else:
                    return
            else:
                return
        else:
            return
        
    def adjusted(self, x_diff:int,y_diff:int,z_diff:int):
        new_points = [(x+x_diff,y+y_diff,z+z_diff) for x,y,z in self.points]
        return type(self)(new_points)

scanner_list = Scanner.from_file("input.txt")
scanned = {i: False for i,_ in enumerate(scanner_list)}
reoriented_list = [(scanner_list[0],(0,0,0))]
scanned[0] = True

while len(reoriented_list) < len(scanner_list):
    gonna_add = []
    for baseline, offset in reoriented_list:
        for i, scanbro in enumerate(scanner_list):
            if scanned[i]:
                continue
            for v in scanbro.orientations():
                if (skew := baseline.differences(v)):
                    gonna_add.append((v.adjusted(*skew),skew))
                    scanned[i] = True
                    break
    reoriented_list.extend(gonna_add)

# part one

all_points = set()
for x,_ in reoriented_list:
    all_points.update(x.points)

print(len(all_points))

# part two
def Manhattan(x,y):
    sum = 0
    for i in range(len(x)):
        sum += abs(x[i]-y[i])
    return sum

print(max([Manhattan(x,y) for x,y in itertools.combinations([x for _,x in reoriented_list],2)]))