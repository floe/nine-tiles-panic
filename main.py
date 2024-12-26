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

# rotate tile by 0˚,90˚,180°,270° (only roads are relevant)
def rotate(tile, rotation):
    for road in tile.roads:
        road.start = (road.start+rotation) % 4
        road.end   = (road.end  +rotation) % 4
    return tile

# arrangement == all rotations and flips, 8^9 (0-3 = rotation front, 4-7 = rotation back)
def fliptile(tile, arrangement, i):
    rotation = arrangement // (8^i)
    if rotation > 3:
        return rotate(tile[1],rotation-4)
    else:
        return rotate(tile[0],rotation)

# returns a list of tiles where position is given by perm and rotation/flip by arrangement
def flip(perm, arrangement):
    list = []
    for i in range(9):
        tile = deepcopy(tiles[perm[i]])
        tile = fliptile(tile,arrangement,i)
        list.append(tile)
    return list

# check if a tile has a road end in direction
def findroadend(tile,direction):
    for road in tile.roads:
        if road.start == direction:
            return True
        if road.end == direction:
            return True
    return False

# see if two tiles are legally connected by roads
def checkroads(tile1,tile2,vertical):
    if vertical:
        dir1 = 0
        dir2 = 2
    else:
        dir1 = 1
        dir2 = 3
    if findroadend(tile1,dir1) and findroadend(tile2,dir2):
        return True
    if not findroadend(tile1,dir1) and not findroadend(tile2,dir2):
        return True
    return False

# checks if grid given by perm and arrangement is legal, i.e., all roads are correctley connected
def islegal(perm, arrangement):
    grid = flip(perm, arrangement)
    ret = True
    for i in {0,1,3,4,6,7}:
        ret = ret and checkroads(grid[i],grid[i+1],False)
    for i in {0,3,1,4,2,5}:
        ret = ret & checkroads(grid[i],grid[i+3],True)
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
