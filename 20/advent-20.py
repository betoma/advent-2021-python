from collections import Counter
from tqdm import trange

class Image:
    def __init__(self, grid:list[list[str]], infinite_field:str="."):
        self.grid = []
        self.n_cols = len(grid[0]) + 2
        self.grid.append([infinite_field for _ in range(self.n_cols)])
        for row in grid:
            g_row = []
            g_row.append(infinite_field)
            g_row.extend(row)
            g_row.append(infinite_field)
            self.grid.append(g_row)
        self.grid.append([infinite_field for _ in range(self.n_cols)])
        self.n_rows = len(self.grid)
        self.n_lights = Counter([x for y in self.grid for x in y])["#"]
        self.background = infinite_field
    
    def __repr__(self) -> str:
        return f"Image({self.n_lights, self.n_rows, self.n_cols})"
    
    def __str__(self) -> str:
        return "\n".join(["".join(x) for x in self.grid])
    
    def gen_no(self, x:int, y:int) -> int:
        bin_str = []
        x_less = x-1 < 0
        x_more = x+1 >= self.n_rows
        y_less = y-1 < 0
        y_more = y+1 >= self.n_cols
        if x_less:
            bin_str.extend([self.background for _ in range(3)])
        else:
            if y_less:
                bin_str.append(self.background)
            else:
                bin_str.append(self.grid[x-1][y-1])
            bin_str.append(self.grid[x-1][y])
            if y_more:
                bin_str.append(self.background)
            else:
                bin_str.append(self.grid[x-1][y+1])
        if y_less:
            bin_str.append(self.background)
        else:
            bin_str.append(self.grid[x][y-1])
        bin_str.append(self.grid[x][y])
        if y_more:
            bin_str.append(self.background)
        else:
            bin_str.append(self.grid[x][y+1])
        if x_more:
            bin_str.extend([self.background for _ in range(3)])
        else:
            if y_less:
                bin_str.append(self.background)
            else:
                bin_str.append(self.grid[x+1][y-1])
            bin_str.append(self.grid[x+1][y])
            if y_more:
                bin_str.append(self.background)
            else:
                bin_str.append(self.grid[x+1][y+1])
        return int("".join(["0" if x=="." else "1" for x in bin_str]),2)

    def enhance(self, algorithm:list[str]):
        new_grid = []
        for row in range(self.n_rows):
            new_row = []
            for col in range(self.n_cols):
                new_row.append(algorithm[self.gen_no(row, col)])
            new_grid.append(new_row)
        if self.background == ".":
            new_background = algorithm[0]
        elif self.background == "#":
            new_background = algorithm[511]
        return type(self)(new_grid, infinite_field=new_background)



with open("input.txt") as f:
    content = f.readlines()

algorithm = list(content[0].strip())

# part one
pic = Image([list(x.strip()) for x in content[2:]])
for i in range(2):
    pic = pic.enhance(algorithm)
print(f"Part One: {pic.n_lights}")

# part two
pic = Image([list(x.strip()) for x in content[2:]])
for i in trange(50):
    pic = pic.enhance(algorithm)
print(f"Part Two: {pic.n_lights}")