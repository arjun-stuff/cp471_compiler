# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 15:07:37 2021

@author: Arjun
"""

from lexer import *
from symbols import *
from inter import *
from parse import *
from tree import *
from generator import *
import sys

filename = sys.argv[1]
file = open(filename)
lex = Lexer(file)
parse = Parser(lex)
parse.program()
generator = CodeGenerator(Node.intermediate_code)
generator.evaluate()
generator.compile_code()
file.close()
print("Compilation Successful")
