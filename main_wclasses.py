#!/usr/bin/python3
import os
import random
import time
import numpy as np
import math
import sys


class worldMap:
    def __init__(self, worldSize=18, numPlayers=36, numHumans=1):
        self.worldSize = worldSize
        self.numPlayers = numPlayers
        self.numHumans = numHumans
        self.numComs = self.numPlayers - self.numHumans
        self.recursions = 0
        self.mapData = []

    colors = {
    "default" : '\033[94m'
    }


    def initializeMap(self):
        #global mapData
        self.mapData = []
        for i in range(self.worldSize):
            self.mapData.append([])
            for j in range(self.worldSize):
                self.mapData[i].append([]) #could use lists here to be more human readable, but makes it hard to see whole data list in debug
                
                self.mapData[i][j].append(0)#terrain tile type | 0=plains, 3=water, 1=city boundary FOR TESTING, 2=city, 4=mountain,
                self.mapData[i][j].append(0)#domain | p1, p2,
                self.mapData[i][j].append(0)#belong to | p1, p2,
                self.mapData[i][j].append(0)#owned by | none, p1, p2, | also determines color/style
                self.mapData[i][j].append(0)#tile entities | berries, gold, (buildings?),
                self.mapData[i][j].append(0)#buildings? or combine with 3? (Or troops? settlers, warriors? Maybe troop ID's?)

    def initializeTribes(self):
        global viableLines
        global tribeMap
        viableLines = []
        tribeMap = []
        for i in range(1, self.worldSize - 1):
            viableLines.append(i)

        #tribe placement viability map
        for y in range(self.worldSize):
            tribeMap.append([])
            for x in range(self.worldSize):
                tribeMap[y].append(x)
        for y in range(self.worldSize):
            tribeMap[y][0] = "!"
            tribeMap[y][-1] = "!"
            for x in range(self.worldSize):
                tribeMap[0][x] = "!"
                tribeMap[-1][x] = "!"

    def tileToChr(self, value):
        if value == 0:
            return chr(9618)
        if value == 1:
            return chr(9617)
        if value == 2:
            return chr(9608)

    def stratifyTribeMapCheck(self):
        global saturationRatio
        if saturationRatio > 0.7:
            for i in range(1, self.worldSize - 1): # (1, worldsize - 1) if not also modifying tribeMap ### This for loop not technically needed, as only modifying viableLines ensures that they wont get checked. Optimize?
                if i not in (1, 4, 7, 10, 13, 16):
                    for j in range(1, self.worldSize - 1):
                        #print(j)
                        #print(tribeMap[i])
                        tribeMap[i].remove(j)
            for x in range(1, self.worldSize - 1):
                if x not in (1, 4, 7, 10, 13, 16):  #max planned to ever be 18, so (...13, 16) will suffice
                    viableLines.remove(x)
            print("tribeMap stratified")

    def doubleStratifyTribeMapCheck(self):
        global saturationRatio
        if saturationRatio > 0.8:
            for y in viableLines:
                for x in range(1, self.worldSize - 1):
                    if x not in (1, 4, 7, 10, 13, 16):
                        tribeMap[y].remove(x)
            print("tribeMap double stratified")

    def areaTestPlayers(self):
        spawnableAreaWithRadius = (self.worldSize - 0)**2
        numPossibleCities = math.floor(math.sqrt(spawnableAreaWithRadius/(3**2))) ** 2
        #print(f"Number of possible cities = {numPossibleCities}")
        if self.numPlayers > numPossibleCities:
            print(f"Maximum number of cities for this worldsize is {numPossibleCities}. You tried to specify {numPlayers}.")
            sys.exit()
                
        domainArea = spawnableAreaWithRadius / self.numPlayers
        avgDistBetweenCities = math.sqrt(domainArea) - 3 #9 cities in a 9x9 world is perfectly placed. distance between all borders = 0
        gapDistRatio = 1 - (self.numPlayers / numPossibleCities) + 0.05 # 0.05 is just to tune the ratio
        ratiodGap = gapDistRatio * avgDistBetweenCities
        claimedArea = self.numPlayers * 3**2

        global minRatGapBetweenCities
        minRatGapBetweenCities = max(min(6, math.floor(ratiodGap)), 0)      # max(min(maxn, n), minn)
        
        global saturationRatio
        saturationRatio = claimedArea / spawnableAreaWithRadius
        print(f"Saturation: {saturationRatio:.2f}")

        self.stratifyTribeMapCheck()
        self.doubleStratifyTribeMapCheck()
        
        print()

    def tribeSetup(self):
        mapFull = False
        #global recursions  ## not needed, needed self.recursions? (below)
        for i in range(self.numPlayers):
            if mapFull == True:
                print("No available positions left. Map is full. Retrying...")
                self.initializeMap()
                self.initializeTribes()
                self.stratifyTribeMapCheck()
                self.doubleStratifyTribeMapCheck()
                self.tribeSetup()
                self.recursions += 1
                return #Not having this return allows the code to progress to the next line (randY = random...) before calling tribeSetup()

            randY = random.choice(viableLines)
            randX = random.choice(tribeMap[randY][1:-1]) #random.choice(tribeMap[randY][2:-2])
            for y in range(3):
                for x in range(3):
                    self.mapData[-1 + (randY) + y][-1 + randX + x][0] = 1
            self.mapData[randY][randX][0] = 2

            borderGap = minRatGapBetweenCities ### from areaTestPlayers !!!!!!!!!!!!!!!!!!!!!!!!!!!
            minCityGap = (borderGap * 2) + 5 # 3 for radius + 2 (1 on each side) = 0 border gap. =>  + 2 (1 on each side) = 1 border gap. Always odd, could do evens if randomly offset
            for y in range(minCityGap):
                randYRad = int((minCityGap - 1) / 2) + randY - y
                for x in range(minCityGap):
                    randXRad = int((minCityGap - 1) / 2) + randX - x        #randXRad = 2 + randX - x
                    if (self.worldSize > randYRad > 0) and randXRad in tribeMap[randYRad]: #this line automatically takes care of randXRad points outside of 0-worldSize (worldSize < randXRad < 0)
                        tribeMap[randYRad].remove(randXRad)

            posCounter = 1 # I think I could start this at 0, but there's no reason to since they would always be "!"
            for i in tribeMap[1:-1]: #tribeMap[2:-2]
                    if i.count("!") == len(i):
                        if posCounter in viableLines:
                            viableLines.remove(posCounter)
                    posCounter += 1
                    
            if len(viableLines) == 0:
                    mapFull = True

    def clear(self):
        os.system('cls' if os.name=='nt' else 'clear')

    def drawMap(self):
        color = '\033[94m'
        viewMap = ""
        for y in range(len(self.mapData)):
            for x in range(len(self.mapData[y])):
                viewMap += (self.tileToChr(self.mapData[y][x][0]) *2)
            viewMap += "\n"
        print(viewMap)

    def drawTribeMap(self):
        viewMap = ""
        for y in range(len(tribeMap)):
            for x in range(len(tribeMap[y])):
                viewMap += str(tribeMap[y][x]) + ","
            viewMap += "\n"
        print(viewMap)

    def assemble(self):
        self.initializeMap()
        self.initializeTribes()
        self.areaTestPlayers() # A debug command
        ### run start
        self.clear()
        #UNCOMMENT next line to debug tile list data
        np.set_printoptions(threshold=2000) #keeps np.asarray from condensing when printing (default 1000)
        #print(f"\n{np.asarray(mapData)}")
        self.tribeSetup()


"""
tick = time.perf_counter()    
theWorld = worldMap(18,10)#change map spawn details here
theWorld.assemble()
theWorld.drawMap()
print(f"Recursions: {theWorld.recursions}")
tock = time.perf_counter()
print(f"Time elapsed: {tock - tick:0.4f}") 
"""
