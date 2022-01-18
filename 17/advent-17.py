import itertools
import math

from tqdm import tqdm


class OceanTrench:
    def __init__(self, x_range: tuple[int], y_range: tuple[int]):
        self.x_coords = list(range(*x_range))
        self.y_coords = list(range(*y_range))

    @classmethod
    def from_file(cls, filename):
        with open(filename) as f:
            content = f.read()
        linesplit = content.split()
        x_range = [int(x) for x in linesplit[2].lstrip("x=").rstrip(",").split("..")]
        y_range = [int(x) for x in linesplit[3].lstrip("y=").rstrip(",").split("..")]
        x_range[1] += 1
        y_range[1] += 1
        return cls(tuple(x_range), tuple(y_range))

    def n_hits(self, run: int):
        output = 0
        candidate_trajectories = [
            Trajectory(*x) for x in itertools.product(range(run), range(-run, run))
        ]
        for traj in tqdm(candidate_trajectories):
            if any([traj.hits(self.x_coords, y) for y in self.y_coords]):
                output += 1
        return output


class Trajectory:
    def __init__(self, x_vel: int, y_vel: int):
        self.x_vel = x_vel
        self.y_vel = y_vel

    def x_pos(self, t: int):
        if t > (last_x := abs(self.x_vel)):
            return self.x_pos(last_x)
        elif self.x_vel > 0:
            return ((2 * self.x_vel * t) - (t ** 2) + t) / 2
        elif self.x_vel < 0:
            return ((2 * self.x_vel * t) + (t ** 2) - t) / 2
        else:
            return 0

    def y_pos(self, t: int):
        return ((2 * self.y_vel * t) - (t ** 2) + t) / 2

    def y_func(self, y: int):
        answers = []
        inner_power = ((1 + 2 * self.y_vel) ** 2) - 8 * y
        if inner_power >= 0:
            pos = (-(2 * self.y_vel) - 1 + math.sqrt(inner_power)) / -2
            neg = (-(2 * self.y_vel) - 1 - math.sqrt(inner_power)) / -2
            if pos > 0:
                answers.append(pos)
            if neg > 0:
                answers.append(neg)
        return answers

    def hits(self, x: list[int], y: int):
        if y_intersections := [n for n in self.y_func(y) if n % 1 == 0]:
            xes = [int(self.x_pos(n)) for n in y_intersections]
            if any([n in x for n in xes]):
                return True
            else:
                return False
        else:
            return False


target = OceanTrench.from_file("input.txt")

# part one
n = -min(target.y_coords) - 1
print("Part One: {}".format(int(n * (n + 1) / 2)))

# part two
print(target.n_hits(500))
