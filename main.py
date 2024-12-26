#!/usr/bin/python3
import itertools
from copy import deepcopy


# convention: top 0, right 1, bottom 2, left 3
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


#array for scoring functions, one for each card
scoringfunctions = {}

def rotate(tile, rotation):
    for road in tile.roads:
        road.start = (road.start+rotation) % 4
        road.end   = (road.end  +rotation) % 4

def fliptile(tile, arrangement, i):
    rotation = arrangement // (8^i)
    if rotation > 3:
        return rotate(tile[1],rotation-4)
    else:
        return rotate(tile[0],rotation)

def flip(perm, arrangment):
    list = []
    for i in range(9):
        tile = deepcopy(tiles[perm[i]])
        tile = fliptile(tile,arrangement,i)
        list.append(tile)
    return list

#checks if grid given by perm and arrangement is legal, i.e., all roads are correctley connected
def islegal(perm, arrangement):
    grid = flip(perm, arrangement)
    ret = True
    for i in {0,1,3,4,6,7}:
        ret = ret and checkroadshorizontally(grid[i],grid[i+1])
    for i in {0,3,1,4,2,5}:
        ret = ret & checkroadsvertically(grid[i],grid[i+3])
    return ret

#computes the score of a grid (given bz perm and arrangement) for the cards in triple
def score(perm, arrangement, triple):
    sum = 0
    for rule in triple:
        sum += scoringfunctions[rule](perm,arrangement)
    return sum

#number of arrangements of the cards, once their order is fixed
combinations = 8^9
#dictionary holding the best value for each triple of cards
best = {}
#dictionary holding the grid witnessing the best value for each triple of cards 
witness = {}

#init
for triple in itertools.permutations(range(25),3):
    best[triple] = 0
    witness[triple] = []

#main loop
for perm in itertools.permutations(range(9)):
    for arrangement in range(combinations):
        if islegal(perm, arrangement):
            for triple in itertools.permutations(range(25),3):
                val = score(perm, arrangement, triple)
                if val > best[triple]:
                    best[triple] = val
                    witness[triple] = [perm,arrangement]
