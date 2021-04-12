# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 18:15:44 2021

@author: Arjun
"""

from lexer import *
from symbols import *
from inter import *

class Parser:
    
    
    
    def __init__(self, l):
    
        self.top = None
        self.used = 0
        self.queue = []
        self.tokens = []
        self.parse_tree = None

        
        self.lex = l
        self.move()
        self.top = Env(self.top)
        
        
    def move(self):
        
        if len(self.queue) == 0:
            tok = self.lex.scan()
            self.tokens.append(tok)
            self.queue.insert(0, tok)
                
        self.look = self.queue.pop(0)
        
          
        
    
    def output_token_stream(self):
        counter = 1
        for tok in self.tokens:
            print(str(counter) + ":", tok)
            counter += 1
    
        
    def error(self, s):
        raise RuntimeError("near line"+str(self.lex.line)+": "+s)
        
    def match(self, t):
        if (self.look.tag == t):
            self.move()
        else:
            self.error("Syntax Error")
        
    def program(self):
        #s = self.block()
        d = self.decls()
        s = self.stmts()
        
        self.parse_tree = [d, s]
        
        for i in range(len(d)):
            begin = d[i].newlabel()
            after = d[i].newlabel()
            d[i].emitlabel(begin)
            d[i].gen(begin, after)
            d[i].emitlabel(after)
        begin = s.newlabel()
        after = s.newlabel()
        s.emitlabel(begin)
        s.gen(begin, after)
        s.emitlabel(after)

    
    def decls(self):
        
        assignments = []
        
        while self.look.tag == Tag.TYPE:
            p = self.type_()
            tok = self.look
            id_ = Id(tok, p, self.used)
            self.top.put(tok, id_)
            self.used = self.used + p.width
            s = self.assign()
            assignments.append(s)
        
        return assignments
            
            
        '''
        self.match(Tag.ID)
        
        self.match(";")
        id_ = Id(tok, p, self.used)
        self.top.put(tok, id_)
        self.used = self.used + p.width'''
    
    def type_(self):
        
        p = self.look
        self.match(Tag.TYPE)
        return p
    
    def stmts(self):
        
        if self.look.tag == "}":
            return Stmt()
        else:
            return Seq(self.stmt(), self.stmts())
        
    def stmt(self):
                
        if self.look.tag == Tag.ASSIGN:
            self.move()
            return Stmt()
        elif self.look.tag == Tag.COND:
            self.match(Tag.COND)
            self.match(Tag.OBRACFLOW)
            x = self.bool_()
            self.match(Tag.CBRACFLOW)
            s1 = self.stmt()
            temp = self.look
            if (temp.tag == "}"):
                self.move()
            if (self.look.tag != Tag.ELSE):
                self.queue.insert(0,self.look)
                self.look = temp
                return Cond(x, s1)
            self.match(Tag.ELSE)
            s2 = self.stmt()
            return Else(x, s1, s2)
        elif self.look.tag == Tag.LOOP:
            whilenode = Loop()
            savedStmt = Stmt.Enclosing
            Stmt.Enclosing = whilenode
            self.match(Tag.LOOP)
            self.match(Tag.OBRACFLOW)
            x = self.bool_()
            self.match(Tag.CBRACFLOW)
            s1 = self.stmt()
            whilenode.init(x, s1)
            Stmt.Enclosing = savedStmt
            return whilenode
        elif self.look.tag == "{":
            self.move()
            return self.stmts()
        elif self.look.tag == Tag.TYPE:            
            return self.program()
        else:
            return self.assign()
        
    def assign(self):
        t = self.look
        self.match(Tag.ID)
        id_ = self.top.get(t)
        if(id_ is None):
            self.error(str(t) + " undeclared")
        if(self.look.tag == Tag.ASSIGN):
            self.move()
            stmt = Set(id_, self.bool_())
        self.match(";")
        return stmt
    
    def bool_(self):
        x = self.join()
        while(self.look.tag == Tag.OR):
            tok = self.look
            self.move()
            x = Or(tok, x, self.join())
        return x
    
    def join(self):
        x = self.equality()
        while(self.look.tag == Tag.AND):
            tok = self.look
            self.move()
            x = And(tok, x, self.equality())
        return x
    
    def equality(self):
        x = self.rel()
        while(self.look.tag == Tag.EQ or self.look.tag == Tag.NE):
            tok = self.look
            self.move()
            x = Rel(tok, x, self.rel())
        return x
    
    def rel(self):
        x = self.expr()
        
        if self.look.tag == Tag.LT or self.look.tag == Tag.LE or \
            self.look.tag == Tag.GT or self.look.tag == Tag.GE:
                tok = self.look
                self.move()
                return Rel(tok, x, self.expr())
        else:
            return x
        
    def expr(self):
        x = self.term()
        while (self.look.tag == "+" or self.look.tag == "-"):
            tok = self.look
            self.move()
            x = Arith(tok, x, self.term())
        return x
    
    def term(self):
        x = self.unary()
        while (self.look.tag == "*" or self.look.tag == "/"):
            tok = self.look
            self.move()
            x = Arith(tok, x, self.unary())
        return x
    
    def unary(self):
        if (self.look.tag == "-"):
            self.move()
            return Unary(Word("-", Tag.MINUS), self.unary())
        elif self.look.tag == Tag.NOT:
            tok = self.look
            self.move()
            return Not(tok, self.unary())
        else:
            return self.factor()
        
    def factor(self):
        x = None
        
        if self.look.tag == "(":
            self.move()
            x = self.bool_()
            self.match(")")
            return x
        elif self.look.tag == Tag.INT:
            x = Constant(self.look, Type("int", Tag.TYPE, 4))
            self.move()
            return x
        elif self.look.tag == Tag.DEC:
            x = Constant(self.look, Type("dec", Tag.TYPE, 8))
            self.move()
            return x
        elif self.look.tag == Tag.STR:
            x = Constant(self.look, Type("str", Tag.TYPE, 1))
            self.move()
            return x
        elif self.look.tag == Tag.TRUE:
            x = Constant(Word("True", Tag.TRUE), Type("boo", Tag.TYPE, 1))
            self.move()
            return x
        elif self.look.tag == Tag.FALSE:
            x = Constant(Word("False", Tag.TRUE), Type("boo", Tag.TYPE, 1))
            self.move()
            return x
        elif self.look.tag == Tag.ID:
            s = str(self.look)
            id_ = self.top.get(self.look)
            if (id_ is None):
                self.error(str(self.look) + " undeclared")
            self.move()
            return id_
        else:
            self.error("Syntax Error")
            return x
            
        
            
        
        
            
        
        
        
        
        

        





















