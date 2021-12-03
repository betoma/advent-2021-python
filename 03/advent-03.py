from collections import Counter

with open("input.txt", "r") as f:
    data = [[x for x in y.strip()] for y in f.readlines()]

# part one
gamma = ""
epsilon = ""

for i, stuff in enumerate(zip(*data)):
    if len(stuff) > 1:
        freq = Counter(stuff).most_common()
        gamma += freq[0][0]
        epsilon += freq[-1][0]
    else:
        thing = stuff[0]
        gamma += thing
        if thing == "1":
            epsilon += "0"
        else:
            epsilon += "1"


print("Part One: {}".format(int(gamma, 2) * int(epsilon, 2)))


# part two
oxygen = data.copy()
co2 = data.copy()
o_halt = False
c_halt = False

for i in range(len(data[0])):
    if not o_halt:
        o_stuff = [x[i] for x in oxygen]
        if len(o_stuff) > 1:
            freq = Counter(o_stuff).most_common()
            if freq[0][1] == freq[-1][1]:
                o_thing = "1"
            else:
                o_thing = freq[0][0]
        else:
            o_thing = o_stuff[0]
        oxygen = [x for x in oxygen if x[i] == o_thing]
        if len(oxygen) == 1:
            o_halt = True
    if not c_halt:
        c_stuff = [x[i] for x in co2]
        if len(c_stuff) > 1:
            freq = Counter(c_stuff).most_common()
            if freq[0][1] == freq[-1][1]:
                c_thing = "0"
            else:
                c_thing = freq[-1][0]
        else:
            if c_stuff[0] == "1":
                c_thing = "0"
            else:
                c_thing = "1"
        co2 = [x for x in co2 if x[i] == c_thing]
        if len(co2) == 1:
            c_halt = True


print("Part Two: {}".format(int("".join(oxygen[0]), 2) * int("".join(co2[0]), 2)))
