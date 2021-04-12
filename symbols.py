# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 16:51:55 2021

@author: Arjun
"""

        
    
class Env:
    
    prev = None
    
    def __init__(self, n):
        
        self.table = {}
        self.prev = n
        
    def put(self, t, i):
        self.table[t] = i
        
    def get(self, w):
        
        e = self
        
        while e is not None:
            
            if w in e.table.keys():
                return e.table[w]
            e = e.prev
            
        return None
    
    
        
    
    
    
    
    