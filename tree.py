# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 15:07:35 2021

@author: Arjun
"""

from lexer import *
from symbols import *
from inter import *
from parse import *

class Tree:
    
    def __init__(self, branch1, branch2, branch3, name):
        
        self.branch1 = branch1
        self.branch2 = branch2
        self.branch3 = branch3
        self.value = None
        self.name = name
        
           
    def create_branch(self, branch):
        
        if type(branch) == list:
            
            branches = []
            for x in branch:
                branches.append(self.create_branch(x))
            top_branch = Tree(branches[0], None, None, "Decls")
            
            
            if len(branches) > 1:
                cur_branch = top_branch
                for x in range(1, len(branches)):
                    cur_branch.branch3 = branches[x]
                    cur_branch = cur_branch.branch3
                
            return top_branch           
            
        
        if type(branch) == Seq:
            
            sub_branch1 = self.create_branch(branch.stmt1)
            sub_branch2 = self.create_branch(branch.stmt2)
            
            new_branch = Tree(sub_branch1, sub_branch2, None, "Seq")
            return new_branch
        
        elif type(branch) == Cond:
            
            sub_branch1 = self.create_branch(branch.expr)
            sub_branch2 = self.create_branch(branch.stmt)
            
            new_branch = Tree(sub_branch1, sub_branch2, None, "Cond")
            return new_branch
        
        elif type(branch ) == Else:
            
            sub_branch1 = self.create_branch(branch.expr)
            sub_branch2 = self.create_branch(branch.stmt1)
            sub_branch3 = self.create_branch(branch.stmt2)
            
            new_branch = Tree(sub_branch1, sub_branch2, sub_branch3, "Else")
            return new_branch
            
        elif type(branch ) == Loop:
            
            sub_branch1 = self.create_branch(branch.expr)
            sub_branch2 = self.create_branch(branch.stmt)
            
            new_branch = Tree(sub_branch1, sub_branch2, None, "Loop")
            return new_branch
        
        elif type(branch) == Set:
            
            sub_branch1 = self.create_branch(branch.id)
            sub_branch2 = self.create_branch(branch.expr)
            
            new_branch = Tree(sub_branch1, sub_branch2, None, "Set")
            return new_branch
            
        elif type(branch) == Expr:
            
            new_branch == Tree(None, None, None, "Expr")
            new_branch.value = str(branch)
            return new_branch
        
        elif type(branch) == Id:
            
            new_branch = Tree(None, None, None, "Id")
            new_branch.value = str(branch)
            return new_branch
        
        elif type(branch) == Arith:
            
            sub_branch1 = self.create_branch(branch.expr1)
            sub_branch2 = self.create_branch(branch.op)
            sub_branch3 = self.create_branch(branch.expr2)
            
            new_branch = Tree(sub_branch1, sub_branch2, sub_branch3, "Arith")
            return new_branch
        
        elif type(branch) == Op:
            
            new_branch = Tree(None, None, None, "Op")
            new_branch.value = str(branch)
            return new_branch
        
        elif type(branch) == Unary:
            
            sub_branch1 = self.create_branch(branch.op)
            sub_branch2 = self.create_branch(branch.expr)
            
            new_branch = Tree(sub_branch1, sub_branch2, None, "Unary")
            return new_branch
        
        elif type(branch) == Constant:
            
            new_branch = Tree(None, None, None, "Constant")
            new_branch.value = str(branch.op)
            return new_branch
        
        elif type(branch) == Logical:
            
            sub_branch1 = self.create_branch(branch.expr1)
            sub_branch2 = self.create_branch(branch.op)
            sub_branch3 = self.create_branch(branch.expr2)
            
            new_branch = Tree(sub_branch1, sub_branch2, sub_branch3, "Logical")
            return new_branch
        
        elif type(branch) == Or:
            
            sub_branch1 = self.create_branch(branch.expr1)
            sub_branch2 = self.create_branch(branch.op)
            sub_branch3 = self.create_branch(branch.expr2)
            
            new_branch = Tree(sub_branch1, sub_branch2, sub_branch3, "Or")
            return new_branch
        
        elif type(branch) == And:
            
            sub_branch1 = self.create_branch(branch.expr1)
            sub_branch2 = self.create_branch(branch.op)
            sub_branch3 = self.create_branch(branch.expr2)
            
            new_branch = Tree(sub_branch1, sub_branch2, sub_branch3, "And")
            return new_branch
        
        elif type(branch) == Not:
            
            sub_branch1 = self.create_branch(branch.op)
            sub_branch2 = self.create_branch(branch.expr1)
            
            new_branch = Tree(sub_branch1, sub_branch2, None, "Not")
            return new_branch
        
        elif type(branch) == Rel:
            
            sub_branch1 = self.create_branch(branch.expr1)
            sub_branch2 = self.create_branch(branch.op)
            sub_branch3 = self.create_branch(branch.expr2)
            
            new_branch = Tree(sub_branch1, sub_branch2, sub_branch3, "Rel")
            return new_branch
        
        elif type(branch) == Stmt:
            
            new_branch = Tree(None, None, None, "Stmt")
            return new_branch
        
        else:
            
            new_branch = Tree(None, None, None, str(branch))
            return new_branch
        
           
    def generate_level(self, branch):
        
        if branch is None:
            return None
        elif branch.value is not None:
            return [branch.name, branch.value]
        else:
            level1 = self.generate_level(branch.branch1)
            level2 = self.generate_level(branch.branch2)
            level3 = self.generate_level(branch.branch3)
            
            return_val = [branch.name, []]
            
            if level1 is not None:
                return_val[1].append(level1)
            if level2 is not None:
                return_val[1].append(level2)
            if level3 is not None:
                return_val[1].append(level3)
            
            if len(return_val[1]) == 0:
                return[branch.name]
            
            return return_val
        
    def print_levels(self, level, indents):
        
        if level is None:
            return
        elif len(level) == 1:
            print("\t"*indents, level[0])
        elif isinstance(level[1], list):
            print("\t"*indents, level[0])
            for x in level[1]:
                self.print_levels(x, indents+1)
        else:
            print("\t"*indents, level[0], level[1])
            
        
        
        
        
            
        