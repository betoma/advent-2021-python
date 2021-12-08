CONTENTS = {
    0: {"a", "b", "c", "e", "f", "g"},
    1: {"c", "f"},
    2: {"a", "c", "d", "e", "g"},
    3: {"a", "c", "d", "f", "g"},
    4: {"b", "c", "d", "f"},
    5: {"a", "b", "d", "f", "g"},
    6: {"a", "b", "d", "e", "f", "g"},
    7: {"a", "c", "f"},
    8: {"a", "b", "c", "d", "e", "f", "g"},
    9: {"a", "b", "c", "d", "f", "g"},
}


def figure_out(signals: list[list[str]]):
    possibilities = {x: CONTENTS[8].copy() for x in CONTENTS[8]}
    lengths = {2: set(), 3: set(), 4: set(), 5: set(), 6: set(), 7: set()}
    for s in signals:
        lengths[len(s)].add(tuple(s))
    if lengths[2]:
        one_signals = set(lengths[2].pop())
        for item in CONTENTS[1]:
            possibilities[item] = possibilities[item].intersection(set(one_signals))
    if lengths[3]:
        seven_signals = set(lengths[3].pop())
        for item in CONTENTS[7]:
            possibilities[item] = possibilities[item].intersection(set(seven_signals))
    if lengths[4]:
        four_signals = set(lengths[4].pop())
        for item in CONTENTS[4]:
            possibilities[item] = possibilities[item].intersection(set(four_signals))
    for sequence in lengths[6]:
        for item in CONTENTS[8] - set(sequence):
            possibilities["a"].discard(item)
            possibilities["b"].discard(item)
            possibilities["f"].discard(item)
            possibilities["g"].discard(item)
    for sequence in lengths[5]:
        for item in CONTENTS[8] - set(sequence):
            possibilities["a"].discard(item)
            possibilities["d"].discard(item)
            possibilities["g"].discard(item)
    output = {}
    while len(output) < 7:
        taken = set()
        for letter, options in possibilities.items():
            if (num := len(options)) == 0:
                continue
            elif num == 1:
                assigned = options.pop()
                output[assigned] = letter
                taken.add(assigned)
        for letter in CONTENTS[8]:
            possibilities[letter] = possibilities[letter] - taken
    return output


with open("input.txt") as f:
    signals = [
        tuple([[list(y) for y in x.split()] for x in line.split("|")])
        for line in f.readlines()
    ]

one = 0
four = 0
seven = 0
eight = 0

result_numbers = []

for tests, output in signals:
    correspondences = figure_out(tests + output)
    digits = []
    for x in output:
        if (length := len(x)) == 2:
            digit = 1
            one += 1
        elif length == 4:
            digit = 4
            four += 1
        elif length == 3:
            digit = 7
            seven += 1
        elif length == 7:
            digit = 8
            eight += 1
        else:
            contents = set([correspondences[y] for y in x])
            if length == 5:
                if contents == CONTENTS[2]:
                    digit = 2
                elif contents == CONTENTS[3]:
                    digit = 3
                elif contents == CONTENTS[5]:
                    digit = 5
            elif length == 6:
                if contents == CONTENTS[0]:
                    digit = 0
                elif contents == CONTENTS[6]:
                    digit = 6
                elif contents == CONTENTS[9]:
                    digit = 9
        digits.append(digit)
    result_numbers.append(int("".join([str(x) for x in digits])))


print("Part One: {}".format(one + four + seven + eight))
print("Part Two: {}".format(sum(result_numbers)))
