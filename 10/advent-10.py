from collections import deque

with open("input.txt") as f:
    chunks = [[x for x in line.strip()] for line in f.readlines()]

PAIRS = {"(": ")", "{": "}", "[": "]", "<": ">"}
SCORES = {")": 3, "]": 57, "}": 1197, ">": 25137}


def autocomplete_score(string: list[str]):
    VALUES = {")": 1, "]": 2, "}": 3, ">": 4}
    total_score = 0
    for char in string:
        total_score *= 5
        total_score += VALUES[char]
    return total_score


illegal_characters = []
autocompletes = []

for c in chunks:
    corrupt = False
    stack = deque()
    for character in c:
        if character in PAIRS:
            stack.append(character)
        else:
            opening_char = stack.pop()
            if character != PAIRS[opening_char]:
                illegal_characters.append(character)
                corrupt = True
                break
    if not corrupt:
        completion_string = []
        while stack:
            completion_string.append(PAIRS[stack.pop()])
        autocompletes.append(completion_string)

# part one

print("Part One: {}".format(sum([SCORES[x] for x in illegal_characters])))

# part two

print(
    "Part Two: {}".format(
        sorted([autocomplete_score(x) for x in autocompletes])[
            (len(autocompletes) - 1) // 2
        ]
    )
)
