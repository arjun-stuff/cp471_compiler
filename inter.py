# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 16:14:23 2021

@author: Arjun
"""

from lexer import *
from symbols import *

class Node:
    
    lexline = 0
    labels = 0
    
    def __init__(self):
        self.lexline = lexer.line
        
    def error(self, s):
        
        raise RuntimeError("near line "+str(self.lexline) + ": " + s)
        
    def newlabel(self):
        Node.labels += 1
        return Node.labels
    
    def emitlabel(self, i):
        
        #print("Node emitlabel. i =", i, )
        
        print("L" + str(i) + ":", end="")
        
    def emit(self, s):
        #print("Node emit. s =", s)
        print("\t" + s)
        
class Expr(Node):
    
    def __init__(self, tok, p):
        self.op = tok
        self.type = p
        
    def gen(self):
        return self
    
    def reduce(self):
        return self
    
    def jumping(self, t, f):
        
        #print("Expr jumping. t=", t, "f=", f)
        
        self.emitjumps(str(self), t, f)
        
    def emitjumps(self, test, t, f):
        
        #print("Expr emitjumps. test=", test, "t=", t, "f=", f)      
        
        if (t != 0 and f != 0):
            
            self.emit("if " + test + " goto L" + str(t))
            self.emit("goto L" + str(f))
            
        elif t != 0:
            self.emit("if "+ test + " goto L" + str(t))
        
        elif f != 0:
            self.emit("iffalse " + test + " goto L" + str(f))
        else:
            pass
        
    def __str__(self):
        return str(self.op)
    
class Id(Expr):
    
    def __init__(self, id_, p, b):
        super().__init__(id_, p)
        self.offset = b
        
class Op(Expr):
    
    def __init__(self, tok, p):
        super().__init__(tok, p)
        
    def reduce(self):
        x = self.gen()
        t = Temp(self.type)     
        
        #print("Op reduce. x=", x, "t=", t)
        
        self.emit(str(t) + " = " + str(x))
        return t
    
class Arith(Op):
    
    def __init__(self, tok, x1, x2):
        super().__init__(tok, None)
        self.expr1 = x1
        self.expr2 = x2
        self.type = Type.max(self.expr1.type, self.expr2.type)
        if (self.type is None):
            self.error("Type Error")
            
    def gen(self):
        
        #print("Arith gen. expr1.reduce=", self.expr1.reduce(), "expr2.reduce = ",
        #      self.expr2.reduce())
        
        return Arith(self.op, self.expr1.reduce(), self.expr2.reduce())
    
    def __str__(self):
        return str(self.expr1) + " " + str(self.op) + " " + str(self.expr2)
    
class Temp(Expr):
    
    count = 0
    number = 0
    
    def __init__(self, p):
        super().__init__(Word("t", Tag.TEMP), p)
        Temp.count += 1
        Temp.number = Temp.count
    
    def __str__(self):
        return "t" + str(Temp.number)
    
class Unary(Op):
    
    def __init__(self, tok, x):
        super().__init__(tok, None)
        self.expr = x
        self.type = Type.max(Type("int", Tag.TYPE, 4), self.expr.type)
        if self.type is None:
            self.error("Type Error")
            
    def gen(self):
        
        #print("Unary Op. expr.reduce=", self.expr.reduce())
        
        return Unary(self.op, self.expr.reduce())
    
    def __str__(self):
        return str(self.op) + " " + str(self.expr)
    
class Constant(Expr):
    
    def __init__(self, tok=None, p = None, i = None):
        
        if i is None:
            super().__init__(tok, p)
        else:
            super().__init__(Int(i), Type("int", Tag.INT, 4))
            
    def jumping(self, t, f):
        
        #print("Constant jumping. t=", t, "f=", f)
        
        if (self == Constant(Word("True", Tag.TRUE), Type("boo", Tag.TYPE, 1)) and t != 0):
            self.emit("goto L" + str(t))
        elif (self == Constant(Word("False", Tag.FALSE), Type("boo", Tag.TYPE, 1)) and f != 0):
            self.emit("goto L" + str(f))
            
class Logical(Expr):
    
    def __init__(self, tok, x1, x2):
        super().__init__(tok, None)
        self.expr1 = x1
        self.expr2 = x2
        self.type = self.check(self.expr1.type, self.expr2.type)
        
        if (self.type is None):
            self.error("Type Error")
            
    def check(self, p1, p2):
                
        if (p1.lexeme == "boo" and p2.lexeme == "boo"):
            return Type("boo", Tag.TYPE, 1)
        else:
            return None
        
    def gen(self):
        
        f = self.newlabel()
        a = self.newlabel()
        
        #print("Logical gen")
        
        temp = Temp(self.type)
        self.jumping(0, f)
        self.emit(str(temp) + " = True")
        self.emit("goto L" + str(a))
        self.emitlabel(f)
        self.emit(str(temp) + " = False")
        self.emitlabel(a)
        return temp
    
    def __str__(self):
        return str(self.expr1) + " " + str(self.op) + " " + str(self.expr2)
        
        
class Or(Logical):
    
    def __init__(self, tok, x1, x2):
        
        #print(x1)
        #print(x2)
        
        super().__init__(tok, x1, x2)

    def jumping(self, t, f):
        
        #print("Or jumping. t=", t, "f=", f)
        
        label = t if t!=0 else self.newlabel()
        self.expr1.jumping(label,0)
        self.expr1.jumping(t,f)
        if(t==0):
            self.emitlabel(label)
            
class And(Logical):
    
    def __init__(self, tok, x1, x2):
        super().__init__(tok, x1, x2)
        
    def jumping(self, t, f):
        
        #print("And jumping. t=", t, "f=", f)
        
        
        label = f if f != 0 else self.newlabel()
        
        self.expr1.jumping(0, label)
        self.expr2.jumping(t,f)
        
        if f ==0:
            self.emitlabel(label)
            
class Not(Logical):
    
    def __init__(self, tok, x2):
        super().__init__(tok, x2, x2)
        
    def jumping(self, t, f):
        
        #print("Not jumping. t=", t, "f=", f)
        
        
        self.expr2.jumping(f, t)
        
    def __str__(self):
        return str(self.op) + " " + str(self.expr)
    
class Rel(Logical):
    
    def __init__(self, tok, x1, x2):
        super().__init__(tok, x1, x2)
        
    def check(self, p1, p2):
        
        if (Type.numeric(p1) and Type.numeric(p2)):
            return Type("boo", Tag.TYPE, 1)        
        elif (p1.lexeme == p2.lexeme):
            return Type("boo", Tag.TYPE, 1)
        else:
            return None
        
    def jumping(self, t, f):
        a = self.expr1.reduce()
        b = self.expr2.reduce()
        
        #print("Rel jumping. t=", t, "f=", f, "expr1.reduce=", self.expr1.reduce(), "expr2.reduce=",
         #     self.expr2.reduce())
        
        
        test = str(a) + " " + str(self.op) + " " + str(b)
        
        self.emitjumps(test, t, f)
        
class Stmt(Node):
        
    def __init__(self):
        pass
    
    def gen(self, b, a):
        
        #print("Stmt gen. b=",b,"a=",a)
        pass
    
    after = 0
    Enclosing = None
    
    
    
class Cond(Stmt):
    
    def __init__(self, x, s):
        self.expr = x
        self.stmt = s
        
        if (self.expr.type.lexeme != "boo"):
            self.expr.error("Boolean required in Cond Statement")
            
    def gen(self, b, a):
        
        label = self.newlabel()
        
        #print("Cond gen. b=", b, "a=", a, "label=", label)
        
        
        self.expr.jumping(0, a)
        self.emitlabel(label)
        self.stmt.gen(label, a)
        
class Else(Stmt):
    
    def __init__(self, x, s1, s2):
        self.expr = x
        self.stmt1 = s1
        self.stmt2 = s2
        if (self.expr.type.lexeme != "boo"):
            self.expr.error("Boolean required in Cond Statement")
        
    def gen(self, b, a):
        
        label1 = self.newlabel()
        label2 = self.newlabel()
        
        #print("Else gen. b=", b, "a=", a, "label1=", label1, "label2=", label2)
        
        
        self.expr.jumping(0, label2)
        self.emitlabel(label1)
        self.stmt1.gen(label1, a)
        self.emit("goto L" + str(a))
        self.emitlabel(label2)
        self.stmt2.gen(label2, a)
        
class Loop(Stmt):
    
    def __init__(self):
        self.expr = None
        self.stmt = None
        
    def init(self, x, s):
        self.expr = x
        self.stmt = s
        
        
        if (self.expr.type.lexeme != "boo"):
            self.expr.error("Boolean required in Loop Statement")
            
    def gen(self, b, a):
        self.after = a
        self.expr.jumping(0, a)
        label = self.newlabel()
        
        #print("Loop gen. b=", b, "a=", a, "label=", label)
        
        
        self.emitlabel(label)
        self.stmt.gen(label, b)
        self.emit("goto L" + str(b))
        
class Set(Stmt):
    
    def __init__(self, i, x):
        self.id = i
        self.expr = x
                
        if self.check(self.id.type, self.expr.type) == None:
            self.error("Type Error")
            
    def check(self, p1, p2):
        if (Type.numeric(p1) and Type.numeric(p2)):
            return p2
        elif (p1.lexeme == "boo" and p2.lexeme == "boo"):
            return p2
        elif (p1.lexeme == "str" and p2.lexeme == "str"):
            return p2
        else:
            return None
        
    def gen(self, b, a):
        
        #print("Set gen. b=", b, "a=", a)
        
        
        self.emit(str(self.id) + " = " + str(self.expr.gen()))
        

class Seq(Stmt):
    
    def __init__(self, s1, s2):
        self.stmt1 = s1
        self.stmt2 = s2
        
    def gen(self, b, a):
        
        #print("Seq gen. b=", b, "a=", a)
        
        
        if (self.stmt1 == Stmt()):
            self.stmt2.gen(b, a)
        elif (self.stmt2 == Stmt()):
            self.stmt1.gen(b, a)
        else:
            label = self.newlabel()
            self.stmt1.gen(b, label)
            self.emitlabel(label)
            self.stmt2.gen(label, a)






    
    
    
    
    
    
    
    
        
    