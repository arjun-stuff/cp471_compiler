# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 14:56:05 2021

@author: Arjun
"""



class Tag:
    
    AND = 100; OR = 101; NOT = 102; EQ = 103; NE = 104; GT = 105; GE = 106;
    LT = 107; LE = 108; COND = 109; LOOP = 110; ELSE = 111; TYPE = 112; 
    TRUE = 113; FALSE = 114; MATHOP = 115; OBRAC = 116; CBRAC = 117; ASSIGN = 118;
    ID = 119; INT = 120; DEC = 121; STR = 122; OBRACFLOW = 122; CBRACFLOW = 122;
    TEMP = 123; MINUS = 124;
    
    
class Token:
    
    def __init__(self, t):
        self.tag = t
        
    def __str__(self):
        return str(self.tag)
    
class Int(Token):
    
    def __init__(self, v):
        super().__init__(Tag.INT)
        self.value = v
        
    def __str__(self):
        return str(self.value)
    
class Dec(Token):
    
    def __init__(self, v):
        super().__init__(Tag.DEC)
        self.value = v
        
    def __str__(self):
        return str(self.value)

class Str(Token):
    
    def __init__(self, v):
        super().__init__(Tag.STR)
        self.value = "'" + v + "'"
        
    def __str__(self):
        return self.value
        

class Word(Token):
    
    def __init__(self, s, t):
        
        super().__init__(t)
        self.lexeme = s
        
    def __str__(self):
        return(str(self.lexeme))
    
class Type(Word):
    
    width = 0
    
    def __init__(self, s, t, w):
        
        super().__init__(s, t)
        self.width = w
        
    def numeric(p):
        
        if (p.lexeme == "int" or p.lexeme == "dec"):
            return True
        else:
            return False
        
    def max(p1, p2):
        
        if ((not Type.numeric(p1)) or (not Type.numeric(p2))):
            return None
        elif (p1.lexeme == "dec" or p2.lexeme == "dec"):
            return Type("dec", Tag.DEC, 8)
        else:
            return Type("int", Tag.INT, 4)
        
    
class Lexer:
    
    line = 1
    peek = " "
    words = {}
    
    def reserve(self, w):
        self.words[w.lexeme] = w
        
    def __init__(self, file):
        
        self.file = file
        
        self.reserve(Word("Cond", Tag.COND))
        self.reserve(Word("|", Tag.ELSE))
        self.reserve(Word("Loop", Tag.LOOP))
        self.reserve(Word("True", Tag.TRUE))
        self.reserve(Word("False", Tag.FALSE))
        self.reserve(Type("int", Tag.TYPE, 4))
        self.reserve(Type("dec", Tag.TYPE, 8))
        self.reserve(Type("str", Tag.TYPE, 1))
        self.reserve(Type("boo", Tag.TYPE, 1))
        
    def readch(self, c=None):
        
        self.peek = self.file.read(1)
        
        if c is None:
            return
        
        if (self.peek != c):
            return False
        
        self.peek = " "
        return True
    
    def scan(self):
        
        while True:
                        
            if (self.peek == " " or self.peek == "\t"):
                self.readch()
                continue
            elif (self.peek == "\n"):
                self.readch()
                self.line += 1
            else:
                break
        
        if self.peek == "^":
            self.peek = " ";
            return Word("^", Tag.AND)
        elif self.peek == "v" and self.readch(" "):
            return Word("v", Tag.OR)
        elif self.peek == ":":
            self.readch()
            return Token(118)
        elif self.peek == "=" and self.readch("="):
            return Word("==", Tag.EQ)
        elif self.peek == "~":
            if self.readch("="):
                return Word("~=", Tag.NE)
            else:
                return Word("~", Tag.NOT)
        elif self.peek == "<":
            if self.readch("="):
                return Word("<=", Tag.LE)
            elif self.peek == "<":
                self.peek = " "
                return Word("<<", Tag.OBRACFLOW)
            else:
                return Word("<", Tag.LT)
        elif self.peek == ">":
            if self.readch("="):
                return Word(">=", Tag.GE)
            elif self.peek == ">":
                self.peek = " "
                return Word(">>", Tag.CBRACFLOW)
            else:
                return Word(">", Tag.GT)
        elif self.peek == "|":
            self.readch();
            return Word("|", Tag.ELSE)
        
        if self.peek.isnumeric():
            
            v = int(self.peek)
            self.readch()
            
            while (self.peek.isnumeric()):
                v *= 10 + int(self.peek)
                self.readch()
                
            if self.peek != ".":
                return Int(v)
            
            v *= 1.0
            d = 10
            
            while True:
                self.readch()
                if not self.peek.isnumeric():
                    break
                v += int(self.peek) / d
                d *= 10
                
            return Dec(v)
        
        if self.peek.isalpha():
            
            b = self.peek
            self.readch()
            
            while (self.peek.isalpha()):
                b += self.peek
                self.readch()
            
            if b in self.words.keys():
                return self.words[b]
            
            w = Word(b, Tag.ID)
            self.words[b] = w
            return w
        
        if self.peek == '"':
            
            s = ""
            
            while not self.readch('"'):
                
                s += self.peek
                
            return Str(s)
            
            
        tok = Token(self.peek)
        self.peek = " "
        return tok
            
            
            
            

    
    
    

    
    