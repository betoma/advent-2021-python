class Board:
    def __init__(self):
        self.pattern = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        self.marked = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]

    def __repr__(self) -> str:
        return "Board({})".format(
            "\n".join([" ".join([str(y) for y in x]) for x in self.pattern])
        )

    @classmethod
    def create_board(cls, lines: list[str]):
        board = cls()
        if len(lines) != 5:
            raise ValueError("Bingo board must be 5x5")
        for i, line in enumerate(lines):
            numbers = [int(x) for x in line.split()]
            board.pattern[i] = numbers
        return board

    def mark_square(self, n: int):
        for i, row in enumerate(self.pattern):
            for j, m in enumerate(row):
                if m == n:
                    self.marked[i][j] = 1

    def is_bingo(self):
        for row in self.marked:
            if all(row):
                return True
        for i in range(5):
            if all([x[i] for x in self.marked]):
                return True
        return False

    def score(self, n: int):
        unmarked = [
            y
            for i, x in enumerate(self.pattern)
            for j, y in enumerate(x)
            if not self.marked[i][j]
        ]
        return sum(unmarked) * n


def play_bingo(boards: list[Board], calls: list[int]):
    bingos = {}
    for n in calls:
        # print(n)
        for i, b in enumerate(boards):
            if i not in bingos:
                b.mark_square(n)
                if b.is_bingo():
                    bingos[i] = b.score(n)
                    print("Bingo! Board #{}: {} Points".format(i, bingos[i]))
        yield (bingos)
        if len(bingos) >= len(boards):
            break


boards = []

with open("input.txt", "r") as f:
    content = f.readlines()

calls = [int(i) for i in content[0].split(",")]

this_board = []
for line in content[2:]:
    if not (numbers := line.strip()):
        boards.append(Board.create_board(this_board))
        this_board = []
    else:
        this_board.append(numbers)
boards.append(Board.create_board(this_board))

for round in play_bingo(boards, calls):
    pass
