from collections import Counter, defaultdict

with open("input.txt") as f:
    lines = f.readlines()
    template = lines[0].strip()
    rules = [tuple(x.strip().split(" -> ")) for x in lines[1:] if x != "\n"]

insertion = {(x[0], x[1]): y for x, y in rules}


def polymerization(n: int):
    letter_counts = Counter(template)
    polymer = Counter([(char, template[i + 1]) for i, char in enumerate(template[:-1])])
    yield polymer, letter_counts
    for _ in range(n):
        subtractions = Counter()
        additions = Counter()
        for pair in insertion:
            if polymer[pair]:
                subtractions[pair] += polymer[pair]
                first_pair = (pair[0], insertion[pair])
                additions[first_pair] += polymer[pair]
                second_pair = (insertion[pair], pair[1])
                additions[second_pair] += polymer[pair]
                letter_counts[insertion[pair]] += polymer[pair]
        polymer.update(additions)
        polymer.subtract(subtractions)
        yield polymer, letter_counts


# part one

for p, l in polymerization(10):
    pass

ranks = l.most_common()
print(ranks[0][1] - ranks[-1][1])


# part two

for p, l in polymerization(40):
    pass

ranks = l.most_common()
print(ranks[0][1] - ranks[-1][1])
