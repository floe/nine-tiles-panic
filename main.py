#!/usr/bin/python3

class Road:
    def __init__(self,s,e,b,al,ag):
        self.start = s
        self.end = e
        self.burger = b
        self.alien = al
        self.agent = ag
    def __repr__(self):
        return f"  Road[{self.start},{self.end}]: B{self.burger},Al{self.alien},Ag{self.agent}\n"

class Tile:
    def __init__(self,d,g,b,u,h,c,r):
        self.dogs = d
        self.girls = g
        self.boys = b
        self.ufos = u
        self.houses = h
        self.captured = c
        self.roads = r
    def __repr__(self):
        tmp = ""
        for r in self.roads:
           tmp += r.__repr__() 
        return f"\nTile: D{self.dogs},G{self.girls},B{self.boys},U{self.ufos},H{self.houses},C{self.captured}\n"+tmp

tiles = [
    (
        Tile(0,1,0,0,0,0,[Road(3,1,0,0,1)]),
        Tile(0,0,0,0,1,0,[Road(0,2,0,0,0),Road(1,3,0,1,0)])
    ),(
        Tile(0,1,0,0,0,0,[Road(2,1,0,0,1)]),
        Tile(1,0,0,0,0,0,[Road(0,2,0,0,0)])
    )
]


print(tiles)
