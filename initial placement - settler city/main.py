#!/usr/bin/python3
import os
import random
import time
import numpy as np
import math

domain = 5 #per polytopia
worldSize = 18 #minimum 11, max 18, per Polytopia
numPlayers = 36 #minimum 2 for gameplay
numHumans = 1
numComs = numPlayers - numHumans

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
    for i in range(1, worldSize - 1):
        viableLines.append(i)


    #tribe placement viability map
    for y in range(worldSize):
        tribeMap.append([])
        for x in range(worldSize):
            tribeMap[y].append(x)
    #drawTribeMap() #debug for initialization
    for y in range(worldSize):
        tribeMap[y][0] = "!"
        #tribeMap[y][1] = "!"           #commented out to allow full map spawnability
        #tribeMap[y][-2] = "!"          #commented out to allow full map spawnability
        tribeMap[y][-1] = "!"
        for x in range(worldSize):
            tribeMap[0][x] = "!"
            #tribeMap[1][x] = "!"       #commented out to allow full map spawnability
            #tribeMap[-2][x] = "!"      #commented out to allow full map spawnability
            tribeMap[-1][x] = "!"
    #drawTribeMap() #debug for initialization

            
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
            viewMap += str(tribeMap[y][x]) + ","
        viewMap += "\n"
    print(viewMap)

def tileToChr(value):
    if value == 0:
        return chr(9618)
    if value == 1:
        return chr(9617)
    if value == 2:
        return chr(9608)

def stratifyTribeMapCheck():
    global saturationRatio
    if saturationRatio > 0.7:
        for i in range(1, worldSize - 1): # (1, worldsize - 1) if not also modifying tribeMap ### This for loop not technically needed, as only modifying viableLines ensures that they wont get checked. Optimize?
            if i not in (1, 4, 7, 10, 13, 16):
                for j in range(1, worldSize - 1):
                    #print(j)
                    #print(tribeMap[i])
                    tribeMap[i].remove(j)
        for x in range(1, worldSize - 1):
            if x not in (1, 4, 7, 10, 13, 16):  #max planned to ever be 18, so (...13, 16) will suffice
                viableLines.remove(x)
        print("tribeMap stratified")

def doubleStratifyTribeMapCheck():
    global saturationRatio
    if saturationRatio > 0.8:
        for y in viableLines:
            for x in range(1, worldSize - 1):
                if x not in (1, 4, 7, 10, 13, 16):
                    #print(y, x)
                    #print(tribeMap[y][x])
                    tribeMap[y].remove(x)
        print("tribeMap double stratified")

def areaTestPlayers(worldWidth, players):
    #area = worldWidth**2
    #spawnableAreaCenter = (worldWidth - 2)**2
    #spawnableAreaWithRadius = (worldWidth - 0)**2
    #print(f"Area is {area}")
    #print(f"Spawnable area centers is {spawnableAreaCenter}")
    #print(f"Spawnable area w/ radius is {spawnableAreaWithRadius}")

    #areaOfPossibleCities  = spawnableAreaWithRadius/(3**2)
    #print(f"Area of possible starting cities = {areaOfPossibleCities}")
    #numPossibleCities = math.floor(math.sqrt(spawnableAreaWithRadius/(3**2))) ** 2
    #print(f"Number of possible cities = {numPossibleCities}")

    #domainArea = area / numPlayers
    #print(f"Domain area per capitals (numPlayers) = {domainArea}")

    #unclaimedArea = spawnableAreaWithRadius - (numPlayers * 3**2) #could just say * 9 here...
    #print(f"Unclaimed area: {unclaimedArea}")

    #claimedArea = numPlayers * 3**2
    #print(f"Claimed area: {claimedArea}")

    #avgDistBetweenCities = math.sqrt(domainArea) - 3 #9 cities in a 9x9 world is perfectly placed. distance between all borders = 0
    #print(f"Average distance between city borders: {avgDistBetweenCities}") #target average?

    #global minGapBetweenCities
    #minGapBetweenCities = math.floor(avgDistBetweenCities)
    #print(f"Minimum gap between city borders: {minGapBetweenCities}")


    spawnableAreaWithRadius = (worldWidth - 0)**2
    numPossibleCities = math.floor(math.sqrt(spawnableAreaWithRadius/(3**2))) ** 2
    domainArea = spawnableAreaWithRadius / numPlayers
    avgDistBetweenCities = math.sqrt(domainArea) - 3 #9 cities in a 9x9 world is perfectly placed. distance between all borders = 0
    gapDistRatio = 1 - (numPlayers / numPossibleCities) + 0.05 # 0.05 is just to tune the ratio
    ratiodGap = gapDistRatio * avgDistBetweenCities
    #print(f"Gap distance ratio: {gapDistRatio:.2f}. \nNew average distance between cities: {ratiodGap:.2f}")
    claimedArea = numPlayers * 3**2

    global minRatGapBetweenCities
    minRatGapBetweenCities = max(min(6, math.floor(ratiodGap)), 0)      # max(min(maxn, n), minn)
    #print(f"New minimum gap between city borders: {minRatGapBetweenCities}")
    
    global saturationRatio
    saturationRatio = claimedArea / spawnableAreaWithRadius
    print(f"Saturation: {saturationRatio:.2f}")

    stratifyTribeMapCheck()
    doubleStratifyTribeMapCheck()
    
    print()


recursions = 0
def tribeSetup():
    mapFull = False
    global recursions
    for i in range(numPlayers):
        if mapFull == True:
            print("No available positions left. Map is full. Retrying...")
            initializeMap()
            initializeTribes()
            stratifyTribeMapCheck()
            doubleStratifyTribeMapCheck()
            tribeSetup()
            recursions += 1
            return #Not having this return allows the code to progress to the next line (randY = random...) before calling tribeSetup()


        randY = random.choice(viableLines)
        #print(randY)
        randX = random.choice(tribeMap[randY][1:-1]) #random.choice(tribeMap[randY][2:-2])
        #print(randX)
        for y in range(3):
            for x in range(3):
                mapData[-1 + (randY) + y][-1 + randX + x][0] = 1
        mapData[randY][randX][0] = 2

        borderGap = minRatGapBetweenCities ### from areaTestPlayers !!!!!!!!!!!!!!!!!!!!!!!!!!!
        minCityGap = (borderGap * 2) + 5 # 3 for radius + 2 (1 on each side) = 0 border gap. =>  + 2 (1 on each side) = 1 border gap. Always odd, could do evens if randomly offset
        for y in range(minCityGap):
            randYRad = int((minCityGap - 1) / 2) + randY - y
            for x in range(minCityGap):
                randXRad = int((minCityGap - 1) / 2) + randX - x        #randXRad = 2 + randX - x
                if (worldSize > randYRad > 0) and randXRad in tribeMap[randYRad]: #this line automatically takes care of randXRad points outside of 0-worldSize (worldSize < randXRad < 0)
                    tribeMap[randYRad].remove(randXRad)

        posCounter = 1 # I think I could start this at 0, but there's no reason to since they would always be "!"
        for i in tribeMap[1:-1]: #tribeMap[2:-2]
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

areaTestPlayers(worldSize, numPlayers) # A debug command
#drawTribeMap() #debug tool

### run start
clear()

#UNCOMMENT next line to debug tile list data
np.set_printoptions(threshold=2000) #keeps np.asarray from condensing when printing (default 1000)
#print(f"\n{np.asarray(mapData)}")
#drawMap()

#drawTribeMap()
tribeSetup()
#drawTribeMap()

#drawTribeMap()  # debug tool
#print(f"\n{np.asarray(mapData)}")

drawMap()
print(f"Recursions: {recursions}")
tock = time.perf_counter()
print(f"Time elapsed: {tock - tick:0.4f}")
