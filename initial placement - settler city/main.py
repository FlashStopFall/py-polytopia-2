#!/usr/bin/python3
import os
import random
import time
import numpy as np

domain = 5 #per polytopia
worldSize = 18 #minimum 11, per Polytopia
numPlayers = 8 #minimum 2 for gameplay
numHumans = 1
numComs = numPlayers - numHumans

playersPerSize = {"11":9,#perfectly placed
                  "12":9,
                  "13":9,
                  "14":16,#perfectly placed | 14 reaches recursion limit
                  "17":25,
                  "18":25 #23 reaches recursion depth limit
                  }

colors = {
    "default" : '\033[94m'
    }

def initializeMap():
    global mapData
    mapData = []
    for i in range(worldSize):
        mapData.append([])
        for j in range(worldSize):
            mapData[i].append([]) #could use lists here to be more human readable, but makes it hard to see whole data list in debug
            
            mapData[i][j].append(0)#terrain tile type | 0=plains, 3=water, 1=city boundary FOR TESTING, 2=city, 4=mountain,
            mapData[i][j].append(0)#domain | p1, p2,
            mapData[i][j].append(0)#belong to | p1, p2,
            mapData[i][j].append(0)#owned by | none, p1, p2, | also determines color/style
            mapData[i][j].append(0)#tile entities | berries, gold, (buildings?),
            mapData[i][j].append(0)#buildings? or combine with 3? (Or troops? settlers, warriors? Maybe troop ID's?)

def initializeTribes():
    global viableLines
    global tribeMap
    viableLines = []
    tribeMap = []
    for i in range(2, worldSize - 2):
        viableLines.append(i)


    #tribe placement viability map
    for y in range(worldSize):
        tribeMap.append([])
        for x in range(worldSize):
            tribeMap[y].append(x)
    #drawTribeMap() #debug for initialization
    for y in range(worldSize):
        tribeMap[y][0] = "!"
        tribeMap[y][1] = "!"
        tribeMap[y][-2] = "!"
        tribeMap[y][-1] = "!"
        for x in range(worldSize):
            tribeMap[0][x] = "!"
            tribeMap[1][x] = "!"
            tribeMap[-2][x] = "!"
            tribeMap[-1][x] = "!"
            
def clear():
    os.system('cls' if os.name=='nt' else 'clear')

def drawMap():
    color = '\033[94m'
    viewMap = ""
    for y in range(len(mapData)):
        for x in range(len(mapData[y])):
            viewMap += (tileToChr(mapData[y][x][0]) *2)
        viewMap += "\n"
    print(viewMap)

def drawTribeMap():
    viewMap = ""
    for y in range(len(tribeMap)):
        for x in range(len(tribeMap[y])):
            viewMap += str(tribeMap[y][x])
        viewMap += "\n"
    print(viewMap)

def tileToChr(value):
    if value == 0:
        return chr(9618)
    if value == 1:
        return chr(9617)
    if value == 2:
        return chr(9608)

def tribeSetup():
    mapFull = False
    for i in range(numPlayers):
        if mapFull == True:
            print("No available positions left. Map is full. Retrying...")
            initializeMap()
            initializeTribes()
            tribeSetup()
            return #Not having this return allows the code to progress to the next line (randY = random...) before calling tribeSetup()
    
        randY = random.choice(viableLines)
        randX = random.choice(tribeMap[randY][2:-2])
        for y in range(3):
            for x in range(3):
                mapData[-1 + (randY) + y][-1 + randX + x][0] = 1
        mapData[randY][randX][0] = 2
        for y in range(5):
                for x in range(5):
                    randXRad = 2 + randX - x
                    randYRad = 2 + randY - y
                    if randXRad in tribeMap[randYRad]:
                        tribeMap[randYRad].remove(randXRad)

        posCounter = 2 # I think I could start this at 0, but there's no reason to since they would always be "!"
        for i in tribeMap[2:-2]:
                if i.count("!") == len(i):
                    if posCounter in viableLines:
                        viableLines.remove(posCounter)
                posCounter += 1
                
        if len(viableLines) == 0:
                mapFull = True
##
"""What if we had settlers like Civ? That would allow more freedom of city placement
and more options for the player, without having to generate them before.

Players could build new cities anywhere they want that isn't inside of a border.
Original cities spawn with a 3x3 border, but player-com built cities can be placed anywhere,
aka no minimum border limit. Wanting to maintain a larger boundary for each city
would govern new city placement via the player-coms."""
##


tick = time.perf_counter()    

initializeMap()
initializeTribes()
#drawTribeMap() #debug tool

### run start
clear()
#UNCOMMENT next line to debug tile list data

np.set_printoptions(threshold=2000) #keeps np.asarray from condensing when printing (default 1000)
#print(f"\n{np.asarray(mapData)}")
#drawMap()


tribeSetup()
#drawTribeMap()  # debug tool
#print(f"\n{np.asarray(mapData)}")
drawMap()
tock = time.perf_counter()
print(f"Time elapsed: {tock - tick:0.4f}")
