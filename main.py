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
        self.done = False
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

class Route:
    def __init__(self,road):
        self.roads = [road]
        self.closed = False
    def __repr__(self):
        tmp = ""
        for road in self.roads:
            tmp += road.__repr__()
        return f"\nRoute: C{self.closed}\n"+tmp

tiles = [
    (
        Tile(0,1,0,0,0,0,[Road(3,1,0,0,1)]), # 0
        Tile(0,0,0,0,1,0,[Road(0,2,0,0,0),Road(1,3,0,1,0)])
    ),(
        Tile(0,1,0,0,0,0,[Road(2,1,0,0,1)]), # 1
        Tile(1,0,0,0,0,0,[Road(0,2,1,0,0)])
    ),(
        Tile(1,0,0,0,0,0,[Road(0,3,1,0,0), Road(1,2,0,0,0)]), # 2
        Tile(2,0,0,0,0,1,[])
    ),(
        Tile(0,0,0,0,1,0,[Road(1,0,0,1,0),Road(2,3,0,0,0)]),
        Tile(0,0,1,0,0,0,[Road(0,2,0,0,0),Road(1,3,1,0,0)]) # 3
    ),(
        Tile(0,1,1,1,0,0,[]),
        Tile(0,0,0,0,1,0,[Road(2,3,1,0,0)]) # 4
    ),(
        Tile(0,0,0,1,2,0,[]), 
        Tile(0,0,0,0,1,0,[Road(3,1,1,0,0)]) # 5
    ),(
        Tile(1,0,0,0,0,0,[Road(2,3,1,0,0)]), # 6
        Tile(0,0,1,0,0,0,[Road(0,3,0,0,0),Road(2,1,0,0,1)])
    ),(
        Tile(0,0,0,0,1,0,[Road(3,2,0,1,0)]),
        Tile(1,0,0,0,0,0,[Road(0,2,0,0,0),Road(3,1,0,0,1)]) # 7
    ),(
        Tile(1,0,0,0,0,0,[Road(1,2,1,0,0),Road(0,3,0,0,0)]), # 8
        Tile(0,0,1,0,0,0,[Road(3,1,0,1,0)])
    )
]


def getnextroad(grid,position,direction):
   if direction == 0:
        if position in [0,1,2]:
            return (None,None,None)
        for road in grid[position - 3].roads:
            if road.start == 2:
                return (road, position - 3, 0)
            if road.end == 2:
                return (road, position - 3, 1)

   if direction == 1:
        if position in [2,5,8]:
            return (None,None,None)
        for road in grid[position + 1].roads:
            if road.start == 3:
                return (road, position + 1, 0)
            if road.end == 3:
                return (road, position + 1, 1)

   if direction == 2:
        if position in [6,7,8]:
            return (None,None,None)
        for road in grid[position + 3].roads:
            if road.start == 0:
                return (road, position + 3, 0)
            if road.end == 0:
                return (road, position + 3, 1)

   if direction == 3:
        if position in [0,3,6]:
            return (None,None,None)
        for road in grid[position - 1].roads:
            if road.start == 1:
                return (road, position - 1, 0)
            if road.end == 1:
                return (road, position - 1, 1)

   return (None,None,None)


def getroutes(grid):
    routes = []
    for i in range(len(tiles)):
        tile = grid[i]
        if len(tile.roads) == 0:
            continue
        for road in tile.roads:
            if road.done:
                continue

            route = Route(road)
            road.done = True

            rnext,pos,d = getnextroad(grid, i, road.end)
            while pos != None:
                rnext.done = True
                route.roads.append(rnext)
                direction = rnext.end if d == 0 else rnext.start
                rnext,pos,d = getnextroad(grid, pos, direction)
                if rnext and rnext.done:
                    route.closed = True
                    break

            rprev,pos,d = getnextroad(grid, i, road.start)
            while pos != None and not rprev.done:
                rprev.done = True
                route.roads.insert(0,rprev)
                direction = rprev.end if d == 0 else rprev.start
                rprev,pos,d = getnextroad(grid, pos, direction)
                if rprev and rprev.done:
                    route.closed = True
                    break

            routes.append(route)    
                
    return routes


#array for scoring functions, one for each card
scoringfunctions = {}

# rotate tile by 0˚,90˚,180°,270° (only roads are relevant)
def rotate(tile, rotation):
    for road in tile.roads:
        road.start = (road.start+rotation) % 4
        road.end   = (road.end  +rotation) % 4
    return tile

# arrangement == all rotations and flips, 8**9 (0-3 = rotation front, 4-7 = rotation back)
def fliptile(tile, arrangement, i):
    rotation = arrangement // (8**i)
    if rotation > 3:
        return rotate(tile[1],rotation-4)
    else:
        return rotate(tile[0],rotation)

# returns a list of tiles where position is given by perm and rotation/flip by arrangement
def flip(perm, arrangement):
    list = []
    for i in range(len(tiles)):
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
        dir1 = 2
        dir2 = 0
    else:
        dir1 = 1
        dir2 = 3
    if findroadend(tile1,dir1) and findroadend(tile2,dir2):
        return True
    if not findroadend(tile1,dir1) and not findroadend(tile2,dir2):
        return True
    return False

# checks if grid given by perm and arrangement is legal, i.e., all roads are correctly connected
def islegal(grid):
    for i in {0,1,3,4,6,7}:
        if not checkroads(grid[i],grid[i+1],False):
            return False
    for i in {0,3,1,4,2,5}:
        if not checkroads(grid[i],grid[i+3],True):
            return False
    return True

# computes the score of a grid (given by perm and arrangement) for the cards in triple
def score(grid, triple):
    sum = 0
    #for rule in triple:
    #    sum += scoringfunctions[rule](grid)
    return sum

#number of arrangements of the cards, once their order is fixed
combinations = 8**len(tiles)
#dictionary holding the best value for each triple of cards
best = {}
#dictionary holding the grid witnessing the best value for each triple of cards 
witness = {}

#init
for triple in itertools.permutations(range(25),3):
    best[triple] = 0
    witness[triple] = []

grid = [
    rotate(tiles[3][1],2),
    tiles[4][1],
    rotate(tiles[0][0],1),
    tiles[2][0],
    rotate(tiles[8][0],1),
    tiles[7][1],
    rotate(tiles[6][0],2),
    rotate(tiles[1][0],2),
    rotate(tiles[5][1],1)
]

#print(grid[5])
#print(getnextroad(grid,1,2))
#print(getroutes(grid))

#exit(0)

#main loop

import time

nanosecs = time.time_ns()

for perm in itertools.permutations(range(len(tiles))):
    print(perm)
    for arrangement in range(combinations):
        if arrangement % 1000000 == 0:
            nanosecs = time.time_ns() - nanosecs
            print(nanosecs//60000000000)
        grid = flip(perm, arrangement)
        #print(grid)
        #print(grid)
        if islegal(grid):
            getroutes(grid)
            for triple in itertools.permutations(range(25),3):
                val = score(grid, triple)
                if val > best[triple]:
                    best[triple] = val
                    witness[triple] = [perm,arrangement]

#print(witness)
