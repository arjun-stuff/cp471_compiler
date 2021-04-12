# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 20:01:13 2021

@author: Arjun
"""

from lexer import *
from symbols import *
from inter import *
from parse import *
from tree import *


print("------------------------Intermediate Code------------------------")
filename = "C:/Users/Arjun/Desktop/Arjun Files/School/Fifth Year/Compiling/Compiler/Test Case 3.txt"
file = open(filename)
lex = Lexer(file)
parse = Parser(lex)
parse.program()

with open("Intermediate Code.txt", "w", encoding="utf-8") as file:
    file.write(Node.intermediate_code)

print("\n")
print("------------------------Lexer Tokens------------------------")
parse.output_token_stream()

print("\n")
print("------------------------Parse Productions------------------------")
tree = Tree(None, None, None, "Program")
x = tree.create_branch(parse.parse_tree[0])
y = tree.create_branch(parse.parse_tree[1])
tree.branch1 = x
tree.branch2 = y

levels = tree.generate_level(tree)

tree.print_levels(levels,0)

print("\n")
print("------------------------Symbol Table------------------------")
print(parse.top.table)
print("\nExpanded\n")
for key in parse.top.table.keys():
    print(key.tag, ":", parse.top.table[key], ":", parse.top.table[key].type)






