from collections import Counter
from tqdm import tqdm

with open("test.txt") as f:
    lines = f.readlines()
    template = lines[0].strip()
    rules = [tuple(x.strip().split(" -> ")) for x in lines[1:] if x != "\n"]

insertion = {(x[0], x[1]): y for x, y in rules}
pair_match = {x[0]: set() for x, _ in rules}
for x, y in insertion:
    pair_match[x].add(y)


def naive_polymerization(template: str, steps: int):
    polymer = template
    yield polymer
    for _ in range(steps):
        final = len(polymer) - 1
        new_polymer = []
        for i, char in enumerate(polymer):
            new_polymer.append(char)
            if i < final and char in pair_match:
                if (next := polymer[i + 1]) in pair_match[char]:
                    new_polymer.append(insertion[(char, next)])
        polymer = "".join(new_polymer)
        yield polymer


# part one

for p in naive_polymerization(template, 10):
    pass

ranks = Counter(p).most_common()
print(ranks[0][1] - ranks[-1][1])
