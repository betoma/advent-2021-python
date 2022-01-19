import itertools
import json
from copy import deepcopy

class Node:
    def __init__(self,left=None,right=None,nestedness=0,parent=None,side=None):
        self.left = left
        self.right = right
        self.nested = nestedness
        self.parent = parent
        self.side = side

    @classmethod
    def from_list(cls,nested_list:list,n=0,parent=None,side=None):
        me = cls(nestedness=n,parent=parent,side=side)
        if len(nested_list) != 2:
            raise ValueError("List needs to be binary")
        if type(nested_list[0]) is list:
            me.left = cls.from_list(nested_list[0],n+1,me,"left")
        else:
            me.left = int(nested_list[0])
        if type(nested_list[1]) is list:
            me.right = cls.from_list(nested_list[1],n+1,me,"right")
        else:
            me.right = int(nested_list[1])
        return me

    def __repr__(self):
        return "Node_{}({},{})".format(self.nested,self.left,self.right)

    def __add__(self,other):
        if type(other) is not Node and type(other) is not int:
            raise TypeError("Nodes can only be added to ints or other nodes")
        self.dominated()
        if type(other) is Node:
            other.dominated()
        result = Node(self,other,self.nested-1)
        self.parent = result
        self.side = "left"
        if type(other) is Node:
            other.parent = result
            other.side = "right"
        return result.reduce()

    def dominated(self):
        if type(self.left) is Node:
            self.left.dominated()
        if type(self.right) is Node:
            self.right.dominated()
        self.nested += 1

    def magnitude(self):
        if type(self.left) is int:
            left_mag = self.left
        else:
            left_mag = self.left.magnitude()
        if type(self.right) is int:
            right_mag = self.right
        else:
            right_mag = self.right.magnitude()
        return 3*left_mag+2*right_mag

    def inorder(self):
        if type(self.left) is Node:
            yield from self.left.inorder()
        else:
            yield self.left, self.nested, self, "left"
        if type(self.right) is Node:
            yield from self.right.inorder()
        else:
            yield self.right, self.nested, self, "right"

    def reduce(self):
        no_explodes = False
        no_splits = False
        while not (no_explodes and no_splits):
            exploded = False
            previous_n = None
            explosion_gen = self.inorder()
            for number, nestedness, parent, side in explosion_gen:
                if nestedness - self.nested > 3 and type(parent.right) is int:
                    exploded = True
                    break
                previous_n = {"number": number, "parent": parent,"side":side}
            if exploded:
                if previous_n:
                    if previous_n["side"] == "left":
                        previous_n["parent"].left += parent.left
                    elif previous_n["side"] == "right":
                        previous_n["parent"].right += parent.left
                try:
                    next(explosion_gen)
                    go = next(explosion_gen)
                    next_n = {"number": go[0],"parent":go[2],"side":go[3]}
                    #print(next_n)
                except StopIteration:
                    #print("last n")
                    pass
                else:
                    if next_n["side"] == "left":
                        next_n["parent"].left += parent.right
                    elif next_n["side"] == "right":
                        next_n["parent"].right += parent.right
                if parent.side == "left":
                    parent.parent.left = 0
                elif parent.side == "right":
                    parent.parent.right = 0
                #print("Exploded! Tree is now {}".format(self))
                continue
            else:
                no_explodes = True
            split = False
            for number, nestedness, parent, side in self.inorder():
                if number >= 10:
                    split = True
                    new_node = Node(number//2,(-1*(-number//2)),nestedness+1,parent,side)
                    if side == "left":
                        parent.left = new_node
                    elif side == "right":
                        parent.right = new_node
                    break
            if split:
                #print("Split! Tree is now {}".format(self))
                continue
            else:
                no_splits = True
        return self

with open("input.txt") as f:
    content = f.readlines()

numbers = []
for line in content:
    numbers.append(Node.from_list(json.loads(line.strip())))

#part one
part_one_nums = deepcopy(numbers)
total = part_one_nums[0]
for n in part_one_nums[1:]:
    total += n
print(total.magnitude())

#part two
possible_pairs = itertools.permutations(numbers,2)
mags = [(deepcopy(x)+deepcopy(y)).magnitude() for x,y in possible_pairs]
print(max(mags))
